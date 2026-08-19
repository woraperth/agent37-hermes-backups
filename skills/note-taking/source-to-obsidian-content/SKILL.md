---
name: source-to-obsidian-content
description: "Use when saving shared sources as Obsidian notes."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Obsidian, writing, YouTube, transcripts, Git]
    related_skills: [youtube-content, obsidian]
---

# Source to Obsidian Content

Use this class-level workflow when the user shares a video, article, or other source and asks to add it to a writing draft, writing materials, or the second brain.

## Core user preference

For this user, a new source or idea becomes a **new Markdown file by default**. Do not append to or modify an existing writing file unless the user explicitly asks to update the old file. If the destination is genuinely ambiguous, ask before editing. A newly created writing file should be committed and pushed to the vault Git repository after verification.

## Workflow

1. **Identify the source and target area.** Resolve the concrete vault path and inspect nearby Writing Materials/Inputs files for naming and folder conventions. Do not infer that “add to my draft” means edit an existing file; create a separate note unless explicitly told otherwise.
2. **Fetch authoritative source data.** For YouTube, prefer a transcript provider/API when direct transcript retrieval is blocked. Keep the source URL, title, channel/author, and transcript language in the note. Never claim a transcript was retrieved unless the API returned non-empty content.
3. **Summarize from the retrieved source.** Separate confirmed source facts from editorial angles or questions for future writing. Use the user’s established Thai writing voice when the note is Thai. Avoid inventing details not supported by the source.
4. **Create the new Markdown note.** Include frontmatter with date and source URL, a clear title, initial framing, source-grounded summary, practical takeaways, and questions or angles for later writing. Preserve the raw transcript externally or in a temporary workspace unless the user explicitly asks to store it in the vault.
5. **Verify the artifact.** Read the created note back, check that it is non-empty, contains the source URL, and has a coherent summary. Check Git status and ensure unrelated pre-existing changes are not included.
6. **Commit and push.** Add only the new note, commit with a descriptive message, push to the configured remote, then verify the branch is synchronized and the working tree is clean. Report the file path and commit identifier concisely.

## YouTube transcript fallback

If the normal YouTube transcript helper is blocked, use SUPADATA when `SUPADATA_API_KEY` is available. The API’s native mode is the preferred first attempt because it retrieves an existing transcript without AI-generation delay or generation cost. If native mode has no transcript and AI generation is appropriate, use the provider’s documented auto/generate mode and poll its job endpoint until `completed` or `failed`; do not wait indefinitely on an `active` job. See `references/supadata-api.md` for the tested request and polling pattern.

## Pitfalls

- Do not silently mutate an existing draft because it appears related.
- Do not leave a newly created note uncommitted when the user’s standing preference is to push writing files to Git.
- Do not treat a provider’s `202 {jobId}` response as the transcript; poll and validate the final result.
- If an async provider job remains `active` unusually long, retry with native/existing-transcript mode before continuing to wait.
- Keep API keys out of notes, logs, commits, and user-facing replies.
