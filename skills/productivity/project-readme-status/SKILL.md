---
name: project-readme-status
title: Project README Status Management
category: productivity
trigger: Use when you need to change the `status:` line in a project's markdown front‑matter.
description: Update the status field in a project's README file.
---

# Overview
Many of your projects keep a simple front‑matter block at the top of the main README with a `status:` field (e.g. `status: in-progress`). When a milestone is completed you want a reliable, repeatable way to update that line and commit the change.

# Workflow
1. **Open the file** – use the absolute path to the README (or any markdown file containing the front‑matter block).
2. **Locate the status line** – typically near the top after `---`.
3. **Patch the line** – run the `patch` tool to replace the old status with the new one.
   ```json
   {
     "mode": "replace",
     "path": "<path-to-README>.md",
     "old_string": "status: in-progress",
     "new_string": "status: done"
   }
   ```
   Adjust `old_string` to match the current value.
4. **Commit the change** – optionally add, commit, and push via `git` if the repository is version‑controlled.
5. **Verify** – read back a few lines of the file to confirm the update.

# Pitfalls
- Ensure the file actually contains a unique `status:` line; otherwise use `replace_all: true`.
- Do not edit protected skills – this workflow is for project files, not skill definitions.
- If the repository has no remote configured, the commit step will fail; set up the remote first.

# Example
Updating a DataTH Discord Automation README from `in-progress` to `done`:
```
patch {
  mode: "replace",
  path: "~/ICloud-vault/Projects/DataTH Dev/Discord Access Automation/README.md",
  old_string: "status: in-progress",
  new_string: "status: done"
}
```

# References
- references/status-line.md – a concise example of the front‑matter block and typical statuses.
