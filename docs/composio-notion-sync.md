---
title: Composio Notion Integration — Growify Client Portal Sync
date: 2026-08-18
status: draft
---

# Composio Notion Integration — Growify Client Portal Setup & Sync

**Purpose:** Automate syncing of meeting summaries, action items, and engagement state from the Context 2.0 vault to a Notion client portal so Growify (Rishab & Disha) can see what's been worked on and what's pending without needing access to GitHub.

**Status:** Notion integration is ready in Composio, but the client portal in Notion doesn't exist yet. This document covers the setup, tools, and workflow to build and maintain it.

---

## Prerequisites

- Composio CLI installed and authenticated
- Notion account with a workspace
- Composio Notion integration already connected (status: ACTIVE via `composio connections list --toolkit notion`)
- Access to the Growify meeting transcripts and summaries in the vault

---

## Current State

### In the Vault
- ✅ 7 meeting files (May 24 through July 29, 2026)
- ✅ Full entity snapshot with current state and open questions
- ✅ Phase 2 proposal drafted and ready

### In Notion
- ❌ Growify client portal does NOT exist yet
- ❌ No Notion page found via Composio search (database_id needed to proceed)

---

## Setup Steps (One-Time)

### Step 1: Create Growify Client Portal in Notion

1. **Manually in Notion (or via Composio NOTION_CREATE_DATABASE):**
   - Create a new Notion database called "Growify Client Portal"
   - Copy the database ID from the URL: `https://notion.so/{workspace_id}/{DATABASE_ID}?v=...`
   - Store the database ID for later use

2. **Database schema (suggested):**
   | Field | Type | Purpose |
   |-------|------|---------|
   | Title | Text | Session date + attendees (e.g., "2026-07-29: Rishab x Dan Hermes Setup") |
   | Date | Date | Meeting date |
   | Attendees | Multi-select | Names of participants |
   | Summary | Rich text | Key takeaways + decisions |
   | Action Items | Relation | Links to action database (if exists) |
   | Status | Select | Pending / Completed / In Progress |
   | Next Steps | Rich text | What comes next |

### Step 2: Create an Action Items Database (Optional but Recommended)

This database tracks open action items from all meetings:

| Field | Type | Purpose |
|-------|------|---------|
| Action | Text | What needs to be done |
| Owner | Select | Daniel / Rishab / Disha / Other |
| Due | Date | Target completion date |
| Status | Select | Backlog / In Progress / Done |
| Related Meeting | Relation | Link back to the meeting |

### Step 3: Document Database IDs

Once created, save the database IDs:

```bash
# In a safe location (e.g., ~/.hermes/.env or your vault's DEFERRED.md)
NOTION_GROWIFY_PORTAL_DB_ID="xxxxxxxxxxxxxxxxxxxxx"
NOTION_ACTION_ITEMS_DB_ID="yyyyyyyyyyyyyyyyyyyyyyy"
```

---

## Composio Notion Tools Reference

### Primary Tools for This Use Case

#### 1. **NOTION_SEARCH_NOTION_PAGE**
Search for existing pages by name.

```bash
composio execute "NOTION_SEARCH_NOTION_PAGE" -d '{"search_query":"Growify"}'
```

#### 2. **NOTION_UPSERT_ROW_DATABASE**
Create or update a row in a Notion database. Best for adding meeting records.

```bash
composio execute "NOTION_UPSERT_ROW_DATABASE" -d '{
  "database_id": "xxxxxxxxxxxxxxxxxxxxx",
  "row_data": {
    "Title": "2026-07-29: Rishab x Dan Hermes Setup",
    "Date": "2026-07-29",
    "Attendees": ["Daniel", "Rishabh"],
    "Summary": "Finalize Hermes assistant setup...",
    "Status": "Completed",
    "Next Steps": "Replace Gemini model, host ontology map"
  }
}'
```

#### 3. **NOTION_APPEND_TEXT_BLOCKS**
Add detailed content (like a full meeting summary) to an existing Notion page.

```bash
composio execute "NOTION_APPEND_TEXT_BLOCKS" -d '{
  "page_id": "xxxxxxxxxxxxxxxxxxxxx",
  "text_blocks": [
    "## Key Takeaways\n\n- Hermes assistant now live in Discord\n- Model upgrade needed: Gemini → Sonnet 5\n- Ontology visualization for cleanup in progress"
  ]
}'
```

