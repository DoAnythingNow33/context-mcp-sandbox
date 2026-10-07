#!/usr/bin/env python3
"""
validate_freshness.py — drift detector for Context 2.0.

Flags stale state at session open so you don't have to notice it manually.
Runs three checks:

  1. STALE SNAPSHOTS  — entity snapshot not updated after a linked meeting
  2. STALE DIGEST     — _digest.md older than the newest snapshot last_updated
  3. INDEX DRIFT      — index.md Entities table out of sync with snapshot last_updated

Usage:
    python scripts/validate_freshness.py

Exit code 0 = no drift. Exit code 1 = drift found.
"""

import re
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).parent.parent
ENTITIES_DIR = ROOT / "entities"
MEETINGS_DIR = ROOT / "meetings"
DIGEST_PATH = ROOT / "_digest.md"
INDEX_PATH = ROOT / "index.md"

# Matches [[some/path/slug]] or [[slug]] — captures the inner text only
WIKILINK_RE = re.compile(r"\[\[([^\]|]+?)(?:\|[^\]]*)?\]\]")

# Matches a YYYY-MM-DD at the start of a filename stem
DATE_PREFIX_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")


# ---------------------------------------------------------------------------
# Shared helpers (mirrors generate_digest.py approach — pure stdlib)
# ---------------------------------------------------------------------------

def parse_frontmatter(content: str) -> dict:
    """Extract frontmatter key/value pairs from a YAML block delimited by ---."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}

    fm: dict = {}
    lines = match.group(1).splitlines()
    current_key = None
    current_list: list[str] = []

    for line in lines:
        # List item under current key
        if re.match(r"^\s{2,}- ", line):
            val = re.sub(r'^\s*-\s*"?|"?\s*$', "", line).strip().strip('"')
            if val:
                current_list.append(val)
            continue

        # New key: value line
        m = re.match(r'^(\w[\w_]*):\s*(.*)', line)
        if m:
            if current_key and current_list:
                fm[current_key] = current_list
                current_list = []
            key = m.group(1)
            value = m.group(2).strip().strip('"')
            if value:
                fm[key] = value
            current_key = key
        else:
            # Continuation of a quoted / multi-line scalar
            if current_key and current_key in fm and isinstance(fm[current_key], str):
                fm[current_key] += " " + line.strip().strip('"')

    if current_key and current_list:
        fm[current_key] = current_list

    return fm


def read_file_safe(path: Path) -> str | None:
    """Read a file, returning None on any error."""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return None


def extract_meetings_section_links(content: str) -> list[str]:
    """Return all wikilink targets listed under a ## Meetings section."""
    in_meetings = False
    links = []
    for line in content.splitlines():
        if re.match(r"^##\s+Meetings\b", line, re.IGNORECASE):
            in_meetings = True
            continue
        if in_meetings:
            if re.match(r"^##\s+", line):
                break
            for m in WIKILINK_RE.finditer(line):
                links.append(m.group(1).strip())
    return links


def meeting_date_from_stem(stem: str) -> str | None:
    """Extract YYYY-MM-DD from a meeting filename stem, or None."""
    m = DATE_PREFIX_RE.match(stem)
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# Check 1 — Stale snapshots
# ---------------------------------------------------------------------------

def check_stale_snapshots() -> list[str]:
    """
    For each snapshot entity file: if any linked meeting date is newer than
    last_updated, flag it.
    """
    findings = []

    for entity_path in sorted(ENTITIES_DIR.rglob("*.md")):
        if entity_path.name.startswith("_"):
            continue

        content = read_file_safe(entity_path)
        if content is None:
            continue

        fm = parse_frontmatter(content)
        if fm.get("type") != "snapshot":
            continue

        last_updated = fm.get("last_updated", "")
        if not last_updated:
            continue  # can't compare without a date

        rel = entity_path.relative_to(ROOT)
        meeting_links = extract_meetings_section_links(content)

        for link in meeting_links:
            # Resolve the link stem — could be a bare slug or a path
            stem = Path(link).stem
            meeting_date = meeting_date_from_stem(stem)
            if not meeting_date:
                continue

            if meeting_date > last_updated:
                findings.append(
                    f"  STALE SNAPSHOT  {rel}"
                    f"  (last_updated: {last_updated}"
                    f" | meeting: [[{stem}]] on {meeting_date})"
                )

    return findings


# ---------------------------------------------------------------------------
# Check 2 — Stale digest
# ---------------------------------------------------------------------------

def check_stale_digest() -> list[str]:
    """
    Compare _digest.md generated: date against the newest snapshot last_updated.
    """
    findings = []

    if not DIGEST_PATH.exists():
        findings.append(
            f"  MISSING DIGEST  {DIGEST_PATH.relative_to(ROOT)} does not exist"
            " — run: python scripts/generate_digest.py"
        )
        return findings

    digest_content = read_file_safe(DIGEST_PATH)
    if digest_content is None:
        findings.append(f"  UNREADABLE  {DIGEST_PATH.relative_to(ROOT)}")
        return findings

    digest_fm = parse_frontmatter(digest_content)
    generated = digest_fm.get("generated", "")
    if not generated:
        findings.append(
            f"  STALE DIGEST  {DIGEST_PATH.relative_to(ROOT)}"
            " — no generated: date in frontmatter"
        )
        return findings

    # Find the most recent snapshot last_updated
    newest_entity = ""
    newest_path = None

    for entity_path in sorted(ENTITIES_DIR.rglob("*.md")):
        if entity_path.name.startswith("_"):
            continue
        content = read_file_safe(entity_path)
        if content is None:
            continue
        fm = parse_frontmatter(content)
        if fm.get("type") != "snapshot":
            continue
        lu = fm.get("last_updated", "")
        if lu and lu > newest_entity:
            newest_entity = lu
            newest_path = entity_path

    if newest_entity and newest_entity > generated:
        rel_entity = newest_path.relative_to(ROOT)
        findings.append(
            f"  STALE DIGEST  {DIGEST_PATH.relative_to(ROOT)}"
            f"  (generated: {generated}"
            f" | newest snapshot: {rel_entity} at {newest_entity})"
            " — run: python scripts/generate_digest.py"
        )

    return findings


