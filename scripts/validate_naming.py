#!/usr/bin/env python3
"""
validate_naming.py — deterministic file naming enforcer for Context 2.0

Checks all files against naming conventions. Reports violations with suggested fixes.
Use --fix to auto-rename (will prompt for confirmation per file).

Usage:
    python scripts/validate_naming.py
    python scripts/validate_naming.py --fix
    python scripts/validate_naming.py --path calendar/2026/Q2/weekly
"""

import os
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent

RULES = [
    {
        "name": "Daily logs",
        "glob": "calendar/**/daily/*.md",
        "pattern": re.compile(r"^\d{4}-\d{2}-\d{2}\.md$"),
        "exclude": re.compile(r"^_"),
        "example": "2026-05-10.md",
        "hint": "Format: YYYY-MM-DD.md",
    },
    {
        "name": "Weekly review files",
        "glob": "calendar/**/weekly/R-*.md",
        "pattern": re.compile(r"^R-\d{2}-\d{2}-\d{2}\.md$"),
        "exclude": re.compile(r"^_"),
        "example": "R-04-05-26.md",
        "hint": "Format: R-DD-MM-YY.md (Monday start date of the week reviewed)",
    },
    {
        "name": "Weekly plan files",
        "glob": "calendar/**/weekly/P-*.md",
        "pattern": re.compile(r"^P-\d{2}-\d{2}-\d{2}\.md$"),
        "exclude": re.compile(r"^_"),
        "example": "P-11-05-26.md",
        "hint": "Format: P-DD-MM-YY.md (Monday start date of the week planned)",
    },
    {
        "name": "Meeting files",
        "glob": "meetings/*.md",
        "pattern": re.compile(r"^\d{4}-\d{2}-\d{2}-.+\.md$"),
        "exclude": re.compile(r"^_"),
        "example": "2026-04-26-growify-call-2.md",
        "hint": "Format: YYYY-MM-DD-[entity]-[descriptor].md (lowercase, hyphens, no spaces)",
    },
    {
        "name": "Content files (linkedin)",
        "glob": "IP/content/linkedin/*.md",
        "pattern": re.compile(r"^\d{4}-\d{2}-\d{2}-.+\.md$"),
        "exclude": re.compile(r"^_"),
        "example": "2026-05-18-stopped-calling-it-work.md",
        "hint": "Format: YYYY-MM-DD-[slug].md (lowercase, hyphens, no spaces)",
    },
    {
        "name": "Content files (x)",
        "glob": "IP/content/x/*.md",
        "pattern": re.compile(r"^\d{4}-\d{2}-\d{2}-.+\.md$"),
        "exclude": re.compile(r"^_"),
        "example": "2026-05-18-stopped-calling-it-work.md",
        "hint": "Format: YYYY-MM-DD-[slug].md (lowercase, hyphens, no spaces)",
    },
    {
        "name": "Monthly review files",
        "glob": "calendar/**/*.md",
        "pattern": re.compile(
            r"^(january|february|march|april|may|june|july|august|september|october|november|december)-\d{4}\.md$"
        ),
        "exclude": re.compile(r"^_|^review"),
        "example": "may-2026.md",
        "hint": "Format: [month]-[year].md (lowercase month name)",
        "match_condition": lambda f: re.match(
            r"^(january|february|march|april|may|june|july|august|september|october|november|december)",
            f.name
        ) or re.match(r"^\w+-\d{4}", f.name),
    },
]

OLD_WEEKLY_PATTERN = re.compile(r"^[RP] - WC .+\.md$")


def check_old_weekly_names(path: Path) -> list[dict]:
    """Catch the legacy 'R - WC DD:MM:YY.md' format."""
    violations = []
    for f in path.rglob("*.md"):
        if OLD_WEEKLY_PATTERN.match(f.name):
            violations.append({
                "file": f,
                "rule": "Legacy weekly naming",
                "hint": "Old format 'R - WC DD:MM:YY.md' — rename to R-DD-MM-YY.md or P-DD-MM-YY.md",
                "suggested": None,
            })
    return violations


def check_rule(rule: dict) -> list[dict]:
    violations = []
    for f in ROOT.glob(rule["glob"]):
        if not f.is_file():
            continue
        if rule["exclude"].match(f.name):
            continue
        if "match_condition" in rule and not rule["match_condition"](f):
            continue
        if not rule["pattern"].match(f.name):
            violations.append({
                "file": f,
                "rule": rule["name"],
                "hint": rule["hint"],
                "example": rule["example"],
                "suggested": None,
            })
    return violations


def suggest_fix(violation: dict) -> str | None:
    """Attempt to suggest a corrected filename for common patterns."""
    f = violation["file"]
    name = f.name

    # Legacy weekly: "R - WC 27:04:26.md" → "R-27-04-26.md"
    m = re.match(r"^([RP]) - WC (\d{2})[:/](\d{2})[:/](\d{2})\.md$", name)
    if m:
        prefix, dd, mm, yy = m.groups()
        return f"{prefix}-{dd}-{mm}-{yy}.md"

    return None


def run(fix: bool = False, target_path: str | None = None):
    violations = []

    search_root = Path(target_path) if target_path else ROOT

    # Check old-style weekly names anywhere in the tree
    violations += check_old_weekly_names(search_root)

    # Check each rule
    for rule in RULES:
        violations += check_rule(rule)

    # Filter to target path if specified
    if target_path:
        abs_target = ROOT / target_path
        violations = [v for v in violations if str(v["file"]).startswith(str(abs_target))]

    if not violations:
        print("All file names are valid.")
        return

    print(f"\n{len(violations)} naming violation(s) found:\n")
    for v in violations:
        suggested = suggest_fix(v) or v.get("suggested")
        rel = v["file"].relative_to(ROOT)
        print(f"  FAIL  {rel}")
        print(f"        Rule: {v['rule']}")
        print(f"        Hint: {v['hint']}")
        if suggested:
            print(f"        Suggested: {suggested}")
        print()

    if fix:
        print("--- Auto-fix mode ---\n")
        for v in violations:
            suggested = suggest_fix(v)
            if not suggested:
                rel = v["file"].relative_to(ROOT)
                print(f"  SKIP  {rel} — no auto-fix available. Rename manually.")
                continue
            new_path = v["file"].parent / suggested
            rel = v["file"].relative_to(ROOT)
            print(f"  Rename: {v['file'].name}  →  {suggested}")
            confirm = input("  Confirm? [y/N] ").strip().lower()
            if confirm == "y":
                v["file"].rename(new_path)
                print(f"  Done.\n")
            else:
                print(f"  Skipped.\n")
    else:
        print("Run with --fix to auto-rename where possible.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate Context 2.0 file naming conventions.")
    parser.add_argument("--fix", action="store_true", help="Auto-rename violations where possible")
    parser.add_argument("--path", type=str, help="Limit check to a subfolder (relative to repo root)")
    args = parser.parse_args()
    run(fix=args.fix, target_path=args.path)