#### 4. **NOTION_INSERT_ROW_DATABASE**
Insert a new row (alternative to UPSERT if you prefer).

```bash
composio execute "NOTION_INSERT_ROW_DATABASE" -d '{
  "database_id": "xxxxxxxxxxxxxxxxxxxxx",
  "row_data": {
    "Action": "Replace Gemini model with Sonnet 5",
    "Owner": "Daniel",
    "Status": "Backlog",
    "Related Meeting": "2026-07-29: Rishab x Dan Hermes Setup"
  }
}'
```

#### 5. **NOTION_QUERY_DATABASE_WITH_FILTER**
Retrieve rows from a database with filters (useful for checking what's already synced).

```bash
composio execute "NOTION_QUERY_DATABASE_WITH_FILTER" -d '{
  "database_id": "xxxxxxxxxxxxxxxxxxxxx",
  "filter": {
    "property": "Status",
    "select": {
      "equals": "Pending"
    }
  }
}'
```

---

## Sync Workflow

### Manual Sync (One-Off)

**Goal:** Sync all 7 existing meetings to Notion for the first time.

```bash
# For each meeting in meetings/ folder:
#   1. Read the meeting file
#   2. Extract: title, date, attendees, summary, action items
#   3. Call NOTION_UPSERT_ROW_DATABASE to add the row
#   4. Call NOTION_APPEND_TEXT_BLOCKS to add full summary if needed
#   5. For each action item, call NOTION_INSERT_ROW_DATABASE to action items DB

# Example for 2026-07-29 meeting:
composio execute "NOTION_UPSERT_ROW_DATABASE" -d '{
  "database_id": "GROWIFY_PORTAL_DB_ID",
  "row_data": {
    "Title": "2026-07-29: Rishab x Dan Hermes Setup",
    "Date": "2026-07-29",
    "Attendees": ["Daniel", "Rishabh"],
    "Summary": "Finalize Hermes assistant setup and review ontology visualization...",
    "Status": "Completed",
    "Next Steps": "Replace Gemini with Sonnet 5; host ontology map with edit functions; Rishab to clean up company context"
  }
}'
```

### Automated Sync (Ongoing)

**Pattern:** After every meeting or vault update, run a cron job that:

1. Pulls latest meetings from vault (via git)
2. Compares what's in Notion vs vault
3. Upserts new/updated meetings
4. Upserts action items from latest meetings

**Example cron job (pseudo-code):**

```python
# cron/growify_notion_sync.py (run weekly or after /wrap)

import json, subprocess
from datetime import datetime
from pathlib import Path

def sync_meetings_to_notion():
    """Pull all meeting files from vault and sync to Notion."""
    vault_path = Path("/home/hermes/context-2.0-github")
    meetings_path = vault_path / "meetings"
    
    # Find all Growify-related meetings
    growify_meetings = sorted(meetings_path.glob("*growify*.md"))
    
    for meeting_file in growify_meetings:
        # Parse meeting frontmatter + content
        # (extract title, date, attendees, summary, action items)
        
        # Upsert to Notion
        composio_cmd = [
            "composio", "execute", "NOTION_UPSERT_ROW_DATABASE",
            "-d", json.dumps({
                "database_id": os.getenv("NOTION_GROWIFY_PORTAL_DB_ID"),
                "row_data": {
                    "Title": parsed["title"],
                    "Date": parsed["date"],
                    "Attendees": parsed["attendees"],
                    "Summary": parsed["summary"],
                    "Status": "Completed",
                    "Next Steps": "\n".join(parsed["action_items"])
                }
            })
        ]
        subprocess.run(composio_cmd)

if __name__ == "__main__":
    sync_meetings_to_notion()
```

---

## Implementation Checklist

- [ ] **Create Notion database** for Growify Client Portal (with schema above)
- [ ] **Create Action Items database** (optional, but recommended)
- [ ] **Save database IDs** to a secure location (env var or vault DEFERRED.md)
- [ ] **Test Composio Notion integration** with a single meeting upsert
- [ ] **Sync all 7 existing meetings** to Notion manually
- [ ] **Create cron job** for ongoing sync (run after `/wrap` or weekly)
- [ ] **Share Notion portal link** with Rishab & Disha
- [ ] **Document** for future reference (Notion permissions, sync cadence, how to add manually if needed)

---

## Example: Syncing the Latest Meeting (2026-07-29)

This is the exact sequence to add the recently-discovered "Rishab x Dan Hermes Setup" meeting:

```bash
#!/bin/bash
export PATH="/home/hermes/.local/bin:$PATH"

# 1. Create the meeting row
composio execute "NOTION_UPSERT_ROW_DATABASE" -d '{
  "database_id": "YOUR_GROWIFY_PORTAL_DB_ID",
  "row_data": {
    "Title": "2026-07-29: Rishab x Dan Hermes Setup",
    "Date": "2026-07-29",
    "Attendees": ["Daniel", "Rishabh"],
    "Summary": "Finalize Hermes assistant setup and review ontology visualization. Hermes assistant now live in Discord. Model upgrade required (Gemini → Sonnet 5). Ontology visualization for cleanup in progress. Three-phase roadmap: 1) Context cleanup, 2) Airtable integration, 3) Full app integration (Zoho).",
    "Status": "Completed",
    "Next Steps": "Daniel: Replace Gemini with Sonnet 5; host ontology map. Rishab: Begin using assistant; clean up context."
  }
}'

# 2. Add action items from this meeting
composio execute "NOTION_INSERT_ROW_DATABASE" -d '{
  "database_id": "YOUR_ACTION_ITEMS_DB_ID",
  "row_data": {
    "Action": "Replace Gemini model with Sonnet 5 or Haiku",
    "Owner": "Daniel",
    "Status": "Backlog",
    "Related Meeting": "2026-07-29: Rishab x Dan Hermes Setup"
  }
}'

composio execute "NOTION_INSERT_ROW_DATABASE" -d '{
  "database_id": "YOUR_ACTION_ITEMS_DB_ID",
  "row_data": {
    "Action": "Host ontology visualization map with edit/delete functions",
    "Owner": "Daniel",
    "Status": "Backlog",
    "Related Meeting": "2026-07-29: Rishab x Dan Hermes Setup"
  }
}'

composio execute "NOTION_INSERT_ROW_DATABASE" -d '{
  "database_id": "YOUR_ACTION_ITEMS_DB_ID",
  "row_data": {
    "Action": "Clean up company context using ontology map",
    "Owner": "Rishabh",
    "Status": "Backlog",
    "Related Meeting": "2026-07-29: Rishab x Dan Hermes Setup"
  }
}'

echo "Sync complete!"
```

---

## Troubleshooting

### "NOTION_SEARCH_NOTION_PAGE returns 0 results"

This is expected if the database hasn't been created yet or Composio doesn't have visibility. **Solution:** Create the Notion database manually first, then use NOTION_FETCH_DATABASE with the explicit database ID.

### "Input validation failed — database_id is required"

You need to know the exact database ID. **Solution:**
1. Go to Notion workspace → open the database
2. Copy from URL: `https://notion.so/{workspace_id}/{DATABASE_ID}?v=...`
3. Pass it explicitly in the `-d` JSON

### "Permission denied when upserting"

Composio Notion integration may not have write access. **Solution:**
1. Run `composio link notion` to re-authenticate
2. Ensure the Notion integration has edit access to the database
3. Try again

### "Composio execute times out"

Long operations or network delays. **Solution:**
1. Increase timeout: `timeout 120 composio execute ...`
2. Break into smaller chunks (fewer rows at once)
3. Check Notion workspace status (not overloaded)

---

## Next Steps

1. **Today:** Create the Notion database structure (or ask Dan to do it)
2. **This week:** Manual sync of all 7 existing meetings
3. **Next week:** Set up cron job for ongoing sync
4. **Ongoing:** After each meeting, run the sync script or manually update Notion

---

## Related Documentation

- **Vault:** `/home/hermes/context-2.0-github/entities/people/growify.md` — Growify entity state
- **Meetings:** `/home/hermes/context-2.0-github/meetings/` — All meeting files (including new 2026-07-29)
- **Composio Notion tools:** `~/.composio/tool_definitions/NOTION_*.json`
- **DEFERRED.md:** Note about pending Notion sync setup

---

**Created:** 2026-08-18 (during Fathom integration)  
**Last updated:** 2026-08-18  
**Author:** Hermes Agent
