---
description: "Client-portal sync — pushes client entity state to the Notion client portal after meetings or snapshot updates."
---

# /client-sync — Notion Client Portal Sync

One-way projection: vault → Notion. Idempotent upsert keyed on client slug. Vault is always source of truth — never read state back from Notion.

## Prerequisites (one-time setup)

1. `NOTION_TOKEN` must be set in the shell environment (Notion internal integration token).
2. `NOTION_PORTAL_DB_ID` must be set (the 32-char hex ID of the client portal DB).
3. `PROPERTY_MAP` in `scripts/notion_sync.py` must be confirmed against the portal DB's actual property names.
4. `pip install -r scripts/requirements.txt` (installs `notion-client`).

If either env var is missing the script exits 1 with a clear message telling Dan exactly what to set.

## Live flow

1. Identify the target client slug — matches `entities/people/<slug>.md`. If the user says a name, derive the slug (e.g. "Growify" → `growify`).
2. Run: `python scripts/notion_sync.py --client <slug>`
3. Report the result line the script prints (CREATED / UPDATED + page URL).
4. Open the relevant meeting file in `meetings/` and remove the `<!-- TODO(client-sync): ... -->` marker(s) now that the sync is confirmed.

For a full sweep: `python scripts/notion_sync.py --all` — loops every `entities/people/*.md` with `type: snapshot`, skips malformed files, prints one result line per client.

## Rules

- Vault is source of truth. Sync is one-way. Match on slug — never duplicate.
- Never commit `NOTION_TOKEN` (it is excluded by `.gitignore` patterns — keep it in `.env` or shell profile).
- One client failing during `--all` does not abort the run; it prints ERROR and continues.
