---
name: writing-draft-source-integration
description: "Use when adding a source to an existing writing draft."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [writing, drafts, Obsidian, sources, YouTube]
    related_skills: [obsidian, youtube-content]
---

# Writing Draft Source Integration

Use this class-level workflow when a user shares an article, video, or other source and asks to “add this” to a writing draft, article, post, or research note.

## Workflow

1. **Resolve the target before editing.** Search the user's writing workspace for likely drafts by title, recent modification, topic, and references to the surrounding conversation. If one target is clearly established, use it. If multiple candidates remain plausible—especially when the source topic does not obviously match the newest draft—ask one concise clarification question rather than silently choosing.
2. **Inspect the target note.** Read enough surrounding content to identify the best insertion point and the draft's existing citation/source format. Preserve its language, tone, headings, and link style.
3. **Verify the source.** For YouTube, first try the transcript workflow. If transcript retrieval is blocked, use a verified metadata fallback such as YouTube oEmbed or the public watch-page metadata to establish the title, channel, and URL. Do not present unverified transcript-level claims as facts.
4. **Choose the smallest useful addition.** Usually add a source heading, canonical link, and a short “why this belongs here” note. If the user only asked to add the link, do not expand into a full summary. Any synthesis must be explicitly framed as a proposed angle or editorial note when based on limited metadata.
5. **Edit with an anchored patch.** Append or insert at a stable heading/paragraph rather than rewriting the entire note. Do not alter unrelated draft text.
6. **Verify the result.** Re-read the edited section and inspect the version-control diff/status. Confirm the source URL, target path, and inserted content are present, and report any pre-existing uncommitted changes separately from the new edit.

## Ambiguity and safety

- “My writing draft” is not enough to justify guessing when there are several drafts or when the source topic conflicts with the apparent draft. Ask which draft the user means.
- A source title alone supports a link and a tentative editorial connection, not detailed claims about the video's contents.
- Never claim a transcript was reviewed if the transcript fetch failed.
- Keep Discord replies concise: name the file, summarize what was added, and mention verification; do not paste raw note contents or verbose tool output.

## References

- See `references/youtube-metadata-fallback.md` for the validated YouTube fallback and evidence boundary.
