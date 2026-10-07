---
description: "Three-way git sync — reconciles your Mac, GitHub, and the Hermes cloud server so all three are on the same commit. Run at the start of any session, or any time you suspect drift."
---

# /gitupdate — Three-Way Sync (Mac ↔ GitHub ↔ Hermes)

There are three places this vault lives: your Mac (where you and Claude Code work), GitHub (the source of truth), and the Hermes cloud server (where Hermes captures ad-hoc updates and pushes/pulls independently). Any of the three can drift ahead of the others — Hermes commits during the day, you commit locally, a PR sits unmerged on GitHub. This skill reconciles all three, in order, and refuses to force anything that isn't safe.

**Config:**
```
HERMES_REPO_PATH = /home/hermes/context-2.0-github
```

---

## Step 1 — Reconcile Mac ↔ GitHub

```bash
cd "/Users/DoAnythingNow./Desktop/Context 2.0"
git status
```

**If there are uncommitted changes:** show Dan what's modified/untracked and ask whether to commit them now (with a short message) or stash them. Do not pull with a dirty working tree.

```bash
git fetch origin
git status
```

This tells you ahead/behind counts against `origin/main`. If diverged (commits on both sides — this is the common case since Hermes pushes independently):

```bash
git pull
```

If this produces a real conflict (not just an auto-mergeable divergence), **stop and surface the conflicting files to Dan** — do not resolve by guessing which side wins.

**Check for open PRs before pushing:**
```bash
gh pr list
```
If there's an open PR against `main`, tell Dan and ask whether to merge it now (via `gh pr merge` or on GitHub directly) before continuing — merging after your local push can cause the exact divergence this skill exists to prevent.

Once clean and merged:
```bash
git push
```

---

## Step 2 — Confirm GitHub state

```bash
git rev-parse HEAD
git ls-remote origin main
```

Both hashes should match. If they don't, something failed silently in Step 1 — stop and report to Dan rather than proceeding to Hermes.

---

## Step 3 — Reconcile Hermes ↔ GitHub

SSH commands go to a host outside the sandbox network allowlist, so each one will need Dan's explicit approval to run — that's expected, not an error.

```bash
ssh hermes "cd $HERMES_REPO_PATH && git status --short"
```

**If Hermes has uncommitted changes:** surface them to Dan. Do not discard or force-pull over them — Hermes may be mid-write on a capture. Wait for Dan's call.

**If clean:**
```bash
ssh hermes "cd $HERMES_REPO_PATH && git pull"
```

If that reports a conflict, stop and surface it — same rule as Step 1.

---

## Step 4 — Confirm all three match

```bash
git rev-parse HEAD
git ls-remote origin main
ssh hermes "cd $HERMES_REPO_PATH && git rev-parse HEAD"
```

Report the three short hashes to Dan in one line. If all three match, sync is done. If any differ, name which one is behind and why (uncommitted changes still pending, conflict unresolved, PR still open) rather than declaring success.

---

## Notes

- Never use `--force`, `reset --hard`, or discard flags in any step. If something can't be reconciled cleanly, that's a signal to stop and ask, not to pick a side.
- This skill assumes `gh` is authenticated. If `gh pr list` fails with an auth error, tell Dan to run `gh auth login` once — don't try to work around it.
