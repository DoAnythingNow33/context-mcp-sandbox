#!/usr/bin/env python3
"""
Generate Weekly Review Questions — proactive Sunday gap-filler.

Runs unattended every Sunday (via the com.dananything.weekly-questions
LaunchAgent). It looks at the week just ended and works out what /weekly-review
won't be able to reconstruct on its own — days with no DPL, planned items that
were never confirmed done, threads left hanging — then asks Claude to phrase a
short, targeted questionnaire. The result is written to:

    calendar/<year>/<quarter>/weekly/_review-questions.md

When Dan runs /weekly-review on Monday, the skill detects that file, walks him
through the questions to fill the gaps, folds his answers into the source data,
then archives the file.

Design notes:
- Python does all file IO and the deterministic gap detection (which days are
  missing, which plan items exist, what got done). This part never fails.
- Claude (via `claude -p`, stdout captured) only *phrases* the questions from
  the context Python hands it. It writes no files and needs no tool permissions.
- If the Claude call fails for any reason, a deterministic template is written
  so the file always exists for Monday.
"""

import os
import re
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

VAULT_ROOT = Path(__file__).parent.parent
CLAUDE_BIN = os.environ.get("CLAUDE_BIN", "claude")
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "sonnet")
CLAUDE_TIMEOUT = int(os.environ.get("CLAUDE_TIMEOUT", "240"))

WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday",
                 "Friday", "Saturday", "Sunday"]


def get_quarter(month: int) -> str:
    return f"Q{(month - 1) // 3 + 1}"


def weekly_dir_for(d: date) -> Path:
    return VAULT_ROOT / "calendar" / str(d.year) / get_quarter(d.month) / "weekly"


def daily_dir_for(d: date) -> Path:
    return VAULT_ROOT / "calendar" / str(d.year) / get_quarter(d.month) / "daily"


# ---------------------------------------------------------------------------
# 1. Resolve the week just ended (Mon..Sun containing `today`)
# ---------------------------------------------------------------------------
def week_bounds(today: date) -> tuple[date, date]:
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday


# ---------------------------------------------------------------------------
# 2. Read the 7 daily logs; flag missing / empty days
# ---------------------------------------------------------------------------
def collect_dpls(monday: date) -> tuple[list[dict], list[str]]:
    """Return (entries, missing_day_labels). entries are non-empty logs."""
    entries: list[dict] = []
    missing: list[str] = []
    for i in range(7):
        d = monday + timedelta(days=i)
        path = daily_dir_for(d) / f"{d.strftime('%Y-%m-%d')}.md"
        label = f"{WEEKDAY_NAMES[i]} {d.strftime('%d %b')}"
        if not path.exists():
            missing.append(label)
            continue
        text = path.read_text().strip()
        # Treat a near-empty scaffold as missing too
        if len(text) < 80:
            missing.append(f"{label} (log exists but empty)")
            continue
        entries.append({"label": label, "text": text})
    return entries, missing


# ---------------------------------------------------------------------------
# 3. Find the P- plan that covered the week just ended
# ---------------------------------------------------------------------------
def find_plan_for_week(monday: date) -> Path | None:
    target = monday.strftime("%d-%m-%y")
    candidate = weekly_dir_for(monday) / f"P-{target}.md"
    if candidate.exists():
        return candidate
    # Fall back: scan the weekly folder for the closest P- on/before monday
    wd = weekly_dir_for(monday)
    best: tuple[date, Path] | None = None
    if wd.exists():
        for p in wd.glob("P-*.md"):
            m = re.match(r"P-(\d{2})-(\d{2})-(\d{2})\.md$", p.name)
            if not m:
                continue
            dd, mm, yy = int(m.group(1)), int(m.group(2)), int(m.group(3))
            try:
                pd = date(2000 + yy, mm, dd)
            except ValueError:
                continue
            if pd <= monday and (best is None or pd > best[0]):
                best = (pd, p)
    return best[1] if best else None


