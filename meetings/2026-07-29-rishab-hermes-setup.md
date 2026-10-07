---
title: Growify — Rishab x Dan: Hermes Setup
type: meeting
date: 2026-07-29
attendees:
  - Daniel (DoAnythingNow)
  - Rishabh Mehra (Growify co-founder)
duration: ~45 mins
status: complete
source: Fathom recording 168187981
---

← [[entities/people/growify]] | [[calendar/2026/Q3/july-2026]]

# Growify — Rishab x Dan: Hermes Setup — 29 July 2026

## Summary

Catch-up call to finalize Hermes assistant setup and review the ontology visualization. The Growify Assistant is now live in a dedicated Discord server ("Glorify Assistant"), with voice-to-text interface for capturing ideas directly into company knowledge. Key decision: replace Gemini with a more reliable model (Sonnet 5 or Haiku) due to context-loss issues. Roadmap clarified into three phases: 1) context cleanup via live ontology map, 2) Airtable integration, 3) full app integration (Zoho) for a complete dynamic agent.

---

## Key Discussion

### Hermes Assistant Status — Now Live

The Hermes assistant is active in the "Glorify Assistant" Discord server. Design allows Rishab to voice-note ideas and receive structured, context-aware responses from the company knowledge base.

**Platform choice:** Discord chosen over WhatsApp for superior organization via channels and threads.

**Access:** Rishab created Discord account and shared User ID; Daniel granted access to the Growify server. Live test confirmed bot is active and responsive.

**Goal:** Enable voice-note capture + structured routing so Rishab can offload ideas into company knowledge without needing to manually structure them.

### Model Performance Issue Identified

Current setup uses Gemini for conversation + Sonnet 5 for heavy lifting, but **Gemini is forgetting context and instructions.**

**Example cited:** When asked about Daniel's work, Gemini gave a poor response, then "remembered" its context only after being prompted. This unreliability breaks the assistant's core value (knowing the business deeply).

**Decision:** Replace Gemini with a more robust model (Sonnet 5 or Haiku) to ensure consistent, accurate performance.

### Ontology Visualization for Context Cleanup

**Problem:** Initial context data in the folder is outdated — old clients, undefined service abbreviations (e.g., "BM," "EM"), stale team structures.

**Solution:** Daniel built a visual map of the company ontology (teams, clients, services) to make cleanup fast and discoverable.

**Implementation:** Daniel will host the map with edit/delete functions. When Rishab updates the map, changes sync back to the underlying "Vault" folder, which serves as the assistant's knowledge base. This closes the loop: assistant can see clean data, and Rishab gets a clear interface for maintaining it.

### Project Roadmap — Three Phases

**Phase 1: Context Cleanup** (now)
- Rishab uses the live ontology map to correct all outdated information
- Once clean, the assistant has accurate company knowledge

**Phase 2: Airtable Integration** (next)
- Assistant connects to Airtable to pull clean, up-to-date data
- Airtable becomes the primary source of truth (not manually-edited vault)

**Phase 3: Full App Integration** (later)
- Assistant connects to Zoho (or other apps) for real-time data access + write-back
- Complete dynamic agent: can both access and update real-time business data
- Eliminates the gap between what's recorded and what the assistant knows

---

## Action Items

| # | Action | Owner | Status |
|---|--------|-------|--------|
| 1 | Replace Gemini model in Hermes assistant with more reliable alternative (Sonnet 5 or Haiku) | Daniel | backlog |
| 2 | Host ontology visualization map with edit/delete functions; send live link to Rishab | Daniel | backlog |
| 3 | Begin using Hermes assistant in Discord to get familiar with its capabilities | Rishab | backlog |
| 4 | Clean up company context using the live ontology map once available | Rishab | backlog |

---

## Notes

This meeting clarified the distinction between the **assistant's knowledge layer** (vault + discord interface) and the **source of truth layer** (Airtable in Phase 2, Zoho in Phase 3). The roadmap avoids the common mistake of trying to do everything at once; cleanup first, then integrate live data sources.

The ontology visualization map is a critical unlock — it gives Rishab visibility + control, and gives the assistant reliable context to build on.

---

Related: [[2026-06-29-growify-session-2]] (Phase 1 wrap), [[entities/people/growify]], [[offers/growify-ai-assistant-proposal]]
