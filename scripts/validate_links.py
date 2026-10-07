#!/usr/bin/env python3
"""
validate_links.py — checks meeting files have matching cross-links in entity and month files.

For each meeting in meetings/:
  - Reads the backlink header (← [[entity]] | [[calendar/month]])
  - Verifies the entity file has a ## Meetings entry linking back
  - Verifies the month file has a ## Meetings entry linking back

Usage:
    python scripts/validate_links.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
MEETINGS_DIR = ROOT / "meetings"

BACKLINK_RE = re.compile(r"\[\[([^\]|]+)")


def get_backlink_targets(content: str) -> list[str]:
    # Backlink header appears after the frontmatter block (after the second ---)
    lines = content.splitlines()
    dashes_seen = 0
    for line in lines[:25]:
        if line.strip() == "---":
            dashes_seen += 1
            continue
        if dashes_seen >= 2 and ("←" in line or "<-" in line):
            return [m.group(1).strip() for m in BACKLINK_RE.finditer(line)]
    return []


def get_meetings_section_links(content: str) -> list[str]:
    in_meetings = False
    links = []
    for line in content.splitlines():
        if re.match(r"^##\s+Meetings\b", line, re.IGNORECASE):
            in_meetings = True
            continue
        if in_meetings:
            if re.match(r"^##\s+", line):
                break
            for m in BACKLINK_RE.finditer(line):
                links.append(m.group(1).strip())
    return links


def run():
    if not MEETINGS_DIR.exists():
        print("meetings/ not found.")
        return

    meeting_files = sorted(MEETINGS_DIR.glob("*.md"))
    if not meeting_files:
        print("No meeting files found.")
        return

    errors = []
    warnings = []

    for meeting_file in meeting_files:
        content = meeting_file.read_text(encoding="utf-8")
        stem = meeting_file.stem
        targets = get_backlink_targets(content)

        if not targets:
            warnings.append(f"  NO BACKLINKS  {meeting_file.name} — no ← header found")
            continue

        for target in targets:
            candidate = ROOT / (target + ".md")
            if not candidate.exists():
                errors.append(f"  MISSING FILE  {meeting_file.name} → [[{target}]] (not found at {candidate.relative_to(ROOT)})")
                continue

            target_content = candidate.read_text(encoding="utf-8")
            backlinks = get_meetings_section_links(target_content)

            if stem not in backlinks:
                errors.append(
                    f"  MISSING LINK  {candidate.relative_to(ROOT)} → ## Meetings missing [[{stem}]]"
                )

    if warnings:
        print(f"\n{len(warnings)} warning(s):\n")
        for w in warnings:
            print(w)

    if errors:
        print(f"\n{len(errors)} broken link(s):\n")
        for e in errors:
            print(e)
        print()
    elif not warnings:
        print("All meeting cross-links are valid.")
    else:
        print("\nNo broken links found.")


if __name__ == "__main__":
    run()
