---
title: Growify — Session 1 (Rishab)
type: meeting
date: 2026-06-13
attendees:
  - Daniel (DoAnythingNow)
  - Rishab Mehra (Growify co-founder)
status: complete
---

← [[entities/people/growify]] | [[calendar/2026/Q2/june-2026]]

# Growify — Rishab Session 1 — 13 June 2026

## Summary

First ontology session with Rishab. He arrived already fluent in second-brain concepts — has watched videos on Claude + Obsidian setups and understands the token/context logic. The session surfaced a clear three-layer architecture for Growify's system: context folder (workflows, brand knowledge, team structure) → PostHog (all analytics data, AI-queryable) → Notion (client-facing portal). Rishab's most pressing internal problem is that rich financial and operational data currently lives in hand-crafted sheets and a Power BI pipeline — accurate but fragile, not scalable, and inaccessible to AI. The planned move to Zoho (People + CRM + Books) would make that data system-native and syncable. The conversation converged on one key insight: the value of the second brain compounds into a switching cost — clients who stay accumulate irreplaceable context history that a competitor can't replicate.

<!-- TODO(client-sync): push summary to Notion client portal when integration is built -->

---

## Key Discussion

### Rishab's existing data infrastructure

Growify already has a meaningful analytics layer: Shopify and ad platform data flows through a middleware into Power BI dashboards. Internal ops data lives in Google Sheets — salary sheets, brand-to-team allocation, profitability by team and brand manager, month-on-month churn. These are real-time (Sheets → Power BI syncs automatically). The problem is they're hand-crafted: employee changes, brand moves, prorated costs all require manual updates, and the system sits outside the reach of AI tools.

The planned fix: migrate to Zoho People + Zoho CRM + Zoho Books, so all people data, client data, and financials are held in a connected system rather than sheets. Once on Zoho, the data can sync into PostHog or equivalent dashboards. Rishab acknowledged this is underway but not complete.

### Three-layer architecture agreed

Daniel walked Rishab through the architecture he's proposing for the full system:

1. **Context folder (Obsidian)** — lightweight, local, workflow-first. Holds brand-level context (strategy, policies, communication, creative guidelines, reporting), team-level context (brand allocations, performance, incentives, payment collection), and company-level workflows. Used as an active AI partner during work sessions.
2. **PostHog** — the analytics and data layer. All brand performance data, ad spend, Shopify revenue, team profitability fed in here. AI-queryable. Custom dashboards per role/hierarchy. Replaces the hand-crafted Power BI setup. Devs needed but PostHog's built-in AI reduces that lift.
3. **Notion** — client-facing portal. External view only. Embeds relevant metrics and shows project state to clients. Syncs from the context folder via Python/Claude/Notion MCP hook.

Rishab confirmed this matches his mental model. The separation is important because bloating one layer with both context and data makes both harder to maintain.

### Brand and team context as the core IP

Rishab articulated what belongs in the context folder clearly: brand-level knowledge (strategy, what's worked, Shopify performance data, policies, creative guidelines), team-level knowledge (brand allocation per month, individual performance, incentives earned vs. potential, payment collection status, churn). This maps directly to what Daniel showed from his own system.

Key insight Rishab named: as brand knowledge accumulates in the system, switching costs compound. A client who leaves loses the institutional context Growify has built. That makes the context folder a retention mechanism, not just an ops tool.

### Company-wide knowledge as a consulting asset

Rishab flagged a second-order benefit: 60+ brands across a niche (Shopify/luxury e-commerce) generates pattern intelligence that individual brands don't have. If that's queryable — what's working, what's trending, what's failing — it becomes a consulting asset. Disha mentioned this separately too. Having all brand data in one queryable place is what makes that possible.

### Role-level dashboards

The discussion touched on PostHog producing custom dashboards per hierarchy level: team member, brand manager, team lead, founder. Rishab's current Power BI setup already shows team-level vs. brand-level vs. individual-level incentive breakdowns. The vision is to migrate that structure into PostHog with AI-queryability layered on.

---

## Action Items

| # | Action | Owner | Status |
|---|--------|-------|--------|
| 1 | Share PostHog link with Rishab | Daniel | done (shared in session) |
| 2 | Rishab to review PostHog — assess fit vs. current Power BI setup | Rishab | backlog |
| 3 | Map brand-level context requirements for Growify context folder | Daniel | backlog |
| 4 | Define team-level context fields (allocation, incentives, churn, payment collection) for folder structure | Daniel + Rishab | backlog |
| 5 | Confirm Zoho migration timeline with Rishab (People + CRM + Books) | Rishab | backlog |
