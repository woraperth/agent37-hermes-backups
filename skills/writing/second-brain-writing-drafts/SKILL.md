---
name: second-brain-writing-drafts
description: "Use for new source drafts in a Git-backed second brain."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [writing, drafts, Obsidian, YouTube, Git]
    related_skills: [obsidian, youtube-content, writing-draft-source-integration]
---

# Second-Brain Writing Drafts

Use this class-level workflow when a user shares a source—especially a YouTube video—and asks to create a new writing draft in a Git-backed Obsidian second brain.

## Core workflow

1. **Resolve the repository and conventions.** Locate the user's vault/repository from known configuration or established workspace context. Inspect nearby source notes and the relevant folder/index before creating anything. Preserve the repository's language, frontmatter, filename/date convention, and Markdown style.
2. **Default to a new note for a new source.** If the user says “create a new writing draft” or shares a source without naming an existing draft, create a new note in the input/source folder. Do not attach it to the newest or most similar draft unless explicitly asked. Ask only when the destination genuinely cannot be determined.
3. **Verify source metadata before synthesis.** For YouTube, attempt the transcript workflow first. If transcript retrieval is blocked or unavailable, use a public metadata fallback such as YouTube oEmbed to verify title, channel, video ID, and canonical URL. Never claim to have reviewed a transcript that was not retrieved.
4. **Create a useful source scaffold.** A new note should normally include:
   - frontmatter marking it unprocessed/source type;
   - verified title, channel, and source link;
   - concise questions or themes to investigate;
   - a tentative editorial angle explicitly labeled as such;
   - a clear note when detailed transcript-level claims remain unavailable.
   Do not invent detailed claims from a title or thumbnail alone.
5. **Write without disturbing unrelated notes.** Use a full new-file write for a new note. Use anchored patches for existing notes. Avoid human-review automation unless the user explicitly asks for it.
6. **Verify and publish the artifact.** Re-read the created note, check Git diff/status, confirm the URL and target path, and distinguish pre-existing changes from the new work. When the user has asked to save the draft and the repository is Git-backed, commit and push the new note, then verify the branch is clean and synchronized.
7. **Report concisely.** Name the created file, summarize what it contains, disclose transcript/metadata limitations, and report commit/push verification without pasting the whole note.

## Pitfalls

- A verified title and channel support metadata, not a detailed summary.
- Do not silently update an existing note when the user's standing preference is new-file-by-default.
- Do not confuse a failed transcript fetch with evidence that the video has no transcript; describe the actual access limitation.
- If the first Git command runs outside the repository, retry with an explicit repository path rather than assuming the write failed.

## Supporting detail

- See `references/youtube-source-fallback.md` for the metadata fallback and evidence boundary used when transcript access is unavailable.
