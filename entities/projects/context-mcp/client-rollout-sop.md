---
type: sop
project: "[[context-mcp]]"
last_updated: 2026-10-01
---

# Context MCP — Client Rollout SOP

← [[context-mcp]] · code: `/home/hermes/context-mcp` · full reference: its `README.md`

Turn a client's context vault into something their team and their own AI can plug into.

## 1. Decide access with the client (don't skip)

Walk the vault with the founder and fill this in:

| Who | Reads | Hidden | Write level |
|---|---|---|---|
| Each founder | everything | the *other* founder's `self/` | `create` |
| Team / employees | the business room (e.g. `Growify/`) | `founders/`, `_flags*`, HR/salary files, `_archive`, `_status` | `flag` |
| Client's own agent (e.g. Hermes) | same as its owner | same as its owner | owner's level |

Write levels: `none` (read only) · `flag` (propose changes for a founder to confirm) · `append` (add to existing files) · `create` (also new files).
Ask specifically: *"Is there anything in meetings/ or people/ you wouldn't want an employee to read?"*

## 2. Config

```bash
cd /home/hermes/context-mcp
cp configs/growify.yaml configs/<client>.yaml
```
Edit: `name`, `vault` (path on the box), `orientation_files` (digest/ontology), `flags_file`, `prompt_dirs`, `audit_log`, `users` (from step 1).

## 3. Tokens

```bash
.venv/bin/python -m context_mcp.tokens add configs/<client>.yaml <user>   # shown once
.venv/bin/python -m context_mcp.tokens list configs/<client>.yaml
.venv/bin/python -m context_mcp.tokens revoke configs/<client>.yaml <user> # then restart
```
Send each token privately (1Password / Signal), never in a group chat or email thread.

## 4. Run it

- Copy `deploy/context-mcp-growify.service` → `/etc/systemd/system/context-mcp-<client>.service`; set `User=` to the vault owner, the config path, and a free `--port`.
- `systemctl enable --now context-mcp-<client>`; check `curl localhost:<port>/health`.
- HTTPS: add a Caddy block (`deploy/Caddyfile.example`) for `<client>.context.<domain>` → `127.0.0.1:<port>`; set `allowed_hosts` in the config; restart.
- If writes should reach GitHub: give the vault owner a deploy key and set `git.push: true`.

## 5. Smoke test before handing over

With each token: `get_map` says the right name + access; an employee token can't read a hidden file; a flag lands in `_flags.md` as a commit by that person. Quick way:

```bash
claude mcp add --transport http <client>-test https://<host>/mcp --header "Authorization: Bearer <token>"
claude -p "Use the <client>-test server: what can I access, and who owns client escalations?"
```

## 6. Send connection instructions

**Claude Code:**
`claude mcp add --transport http <client> https://<host>/mcp --header "Authorization: Bearer <token>"`

**Claude Desktop / Cursor / other JSON-config clients:**
```json
{"mcpServers": {"<client>": {"type": "http", "url": "https://<host>/mcp",
  "headers": {"Authorization": "Bearer <token>"}}}}
```

**Hermes:** add the same URL + header as an MCP server in that instance's config.

Tell them: *"Start by asking it what's in the vault. To log a meeting, use the /meeting prompt."*

## 7. After go-live

- Check the audit log (`logs/<client>-audit.jsonl`) weekly at first.
- Triage flags raised by the team in `_flags.md` with the founder.
- Make sure the digest/ontology still gets regenerated (owner sessions or a GitHub Action); remote agents can't run scripts.
