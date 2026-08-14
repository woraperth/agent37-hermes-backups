---
name: typefully-mcp
description: "Interact with Typefully MCP server tools."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [mcp, typefully, integration]
    homepage: https://typefully.com
    related_skills: []
---

# Typefully MCP Integration

This skill provides guidance and reference material for using the **typefully** MCP server within Hermes Agent. It includes a concise summary of the tools discovered during a test run and typical usage patterns.

## When to Use
- After adding the `typefully` MCP server via `hermes mcp add`.
- To query available Typefully tools, create drafts, edit media, or retrieve analytics.
- For automation scripts that manage social sets, drafts, tags, and queue schedules.

## Quick Reference
- Run `hermes mcp test typefully` to verify connection and list tools.
- Tools follow the prefix `typefully_` (e.g., `typefully_get_me`).
- See the attached reference file for the full tool list and brief descriptions.

## Common Tasks
| Goal | Suggested Tool |
|------|----------------|
| Get authenticated user info | `typefully_get_me` |
| List social sets (accounts) | `typefully_list_social_sets` |
| Retrieve drafts for a set | `typefully_list_drafts` |
| Create a new draft | `typefully_create_draft` |
| Edit an existing draft | `typefully_edit_draft` |
| Delete a draft | `typefully_delete_draft` |
| Upload media (image/video) | `typefully_create_media_upload` |
| Check media processing status | `typefully_get_media_status` |
| Manage tags | `typefully_list_tags`, `typefully_create_tag` |
| Work with queue schedules | `typefully_get_queue_schedule`, `typefully_queue_put_queue_schedule` |
| Retrieve queue slots | `typefully_get_queue` |
| Manage comments on drafts | `typefully_list_comments`, `typefully_create_comment`, `typefully_comments_add_comment_to_thread` |

## Pitfalls & Tips
- **Authorization**: Ensure the `TYPEFULLY_API_KEY` env var is set for the MCP server configuration.
- **Tool Naming**: All tools are lower‑case with underscores; use the exact names when invoking via Hermes.
- **Rate Limits**: Typefully may enforce API rate limits; handle `429` responses with retries.
- **Media Uploads**: First call `typefully_create_media_upload` to get a presigned URL, upload the file, then call `typefully_get_media_status`.
- **Queue Scheduling**: Updating the queue schedule replaces the entire rule set; retrieve the current schedule first if you only need to modify part of it.

## Further Reading
- See the attached `references/typefully-mcp.md` for the full list of discovered tools and their short descriptions.
- Typefully API docs: https://typefully.com/api (external).
