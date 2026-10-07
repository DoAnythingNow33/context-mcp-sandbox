# ops/ — Workflows Layer

Operational workflows that run the business. Each subfolder is one workflow with its own data, templates, and (where relevant) an Obsidian Base over it.

## sales/ — Prospecting CRM

The outbound pipeline. One markdown file per prospect in `sales/prospects/`, viewed through `sales/prospects.base`.

**Workflow:**
1. `/prospect` generates a researched batch of prospects matching Dan's targeting criteria → one file each in `sales/prospects/`, `status: new`
2. Dan works the "To Contact" view in the Base — sends the opening line via the prospect's channel, updates `status: contacted` + `last_touch`
3. Replies move to `status: replied` → `call-booked` → `won` (promote to `entities/people/` + `entities/projects/`) or `dead`
4. Every touch gets a row in the prospect file's Touch Log

**Status pipeline:** `new → contacted → replied → call-booked → won | dead`

**Rules:**
- A `won` prospect graduates: create the entity file in `entities/people/`, link back to the prospect file, set status `won`. The prospect file stays as the origin record.
- `fit_score` is 1–10; anything under 6 doesn't get generated.
- Prospect files are real companies found by research, never invented. If research can't verify a company exists, it doesn't get a file.
- The visual front-end for this pipeline will live in `visual/index.html` (planned — see DPL carry-forwards).
