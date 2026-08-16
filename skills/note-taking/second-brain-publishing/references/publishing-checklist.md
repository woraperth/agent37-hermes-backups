# Publishing Checklist

Use this compact checklist before pushing an approved vault change:

1. `git status --short --branch` — record pre-existing modifications.
2. Resolve the exact project folder and date-based filename.
3. Write the note and inspect its diff.
4. Stage explicit paths; inspect `git diff --cached --name-status`.
5. Commit with a descriptive message and push the intended branch.
6. Verify remote sync with `git status --short --branch` and the latest commit ID.
7. Report any remaining dirty files accurately; do not imply they were created by the current task.
