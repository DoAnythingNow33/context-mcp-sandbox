# ICM — Intelligent Context Management

**Framework by Jake Clief** | [Research Paper](https://drive.google.com/file/d/1cMubR3UrpsXlXIg-2br3Qp8Z2hTc9LKp/view?usp=sharing)

---

## Core Idea

A folder is a workspace. A workspace tells the AI where it is, what to do, and where to put the work. Three layers. Plain English. No code, no frameworks, no agents.

The problem this solves: dumping everything into one conversation forces AI to read irrelevant context, burns tokens, and makes you start from zero every session. Separating work into workspaces with explicit routing eliminates all of that.

---

## The Three Layers

### Layer 1 — The Map (`CLAUDE.md`)

Sits at the root of the project. Loaded on every task, in every workspace. This is the floor plan.

**What it contains:**
- What this project is and who it serves
- Full folder structure and what each area is for
- Naming conventions for every file type
- A routing table: for this task → read these files, skip those, use these skills

**Why it matters:** Without this, the AI either reads everything (wasted tokens), guesses wrong about what matters, or can't be edited along the way. The routing table in `CLAUDE.md` eliminates all three problems.

---

### Layer 2 — The Rooms (Workspace Context Files)

Each workspace has its own `context.md` (or similar). Loaded only when working in that workspace — not globally.

**What it contains:**
- What this workspace is for
- The process (first I do this, then that)
- File organization within the workspace
- Which skills or tools apply here

**Result:** One short prompt like "go to writing room, let's make something" loads the right context, the right voice, the right process — without reading anything irrelevant.

---

### Layer 3 — The Tools (Skills and MCP Servers)

Skills are packaged processes — sets of markdown files (sometimes Python scripts) that tell Claude how to do a specific task. MCP servers let the AI talk to external apps.

**Key rule:** Don't load every skill globally. Wire each skill into the workspace where it's needed. A writing workspace loads a humanizer skill. A production workspace loads a front-end design skill. The workspace context file references only what applies.

You can have 100 skills in a project. Each workspace loads only its own.

---

## Naming Conventions (Replace Databases)

Add naming conventions to `CLAUDE.md`. This lets the AI find, move, and organize files without any database, SQL, or vector search.

**Examples:**
```
Blog drafts:     [topic-slug]_draft.md
Newsletters:     YYYY-MM-[slug].md
Script versions: [name]_v2.md
Specs:           [name]_spec.md
```

With consistent naming, "pull my demo v2 and build a spec from it" gives the AI everything it needs to find the file, read the relevant docs, and produce output — zero custom infrastructure.

---

## Workspace Structure Pattern

Three workspaces is a common starting point. Names change per person; structure stays the same.

| Role | Example Workspace Names |
|------|------------------------|
| Content creator | Script Lab / Edit Bay / Distribution Hub |
| Freelancer | Client Intake / Delivery / Admin |
| Developer | Frontend / Backend / Docs |
| Coach / consultant | Client Work / IP Development / Content |

Each workspace gets:
- Its own subfolder
- Its own `context.md`
- Its own set of referenced skills
- Its own naming conventions (or inherits from root)

---

## Routing Table (Core Pattern)

The most important pattern in the system. Put this in `CLAUDE.md`:

| Task | Read | Skip | Skills |
|------|------|------|--------|
| Write blog post | `writing-room/context.md`, `references/voice.md` | `production/`, `community/` | humanizer |
| Build demo | `production/context.md`, `production/design-system.md` | `writing-room/`, `community/` | frontend-design |
| Community post | `community/context.md` | `production/`, `writing-room/` | — |

Adapt columns to your work. The point: explicit routing = no wasted tokens, no wrong guesses, full editability at each stage.

---

## Minimum Viable Setup (Three Files)

Start here. One folder, three files.

**`CLAUDE.md`**
```markdown
# Identity
You are helping [NAME] with [WHAT YOU DO].

# Folder Structure
- /drafts — work in progress
- /final — finished outputs
- /references — background material

# Rules
- Read this file first on every task
- Ask before creating files outside /drafts
- When unsure, ask

# Naming Conventions
- Drafts: [topic]_draft.md
- Finals: [topic]_final.md
```

**`context.md`** — describe the current project in 2–3 sentences, what good output looks like, what to avoid.

**`references.md`** — examples, style guides, background material Claude should know but not act on directly.

---

## How to Scale Up

1. Add workspaces as distinct areas of work emerge
2. Write a `context.md` per workspace
3. Add skills to workspace context files as needed
4. Tighten naming conventions as patterns solidify
5. Refine the routing table in `CLAUDE.md` as you learn what actually gets loaded per task

The three-layer structure (map → rooms → tools) holds regardless of domain. Only the labels and context change.

---

## Key Principles

- **Tokens are finite.** Only load context relevant to the current task.
- **Folders are the UI.** No app, no database, no framework required.
- **Naming replaces search.** Consistent file names let the AI navigate without infrastructure.
- **Skills belong in workspaces, not globally.** Wire tools where they're needed.
- **English is the architecture.** This is traditional separation-of-concerns, expressed in plain language.
