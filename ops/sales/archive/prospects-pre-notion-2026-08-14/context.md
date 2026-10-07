# ops/sales/prospects/ — Prospect Files

One file per company. Each file is a scored, researched prospect record that tracks the full outbound journey from first research to won or dead.

## Frontmatter schema

```yaml
---
type: prospect
company: Company Name
industry: Category
size: X-Y employees
location: City, Country
region: United Kingdom
channel: Email | LinkedIn
fit_score: 1-10
status: new | contacted | replied | call-booked | won | dead
added: YYYY-MM-DD
last_touch: YYYY-MM-DD
next_action: What to do next
source: https://...
email: contact@...
linkedin_search: Role at Company
batch: YYYY-MM-DD
---
```

## File body structure

```
## AI Opportunity
What specifically could AI do for this company, and why would they care.

## Opening Line
> The exact message to send. Personalised, problem-first.

## Contact
Name, role, email, LinkedIn URL.

## Touch Log
| Date | Channel | Message | Response |
```

## Naming

`[company-slug].md` — e.g., `favoured.md`, `prohibition-pr.md`

Slugs are lowercase, hyphenated, no special characters. Match the company's common short name.
