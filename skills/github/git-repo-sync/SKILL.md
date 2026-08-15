---
name: git-repo-sync
description: "Mirror a git repo locally, synced via Hermes cron."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [GitHub, git, cron, sync, deploy-keys, obsidian, second-brain]
    related_skills: [github-auth, github-repo-management, obsidian]
---

# Git Repo Sync (local mirror + auto-pull)

Use when the user wants a GitHub repo cloned/mirrored locally AND kept
up-to-date automatically so you can search/read its contents (common for
Obsidian second-brain vaults, config repos, notes). Covers choosing the right
auth, cloning, and wiring a repeat `no_agent` cron pull.

## When to Use
- "clone this repo and sync it automatically"
- "pull my vault / second brain / notes repo periodically"
- A repo the agent must be able to read on demand but should never push to

## Auth decision (IMPORTANT — ask, don't assume)
For a **read-only mirroring** task, prefer a **deploy key over a PAT**:
- **Deploy key** = one SSH key scoped to ONE repo. Safer: no access to the
  whole account. Best when the repo is private and the user is OK dropping the
  public key into GitHub → repo Settings → Deploy keys. Keep it **read-only**
  (do NOT tick "Allow write access") for pure pulling.
- **PAT** = account-wide token; use only when deploy keys are impractical.
If the user brings up deploy keys themselves, confirm and go that route.

**Pitfall — silent private/empty distinction:** a private repo and a
non-existent repo BOTH return HTTP 404 on `https://github.com/...` and
`raw.githubusercontent.com`, so you can't tell them apart without auth. Probe
via SSH after the alias works before concluding "repo doesn't exist." Also a
clone that succeeds but reports `You appear to have cloned an empty
repository` is NOT a failure — the repo just has no commits yet. Tell the user
it's empty and waiting for content; the sync script still works.

## Steps
1. **Generate a dedicated SSH key** (one per repo, not your personal key):
   ```bash
   ssh-keygen -t ed25519 -C "<repo>-deploy" -f ~/.ssh/<repo_key> -N "" -q
   cat ~/.ssh/<repo_key>.pub   # give this to the user
   ```
   User pastes it at GitHub → repo → Settings → Deploy keys → Add (read-only).
2. **Add a host alias** in `~/.ssh/config` so the key is used only for this clone
   (and doesn't collide with your own GitHub identity):
   ```
   Host github.com-<owner>-<repo>
       HostName github.com
       User git
       IdentityFile ~/.ssh/<repo_key>
       IdentitiesOnly yes
   ```
   `chmod 600 ~/.ssh/config`.
3. **Clone through the alias**:
   ```bash
   git clone git@github.com-<owner>-<repo>:<owner>/<repo>.git ~/<local_dir>
   ```
   STOP if it says "empty repository" (the repo has no content yet; step 4 still works).
4. **Write a sync script** to `~/.hermes/scripts/sync-<repo>.sh`. Idempotent,
   empty-repo-safe, never modifies the remote. Copy from scripts/sync-repo.sh.
5. **Create the cron job** with `no_agent=true` (no LLM burn, just run the script):
   ```bash
   cronjob action=create \
     name=sync-<repo> deliver=local no_agent=true enabled_toolsets=["terminal"] \
     schedule="*/30 * * * *" script=sync-<repo>.sh
   ```
   - **deliver=local** — the sync is internal plumbing; don't spam a channel.
   - Cadence: 5 min is eager; **30 min** is what this user prefers for
     second-brain vaults. Confirm rather than defaulting to 5.
6. **Verify**: run the script once and confirm it printed `files=N`. Then
   `cronjob action=list` to confirm next_run_at.

## Pitfalls
- **Don't `git pull` in a cron on a divergable branch.** `git reset --hard
  origin/HEAD` is the reliable read-only mirror; plain `git pull` needs a
  tracking branch and can block on merge conflicts.
- **Do not push/publish from the mirror.** The deploy key is read-only by design;
  keep the cron/local copy read-only so the vault stays the source of truth.
- **Save the setup to memory** so future sessions know the repo path + local dir
  + cron id and can answer questions about the vault's contents immediately.

## Support files
- `scripts/sync-repo.sh` — copy to `~/.hermes/scripts/sync-<repo>.sh`, edit paths.
