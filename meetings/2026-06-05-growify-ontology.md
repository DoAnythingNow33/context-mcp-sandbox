---
title: Growify — Meeting Summary & Ontology Map
type: meeting
date: 2026-06-05
attendees:
  - Disha Bhatnagar (Founder, Growify)
  - Daniel (AI/automation consultant)
duration: ~50 mins
entity: growify
---

← [[entities/people/growify]]

# Growify — Meeting Summary & Ontology Map
**Date:** 5 June 2026 · **Participants:** Disha Bhatnagar (Founder, Growify), Daniel (AI/automation consultant) · **Duration:** ~50 mins
**Format note:** This was a "brain dump" session. Disha narrated context while Daniel guided. Below is everything extracted, organised into ontology building blocks: *Actors → Clients → Teams → Systems/Tools → Strategic Vision → Processes → Problems → Proposed Architecture → Actions.*

---

## 1. Company Overview & Context

- **Growify** is a digital-services / growth agency for fashion designer brands (primarily India-based, made-to-order luxury/couture fashion).
- **Industry characteristic:** "Made-to-order" industry built on hand embroidery and craft. Hand embroiderers cannot be replaced by AI; many processes still run on pen and paper. Disha estimates meaningful tech replacement is **5–6 years away**.
- **Scale:** ~**60 clients** total. At the time of the meeting, ~**40 clients** had gone on sale within two days (end-of-season sale period — extremely hectic, staff working through the night).
- **Revenue model:** Incentive-based — Growify earns a cut of the client's revenue. (Example: client Mahima Mahajan generates ~**₹2 crore/month**; Growify earns incentive on that figure.) This means delivery problems (e.g., undelivered garments) are a direct loss to Growify too.
- **Client relationship basis:** Clients collaborate with Growify almost entirely via **targets** (e.g., ₹2L, ₹3L, ₹4L monthly). Targets are the central performance unit.

---

## 2. Actors / People (Roles)

| Person | Role | Notes |
|---|---|---|
| **Disha Bhatnagar** | Founder | 7 years of accumulated knowledge. Holds most strategic/contextual knowledge in her head → single point of dependency. Directly manages relationships with founder/legacy clients. |
| **Rishabh** | Co-founder / Business Development | Does most **closure (sales) calls**. Owns the analytics dashboard tool. Makes ad-account card decisions. Frequently unavailable. Was absent from this meeting. A recurring source of process gaps (see §8). |
| **Chandrika / Chandika / "Shandika"** *(same person — transcription variants)* | Day-to-day brand management | Knows exact folder locations and current data structures. Previously built an Excel organisation sheet at Rishabh's request. Best person to define the "context folder" architecture. |
| **Rohit** | Operations Head ("Op") | Built the lookup-based weekly performance/"brands in red" tool. Aligned with Disha on automation over manual reporting. |
| **Daniel** | External AI/automation consultant | Guiding the AI adoption. Will prototype workflows and research tooling. |
| **Abhishek Sharma** | Example employee | Cited as someone managing ~5 brands (used to illustrate the reporting concept). |
| **Marketing team** | Internal function | Currently has its own separate AI account producing inconsistent/wrong copy. |

**Generic internal roles referenced:**
- **POC (Point of Contact)** — Growify's assigned contact for a brand (when the founder isn't working directly with Disha).
- **Brand Manager** — works directly on a brand; first line for spotting escalation triggers.
- **Team Lead** — one per team; first escalation tier.
- **CSM Team (Client Service Management)** — strategy/retention team; later escalation tier.

---

## 3. Clients / Brands (Entities)

