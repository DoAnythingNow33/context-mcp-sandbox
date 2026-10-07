# Context 2.0 — DoAnythingNow Operating System

Personal operating system for Dan Tejada Salazar. Tracks business, clients, family, and self across a structured folder hierarchy. Designed to be loaded into Claude Code sessions — and worked by Hermes, Dan's always-on assistant — for intelligent, context-aware assistance.

---

## Folder Structure

```
Context 2.0/
├── self/                        # Identity layer — built/maintained via /internal-os
│   ├── identity.md              # Current self — MBTI + interests merged in
│   ├── goals.md                 # Active threads — loaded every session
│   ├── arc.md                   # Character arc progress
│   ├── beliefs.md               # Personal convictions
│   ├── writing-dna.md           # Voice + style guide for all content
│   └── context.md               # Workspace routing for self work
│
├── entities/                    # Everyone + everything Dan is responsible for
│   ├── people/                  # Clients + family, one file each
│   ├── projects/                # DoAnythingNow business state
│   │   ├── snapshot.md          # DAN business state
│   │   ├── content-strategy.md  # Posting schedule, platform map, SOP
│   │   └── offers/              # Offer line detail files (type: profile)
│   └── context.md
│
├── calendar/                    # Time structure
│   └── [year]/[quarter]/
│       ├── daily/               # YYYY-MM-DD.md — DPL logs
│       ├── weekly/              # R-DD-MM-YY.md (review) + P-DD-MM-YY.md (plan)
│       ├── [month]-[year].md    # Monthly review
│       └── review.md            # Quarterly review
│
├── IP/                          # Knowledge library — every concept, technique, framework
│   ├── _index.md                # IP database index
│   ├── _template.md             # Entry template
│   └── <slug>.md                # One file per concept / framework / technique
│
├── meetings/                    # Single source of truth for client + external meetings
│   │                            # YYYY-MM-DD-[entity]-[descriptor].md
│   └── archived/                # Old workflow artifacts (pre-Hermes)
│
├── actions/                     # Frozen archive — live actions are in Notion
│   ├── backlog/ doing/ done/
│   └── _template.md
│
├── ops/                         # Operational workflows, one subfolder each
│   ├── content/                 # Output layer — linkedin/ + x/, each Posted/ + Deferred/
│   ├── sales/                   # Prospecting workflow docs — the CRM itself lives in Notion
│   │   └── archive/             # Retired vault-based CRM (pre-2026-08-14), reference only
│   ├── notion-index/            # Temporary triage index of the Notion workspace (2,779 pages,
│   │                            #   ahead of a migration decision) — delete once triage is done
│   └── context.md
│
├── visual/                      # Micro-app layer — dashboard + client pitch decks (see visual/README.md)
│
├── hermes/                      # Hermes agent-harness infrastructure docs (SSH, multi-tenant SOP,
│                                 #   troubleshooting) — not vault content, this is the agent's own docs
│
├── scripts/                     # Deterministic Python utilities
│   ├── validate_naming.py       # Naming convention enforcer
│   ├── validate_links.py        # Cross-link checker (meetings ↔ entities ↔ months)
│   ├── validate_freshness.py    # Drift detector — stale snapshots, stale _digest.md, index dates out of sync
│   ├── extract_carry_forwards.py # Extracts week's DPL data into one file — cuts review tokens ~80%
│   ├── generate_digest.py       # Regenerates _digest.md — compressed entity states
│   ├── generate_review_questions.py # Sunday: writes _review-questions.md for /weekly-review
│   ├── system_health.py         # Nightly deterministic scan → _health.md (findings, no score)
│   └── scaffold_quarter.py      # New quarter folder scaffolder
│
├── docs/                        # Reference docs
│   ├── ICM.md                   # Methodology explainer (Jake Clief)
│   ├── DEFERRED.md              # Built-but-needs-setup items (Notion sync credentials)
│   ├── hermes-capture.md        # How Hermes routes ad-hoc inputs into the vault
│   └── hermes-setup.md          # What each Hermes scheduled message does (superseded by GitHub Actions
│                                 #   for scheduling — see below — but still the reference for message content)
│
├── .github/workflows/           # Scheduled messages — morning-debrief.yml, evening-debrief.yml, self-heal.yml
│
├── .claude/commands/            # Claude Code skills (slash commands) — see table below
│
├── _digest.md                   # Auto-generated: compressed entity states (1 read vs N)
├── _health.md                   # Auto-generated nightly: what's worth a look (no score)
├── index.md                     # Navigation map + availability (consulted on demand)
├── CLAUDE.md                    # Full system instructions for Claude — the source of truth
└── README.md                    # This file
```

---

## Session Quickstart

Every session, Claude loads `self/goals.md` and `_digest.md` (if it exists). `index.md` is consulted on demand as a navigation reference. Then:

| What you're doing | Run |
|---|---|
| Capturing work in progress | `/dpl` |
| Ending any session | `/wrap` |
| Sunday planning | `/weekly-review` |
| After a meeting | `/meeting` |
| End of month | `/month-close` |
| Self work / accountability | `/internal-os` |
| Step back / connect the dots across self + clients + calendar | `/synthesis` |
| Generating content (LinkedIn + X) | `/written-content` |
| Weekly outbound prospecting | `/prospect` |
| Client-portal sync (Notion) | `/client-sync` |
| Full-auto vault maintenance | `/maintain` |
| Check file naming | `python scripts/validate_naming.py` |
| Check cross-links | `python scripts/validate_links.py` |
| Check for drift (stale snapshots / digest / index) | `python scripts/validate_freshness.py` |
| Pre-process week for review | `python scripts/extract_carry_forwards.py --days 7` |
| Starting a new quarter | `python scripts/scaffold_quarter.py [year] [Q]` |

Full skill list (17 slash commands) and script table: `CLAUDE.md`.

---

## Naming Conventions

Enforced by `scripts/validate_naming.py`. Runs automatically inside `/weekly-review`.

| File type | Format | Example |
|---|---|---|
| Daily log | `YYYY-MM-DD.md` | `2026-05-10.md` |
| Weekly review | `R-DD-MM-YY.md` | `R-04-05-26.md` |
| Weekly plan | `P-DD-MM-YY.md` | `P-11-05-26.md` |
| Meeting | `YYYY-MM-DD-[entity]-[descriptor].md` | `2026-04-26-growify-call-2.md` |
| Monthly | `[month]-[year].md` | `may-2026.md` |

---

## System Design Principles

**Deterministic layer** (Python scripts): naming validation, link checking, folder scaffolding, data extraction, the nightly attention scan. Run the same way every time. No model, no judgment.

**Probabilistic layer** (Claude skills): synthesis, writing, routing, judgment calls. Draw on loaded context and writing DNA to produce output that requires intelligence.

The boundary is intentional. Scripts handle structure; Claude handles meaning.

---

## Architecture: ICM (Intelligent Context Management)

This system follows the three-layer ICM pattern (Jake Clief):

**Layer 1 — The Map (`CLAUDE.md`)**
Loaded every session. Contains the routing table — for this task → read these workspace files, skip those, use these skills. Controls what gets into context so tokens aren't wasted on irrelevant material.

**Layer 2 — The Rooms (workspace `context.md` files)**
Each workspace has a `context.md` loaded only when working there. It describes what the workspace is for, the process, which skills apply, and local naming conventions.

| Workspace | Context file | Purpose |
|---|---|---|
| `self/` | `self/context.md` | Identity, arc, voice |
| `entities/` | `entities/context.md` | Stakeholder snapshots |
| `IP/` | `IP/context.md` | Knowledge library |
| `ops/content/` | `ops/content/context.md` | Output and distribution |
| `ops/sales/` | `ops/sales/context.md` | Prospecting workflow (CRM lives in Notion) |
| `calendar/` | `calendar/context.md` | Time layer — daily, weekly, monthly |

**Layer 3 — The Tools (skills)**
Skills are scoped to the workspace where they're needed, not loaded globally. The routing table in `CLAUDE.md` specifies which skills apply per task type.

**Layer 4 — Deterministic scripts**
An addition to base ICM: Python utilities that enforce naming conventions, validate cross-links, scaffold folders, and pre-process data. Scripts handle structure without model judgment — they run the same way every time and fail loudly when conventions are broken.

### How to extend
- New workspace → create the folder, add a `context.md`, add a row to the routing table in `CLAUDE.md`
- New skill → wire it into the relevant workspace `context.md`, add it to the routing table
- New naming pattern → add to `validate_naming.py` and document in the relevant workspace `context.md`

---

## Hermes + GitHub Actions

Hermes is Dan's always-on assistant (SSH access to this repo) — it handles ad-hoc capture during the day (routing rules: `docs/hermes-capture.md`). Scheduled proactive messages (morning brief, Sunday self-heal, Sunday synthesis) run as GitHub Actions in `.github/workflows/`, sent via Discord webhook — not Hermes-side crons. They inform, never interrogate: Dan sends voice notes when he has something to add. Full detail in `CLAUDE.md`'s Hermes section.

---

## Weekly Rhythm

```
Mon–Fri  /dpl                             → capture daily progress
After meetings  /meeting                  → transcript → structured file
Sunday   (automatic via self-heal.yml)    → /maintain runs headless + generates review questions
Sunday   /weekly-review                   → synthesise week + plan ahead
Sunday   /written-content                 → turn week into 4 LinkedIn posts + 7 tweets
Anytime  /wrap                            → close session, persist context, refresh _digest.md, offer git commit
Monthly  /month-close                     → synthesise month
Quarter  python scripts/scaffold_quarter.py [year] [Q]   → set up new folder structure
```