# ---------------------------------------------------------------------------
# 4. Scan the actions kanban for evidence of what moved
# ---------------------------------------------------------------------------
def read_action_titles(folder: Path) -> list[str]:
    out: list[str] = []
    if not folder.exists():
        return out
    for p in sorted(folder.glob("*.md")):
        if p.name.startswith("_"):
            continue
        title = p.stem
        for line in p.read_text().splitlines():
            m = re.match(r'\s*title:\s*"?(.+?)"?\s*$', line)
            if m:
                title = m.group(1).strip()
                break
        out.append(title)
    return out


def done_this_week(folder: Path, monday: date) -> list[str]:
    """Action files in done/ touched within the review week (by mtime)."""
    out: list[str] = []
    if not folder.exists():
        return out
    week_start = datetime.combine(monday, datetime.min.time()).timestamp()
    for p in sorted(folder.glob("*.md")):
        if p.name.startswith("_"):
            continue
        if p.stat().st_mtime < week_start:
            continue
        title = p.stem
        for line in p.read_text().splitlines():
            m = re.match(r'\s*title:\s*"?(.+?)"?\s*$', line)
            if m:
                title = m.group(1).strip()
                break
        out.append(title)
    return out


# ---------------------------------------------------------------------------
# 5. Build the context block handed to Claude
# ---------------------------------------------------------------------------
def build_context(monday: date, sunday: date) -> dict:
    dpls, missing = collect_dpls(monday)
    plan_path = find_plan_for_week(monday)
    plan_text = plan_path.read_text() if plan_path else ""

    digest_path = VAULT_ROOT / "_digest.md"
    digest_text = digest_path.read_text() if digest_path.exists() else ""

    actions_root = VAULT_ROOT / "actions"
    return {
        "monday": monday,
        "sunday": sunday,
        "dpls": dpls,
        "missing": missing,
        "plan_name": plan_path.name if plan_path else None,
        "plan_text": plan_text,
        "digest_text": digest_text,
        "done": done_this_week(actions_root / "done", monday),
        "doing": read_action_titles(actions_root / "doing"),
        "backlog": read_action_titles(actions_root / "backlog"),
    }


def compose_prompt(ctx: dict) -> str:
    span = f"{ctx['monday'].strftime('%a %d %b')} – {ctx['sunday'].strftime('%a %d %b %Y')}"
    parts: list[str] = []
    parts.append(
        "You are preparing a weekly-review gap questionnaire for Dan, a solo "
        "founder/coach. The week just ended and his daily logs are incomplete. "
        "Your job: write the SHORT list of targeted questions that /weekly-review "
        "will need answered on Monday to reconstruct what actually happened and "
        "plan the coming week. Only ask about things that CANNOT be confirmed from "
        "the data below. Never ask a generic 'how did the week go'. Anchor every "
        "question to a specific planned item, a missing day, or an open thread.\n"
    )
    parts.append(f"WEEK UNDER REVIEW: {span}\n")

    if ctx["missing"]:
        parts.append("DAYS WITH NO USABLE DPL:\n- " + "\n- ".join(ctx["missing"]) + "\n")
    else:
        parts.append("DAYS WITH NO USABLE DPL: none — all 7 logged.\n")

    if ctx["dpls"]:
        logged = ", ".join(e["label"] for e in ctx["dpls"])
        parts.append(f"DAYS THAT WERE LOGGED (don't re-ask these): {logged}\n")

    if ctx["plan_text"]:
        parts.append(
            f"LAST WEEK'S PLAN ({ctx['plan_name']}) — the source of intent. "
            "Cross-check each planned item against the evidence; ask about any that "
            "can't be confirmed done:\n\n" + ctx["plan_text"].strip() + "\n"
        )
    else:
        parts.append("LAST WEEK'S PLAN: not found.\n")

    if ctx["done"]:
        parts.append("ACTIONS COMPLETED THIS WEEK (evidence — do NOT ask if these happened):\n- "
                     + "\n- ".join(ctx["done"]) + "\n")
    if ctx["doing"]:
        parts.append("ACTIONS STILL IN PROGRESS:\n- " + "\n- ".join(ctx["doing"]) + "\n")
    if ctx["backlog"]:
        parts.append("ACTIONS STILL IN BACKLOG:\n- " + "\n- ".join(ctx["backlog"]) + "\n")

    if ctx["digest_text"]:
        parts.append("CURRENT ENTITY STATES (_digest.md, for context only):\n\n"
                     + ctx["digest_text"].strip()[:4000] + "\n")

    parts.append(
        "\nOUTPUT RULES:\n"
        "- Output ONLY GitHub-flavoured markdown for the questionnaire body. No preamble, "
        "no sign-off, no code fences.\n"
        "- Group questions under `## ` headings: one per missing day, plus `## Plan items to "
        "confirm` and `## Open threads` as needed.\n"
        "- Each question is a `- [ ] ` checkbox line ending with a blank `→ ` answer prompt "
        "Dan can type after, e.g. `- [ ] Plan had 100×100 outreach Wed–Fri — did it run? Count? → `\n"
        "- 6–14 questions total. Ruthlessly skip anything already evidenced above.\n"
        "- No fabricated facts. If unsure whether something happened, ask; don't assert.\n"
    )
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# 6. Call Claude (text-gen only) with a deterministic fallback
# ---------------------------------------------------------------------------
def call_claude(prompt: str) -> str | None:
    try:
        result = subprocess.run(
            [CLAUDE_BIN, "-p", prompt, "--model", CLAUDE_MODEL],
            capture_output=True, text=True, timeout=CLAUDE_TIMEOUT,
            cwd=str(VAULT_ROOT),
        )
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"WARN: claude call failed ({e}); using fallback template.")
        return None
    if result.returncode != 0:
        print(f"WARN: claude exited {result.returncode}: {result.stderr[:400]}")
        return None
    body = result.stdout.strip()
    body = re.sub(r"^```[a-zA-Z]*\n", "", body)
    body = re.sub(r"\n```$", "", body)
    return body or None


