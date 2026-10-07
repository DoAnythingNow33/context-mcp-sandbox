#!/usr/bin/env python3
"""
system_health.py — zero-token attention scan for Context 2.0.

Surfaces what's worth Dan's attention and writes it to _health.md.
Offline, pure stdlib, no network. Always exits 0.

Usage:
    python scripts/system_health.py

It deliberately does NOT grade. The health score (/100, with trend arrows and
a pass/fail exit code) was retired 2026-08-25 at Dan's request: its biggest
penalty was the daily-log gap, so the number mostly measured how diligently he
fed the vault rather than how useful the vault was to him — a quiet family
fortnight rendered as 11/100 and a red card in Discord every night. Habit
metrics (DPL gaps, commit→done ratio) went with it. Don't reintroduce either.

Action checks are also gone: actions moved to the Notion Tasks Tracker on
2026-09-02 and this script has no network access, so rotting/stale detection is
now a Notion view and the unfiled-next_action reconciliation belongs to
/maintain. What's left is the layer this script can actually see — entities,
IP, meetings, index links.
"""

import json
import re
import subprocess
import sys
from datetime import date, timedelta
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).parent.parent

ENTITIES_DIR   = ROOT / "entities"
ACTIONS_DIR    = ROOT / "actions"
CALENDAR_DIR   = ROOT / "calendar"
DAILY_DIR      = ROOT / "calendar" / "2026" / "Q2" / "daily"
MEETINGS_DIR   = ROOT / "meetings"
IP_DIR         = ROOT / "IP"
GOALS_PATH     = ROOT / "self" / "goals.md"
INDEX_PATH     = ROOT / "index.md"
HEALTH_PATH    = ROOT / "_health.md"
SUPPRESS_PATH  = Path(__file__).parent / ".health-suppress.json"

# Matches [[some/path/slug]] or [[slug]] — captures inner text only
WIKILINK_RE = re.compile(r"\[\[([^\]|]+?)(?:\|[^\]]*)?\]\]")

# Matches YYYY-MM-DD at the start of a filename stem
DATE_PREFIX_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")

TODAY = date.today()


# ---------------------------------------------------------------------------
# Shared helpers — verbatim from validate_freshness.py
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
# Index helpers — verbatim from validate_freshness.py
# ---------------------------------------------------------------------------

