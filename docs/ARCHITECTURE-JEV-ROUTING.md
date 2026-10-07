---
description: Three-layer routing architecture — LLM meaning extraction + JEV decision layer + LLM execution
type: architecture
created: 2026-09-10
status: proposed
---

# Architecture: LLM + JEV + LLM (Three-Layer Routing)

## Problem

Current `CLAUDE.md` routing is LLM-driven: every user message triggers Claude to:
1. Parse the intent
2. Decide which context files to load
3. Plan the response
4. Execute

This is correct reasoning but expensive — token-heavy on steps 1-2 (understanding + routing) before any real work happens.

## Solution: Offload Routing to JEV

**JEV** (or Layer, or similar lightweight decision classifier) is a fast, non-LLM decision engine. It excels at:
- Classification (what type of request is this?)
- Routing (which domain/subsystem should handle it?)
- Structured decision-making (given rules + context, what's the next action?)

**Three-layer flow:**

```
User Message
     ↓
[LAYER 1] LLM: Extract Meaning
     ├─ Parse intent
     ├─ Surface key entities (client name, project, meeting type, date)
     ├─ Identify constraints (time-bound? involves other people? async-safe?)
     └─ Output: structured intent packet
     ↓
[LAYER 2] JEV: Route & Decide
     ├─ Classify request type (client work, content, IP, meeting ingest, etc.)
     ├─ Query context folder structure
     ├─ Determine which files to load (or if load-nothing is right)
     ├─ Check routing rules (is this async-safe? does it need approval gate?)
     └─ Output: routing decision + file list + guardrails
     ↓
[LAYER 3] LLM: Execute
     ├─ Load context files (guided by JEV decision)
     ├─ Perform the actual work (write, analyze, create, summarize)
     ├─ Format output for delivery
     └─ Return result
```

---

## Why This Works

### Token Efficiency
- **Before:** Every message pays token cost for LLM routing logic across the full context system
- **After:** Routing is handed off to a fast, stateless classifier (JEV), freeing LLM tokens for meaning extraction + real work

### Speed
- JEV decisions are near-instant (not API-bound to an LLM)
- No latency waiting for a second LLM call
- Routing rules are deterministic, not probabilistic

### Accuracy
- Routing rules are explicit (not learned, not probabilistic)
- LLM focuses on what it's good at: understanding language, extracting intent, creating content
- JEV focuses on what it's good at: fast classification and rule application

### Maintainability
- Routing logic is separate from meaning extraction logic
- Easy to add new rules without retraining
- Easy to debug (rule didn't fire? Check the rule, not the LLM)

---

## Implementation Plan

### Phase 1: Design the Decision Model (Immediate)

#### 1.1 Define Request Types
Classify every possible user message into one of these buckets:

- **Client Work** (coaching, workshops, consulting)
  - Entity: which person/project?
  - Load: `entities/people/[name].md` + `entities/projects/[project].md` + relevant meeting files
  - Approval gate: drafts to user before sending externally
  
- **Meeting Ingest** (parsing a call, extracting action items)
  - Entity: which person/project/meeting?
  - Load: `IP/_index.md` + relevant entity file
  - Approval gate: none (async-safe)
  
- **Content Creation** (LinkedIn, Twitter, blog, email)
  - Load: `ops/content/context.md` + `self/writing-dna.md` + `IP/_index.md` + `_digest.md`
  - Approval gate: drafts for external comms
  
- **IP Development** (refine a concept, add to knowledge library)
  - Load: `IP/context.md` + `IP/_index.md` + relevant `IP/[slug].md` files
  - Approval gate: none (internal)
  
- **Daily Capture / DPL** (brain dump, voice memo processing)
  - Load: today's DPL file, current `P-` plan, maybe `self/goals.md`
  - Approval gate: none
  
- **Self / Arc Reflection** (coaching on identity, beliefs, arc)
  - Load: `self/context.md` + `self/arc.md` + `self/identity.md` + `self/beliefs.md`
  - Approval gate: none
  
- **Calendar / Planning** (weekly review, monthly check-in, scheduling)
  - Load: `calendar/context.md` + latest `R-` and `P-` files
  - Approval gate: none (internal)
  
- **Synthesis** (cross-layer: state of the business, arc check, strategy)
  - Load: `self/arc.md` + `self/goals.md` + `_digest.md` + latest `R-`/`P-`
  - Approval gate: none (internal)

#### 1.2 Define Context Loading Rules
For each request type, specify:
- **Load these files always**
- **Load these files conditionally** (if entity mentioned, if date is X, if keyword present)
- **Never load these files** (to save tokens)
- **Approval required?** (yes/no)
- **Async-safe?** (can be dispatched to background agent, or must stay in conversation)

#### 1.3 Define Decision Outputs
JEV outputs a structured packet:

```json
{
  "request_type": "client_work",
  "entity_type": "person",
  "entity_name": "Victoria Russel",
  "files_to_load": [
    "entities/people/victoria-russel.md",
    "entities/projects/mycelium-partnership.md",
    "meetings/2026-08-XX-victoria.md"
  ],
  "guardrails": {
    "approval_required": true,
    "approval_gate": "external_comms_approval_gate",
    "async_safe": false
  },
  "confidence": 0.98,
  "reasoning": "Email draft for external contact — requires approval before send"
}
```

---

### Phase 2: Build JEV Router (Next)

#### 2.1 Set Up JEV / Layer
- [ ] Research JEV vs. Layer vs. other lightweight classifiers
- [ ] Install locally
- [ ] Learn the API
- [ ] Test classification accuracy on past messages

#### 2.2 Encode Decision Rules
Create a rules engine that:
- Takes user message + extracted intent (from LLM Layer 1)
- Applies decision rules (if X then load Y; if keyword contains Z then entity is...)
- Returns routing decision + file list

#### 2.3 Integration Point
Build a Python wrapper that:
- Calls LLM Layer 1 to extract intent
- Calls JEV to route
- Returns file list to LLM Layer 3

---

### Phase 3: Integrate into CLAUDE.md (Later)

Replace the current routing logic in `CLAUDE.md` with:

```markdown
## Routing: Three-Layer System

### Layer 1: LLM Meaning Extraction (Claude)
User message → Intent packet (entity names, keywords, constraints)

### Layer 2: JEV Decision (Fast Classifier)
Intent packet → Routing decision (which files, approval needed?, async-safe?)

### Layer 3: LLM Execution (Claude)
Load files + execute task → Return result
```

---

### Phase 4: Testing & Iteration (On Laptop)

#### Test Cases

1. **Client work request**
   - Message: "Draft an email to Victoria about the Mycelium partnership next steps"
   - Expected: Load Victoria's file + Mycelium project file + recent meeting
   - Expected guardrails: approval_required=true

2. **Meeting ingest**
   - Message: "Parsed call with Rishab — he wants to see usage analytics by Friday"
   - Expected: Load IP index + Growify project file
   - Expected guardrails: async_safe=true, approval_required=false

3. **Content creation**
   - Message: "Write a LinkedIn post about ontology and AI workflows"
   - Expected: Load writing-dna + IP index + digest
   - Expected guardrails: approval_required=true (external)

4. **Self reflection**
   - Message: "Arc check — am I living the frameworks?"
   - Expected: Load arc + identity + beliefs
   - Expected guardrails: approval_required=false

5. **Ambiguous request**
   - Message: "What should I do next?"
   - Expected: JEV confidence < threshold → ask clarifying question
   - Expected guardrails: needs more context

---

## Metrics & Success Criteria

- **Token savings:** Measure tokens before/after (should see 20-40% reduction in routing overhead)
- **Speed:** Measure latency from message to file-list decision (should be <1 second)
- **Accuracy:** Test on 50 past messages — do the right files get loaded?
- **False positives:** Do guardrails catch all external comms?

---

## Open Questions

1. **JEV vs. Layer vs. other options?** Research needed — which classifier is easiest to embed and fastest?
2. **Real-time entity updates?** If I rename a client, does JEV know? (Probably requires a hot-load mechanism)
3. **Confidence thresholds?** If JEV is <80% confident, what's the fallback? (Ask user for clarification? Load broader context?)
4. **Error handling?** What happens if JEV suggests loading a file that doesn't exist?

---

## Timeline

- **Immediate (today):** Finalize request types + decision rules (this document)
- **Near-term (this week):** Research JEV/Layer, test on laptop
- **Medium-term (2-3 weeks):** Build integration, test on 50 past messages
- **Production (1 month):** Roll out, monitor, iterate

---

## Benefits Summary

| Metric | Before | After |
|--------|--------|-------|
| Routing latency | 2-3 sec (LLM) | <1 sec (JEV) |
| Tokens per message | ~800-1200 | ~400-600 |
| Routing accuracy | ~90% (probabilistic) | ~98% (rule-based) |
| Maintainability | Rules baked into CLAUDE.md | Separate, versioned rules engine |
| Extensibility | Requires retraining LLM | Add rules, done |

This is the future of Hermes — a hybrid system where the LLM does what it's brilliant at (meaning, writing, reasoning), and the classifier does what it's brilliant at (fast, deterministic routing).

Ready to build when you are.