- **Mahima Mahajan** *(appears variously as "Maimam Hach", "my mom Marjan", "Mahima Majan")* — generates ~₹2cr/month. Has an **inventory data problem** (doesn't know what sells in which season, peak/slow months, RTS vs made-to-order split). Contact person: **Vikram**, who calls Disha directly for ad-hoc issues (e.g., DHL misplacing a garment → chargeback). A flagship example for both the external inventory-tool opportunity and the ad-hoc query problem.
- **Aisha Rao** — referenced in the image-resizing example.
- **"Amarimah Mahatandrasya"** *(transcription garbled)* — a legacy brand Disha started the company with (6–7 year relationship).
- Brands are internally categorised by tier: **Top / High / Medium / Low**. Monthly calls (with Disha present) happen only for **Top** brands.

---

## 4. Team Structure

- **4 teams.**
- Each team manages **~17–18 brands (max 20)**.
- Each team has **~10 people**: a mix of designers, maintenance people, ad people, and **one team lead**.
- **Website team** is a separate, dedicated function — the *only* group permitted to upload to client websites.
- **Imagery sizing team** is a separate, dedicated function for resizing/touch-ups.

---

## 5. Systems & Tools (Current State)

| Tool/System | Purpose | Status / Problem |
|---|---|---|
| **Analytics dashboard** (built by Rishabh's developers) | Pulls data from **Meta, Google, Shopify** via **Funnel**; displays real-time. | Costs **~₹5 lakh/quarter** to maintain. Clients can't understand it. |
| **Rohit's lookup tool** | Flags any brand "**red**" when it hasn't hit 25% of target. | Built but politically contested (Rishabh wants manual reporting instead). |
| **Google Drive** | Stores some brand files. | Fragmented — files scattered. |
| **Floating GPTs / personal ChatGPT accounts** | Ad-hoc per person (Rishabh, Disha, Chandrika, Marketing each have their own). | No shared account → inconsistent data, wrong copy, can't train. |
| **WeTransfer** | How clients (via photographers) deliver raw image content. | Manual download/re-upload step. |
| **Photoshop / Adobe** | Designers' creative tool. | Daniel will keep this and explore **Adobe Firefly** rather than forcing Canva/Figma. |
| **Funnel** | Data-connection layer feeding the dashboard. | — |
| **Shopify** | Client e-commerce platform (within Growify's umbrella of responsibility). | — |

**Disha's own benchmark example (Daniel's setup):** Daniel demonstrated a "Context 2.0" folder system and a Claude **"skill"/workflow** ("written content" / "LinkedIn engine") that reads his weekly review, generates 8 post ideas in his tone of voice, and drafts full posts — cutting 1–2 hours to minutes. This is the model for the workflows Growify wants.

---

## 6. Strategic AI Vision (Disha's framing)

Disha splits AI into two domains:

### A. Internal AI (make the business run leaner)
Goal: simplify Disha's life, pull data faster from teams, feed that data into learning, ads, and client communication. Reduce dependency on Disha as the sole knowledge-holder.

### B. External AI (productised services for clients)
Goal: position **Growify as a hub** that provides digital services / tools to client businesses.
- **Core insight (the data-hub thesis):** Growify sits in the middle of ~60 brands. Each client only has *their own* data; Growify has *everyone's*. Aggregated cross-client/industry data can advise each individual client — e.g., "this is happening across the industry; you're lacking here; add these 10 fast-moving products to ready-to-ship inventory."
- **Example product — Inventory Tool:** Solve the Mahima Mahajan-type problem — real-time visibility into what sells by season, peak vs slow months, RTS vs made-to-order. Even 25–30-year legacy brands lack this data.
- Disha feels website/tool building alone is "playing small" — the bigger play is data-driven advisory tooling.

---

## 7. Processes (Core Ontology — the business "verbs")

Daniel asked Disha to enumerate every process. The full list of process "headers":

1. **Creative process** (image/sale-asset production)
2. **Reporting process**
3. **Client onboarding process**
4. **Client escalation process**
5. **Client exit process**
6. **Employee onboarding process**
7. **Employee exit process**
8. **Internal / interdepartmental workflows** (the "ideal workflow between departments")

> Disha noted internal workflows are "doing fine" — manageable even if not optimal. The friction is concentrated at **department-to-department handoffs** and in **client-facing** processes. Client exit, employee onboarding, and employee exit were named but **not detailed** in this session.

### 7.1 Creative Process — Image Resizing
- Designers supply **raw edited content**: files **>500MB**, with **inconsistent dimensions**.
- Every brand needs **uniform** head-spacing and left/right spacing so products look consistent on the site.
- **Current flow:**
  1. Client sends **WeTransfer** (or Google Drive) link — usually WeTransfer, since that's how they get it from the photographer.
  2. Growify team **downloads** WeTransfer → **re-uploads to Google Drive** → shares link back to client ("this is the main content").
  3. Link goes to **imagery sizing team** → they edit/resize each image one by one.
  4. Re-upload final versions to Google Drive.
  5. **Website team** downloads → uploads to the website.
  6. Client notified that upload is done.
- Each product = **5 images**; resizer must sit on every product manually.
- **Pain:** ~**5 days** end-to-end; ties up ~**3 resources**.
- **Desired tool:** auto-resize to the company's **3 standard sizes** + reduce file size **without quality loss**.
- Daniel has done an analogous thing for video (auto-detecting "viral moments" and clipping into a folder) → believes this is straightforward.

### 7.2 Creative Process — Sale/Ad Image Design
- **90% of creatives** follow one template: **image + logo + text** (sale text, or just logo + collection name).
- Brand book (fonts, etc.) is **already decided**; only **placement** changes.
- **Pain:** Designers over-experiment with fonts/placement and pixel-perfect tweaking. This is the **biggest bottleneck** — exacerbated by designers being on leave / slow / unwilling.
- **Timing:** ~20 min to create a template, then more per asset. One "task" = **5 images = 1 carousel ad** = **~1hr–1hr15min**.
- **Demand vs capacity:** Daily requirement ≈ **20 campaigns**; team delivers only **9–10/day** → permanent **backlog**.
- **Desired tool:** upload picture → specify brand (e.g., "Mahima Mahajan logo") → preset font/brand book → quick top/bottom/below placement → publish. Built in Photoshop/Adobe (likely **Firefly**) to avoid switching tools.

### 7.3 Reporting Process
- Flagged (alongside design & website teams) as the **biggest problem**.
- Real-time dashboard exists (Meta/Google/Shopify via Funnel) but **clients can't interpret it**. Their problem is **not numbers — it's insights**: they only want "what worked, what didn't, what we're fixing, did it get fixed."
- Despite the automated dashboard, teams still build **manual weekly reports**: screenshot dashboard → paste into **PPT** → add insights → send to client → re-fix on feedback.
- **Volume/cost:** ~**20 client conversations/week**; each manual report = **1.5–2 hours** of one resource.
- **Desired state:** connect reports to **Claude** → instant, standardised, insight-led reports in a chosen format.
- **Cost angle:** The custom dashboard costs ₹5L/quarter to maintain. Daniel proposes **PostHog** as a cheaper analytics hub with built-in AI to generate the report from a good example template.

### 7.4 Performance Tracking — "Brands in Red"
- Disha wants a **weekly view** of which brands are underperforming / "in red."
- **Original plan:** team posts manually on WhatsApp every Friday (e.g., Abhishek Sharma's 5 brands + ROIs).
- **Rohit's counter:** manual = error-prone & wasteful → he built a **lookup tool** that auto-flags red when a brand misses **25% of target**.
- **Conflict:** **Rishabh** insists on manual Friday posting (so the team *feels* accountable for poor performance); **Rohit + Disha** prefer automation.
- **Disha's envisioned model:** brands already tiered (top/high/medium/low) → track week-on-week → one week <25% is acceptable, but **2–3 consecutive weeks** = genuinely red → for **top-priority** red brands, **Rohit (Ops)** should be alerted and instruct his team, rather than a junior flagging upward.
- **Guiding philosophy (shared by Daniel & Disha):** *"Humans do the human work; robots do the robot work."*

### 7.5 Client Onboarding Process
- **Core gap:** mismatch between what **BD/Rishabh promises on closure calls** and what the **operations team** is told.
- **No accountability / no record** of promises.
- **Standard onboarding expectation set with clients:** "For the first **3 months**, don't expect revenue."
- **During the 3 months:** After **month 1**, Chandika calls the brand to check satisfaction and resolve issues early.
- **Desired fix:** record/document/route what Rishabh promises on calls to the relevant person.

### 7.6 Client Escalation Process
**Four trigger parameters:**
1. **Target not met** — within **2 months** a brand hasn't hit promised revenue.
2. **Ad account in error** — card couldn't be processed on Meta.
3. **Legacy brand not growing** — vs last year / last month; no growth for a quarter.
4. **Client unhappy with their POC.**

**Escalation ladder:**
- Brand Manager → Team Lead (month 3 "dip check") → CSM Team (strategy + upsell) → Disha.
- **Current failure mode:** Without a defined process, an escalation surfacing in June leads to the client leaving by July.

### 7.7 Client Relationship Model & Ad-hoc Queries
- Founders mostly deal directly with Disha, not the team.
- **No client portal exists.** Daniel proposes a **client-facing "notice board"** so brands self-serve information before contacting Disha.

---

## 8. Key Problems / Gaps (Risk Register)

1. Knowledge concentrated in Disha.
2. Fragmented tooling — separate ChatGPT accounts, no shared AI.
3. Scattered context — no single source of truth per brand.
4. Creative bottleneck — capacity 9–10/day vs demand 20/day.
5. Resizing drag — 5-day, 3-resource manual cycle.
6. Reporting overload — ~20 manual weekly reports at 1.5–2 hrs each.
7. Onboarding expectation mismatch — undocumented BD promises.
8. Escalation has no defined, fast path.
9. Card/Meta-account ownership chaos (Rishabh deviating from policy, no audit trail).

---

## 9. Proposed Solution Architecture

Four pillars, all feeding **one source of truth**:

1. **Analytics → PostHog** — cheaper analytics hub vs ₹5L/quarter custom dashboard.
2. **Workflows → Claude** — individual repeatable skills: image resizing, sale-image generation, reports.
3. **Context / brand info → Google Drive (or GitHub)** — one place per brand; role-gated sharing.
4. **Layered dashboards (role-specific views)** — brand managers, team leads, founders all get the view that matters to them.

**Enabling step:** Build one example "good" context folder with Chandika → replicate across brands.

---

## 10. Action Items

| # | Owner | Action |
|---|---|---|
| 1 | Disha | Send Daniel 5 raw images + resizing specs + ad brief + sample "good" client report. |
| 2 | Daniel | Research PostHog and report back to Disha. |
| 3 | Daniel | Send Disha Notion availability link; Disha books syncs with Chandika & Rohit. |
| 4 | Daniel | Work with Chandika to define example context-folder architecture and pick template brand. |
| 5 | Daniel | Report back within one week on everything discussed. |
| 6 | Disha | Resolve with Rishabh: card-usage process and manual-vs-automated reporting disagreement. |

---

### Quick Ontology Index
- **Org:** Growify
- **Actors:** Disha (Founder), Rishabh (Co-founder/BD), Chandika (Brand Mgmt), Rohit (Ops), Daniel (Consultant); roles: POC, Brand Manager, Team Lead, CSM Team, Marketing.
- **Teams:** 4 client teams (~18 brands, ~10 ppl each) + Website team + Imagery Sizing team.
- **Clients:** Mahima Mahajan (Vikram), Aisha Rao, [legacy founding brand]; tiered Top/High/Medium/Low.
- **Systems:** Custom dashboard (Funnel→Meta/Google/Shopify), Rohit's lookup tool, Google Drive, WeTransfer, Photoshop/Adobe, ChatGPT/GPTs. Proposed: PostHog, Claude, Google Drive/GitHub.
- **Processes:** Creative (resize + sale-design), Reporting, Performance-tracking, Onboarding, Escalation (4 triggers, multi-stage ladder), Client Exit*, Employee Onboarding*, Employee Exit*, Interdepartmental handoffs.
- **Core metrics:** Targets (₹), 25% threshold = red, ROI, monthly revenue, campaigns/day (need 20, do 9–10).
