# Exact supplied-post preservation

Use this checklist when saving a user-supplied campaign or social post into a Git-backed Obsidian project:

1. Inspect neighboring Markdown files before choosing the destination filename. If the project uses dated campaign names such as `YYYY-MM-DD <descriptor> (Facebook, Email).md`, preserve that convention.
2. Read one or two neighboring notes and reuse their frontmatter, channel headings, and related-note wikilinks where useful. Do not invent copy around the supplied post unless needed for navigation.
3. Keep the post body verbatim. Preserve Unicode punctuation, emoji, arrows, spacing, URLs, and Thai wording. Metadata outside the body may follow the project's existing format.
4. Compare the extracted saved body with the source programmatically before commit. A byte/string comparison catches changes that visual review can miss.
5. Stage only the intended note, commit, push, and verify the final branch status and remote commit. If a command is run outside the repo, retry with an explicit repository path and do not report success until Git confirms it.
