---
name: bigmarker
description: "Copy a past BigMarker episode to create a new webinar."
version: 1.0.0
author: hermes
license: MIT
metadata:
  tags: [bigmarker, webinar, conference, curl, "tech cafe"]
  related_skills: [airtable, box, notion]
---

# BigMarker REST API (manage webinar conferences)

BigMarker is the user's live-webinar platform (Tech Cafe weekly series, DataTH R2DE live sessions, Vibe Coding lives, bonus lives). All management is plain REST + an `API-KEY` header — no extra tooling.

## When to Use
- The user asks to create/schedule a new webinar on BigMarker, especially a new episode of a recurring series ("config similar to past EP.N", "create BigMarker for Tech Cafe EP.X").
- Managing an existing conference: list episodes, pull a template record, verify a just-created conference, or add presenters.

## Auth & setup
- API key lives at `/home/node/bigmarker/.env.bm` as `BIGMARKER_API_KEY=<key>`. Read it inline: `KEY=$(grep -oP 'BIGMARKER_API_KEY=\K.*' /home/node/bigmarker/.env.bm)`.
- Base URL: `https://www.bigmarker.com/api/v1`. Send header `-H "API-KEY: $KEY"`.
- **Never print the key into the chat / tool output that reaches the user.** Read it from the env file, never hardcode it in visible output.

## Core workflow — CREATE a new episode by COPYING a past one (VALIDATED)
This is the proven, reliable way to make a new series episode ("config similar to past EP.N"). Copying pulls over presenters, banner, privacy, capacity, style automatically — far better than hand-building every field.

1. **List current state** (search across the whole account, works for past+future):
   ```bash
   curl -sS -X POST "$BASE/conferences/search/" -H "API-KEY: $KEY" \
     -H "Content-Type: application/json" -d '{"title":"<SeriesName>","page":1}'
   ```
   Returns `conferences[]`, each with `id`, `title`, `start_time`, `duration`, `channel_id`, `conference_address`. Confirms numbering and that the target doesn't already exist (avoid duplicates).

2. **Pull the full template record** from the episode you're mirroring (nested under `conference`):
   ```bash
   curl -sS "$BASE/conferences/<ID>" -H "API-KEY: $KEY" > /tmp/tmpl.json
   ```
   Inspect `conference.presenters[]` (the email/name/moderator list that the copy preserves) and `purpose`.

3. **Create with `conference_copy_id` = the template's id**, overriding title / start_time / time_zone / duration_minutes / privacy / purpose. Build the payload with Python (avoids shell-escaping Thai text) and POST to `$BASE/conferences`:
   ```bash
   python3 - "$KEY" <<'PY'   # writes /tmp/create.json, prints it
   import json
   payload = {
     "channel_id": "<channel>",
     "title": "[Series] Title EP.N",
     "conference_copy_id": "<template-id>",
     "start_time": "YYYY-MM-DD 10:00",   # in the conference's TZ
     "time_zone": "Bangkok",
     "duration_minutes": 90,
     "privacy": "private",
     "purpose": "วัน-เวลา: ...\n\nหัวข้อ...",
   }
   json.dump(payload, open('/tmp/create.json','w'), ensure_ascii=False)
   print(json.dumps(payload, ensure_ascii=False))
   PY
   curl -sS -X POST "$BASE/conferences" -H "API-KEY: $KEY" \
     -H "Content-Type: application/json" -d @/tmp/create.json
   ```
   Response returns the new `id` + `conference_address` + copied settings.

4. **Verify** by GETting the new id and confirming presenters (should be copied over), start time, duration, privacy, URL:
   ```bash
   curl -sS "$BASE/conferences/<new-id>" -H "API-KEY: $KEY"
   ```

## Key API facts / pitfalls
- **Auth:** `API-KEY` header (NOT Bearer). 401 `"Missing or invalid API key."` = wrong/missing key; 403 `"You don't have access to this Channel"` = wrong channel_id for the key's account.
- **Search** (`/conferences/search/`) is a **POST**, not GET; `title` is a plain string (no wildcard needed, it's a substring match).
- **Naming/time convention in the series:** past Tech Cafe episodes all start 10:00 **Bangkok** (+07:00), 90 min, `privacy=private`, `max_attendance=1100`, `webcast_mode=required`. Copying an episode inherits all of these.
- **Time zone:** pass `time_zone` explicitly (e.g. `Bangkok`) or it defaults to US Central. `start_time` is interpreted in that TZ.
- **`purpose`** is the Thai description block; topic often "TBD" at creation and updated later.
- **Verification of presenters matters** — the headline value of copying is that presenters (Perth + co-hosts) and banner carry over; always confirm via the GET.
- **To add presenters later:** POST to `$BASE/conferences/<id>/presenters` (only needed when NOT copying an existing episode).
- Deletion/rename is easy if an episode number is wrong — creating is low-stakes and reversible.

## References
- `references/tech-cafe-series.md` — the Tech Cafe series template (channel, title pattern, presenters, sample purpose, episode history). Use for `Tech Cafe` and similar recurring live series.
