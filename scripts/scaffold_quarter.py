#!/usr/bin/env python3
"""
scaffold_quarter.py — creates the full folder structure for a new quarter in Context 2.0

Usage:
    python scripts/scaffold_quarter.py 2026 Q3
    python scripts/scaffold_quarter.py 2027 Q1 --dry-run

Creates:
    calendar/[year]/[quarter]/
        daily/
            _template.md    (copied from existing daily template)
        weekly/
            _template.md    (copied from existing weekly template)
        [month1]-[year].md
        [month2]-[year].md
        [month3]-[year].md
        review.md
"""

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

QUARTER_MONTHS = {
    "Q1": ["january", "february", "march"],
    "Q2": ["april", "may", "june"],
    "Q3": ["july", "august", "september"],
    "Q4": ["october", "november", "december"],
}

DAILY_TEMPLATE_SOURCE = ROOT / "calendar/2026/Q2/daily/_template.md"
WEEKLY_TEMPLATE_SOURCE = ROOT / "calendar/2026/Q2/weekly/_template.md"


def month_template(month: str, year: int, quarter: str) -> str:
    month_title = month.capitalize()
    return f"""---
type: monthly-review
month: {month_title} {year}
quarter: {quarter}
last_updated: {year}-01-01
---

# {month_title} {year}

## Focus This Month

-

## Meetings

-

## Key Wins

-

## Notes

-
"""


def review_template(year: int, quarter: str, months: list[str]) -> str:
    m1, m2, m3 = [m.capitalize() for m in months]
    return f"""---
type: quarterly-review
quarter: {quarter} {year}
last_updated: {year}-01-01
---

# {quarter} {year} Quarterly Review

{m1} – {m2} – {m3}

## What This Quarter Was About

-

## Biggest Wins

-

## What Didn't Move

-

## Patterns and Themes

-

## Heading Into Q{int(quarter[1]) % 4 + 1}

-
"""


def scaffold(year: int, quarter: str, dry_run: bool = False):
    if quarter not in QUARTER_MONTHS:
        print(f"Invalid quarter '{quarter}'. Must be Q1, Q2, Q3, or Q4.")
        sys.exit(1)

    months = QUARTER_MONTHS[quarter]
    base = ROOT / "calendar" / str(year) / quarter

    if base.exists():
        print(f"Warning: {base.relative_to(ROOT)} already exists.")
        confirm = input("Continue and add missing files? [y/N] ").strip().lower()
        if confirm != "y":
            print("Aborted.")
            sys.exit(0)

    actions = []

    # Directories
    daily_dir = base / "daily"
    weekly_dir = base / "weekly"
    actions.append(("mkdir", daily_dir))
    actions.append(("mkdir", weekly_dir))

    # Daily template
    daily_dest = daily_dir / "_template.md"
    if DAILY_TEMPLATE_SOURCE.exists():
        actions.append(("copy", DAILY_TEMPLATE_SOURCE, daily_dest))
    else:
        print(f"  Warning: daily template not found at {DAILY_TEMPLATE_SOURCE.relative_to(ROOT)}")

    # Weekly template
    weekly_dest = weekly_dir / "_template.md"
    if WEEKLY_TEMPLATE_SOURCE.exists():
        actions.append(("copy", WEEKLY_TEMPLATE_SOURCE, weekly_dest))
    else:
        print(f"  Warning: weekly template not found at {WEEKLY_TEMPLATE_SOURCE.relative_to(ROOT)}")

    # Monthly files
    for month in months:
        dest = base / f"{month}-{year}.md"
        actions.append(("write", dest, month_template(month, year, quarter)))

    # Quarterly review
    review_dest = base / "review.md"
    actions.append(("write", review_dest, review_template(year, quarter, months)))

    # Execute or preview
    print(f"\n{'DRY RUN — ' if dry_run else ''}Scaffolding {quarter} {year}:\n")
    for action in actions:
        kind = action[0]
        if kind == "mkdir":
            path = action[1]
            rel = path.relative_to(ROOT)
            print(f"  mkdir  {rel}/")
            if not dry_run:
                path.mkdir(parents=True, exist_ok=True)
        elif kind == "copy":
            src, dest = action[1], action[2]
            rel = dest.relative_to(ROOT)
            if dest.exists():
                print(f"  skip   {rel}  (already exists)")
            else:
                print(f"  copy   {rel}")
                if not dry_run:
                    shutil.copy2(src, dest)
        elif kind == "write":
            dest, content = action[1], action[2]
            rel = dest.relative_to(ROOT)
            if dest.exists():
                print(f"  skip   {rel}  (already exists)")
            else:
                print(f"  write  {rel}")
                if not dry_run:
                    dest.write_text(content)

    if dry_run:
        print("\nDry run complete. Run without --dry-run to create files.")
    else:
        print(f"\nDone. {quarter} {year} scaffold created at calendar/{year}/{quarter}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold a new quarter in Context 2.0.")
    parser.add_argument("year", type=int, help="Year (e.g. 2026)")
    parser.add_argument("quarter", type=str, help="Quarter (Q1, Q2, Q3, or Q4)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without creating files")
    args = parser.parse_args()
    scaffold(args.year, args.quarter, dry_run=args.dry_run)