def fallback_body(ctx: dict) -> str:
    lines: list[str] = []
    for label in ctx["missing"]:
        lines.append(f"## {label}")
        lines.append(f"- [ ] What actually happened this day vs the plan? → ")
        lines.append("")
    if ctx["plan_text"]:
        lines.append("## Plan items to confirm")
        # Pull checkbox/bulleted plan lines as confirmation prompts
        for raw in ctx["plan_text"].splitlines():
            m = re.match(r"^\s*-\s+(?:\[[ xX]\]\s+)?(.+)$", raw)
            if m and len(m.group(1)) > 8:
                lines.append(f"- [ ] Did this happen? {m.group(1).strip()} → ")
        lines.append("")
    lines.append("## Open threads")
    lines.append("- [ ] Anything that moved this week the data above didn't capture? → ")
    lines.append("- [ ] Anything urgent that must land in next week's plan? → ")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 7. Write the questions file
# ---------------------------------------------------------------------------
def write_file(ctx: dict, body: str) -> Path:
    out_dir = weekly_dir_for(ctx["monday"])
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "_review-questions.md"
    span = f"{ctx['monday'].strftime('%d %b')} – {ctx['sunday'].strftime('%d %b %Y')}"
    header = (
        "---\n"
        "type: review-questions\n"
        f"generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"week: {ctx['monday'].strftime('%d-%m-%y')}\n"
        "---\n\n"
        f"# Weekly Review — gaps to fill ({span})\n\n"
        "_Auto-generated Sunday. Your DPLs didn't cover the whole week, so answer "
        "these inline (type after each `→`) before or during `/weekly-review`. "
        "The skill reads this file first, folds your answers into the review, then "
        "archives it._\n\n"
    )
    out_path.write_text(header + body.strip() + "\n")
    return out_path


def main():
    today = date.today()
    monday, sunday = week_bounds(today)
    print(f"Generating review questions for week {monday} .. {sunday}")

    ctx = build_context(monday, sunday)

    # Nothing to ask if the whole week is logged and there's no plan to confirm.
    if not ctx["missing"] and not ctx["plan_text"]:
        print("Full week logged and no plan to cross-check — skipping.")
        return

    prompt = compose_prompt(ctx)
    body = call_claude(prompt)
    if not body:
        body = fallback_body(ctx)
        print("Wrote deterministic fallback questionnaire.")

    out_path = write_file(ctx, body)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
