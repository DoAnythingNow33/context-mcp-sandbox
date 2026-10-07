---
title: Session Handoff — architecture migration
updated: 2026-09-03
---

# Session Handoff

Rolling handoff for the three-layer migration Dan is running: **vault = context
and routing**, **Notion = database and shareable layer**, **Composio = tool layer
so Hermes can actually act**. Read this before picking the work back up.

Written 2026-09-03, covering sessions from 2026-08-19.

---

## The architecture, and the rule that changed

Source of truth is split **by object type**, not by tool:

| Object | Lives in | Why |
|---|---|---|
| `self/`, `IP/` bodies, `calendar/`, meeting transcripts | **Vault** | Narrative, private, git-versioned, feeds prompts |
| Actions, Clients, Prospects, Projects | **Notion** | Relational, status-bearing, shareable, needs views |

This **supersedes** the old rule still quoted in places: *"vault is source of truth;
Notion is a projection of it, one-way. Never read state back from Notion."* That was
already false in practice — the Prospects CRM moved to Notion in August and
`/prospect` writes into it. Actions followed on 2026-09-02. If you hit that
sentence in an old doc, it's stale; fix it rather than following it.

---

## Done

### Scoring retired (2026-08-25)
The `/100` health score, trend arrows, `.health-history.json`, the pass/fail exit
code and the score-driven Discord embed colour are all gone. **Never reintroduce
them.** Dan's reason: the biggest penalty was the daily-log gap, so the number
mostly measured how diligently he fed the vault, not how useful the vault was to
him — a quiet family fortnight rendered as 11/100 and a red card every night.

Retired with it: the **DPL-gap** and **commit→done ratio** checks. Do not re-add
habit metrics of any kind. `_health.md` is now "Worth a look" with two plain
sections and no grade.

### Scheduled layer informs, never interrogates (2026-08-25)
Dan takes responsibility for sending voice notes to Discord. Nothing scheduled
asks him questions.

| When | Workflow | What |
|---|---|---|
| Daily 07:11 UTC | `morning-debrief.yml` | `claude -p` over goals/digest/health → one line on what matters, three concrete moves, one thing needing attention. Invites a voice note. |
| Sun 16:00 UTC | `self-heal.yml` | Headless `/maintain` + interview file to Discord |
| Sun 18:00 UTC | `weekly-synthesis.yml` | Headless read-only `/synthesis` (Step 4 skipped) |
| — | ~~`evening-debrief.yml`~~ | **Retired.** Recoverable via git. |

### Two CI bugs fixed (2026-08-25)
Both failed silently for weeks — the vault work committed fine, only the
notification died, so nothing surfaced the failure.

- **Evening debrief**: the "Tomorrow" fallback pulled 1822 chars from `goals.md`
  against Discord's 1024-char embed field limit → 400 → `curl -sf` exit 22. Fields
  are now capped and the HTTP code is reported instead of swallowed.