# ---------------------------------------------------------------------------
# Check 3 — Index drift
# ---------------------------------------------------------------------------

def parse_index_entity_table(content: str) -> list[tuple[str, str, str]]:
    """
    Parse the ## Entities table in index.md.
    Returns list of (entity_label, wikilink_target, date_in_index).
    Table format: | Entity | [[wikilink]] | YYYY-MM-DD |
    """
    rows = []
    in_entities = False

    for line in content.splitlines():
        if re.match(r"^##\s+Entities\b", line, re.IGNORECASE):
            in_entities = True
            continue
        if in_entities:
            if re.match(r"^##\s+", line):
                break
            # Match a table data row (not header or separator)
            if not line.startswith("|") or re.match(r"^\|[-\s|]+\|$", line):
                continue
            cols = [c.strip() for c in line.strip("|").split("|")]
            if len(cols) < 3:
                continue
            entity_label = cols[0].strip()
            link_col = cols[1].strip()
            date_col = cols[2].strip()
            # Extract wikilink target
            m = WIKILINK_RE.search(link_col)
            if not m:
                continue
            wikilink_target = m.group(1).strip()
            # Skip header row
            if entity_label.lower() in ("entity", ""):
                continue
            rows.append((entity_label, wikilink_target, date_col))

    return rows


def resolve_entity_path(wikilink_target: str) -> Path | None:
    """
    Given a wikilink target like 'entities/people/fadwa' or 'entities/projects/snapshot',
    find the corresponding .md file in the vault.
    """
    candidate = ROOT / (wikilink_target.rstrip("/") + ".md")
    if candidate.exists():
        return candidate

    # Try searching under entities/ by stem
    stem = Path(wikilink_target).stem
    for p in ENTITIES_DIR.rglob(f"{stem}.md"):
        if not p.name.startswith("_"):
            return p

    return None


def check_index_drift() -> list[str]:
    """
    Compare dates in index.md Entities table against actual snapshot last_updated.
    """
    findings = []

    if not INDEX_PATH.exists():
        findings.append(f"  MISSING  {INDEX_PATH.relative_to(ROOT)} not found")
        return findings

    content = read_file_safe(INDEX_PATH)
    if content is None:
        findings.append(f"  UNREADABLE  {INDEX_PATH.relative_to(ROOT)}")
        return findings

    rows = parse_index_entity_table(content)
    if not rows:
        findings.append(
            f"  NO TABLE  {INDEX_PATH.relative_to(ROOT)} — ## Entities table not found or empty"
        )
        return findings

    for entity_label, wikilink_target, index_date in rows:
        entity_path = resolve_entity_path(wikilink_target)
        if entity_path is None:
            findings.append(
                f"  INDEX DRIFT  '{entity_label}'"
                f" → [[{wikilink_target}]] not found"
            )
            continue

        entity_content = read_file_safe(entity_path)
        if entity_content is None:
            continue

        fm = parse_frontmatter(entity_content)
        actual_date = fm.get("last_updated", "")
        if not actual_date:
            continue

        if index_date != actual_date:
            rel = entity_path.relative_to(ROOT)
            findings.append(
                f"  INDEX DRIFT  '{entity_label}'"
                f"  (index.md shows {index_date}"
                f" | snapshot is {actual_date}"
                f" → {rel})"
            )

    return findings


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run():
    parser = argparse.ArgumentParser(
        description=(
            "validate_freshness.py — drift detector for Context 2.0.\n"
            "Flags stale snapshots, stale digest, and index drift at session open."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.parse_args()

    print("validate_freshness.py — Context 2.0 drift check")
    print("=" * 52)
    print()

    total_findings = 0

    # --- Check 1 ---
    print("CHECK 1 — Stale snapshots (meeting newer than last_updated)")
    snapshot_findings = check_stale_snapshots()
    if snapshot_findings:
        for f in snapshot_findings:
            print(f)
        total_findings += len(snapshot_findings)
    else:
        print("  ✓ All snapshots are current with their linked meetings")
    print()

    # --- Check 2 ---
    print("CHECK 2 — Stale digest (_digest.md)")
    digest_findings = check_stale_digest()
    if digest_findings:
        for f in digest_findings:
            print(f)
        total_findings += len(digest_findings)
    else:
        print("  ✓ _digest.md is up to date")
    print()

    # --- Check 3 ---
    print("CHECK 3 — Index drift (index.md Entities table)")
    index_findings = check_index_drift()
    if index_findings:
        for f in index_findings:
            print(f)
        total_findings += len(index_findings)
    else:
        print("  ✓ index.md is in sync with all snapshots")
    print()

    # --- Summary ---
    print("=" * 52)
    if total_findings == 0:
        print("No drift found. Vault is fresh.")
        sys.exit(0)
    else:
        print(f"{total_findings} finding(s). Resolve before relying on cached state.")
        sys.exit(1)


if __name__ == "__main__":
    run()
