---
name: second-brain-context
description: Auto-include relevant Obsidian note excerpts in replies.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Purpose
When a keyword or phrase is mentioned in conversation, this skill searches the user's Obsidian vault and inserts a concise relevant excerpt into the reply.

# Prerequisites
- `OBSIDIAN_VAULT_PATH` env var set or vault at `~/Documents/Obsidian Vault`.
- Vault contains markdown notes.

# Steps
1. **Resolve vault path** using `terminal` to expand `$OBSIDIAN_VAULT_PATH` or fallback.
2. **Search note titles** with `search_files` (`target:"files"`, pattern:`*${TERM}*.md`) under the vault, limit 5.
3. If titles found, **read** top note via `read_file` (first 200 lines) and extract a paragraph containing the term.
4. If no title match, **content search** with `search_files` (`target:"content"`, pattern:term, `file_glob:"*.md"`).
5. **Trim excerpt** to ≤500 characters.
6. **Compose snippet**:
   ```markdown
   **Relevant note:**
   > {excerpt}
   [[{Note Title}]]
   ```
   Include wikilink.

# Pitfalls
- Multiple matches: include only the top result, note others exist.
- Large notes: truncate excerpt.
- No match: omit snippet.
- Performance: limit searches to 5 and read only needed lines.

# Verification
- Ensure excerpt contains the term and file exists before reading.

# Example
```bash
TERM="Kanban"
# Run skill to get excerpt ready for reply.
```