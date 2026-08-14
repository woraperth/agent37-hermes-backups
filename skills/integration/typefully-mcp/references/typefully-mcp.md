# Typefully MCP Tools Discovered

The `hermes mcp test typefully` command reported **25 tools**. Below is a concise list with brief descriptions.

| Tool | Description |
|------|-------------|
| `typefully_get_me` | Retrieve the currently authenticated Typefully user information. |
| `typefully_list_social_sets` | List all social sets (accounts) you can access. |
| `typefully_get_social_set_details` | Get detailed information about a specific social set, including settings and platforms. |
| `typefully_list_drafts` | Retrieve all drafts for a specific social set, with optional pagination. |
| `typefully_create_draft` | Create a new draft with content for one or more social sets. |
| `typefully_get_draft` | Retrieve a specific draft by ID, including its full content. |
| `typefully_edit_draft` | Update an existing draft (supports partial updates). |
| `typefully_delete_draft` | Delete a draft (requires write access). |
| `typefully_create_media_upload` | Generate a presigned S3 URL for uploading images or videos. |
| `typefully_get_media_status` | Check the processing status of an uploaded media file. |
| `typefully_list_tags` | List all tags for a social set, ordered by usage. |
| `typefully_create_tag` | Create a new tag for a social set (slug auto‑generated). |
| `typefully_get_queue_schedule` | Retrieve the queue schedule rules for a social set. |
| `typefully_queue_put_queue_schedule` | Replace the queue schedule rules for a social set. |
| `typefully_get_queue` | Retrieve queue slots and the scheduled/planned draft times. |
| `typefully_linkedin_resolve_linkedin_organization_from_url` | Resolve a LinkedIn organization URL into its internal ID and metadata. |
| `typefully_list_comments` | Retrieve comment threads attached to a draft, ordered by creation time. |
| `typefully_create_comment` | Create a new comment thread on a draft. |
| `typefully_comments_add_comment_to_thread` | Append a comment to an existing thread. |
| `typefully_comments_resolve_thread` | Resolve a comment thread and remove the corresponding placeholder. |
| `typefully_delete_comment` | Delete a comment from a thread. |
| `typefully_update_comment` | Update the plain‑text body of a single comment. |
| `typefully_delete_thread` | Delete an entire comment thread and all its comments. |
| `typefully_get_queue_schedule` (duplicate) | *see above* |
| `typefully_queue_put_queue_schedule` (duplicate) | *see above* |

**Typical workflow example**:
1. `typefully_get_me` – confirm authentication.
2. `typefully_list_social_sets` – choose a social set.
3. `typefully_create_draft` – draft a post.
4. Optionally upload media with `typefully_create_media_upload` then `typefully_get_media_status`.
5. Publish via the relevant queue tools.

Refer to the official Typefully API docs for parameter details: https://typefully.com/api
