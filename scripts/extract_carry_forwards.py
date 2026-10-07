#!/usr/bin/env python3
"""
extract_carry_forwards.py — pulls Carry Forward items from daily logs for a date range.

Usage:
    python scripts/extract_carry_forwards.py              # past 7 days
    python scripts/extract_carry_forwards.py --days 14
    python scripts/extract_carry_forwards.py --from 2026-05-04 --to 2026-05-10
    python scripts/extract_carry_forwards.py --output calendar/2026/Q2/weekly/_carries.md
"""

import argparse
import re
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent

QUARTER_MAP = {
    1: "Q1", 2: "Q1", 3: "Q1",
    4: "Q2", 5: "Q2", 6: "Q2",
    7: "Q3", 8: "Q3", 9: "Q3",
    10: "Q4", 11: "Q4", 12: "Q4",
}

SECTIONS = ["Done", "Blockers / Friction", "Carry Forward", "Notes / Observations", "Today's Focus"]
SECTION_PATTERN = re.compile(r"^##\s+(.+)")


def daily_log_path(d: date) -> Path:
    quarter = QUARTER_MAP[d.month]
    return ROOT / "calendar" / str(d.year) / quarter / "daily" / f"{d.isoformat()}.md"


def extract_sections(content: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    current_section = None
    for line in content.splitlines():
        m = SECTION_PATTERN.match(line)
        if m:
            current_section = m.group(1).strip()
            continue
        if current_section and line.strip().startswith("- ") and len(line.strip()) > 2:
            result.setdefault(current_section, []).append(line.strip())
    return result


def run(start: date, end: date, output: str | None = None):
    days_data = {}
    current = start
    while current <= end:
        path = daily_log_path(current)
        if path.exists():
            content = path.read_text()
            sections = extract_sections(content)
            if any(sections.values()):
                days_data[current.isoformat()] = sections
        current += timedelta(days=1)

    if not days_data:
        print("No daily log data found in the date range.")
        return

    lines = [
        f"# Week Summary — {start.isoformat()} to {end.isoformat()}",
        "_Pre-processed by extract_carry_forwards.py. Feed to /weekly-review._",
        "",
    ]

    for day, sections in sorted(days_data.items()):
        lines.append(f"## {day}")
        for section_name in ["Today's Focus", "Done", "Blockers / Friction", "Carry Forward", "Notes / Observations"]:
            items = sections.get(section_name, [])
            if items:
                lines.append(f"**{section_name}**")
                lines.extend(items)
                lines.append("")
        lines.append("")

    output_text = "\n".join(lines)
    print(output_text)

    if output:
        out_path = ROOT / output
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output_text)
        print(f"\nWritten to {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract weekly data from daily logs.")
    parser.add_argument("--days", type=int, default=7, help="Past N days to scan (default: 7)")
    parser.add_argument("--from", dest="from_date", type=str, help="Start date YYYY-MM-DD")
    parser.add_argument("--to", dest="to_date", type=str, help="End date YYYY-MM-DD (default: today)")
    parser.add_argument("--output", type=str, help="Write to this path (relative to repo root)")
    args = parser.parse_args()

    today = date.today()
    if args.from_date:
        start = date.fromisoformat(args.from_date)
        end = date.fromisoformat(args.to_date) if args.to_date else today
    else:
        end = today
        start = end - timedelta(days=args.days - 1)

    run(start, end, args.output)
