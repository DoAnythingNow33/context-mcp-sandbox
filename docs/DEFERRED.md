# Deferred Builds

The items below are built but need a one-time setup step from Dan to go fully live. Section 1 needs a Notion token + property mapping. Sections 2–4 document capabilities now delivered by Hermes' evening cron — the Python scripts are kept and callable on demand; the old LaunchAgent setup has been superseded.

---

## 1. Notion client-portal sync — `/client-sync`  ✓ BUILT

**Goal:** after a meeting or a snapshot update, push the relevant client state to a Notion client portal so clients see a live view of the engagement.

**Status:** two implementations are available (2026-08-18):
  - **Legacy:** `scripts/notion_sync.py` (Python-based, fully built, requires NOTION_TOKEN + DB ID setup)
  - **New:** Composio-based Notion integration (via `composio execute NOTION_*` tools; Composio already authenticated)

**Current state:** Composio Notion integration is ACTIVE and ready to use. See `docs/composio-notion-sync.md` for setup and usage examples. The legacy Python script is still available as a fallback.

**What's in place:**
- `scripts/notion_sync.py` — legacy full implementation (if Python route is preferred)
- `docs/composio-notion-sync.md` — **new** Composio approach with schema, tools reference, sync workflow, and examples
- Composio Notion toolkit already connected (status: ACTIVE)
- `/summary` (Agent 2 of `/meeting`) leaves `<!-- TODO(client-sync) -->` markers in meeting files — clear these after each successful sync.

**Setup for Dan (one-time, choose ONE approach):**

### Option A: Composio Approach (Recommended)

1. **Create Notion database** for Growify Client Portal (suggested schema in `docs/composio-notion-sync.md`)
2. **Get database ID** from Notion URL
3. **Test sync** using example commands in `docs/composio-notion-sync.md`
4. **Set up cron job** (optional) to sync weekly or after `/wrap`

### Option B: Legacy Python Approach

1. **Create a Notion internal integration** at https://www.notion.so/my-integrations → copy the `secret_...` token → add to shell profile or `.env`:
   ```
   export NOTION_TOKEN=secret_...
   ```
2. **Share the portal DB with the integration.** Open the Notion client portal database → Share → Invite → select the integration.
3. **Get the DB ID.** Open the portal DB as a full page → copy the URL. The 32-char hex segment after the last `/` and before `?` is the ID:
   ```
   export NOTION_PORTAL_DB_ID=<32-char-hex-id>
   ```
4. **Confirm `PROPERTY_MAP` in `scripts/notion_sync.py`.** Open the portal DB → ... → Properties. Ensure the right-hand strings in `PROPERTY_MAP` match the exact property names in Notion (case-sensitive). The Slug property is the stable match key — don't rename it in Notion once set.
5. **Install the library:**
   ```
   pip install -r scripts/requirements.txt
   ```
6. **Test:**
   ```
   python scripts/notion_sync.py --client growify
   ```
   Expected output: `CREATED  growify  https://notion.so/...` (first run) or `UPDATED  growify  ...` (subsequent runs).

**Decision recorded:** vault is source of truth; Notion is a projection of it, one-way (vault → Notion). Never read state back from Notion. Match on client slug — never duplicate.

---

## 2. Proactive evening DPL coach — DELIVERED VIA HERMES

**Goal:** at day's end the assistant prompts Dan with a coaching nudge built from today's `P-DD-MM-YY.md` checklist, skipping if the DPL is already closed.

**How it's delivered now:** Hermes' evening cron handles this. Hermes reads the active `P-` plan, checks whether today's DPL is closed, and sends the coaching message. No local script or LaunchAgent needed.

**Setup:** see `docs/hermes-setup.md` for the cron spec.

**Decision recorded:** capability proved the habit; delivery migrated to Hermes (2026-06-26).

---

## 3. Proactive Sunday weekly-review questions — DELIVERED VIA HERMES

**Goal:** every Sunday, inspect the week just ended and write a targeted questionnaire of gaps that `/weekly-review` can't reconstruct from sparse DPLs alone. Monday, `/weekly-review` Step 0.5 reads it, walks Dan through the gaps, then archives it.

**What's in place:**
- `scripts/generate_review_questions.py` — Python gathers the week's data deterministically (7 daily logs + which are missing, the week's `P-` plan, `actions/done|doing|backlog`, `_digest.md`) and `claude -p` phrases the questions. Deterministic fallback if Claude call fails. Output → `calendar/<year>/<Q>/weekly/_review-questions.md`.
- `/weekly-review` Step 0.5 — unchanged; detects the file and runs Dan through it.

**How it runs now:** Hermes' Sunday evening cron calls `scripts/generate_review_questions.py` and commits the output to the repo. See `docs/hermes-setup.md` for the cron spec.

**To run on demand:**
```bash
python3 "/Users/DoAnythingNow./Desktop/Context 2.0/scripts/generate_review_questions.py"
```

**Decision recorded:** capability migrated from local LaunchAgent to Hermes evening cron (2026-06-26). Vault syncs via GitHub; Hermes pushes over SSH so output is available on Dan's machine. Reminders are retired; `actions/` is the evidence source.

---

## 4. Nightly system-health eval + `/maintain` — DELIVERED VIA HERMES

**Goal:** a deterministic eval runs nightly for free; the weekly full-auto `/maintain` skill heals what it finds and logs every change.

**What's in place:**
- `scripts/system_health.py` — pure-stdlib eval engine. Scans **decay**, **accountability**, **coherence** → writes `_health.md` (score /100 + trend vs previous run). History in `scripts/.health-history.json` (last 30 runs). Zero tokens. Exit 0 if score ≥ 80, else 1.
- `/maintain` skill (`.claude/commands/maintain.md`) — unchanged. Reads `_health.md` + flagged files; auto-fixes mechanical drift; acts-with-judgment on the rest; logs everything to `calendar/[year]/[quarter]/_maintenance-log.md`. Ambiguous items become questions in `_maintenance-interview.md`. Runs inside `/weekly-review` or standalone.

**How it runs now:** Hermes' nightly evening cron calls `scripts/system_health.py` and commits `_health.md` to the repo. See `docs/hermes-setup.md` for the cron spec.

**To run on demand:**
```bash
python3 "/Users/DoAnythingNow./Desktop/Context 2.0/scripts/system_health.py"
```

**First-run baseline:** score **36/100** (6 quiet entities, 7 rotting actions, 9 DPL gaps/14d, 21 unfiled next_actions, 2 index drifts). Trend climbs as `/maintain` runs.

**Decision recorded:** detection is deterministic and free; only interpretation costs tokens. `/maintain` reads the 60-line report instead of the whole vault. Full-auto with a changelog — the log is Dan's review surface. Delivery migrated from local LaunchAgent to Hermes evening cron (2026-06-26).
