# Hermes Setup — Scheduled Messages

> **Superseded (2026-07-02):** Hermes-side crons proved awkward. The scheduled messages now run as GitHub Actions in `.github/workflows/` (`morning-debrief.yml`, `evening-debrief.yml`, `self-heal.yml`), sending via Discord webhook. This file remains the reference for what each message *does*; Hermes keeps only the ad-hoc capture role (`docs/hermes-capture.md`).

## Role

Hermes is Dan's always-on AI assistant. It has SSH access to the Context 2.0 GitHub repo and is responsible for two scheduled messages per day plus handling ad-hoc capture during the day (see `docs/hermes-capture.md`).

The scheduled messages replace three retired macOS LaunchAgents:
- `com.dananything.dpl-nudge` (9pm coaching nudge)
- `com.dananything.system-health` (10:30pm health eval)
- `com.dananything.weekly-questions` (Sunday 5pm review questions)

The `.telegram/` bot is also retired. Hermes is the single capture and proactive-nudge channel.

### Server access

As of 2026-07-08, the server (`5.75.188.204`) runs Hermes/Claude under a dedicated non-root `hermes` user rather than root. Secrets (`DISCORD_BOT_TOKEN`, `DISCORD_ALLOWED_USERS`, `OPENROUTER_API_KEY`) live in `/home/hermes/.hermes/.env`, owned `hermes:hermes`, mode `600`. Dan's Mac `~/.ssh/config` points the `hermes` SSH alias directly at `User hermes` (public key copied from root's `authorized_keys`), so `ssh hermes` logs straight into the `hermes` account — no more landing as root.

---

## Git Discipline

Before every read-to-message cycle:

```bash
cd /path/to/context-2.0-repo
git pull
```

After every write (morning or evening, if Hermes writes anything to the repo):

```bash
git add <specific files>
git commit -m "hermes: <brief description> (YYYY-MM-DD)"
git push
```

Use the `hermes:` prefix on all commit messages. Examples:
- `hermes: morning debrief prep — pulled _digest.md (2026-06-27)`
- `hermes: evening debrief — wrote _health.md (2026-06-27)`
- `hermes: routed brain dump to DPL + goals.md (2026-06-27)`

Never leave the working tree dirty. If there is a conflict on pull, surface it to Dan immediately rather than attempting a resolution.

---

## Morning Debrief

**Suggested time:** 7:30am

### What to read

```
self/goals.md                                   — active threads, always first
calendar/[year]/[quarter]/weekly/P-DD-MM-YY.md  — current week's plan (latest file in weekly/)
_digest.md                                      — entity snapshots (if file exists)
```

To find the current week's P- file:

```bash
ls calendar/*/Q*/weekly/P-*.md | sort | tail -1
```

### Message shape

Send Dan one short message:

1. **One-sentence orientation** — what the week's plan says the priority is today, cross-referenced against `self/goals.md` active threads.
2. **Two questions max** — targeted at what's likely changed since yesterday or what today's priority demands. Do not ask generic "how are you" questions. Ground them in the plan.

Keep the whole message to five or six lines. Dan is starting his day.

**Example (not a template — vary this):**

> Week plan has outreach to three prospects today and a Growify prep call. Goals file still shows revenue to £5k before August as the live thread.
>
> Two things: did anything shift with Growify since last we spoke? And are the three prospects already identified or do you need to pick them this morning?

---

## Evening Debrief

**Suggested time:** 9:00pm

### Steps (run in order)

**Step 1 — Health eval**

```bash
python scripts/system_health.py
```

Read `_health.md`. Extract: the current score, the trend line (up/down/flat vs last run), and the top one or two flagged findings. Summarise in one or two lines maximum — do not dump the full file at Dan.

**Step 2 — Accountability nudge**

Read today's DPL: `calendar/[year]/[quarter]/daily/YYYY-MM-DD.md`

Check whether the DPL is already closed (look for a "Close" or "End of day" section, or a `closed: true` frontmatter flag). If it is closed, skip the nudge entirely — Dan is done.

If it is not closed: cross-reference today's `P-` plan checklist against what Dan reported in the DPL. Call out one or two specific items that were committed but not yet mentioned. Be direct, not punitive — the tone is a coach checking in, not an auditor.

**Step 3 — Sunday only: review questions**

On Sundays, after steps 1 and 2:

```bash
python scripts/generate_review_questions.py
```

This writes `_review-questions.md` into the current week's `calendar/.../weekly/` folder. Commit and push that file (commit message: `hermes: generated weekly review questions (YYYY-MM-DD)`), then surface the top two or three questions in the message so Dan sees them before Monday's weekly review.

**Step 4 — Send one consolidated message**

Do not send three separate messages. Combine health summary + nudge (+ Sunday questions if applicable) into a single message. Lead with health score if it is meaningfully different from last time or flags something important; lead with the nudge if it is a routine evening. Keep it under ten lines.

---

## Notes

- **Scheduling is Hermes's to implement.** This file specifies what each message does. Wire the actual cron schedule or trigger inside Hermes's own scheduling system.
- **No queue files.** The old `.telegram/` bot wrote `YYYY-MM-DD-queue.md` files for later import. That architecture is gone. Hermes routes inputs directly (see `docs/hermes-capture.md`).
- **Repo path on Hermes's machine** — set this wherever Hermes clones the repo; the vault structure inside it is always relative to repo root.