def parse_index_entity_table(content: str) -> list[tuple[str, str, str]]:
    """
    Parse the ## Entities table in index.md.
    Returns list of (entity_label, wikilink_target, date_in_index).
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
            if not line.startswith("|") or re.match(r"^\|[-\s|]+\|$", line):
                continue
            cols = [c.strip() for c in line.strip("|").split("|")]
            if len(cols) < 3:
                continue
            entity_label = cols[0].strip()
            link_col = cols[1].strip()
            date_col = cols[2].strip()
            m = WIKILINK_RE.search(link_col)
            if not m:
                continue
            wikilink_target = m.group(1).strip()
            if entity_label.lower() in ("entity", ""):
                continue
            rows.append((entity_label, wikilink_target, date_col))

    return rows


def resolve_entity_path(wikilink_target: str) -> Path | None:
    """Resolve a wikilink target to an .md file in the vault."""
    candidate = ROOT / (wikilink_target.rstrip("/") + ".md")
    if candidate.exists():
        return candidate
    stem = Path(wikilink_target).stem
    for p in ENTITIES_DIR.rglob(f"{stem}.md"):
        if not p.name.startswith("_"):
            return p
    return None


# ---------------------------------------------------------------------------
# Vault helpers
# ---------------------------------------------------------------------------

def iter_action_files(subfolder: str):
    """Yield valid action .md files from actions/<subfolder>/. Skip Icon, _, template."""
    folder = ACTIONS_DIR / subfolder
    if not folder.exists():
        return
    for p in sorted(folder.glob("*.md")):
        if p.name.startswith("_") or p.name.startswith("Icon"):
            continue
        yield p


@lru_cache(maxsize=1)
def git_add_dates() -> dict:
    """
    Map repo-relative path -> date the file was first committed.

    Needed because mtime is worthless in CI: actions/checkout writes a fresh
    clone, so every file's mtime is the checkout time and nothing ever looks
    old. Before this, 43 of 67 backlog actions had no date of their own and
    silently read as 0 days old on every scheduled run.

    Requires full history — the workflows that run this set fetch-depth: 0.
    One `git log` for the whole tree rather than one per file.
    """
    try:
        out = subprocess.run(
            ["git", "log", "--diff-filter=A", "--name-only", "--format=%at", "--", "actions/"],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
        ).stdout
    except Exception:
        return {}

    dates: dict[str, date] = {}
    current: date | None = None
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.isdigit():
            current = date.fromtimestamp(int(line))
        elif current:
            # git log walks newest-first, so keep overwriting to land on the
            # oldest (first) addition for paths added more than once.
            dates[line] = current
    return dates


def action_source_date(fm: dict, path: Path) -> date:
    """
    Best available creation date for an action, most to least trustworthy:
    the source meeting wikilink, a YYYY-MM-DD- filename prefix, an explicit
    frontmatter date, when git first saw it, and only then mtime.
    """
    source = fm.get("source", "")
    if source:
        # source looks like "[[2026-06-05-some-slug]]"
        m = WIKILINK_RE.search(source)
        if m:
            stem = Path(m.group(1)).stem
            d = meeting_date_from_stem(stem)
            if d:
                try:
                    return date.fromisoformat(d)
                except ValueError:
                    pass

    m = DATE_PREFIX_RE.match(path.name)
    if m:
        try:
            return date.fromisoformat(m.group(1))
        except ValueError:
            pass

    for key in ("created", "date", "due"):
        val = str(fm.get(key, "")).strip()[:10]
        if val:
            try:
                return date.fromisoformat(val)
            except ValueError:
                pass

    try:
        rel = path.relative_to(ROOT).as_posix()
    except ValueError:
        rel = path.as_posix()
    git_date = git_add_dates().get(rel)
    if git_date:
        return git_date

    return date.fromtimestamp(path.stat().st_mtime)


def load_snapshot_entities() -> list[tuple[str, dict, Path, str]]:
    """Return list of (entity_name, frontmatter, path, content) for all snapshots."""
    results = []
    for p in sorted(ENTITIES_DIR.rglob("*.md")):
        if p.name.startswith("_") or p.name.startswith("Icon"):
            continue
        content = read_file_safe(p)
        if not content:
            continue
        fm = parse_frontmatter(content)
        if fm.get("type") != "snapshot":
            continue
        # dormant: true means Dan has deliberately parked this thread. A parked
        # entity is not decaying, so flagging it as quiet is just nagging about
        # a decision he already made. Unset it to bring the entity back.
        if str(fm.get("dormant", "")).strip().lower() in ("true", "yes"):
            continue
        name = fm.get("entity", p.stem)
        results.append((name, fm, p, content))
    return results


# ---------------------------------------------------------------------------
# DECAY checks
# ---------------------------------------------------------------------------

def check_quiet_entities(snapshots) -> list[str]:
    """
    [decay.quiet_entity] — snapshot entity whose newest Meetings link date
    is >14 days ago AND last_updated >14 days ago.
    """
    findings = []
    cutoff = (TODAY - timedelta(days=14)).isoformat()

    for name, fm, path, content in snapshots:
        last_updated = fm.get("last_updated", "")
        if last_updated and last_updated >= cutoff:
            continue  # recently updated — not quiet

        meeting_links = extract_meetings_section_links(content)
        newest_meeting = None
        for link in meeting_links:
            stem = Path(link).stem
            d = meeting_date_from_stem(stem)
            if d and (newest_meeting is None or d > newest_meeting):
                newest_meeting = d

        if newest_meeting and newest_meeting >= cutoff:
            continue  # recent meeting, even if snapshot is old

        # Both conditions: no meeting and no update in >14 days
        rel = path.relative_to(ROOT)
        if newest_meeting:
            last_date = max(newest_meeting, last_updated) if last_updated else newest_meeting
        else:
            last_date = last_updated or "unknown"

        if last_date and last_date >= cutoff:
            continue

        # Compute days since last touch
        if last_updated:
            try:
                days_snapshot = (TODAY - date.fromisoformat(last_updated)).days
            except ValueError:
                days_snapshot = "?"
        else:
            days_snapshot = "?"

        if newest_meeting:
            try:
                days_meeting = (TODAY - date.fromisoformat(newest_meeting)).days
            except ValueError:
                days_meeting = "?"
            summary = (
                f"{name} — no meeting in {days_meeting}d "
                f"(last {newest_meeting}), snapshot {days_snapshot}d old"
            )
        else:
            summary = f"{name} — no meetings logged, snapshot {days_snapshot}d old"

        findings.append(f"- [decay.quiet_entity] {summary} → {rel}")

    return findings


def check_dpl_gaps(suppressed_dates: set | None = None) -> list[str]:
    """[decay.dpl_gap] — missing daily logs in the last 14 calendar days.

    Dates in suppressed_dates (resolved 'gone is gone' via /maintain) are
    excluded from the gap count so they stop dragging the score.
    """
    suppressed_dates = suppressed_dates or set()
    existing = set()
    if DAILY_DIR.exists():
        for p in DAILY_DIR.glob("*.md"):
            if p.name.startswith("_") or p.name.startswith("Icon"):
                continue
            m = DATE_PREFIX_RE.match(p.stem)
            if m:
                existing.add(m.group(1))

    missing = []
    for i in range(14):
        day = TODAY - timedelta(days=i)
        ds = day.isoformat()
        if ds not in existing and ds not in suppressed_dates:
            missing.append(ds)

    missing.sort()
    if not missing:
        return []

    date_list = ", ".join(missing[:14])
    return [f"- [decay.dpl_gap] {len(missing)} of last 14 days missing: {date_list}"]


def check_parked_threads() -> list[str]:
    """[decay.parked_thread] — Active/Business threads containing stalled language."""
    findings = []
    content = read_file_safe(GOALS_PATH)
    if not content:
        return findings

    # Find Active Threads and Business Threads sections
    in_target_section = False
    target_sections = re.compile(r"^##\s+(Active Threads|Business Threads)\b", re.IGNORECASE)
    end_section = re.compile(r"^##\s+", re.IGNORECASE)
    stall_words = re.compile(r"\b(parked|waiting on|stalled|someday)\b", re.IGNORECASE)

    for line in content.splitlines():
        if target_sections.match(line):
            in_target_section = True
            continue
        if in_target_section and end_section.match(line):
            in_target_section = False
            continue
        if in_target_section and line.startswith("- ") and stall_words.search(line):
            text = line[2:].strip()
            if len(text) > 80:
                text = text[:77] + "..."
            findings.append(f"- [decay.parked_thread] {text}")

    return findings


# ---------------------------------------------------------------------------
# ACCOUNTABILITY checks
# ---------------------------------------------------------------------------

def check_acct_ratio() -> tuple[list[str], int, int]:
    """
    [acct.ratio] — actions created vs completed last 7 days.
    Returns (findings, created_count, done_count).
    """
    cutoff = TODAY - timedelta(days=7)

    created = 0
    for subfolder in ("backlog", "doing", "done"):
        for p in iter_action_files(subfolder):
            content = read_file_safe(p)
            fm = parse_frontmatter(content) if content else {}
            age_date = action_source_date(fm, p)
            if age_date > cutoff:
                created += 1

    done_7d = 0
    for p in iter_action_files("done"):
        mtime = date.fromtimestamp(p.stat().st_mtime)
        if mtime > cutoff:
            done_7d += 1

    ratio = done_7d / max(created, 1)
    findings = [
        f"- [acct.ratio] Commit→done last 7d: {created} created / {done_7d} done "
        f"(ratio {ratio:.2f})"
    ]
    return findings, created, done_7d


def normalize_text(text: str) -> str:
    """Lowercase + strip punctuation for loose matching."""
    return re.sub(r"[^\w\s]", "", text.lower())


def check_unfiled_next_actions(snapshots) -> list[str]:
    """
    [acct.unfiled_next_action] — snapshot next_actions with no matching action file title.
    Uses 12+ char substring overlap as the matching heuristic.
    """
    # Build set of normalized action titles
    action_titles = []
    for subfolder in ("backlog", "doing"):
        for p in iter_action_files(subfolder):
            content = read_file_safe(p)
            if content:
                fm = parse_frontmatter(content)
                title = fm.get("title", "")
                if title:
                    action_titles.append(normalize_text(title))

    findings = []
    for name, fm, path, _content in snapshots:
        next_actions = fm.get("next_actions", [])
        if isinstance(next_actions, str):
            next_actions = [next_actions]
        for action_text in next_actions:
            norm_action = normalize_text(action_text)
            if len(norm_action) < 12:
                continue  # too short to match reliably

            matched = False
            for title_norm in action_titles:
                # Check if any 12+ char substring of norm_action appears in title_norm
                for start in range(len(norm_action) - 11):
                    chunk = norm_action[start:start + 12]
                    if chunk in title_norm:
                        matched = True
                        break
                if matched:
                    break

            if not matched:
                truncated = action_text[:60] + ("..." if len(action_text) > 60 else "")
                rel = path.relative_to(ROOT)
                findings.append(
                    f'- [acct.unfiled_next_action] {name}: next_action not filed'
                    f' — "{truncated}" → {rel}'
                )

    return findings


# ---------------------------------------------------------------------------
# COHERENCE checks
# ---------------------------------------------------------------------------

def check_index_drift(snapshots) -> list[str]:
    """[cohere.index_drift] — reuses validate_freshness.py logic."""
    findings = []

    if not INDEX_PATH.exists():
        findings.append("- [cohere.index_drift] index.md not found")
        return findings

    content = read_file_safe(INDEX_PATH)
    if not content:
        findings.append("- [cohere.index_drift] index.md unreadable")
        return findings

    rows = parse_index_entity_table(content)
    if not rows:
        return findings

    for entity_label, wikilink_target, index_date in rows:
        entity_path = resolve_entity_path(wikilink_target)
        if entity_path is None:
            findings.append(
                f"- [cohere.index_drift] {entity_label} — "
                f"[[{wikilink_target}]] not found"
            )
            continue

        entity_content = read_file_safe(entity_path)
        if not entity_content:
            continue
        fm = parse_frontmatter(entity_content)
        actual_date = fm.get("last_updated", "")
        if not actual_date:
            continue

        if index_date != actual_date:
            rel = entity_path.relative_to(ROOT)
            findings.append(
                f"- [cohere.index_drift] {entity_label} — "
                f"index {index_date} / snapshot {actual_date} → {rel}"
            )

    return findings


def check_unused_ip() -> list[str]:
    """[cohere.unused_ip] — count IP files with content_made: false."""
    total_false = 0
    old_false = 0
    cutoff = TODAY - timedelta(days=30)

    for p in sorted(IP_DIR.glob("*.md")):
        if p.name.startswith("_") or p.name.startswith("Icon"):
            continue
        # Skip context.md (operational, not IP database)
        if p.stem == "context":
            continue
        content = read_file_safe(p)
        if not content:
            continue
        fm = parse_frontmatter(content)
        # Only count files that explicitly have content_made field
        if "content_made" not in fm:
            continue
        val = str(fm.get("content_made", "")).lower()
        if val == "false":
            total_false += 1
            mtime = date.fromtimestamp(p.stat().st_mtime)
            if mtime <= cutoff:
                old_false += 1

    if total_false == 0:
        return []

    return [
        f"- [cohere.unused_ip] {total_false} IP entries content_made:false "
        f"({old_false} older than 30d)"
    ]


def check_missing_tension(snapshots) -> list[str]:
    """[cohere.missing_tension] — snapshot missing or empty tensions or open_questions."""
    findings = []
    for name, fm, path, _content in snapshots:
        tensions = fm.get("tensions", [])
        oq = fm.get("open_questions", [])
        missing = []
        if not tensions:
            missing.append("tensions")
        if not oq:
            missing.append("open_questions")
        if missing:
            rel = path.relative_to(ROOT)
            findings.append(
                f"- [cohere.missing_tension] {name} snapshot missing "
                f"{'/'.join(missing)} → {rel}"
            )
    return findings


def check_orphan_meetings() -> list[str]:
    """
    [cohere.orphan_meeting] — meeting file not referenced anywhere in
    entities/ or calendar/ as a [[stem]] wikilink.
    """
    findings = []

    # Build a blob of all entity + calendar text for substring search
    blob_parts = []
    for p in ENTITIES_DIR.rglob("*.md"):
        if p.name.startswith("_") or p.name.startswith("Icon"):
            continue
        c = read_file_safe(p)
        if c:
            blob_parts.append(c)

    for p in CALENDAR_DIR.rglob("*.md"):
        if p.name.startswith("_") or p.name.startswith("Icon"):
            continue
        c = read_file_safe(p)
        if c:
            blob_parts.append(c)

    blob = "\n".join(blob_parts)

    if not MEETINGS_DIR.exists():
        return findings

    # context.md is the meetings/ workspace README described in CLAUDE.md, not a
    # meeting record. /maintain identified it as a false positive on three
    # consecutive runs before it was excluded here.
    NON_MEETINGS = {"context", "README"}

    for p in sorted(MEETINGS_DIR.rglob("*.md")):
        if p.name.startswith("_") or p.name.startswith("Icon"):
            continue
        stem = p.stem
        if stem in NON_MEETINGS:
            continue
        # A meeting is referenced if [[stem]] appears anywhere in entities/calendar
        if f"[[{stem}]]" not in blob and f"[[{stem}|" not in blob:
            rel = p.relative_to(ROOT)
            findings.append(
                f"- [cohere.orphan_meeting] {stem} — not linked in entities/ or calendar/"
                f" → {rel}"
            )

    return findings


# ---------------------------------------------------------------------------
# Suppressions
# ---------------------------------------------------------------------------

def load_suppress() -> dict:
    """
    Load scripts/.health-suppress.json — resolutions /maintain applied from
    Dan's interview answers. Shape:
      {
        "dpl_gap_dates": ["YYYY-MM-DD", ...],   # excluded from the gap count
        "suppress_until": {"<tag>": "YYYY-MM-DD"}  # finding tag muted until date
      }
    """
    if not SUPPRESS_PATH.exists():
        return {}
    try:
        data = json.loads(SUPPRESS_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def is_suppressed(tag: str, suppress: dict) -> bool:
    """True if a finding tag is muted until a future date."""
    until = suppress.get("suppress_until", {}).get(tag)
    if not until:
        return False
    try:
        return TODAY < date.fromisoformat(until)
    except ValueError:
        return False


def filter_suppressed(findings: list[str], suppress: dict) -> list[str]:
    """Drop finding lines whose [tag] is currently suppressed."""
    if not suppress.get("suppress_until"):
        return findings
    out = []
    for f in findings:
        m = re.search(r"\[([\w.]+)\]", f)
        tag = m.group(1) if m else ""
        if tag and is_suppressed(tag, suppress):
            continue
        out.append(f)
    return out


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run():
    """
    Surface what's worth Dan's attention. Deliberately does not grade.

    There is no score, no trend, and no pass/fail exit code. An earlier version
    computed a health score out of 100, and because the biggest single penalty
    was the daily-log gap, the number mostly measured how diligently Dan had fed
    the vault rather than how useful the vault was to him — which made a quiet
    family fortnight read as a failing grade. Retired 2026-08-25 at his call.

    Habit-grading checks (DPL gaps, commit→done ratio) are retired with it. The
    functions remain defined but unused, so the intent is recoverable from git
    rather than guessed at.

    Action checks are gone too, for a different reason: actions moved to the
    Notion Tasks Tracker on 2026-09-02, and this script is deliberately offline
    pure-stdlib, so it can no longer see them. Rotting/stale detection is now a
    Notion view, and the unfiled-next-action reconciliation moved to /maintain,
    which has Notion access. A checker that cannot read the data should not
    pretend to check it — with actions/ empty, the unfiled check reported all 42
    next_actions as loose ends, which was noise, not signal.
    """
    today_str = TODAY.isoformat()

    suppress = load_suppress()

    # --- Load all snapshot entities once ---
    snapshots = load_snapshot_entities()

    # --- People and commitments going quiet ---
    quiet_entities  = filter_suppressed(check_quiet_entities(snapshots), suppress)
    parked_threads  = filter_suppressed(check_parked_threads(), suppress)

    attention_findings = quiet_entities + parked_threads

    # --- Mechanical drift /maintain can usually just fix ---
    index_drift     = filter_suppressed(check_index_drift(snapshots), suppress)
    unused_ip       = filter_suppressed(check_unused_ip(), suppress)
    missing_tension = filter_suppressed(check_missing_tension(snapshots), suppress)
    orphan_meetings = filter_suppressed(check_orphan_meetings(), suppress)

    mechanics_findings = index_drift + unused_ip + missing_tension + orphan_meetings

    total_findings = len(attention_findings) + len(mechanics_findings)

    archived_done = len(list(iter_action_files("done")))

    def section_body(findings):
        if not findings:
            return "- ✓ nothing flagged"
        return "\n".join(findings)

    report = f"""---
type: attention
generated: {today_str}
findings: {total_findings}
---

# Worth a look — {today_str}

Not a scorecard. Nothing here is overdue homework; it's what the vault noticed
while you were busy. Ignore anything that isn't true.

- Open items: {total_findings}
- Live actions live in Notion (Tasks Tracker → **Active** view), not here.
  This scan covers the vault only; `done/` holds {archived_done} archived items.

## GOING QUIET
People and commitments that haven't moved in a while.

{section_body(attention_findings)}

## VAULT MECHANICS
Link drift and bookkeeping — `/maintain` fixes most of this without asking.

{section_body(mechanics_findings)}
"""

    HEALTH_PATH.write_text(report, encoding="utf-8")

    # --- Console summary ---
    print("system_health.py — Context 2.0")
    print("=" * 40)
    print(f"Open items: {total_findings}  "
          f"(going quiet {len(attention_findings)} / mechanics {len(mechanics_findings)})")
    print(f"Actions:    in Notion; {archived_done} archived in actions/done/")
    print(f"Written:    {HEALTH_PATH.relative_to(ROOT)}")

    # Always exit 0 — this is an observation, not a test that can fail.
    sys.exit(0)


if __name__ == "__main__":
    run()
