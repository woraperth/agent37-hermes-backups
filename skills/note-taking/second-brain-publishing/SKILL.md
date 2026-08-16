---
name: second-brain-publishing
description: Publish approved notes safely to a Git-backed second brain.
version: 0.1.0
author: Perth888, Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [obsidian, second-brain, git, publishing]
    related_skills: []
---

# Second-Brain Publishing Skill

Use this skill when the user asks to save approved content into a Git-backed Obsidian second brain and push it to the remote repository. It covers locating the right project folder, creating dated notes, preserving user-provided wording, and publishing only the intended changes.

## When to Use

- Save a final email, campaign, article, meeting note, or project artifact into the Obsidian vault.
- Rename or reorganize a project subfolder and push the change.
- Commit approved pre-existing note changes after showing what will be published.

Don't use for: read-only vault search, broad vault cleanup, or unapproved content editing.

## Prerequisites

- Resolve the concrete vault path before file operations; do not pass unresolved environment variables to file tools.
- Read applicable `AGENTS.md` instructions.
- Check Git status before editing so pre-existing changes are known.
- Confirm the target project folder from existing files or ask when multiple folders are plausible.
- Use the user's local date/timezone for date-based filenames.

## Procedure

1. **Inspect scope first.** Run `git status --short --branch` and identify pre-existing changes. Do not claim that all modifications came from the current task. Completion criterion: the initial status is recorded and the target path is known.
2. **Match project conventions.** Search the vault for related filenames/content and read one or two nearby notes. Preserve the user's final wording; only add useful frontmatter or Markdown structure. Completion criterion: the destination folder and filename convention are clear.
3. **Create or edit the note.** Use `write_file` or `patch` with a concrete absolute path. For final approved content, prefer `YYYY-MM-DD descriptive-name.md`. Avoid inventing extra copy or changing wording supplied by the user. Completion criterion: the file exists at the intended path and contains the approved content.
4. **Review the diff.** Run `git diff --stat` and inspect the target diff. If the file is user-facing Markdown, follow repository review instructions when applicable. Completion criterion: only intended content changes are present.
5. **Stage narrowly.** Stage explicit target paths, not `git add -A`, when unrelated modifications are present. If the user explicitly approves all existing changes, then `git add -A` is allowed after reporting the complete scope. Completion criterion: `git diff --cached --name-status` contains exactly the approved paths.
6. **Commit and push.** Use a descriptive commit message, push the intended branch, and verify with `git status --short --branch` plus the remote commit ID. Completion criterion: the branch is synchronized and the working tree state is accurately reported.
7. **If an unrelated file is accidentally included.** Do not hide it. Preserve its local content, restore the remote file to its pre-task version in a corrective commit, push, and report the correction plainly. Then re-check status.

## Git Status Language

- `M` means the working-tree file differs from the latest commit; it does not identify who made the change.
- “Uncommitted” means local changes are not in the current commit; it does not mean the changes are bad.
- Report filenames and concise diff summaries when asked what is uncommitted.
- Never imply that unrelated local edits were created by the current task without evidence.

## Verification

- Confirm the exact destination path and filename.
- Confirm the commit includes only approved files unless the user explicitly approved a broader scope.
- Confirm `git status --short --branch` after pushing.
- If the working tree is dirty, list the remaining files and explain that they were not pushed.
- If a folder was renamed, verify the remote contains the new path and the old path is absent.

## Pitfalls

- A pre-staged unrelated file can be included even when staging a specific new file; inspect the index before committing.
- `git add -A` publishes every current local modification; never use it for a narrow task unless the user has approved all listed changes.
- Git may display Unicode folder names escaped or split-looking; verify the actual path before renaming.
- A successful push does not prove the right scope was committed; inspect the commit file list.

See `references/publishing-checklist.md` for the concise pre-push checklist.
