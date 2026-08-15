#!/usr/bin/env bash
# Read-only sync of a remote GitHub repo to a local mirror.
# Copy to ~/.hermes/scripts/sync-<repo>.sh and edit the "cd" path + remote.
# Empty-repo-safe and idempotent; never modifies the remote.
# Works through an SSH host alias configured in ~/.ssh/config (deploy key).
set -e
cd ~/<local_dir>   # EDIT: your local mirror path

# Remote is fetched via the host alias too; show both edits together.
git fetch --depth 1 origin 2>/dev/null || git fetch origin 2>/dev/null || exit 0

# Detect HEAD branch (fallback main) and hard-reset the local mirror to it.
HEAD_BRANCH=$(git remote show origin 2>/dev/null | sed -n 's/.*HEAD branch: //p' || echo main)
HEAD_BRANCH=${HEAD_BRANCH:-main}
if git rev-parse --verify "origin/$HEAD_BRANCH" >/dev/null 2>&1; then
  git checkout -q "$HEAD_BRANCH" 2>/dev/null || git checkout -q -b "$HEAD_BRANCH" "origin/$HEAD_BRANCH"
  git reset -q --hard "origin/$HEAD_BRANCH"
fi

echo "synced $(date +%Y-%m-%dT%H:%M:%S) branch=$HEAD_BRANCH files=$(find . -type f -not -path './.git/*' | wc -l)"