- **Self-heal**: `payload_json` was passed inline to `curl -F`, and curl treats `;`
  in an `-F` value as a parameter separator. The message "Hermes files them; next
  Sunday applies them." truncated to `{"content":"files them` — unterminated JSON.
  Now built with `jq` into a file and passed as `-F name=<file`. **This is why
  eight consecutive maintenance interviews went unanswered** — they never reached
  him.

### Action dating fixed (2026-08-25)
`action_source_date()` fell back to file mtime, but `actions/checkout` writes a
fresh clone so every mtime was checkout time. 43 of 67 backlog actions had no date
of their own and read as 0 days old on **every** scheduled run. Now dated by first
git commit; workflows set `fetch-depth: 0`, which they still need.

### Maintenance interview cleared (2026-08-25)
First since 2026-07-26. 13 actions closed, 1 filed, 1 thread parked.
**`dormant: true`** is a new mechanism on entity snapshots — `system_health.py`
skips dormant entities so a deliberately parked thread stops reading as decay.
Ontology for Creatives is the first; unset to bring it back.

### Actions → Notion (2026-09-02)
54 live actions migrated into the existing **Tasks Tracker**. See
`actions/README.md` for the field mapping. `actions/done/` + `cancelled/` are a
**frozen archive** — the maintenance logs reference them by path. Never write there.

---

## Notion IDs

| Thing | ID / URL |
|---|---|
| Workspace | `b38a00a4-d201-488e-a3d0-8823ee467195` (DoAnythingNow.) |
| **Tasks Tracker** data source | `1e64c614-f809-80b6-944a-000b9e6dfad4` |
| Tasks Tracker database | `1e64c614-f809-8009-b9e7-f06fa12afd8c` |
| Clients data source | `2224c614-f809-80bd-b4e7-000b8ee69a46` |
| Projects data source | `2224c614-f809-806b-93ac-000b5a2d91e7` |
| Prospects data source | `afb84c58-1563-4002-869c-7ee44bf44d97` |
| Home page | `a294c614-f809-821d-8ee1-0124bfdad85e` |

**Tasks Tracker gotchas:**
- The Clients relation property is named `"Clients "` — **with a trailing space**.
- `Do On` accepts **ISO dates only**. "ASAP"/"This week" go in the page body.
- `Assignee` is a person field needing real workspace users; the clients aren't.
  Use the `Owner` select instead.
- `Vault Slug` is the stable match key for idempotent re-runs. Don't rename it.
- 146 legacy rows (2025-era, incl. personal medical) sit in Done/Cancelled. The
  **Active**, **Board** and **By client** views filter them out. Nothing was archived.

---

## Outstanding

### 1. Notion token for CI — blocks the morning brief seeing tasks
CI has no `NOTION_TOKEN`, so the morning brief runs blind on the actual task list.
Its prompt currently says so and forbids inventing task names. Setup steps are in
the section below; once the secret exists, wire the Notion MCP into
`morning-debrief.yml` and let the brief read the **Active** view.

### 2. Morning brief arrives 5–12 hours late
GitHub's scheduler is best-effort and 07:11 UTC is peak contention. Measured:
+5.3h, +7.8h, +5.6h, +5.9h, **+12.2h**, +11.1h. A "morning" brief landing at 19:23
is worse than none.

Fix: move it to Hermes. The box has a real scheduler at `~/.hermes/cron/jobs.json`
(currently 2 jobs, both vault auto-pull, firing reliably), Claude Code CLI at
`/usr/local/bin/claude`, and the repo at `~/context-2.0-github`. Note the historical
caveat in `docs/hermes-setup.md`: scheduling moved *off* Hermes to Actions in July
because "Hermes crons proved awkward" — but that predates the current cron system,
which works.

### 3. Notion Projects DB is stale
Lists 2025 work; none of Mycelium, Sleevenote, Content Strategy or Token Sniper
exist. **14 migrated actions have no project relation** because of this. Dan chose
"create people only, park the projects" — reconciling Projects is its own job.

### 4. Phase 3 — delete dead weight (~24MB)
`ops/notion-index/` (3.4M, one-time triage artifact, archiving never started),
`visual/` (12M) and `Excalidraw/` (8.3M) belong in their own repo, `hermes/hermes/`
is an empty nested Obsidian vault.

### 5. Phase 4 — IP layer duplication
50 vault `IP/*.md` files vs. Notion's **Tools, Concepts & Techniques** DB
(`feac1e47-7e3c-45ba-a6ef-c2575a03eede`), no sync, incompatible schemas (vault:
`type`/`tags`/`content_made`; Notion: `Category`/`Module / Pillar`/`Content`).
Proposed: bodies stay in the vault, Notion becomes the index with content status.

### 6. Composio can't see the Growify portal
`docs/composio-notion-sync.md` claims the Growify Client Portal doesn't exist in
Notion. **It does** — Composio's connection just hasn't been granted access to
those pages. Fix before building on it or syncs will create duplicates instead of
updating. That doc also predates the Tasks Tracker decision and proposes building
separate per-client databases — treat its *tool reference* as useful and its
*plan* as superseded.

### 7. Two things Dan raised that aren't captured anywhere
- **Reality Architects × work merge.** He said he's "pulling together both the
  reality architect coach and the work stuff" and needs to figure out how that
  works. Not in `self/goals.md` active threads. It arguably determines whether
  Ontology for Creatives stays dormant. Worth its own session.
- **Token Sniper secrets.** `entities/projects/token-sniper.md` carries
  "Rotate DISCORD_BOT_TOKEN and HELIUS_API_KEY — still outstanding" as a
  next_action. Live credentials, still unrotated.

---

## Working notes

- **Hermes models**: conversational `claude-haiku-4.5` (deliberate, stretches
  credits), delegation `claude-sonnet-5`. Three docs wrongly claimed both slots ran
  Sonnet; corrected 2026-08-25. Live config wins — `~/.hermes/config.yaml`.
- **There is one proactive system, not three.** GitHub Actions sends everything.
  Hermes has no debrief/health skills — it's interactive capture only. GitHub's
  failure emails were the confusing third signal.
- **Vault writes are background work.** Dan's standing preference: dispatch as
  background agents, surface a short outcome line, don't narrate file edits.
- **Sandbox**: writes under `.claude/` need `dangerouslyDisableSandbox: true`.
  Use `$TMPDIR`, never `/tmp`.
- **Git**: local, Hermes and CI all push. Always `git fetch` and inspect before
  pulling; divergence is normal, not a problem.
