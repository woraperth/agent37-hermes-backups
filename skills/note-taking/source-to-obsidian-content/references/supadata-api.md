# SUPADATA transcript fallback

Use the REST API when the normal YouTube transcript helper is blocked or unavailable and `SUPADATA_API_KEY` is present.

## Tested native request

```bash
curl -G 'https://api.supadata.ai/v1/transcript' \
  -H "x-api-key: $SUPADATA_API_KEY" \
  --data-urlencode 'url=https://youtu.be/VIDEO_ID' \
  --data-urlencode 'lang=th' \
  --data-urlencode 'text=true' \
  --data-urlencode 'mode=native'
```

The tested video returned HTTP 200 with:

```json
{"lang":"th","availableLangs":["th"],"content":"..."}
```

Validate that `content` is non-empty before summarizing. Never print the API key or write it into a note.

## Async responses

Default/AI-generation mode can return HTTP 202:

```json
{"jobId":"..."}
```

Poll:

```bash
curl -H "x-api-key: $SUPADATA_API_KEY" \
  'https://api.supadata.ai/v1/transcript/JOB_ID'
```

Poll until `status` is `completed` or `failed`. A completed response contains transcript content; a failed response contains error details. If a job remains `active` unusually long, stop waiting and retry with `mode=native` before considering another approach.

## Relevant query parameters

- `url` — required source URL
- `lang=th` — preferred Thai transcript language
- `text=true` — plain text content
- `mode=native` — existing transcript only; avoids unnecessary AI generation
- `mode=auto` — native first, AI fallback when unavailable
- `mode=generate` — always use AI transcript generation

## Source note metadata

Record the source URL and transcript language in the Markdown note. It is usually better to store a concise summary than the full raw transcript unless the user explicitly requests the transcript itself.
