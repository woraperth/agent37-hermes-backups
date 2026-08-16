---
name: akiflow-weekend-schedule
description: Fetch and summarise a user's Akiflow schedule (weekend, daily, or tasks), optionally enriched with Obsidian second-brain context per task.
category: productivity
trigger: "When the user asks for their schedule from Akiflow — weekend, today/daily, or a list of tasks."
summary: "Retrieve Akiflow events and/or tasks for a date range and present a concise bullet list. For task-oriented requests, enrich each task with context pulled from the Obsidian second-brain vault."
---
## Overview
Provides a concise, repeatable workflow for retrieving a user's Akiflow schedule — weekend *events*, or daily/task-oriented views — respecting the user's preference for brevity and avoiding unnecessary `tool_describe` calls. Task-oriented requests can be enriched with Obsidian second-brain context (see the daily/task section below).

## Steps (events / weekend)
1. **Determine upcoming weekend dates**
   - Compute the next Saturday and Sunday in `YYYY-MM-DD` format based on the current date (use the current weekend if today is Saturday or Sunday).
2. **Call the Akiflow schedule tool**
   ```json
   {
     "name": "mcp__akiflow__get_schedule",
     "arguments": {
       "start_date": "<Saturday>",
       "end_date": "<Sunday>",
       "entities": "events",
       "sort": "startTime",
       "filters": {}
     }
   }
   ```
   - Request only `events` to keep output focused.
3. **Summarise the events**
   - List each event with its start time, title, and any guests.
   - Group by day (Saturday then Sunday).
4. **Present the summary**
   - Use a short bullet list.
   - Omit extra explanations unless the user explicitly asks for details.

## Steps (daily / task-oriented, with second-brain enrichment)
When the user asks for *today's* schedule or for *tasks* (not just calendar events), and especially when they ask you to pull related notes for each task:
1. **Call `get_schedule` with `entities: "all"`** (returned JSON has `structuredContent.tasks` listing each task with title, description, datetime, duration, priority, project_name, and `is_overdue`). Today's date from `date "+%Y-%m-%d"`.
2. **Map each task to its Obsidian vault project** — the task's `project_name` (e.g. "DataTH Courses", "Tech Cafe", "Life Routines") usually has a matching folder under `~/ICloud-vault/Projects/`. Search that folder for the course/project notes.
3. **Search the vault for task-specific keywords** — course name (e.g. "Vibe"), platform ("BigMarker"), product ("R2GAI"/"bundle"), topic ("grok"). Use `search_files` (case-insensitive regex like `(?i)bigmarker`) since exact-case matches often miss. Diary entries (`Diary/YYYY-MM-DD.md`) and project bulletins are the richest source.
4. **Read the 1–2 most relevant notes** before writing the summary so the context is grounded, not guessed.
5. **For each task, deliver a consistent 4-part card:** (for posted/daily briefings see the *Scheduled daily briefing* section — context is RICH multi-sentence, workout/habit tasks are bare lines)
   - 📌 **Rich context, 2–4 sentences** (Perth's explicit preference — see below: wants a LOT of second-brain context to think with, not 1 clause)
   - 💻 **laptop vs 📱 mobile** (based on whether it needs editing/spreadsheets/sales-page work vs drafting/posting)
   - 📋 **steps to accomplish** (lift the numbered checklist from the task description + vault run-sheet)
   - ▶️ **1 action to start now** (the smallest concrete first step)

## "What's still left today?" (current-status / "just finished dinner" pattern)
When the user asks *"what's on my schedule / what's left tonight / any unfinished items"* AFTER the day has started (mid-afternoon, dinnertime, evening) — NOT a fresh full-day summary — the useful answer is a **status split by current local time**, not a replay of the whole day:
1. **Resolve the current Sydney time** with `TZ=Australia/Sydney date "+%H:%M %A %Y-%m-%d"`. This is the dividing line for "left tonight."
2. **Re-pull the day with `filters: {exclude_all_day: false}` AND `completed_mode: "with_completed"`** — the default (omitted `completed_mode`) hides items already marked done, but here you NEED the done set to tell the user "you already cleared X, Y, Z — good progress." Read `done`/`done_at` on each task.
3. **Split into three buckets** in the reply: ✅ **done** (items already finished — briefly acknowledge these so the user sees they're NOT outstanding), 🔶 **overdue** (`is_overdue: true` — planned earlier, not done; flag HIGH ones), and 📋 **upcoming** (`datetime` > current time). Note any items whose `datetime` has passed but are NOT flagged overdue (slipped/backlog).
4. **Anchor on the heavy item first.** A 3-hour block that should've started earlier (e.g. Vibe Code slides 19:00) realistically eats the rest of the evening — tell the user what's genuinely feasible vs what silently won't fit, and offer to re-order in Akiflow or open time slots if the tail collides. Small overdue items (30m) are quick wins to clear first UNLESS they're genuinely blocked (e.g. "waiting for SV Support") — offer to skip those.


## Scheduled daily briefing (cron / posting form)
Perth runs this as a **daily 7am Sydney cron job** delivered into Discord (#dev). Format preference from a real correction: the briefing posted flat was too long — they want it **thread-shaped and summary-led**.
- **Sydney "today"** — container is UTC; compute the day with `TZ=Australia/Sydney date "+%Y-%m-%d %A"` and use THAT as the query date (not the UTC `date`, which is the prior day). Sydney = AEST (UTC+10) in Aug–Sep, AEDT (UTC+11) in Oct–Mar daylight-saving.
- **Cron schedule** — 7am Sydney = `0 21 * * *` UTC under AEST. Keep it UTC-anchored rather than locale-cron so daylight-saving correctness is handled at the TzLookup layer.
- **Cron delivery constraint (hard)** — Hermes cron posts **ONE final message per run**; a job cannot natively fire a separate "thread OP" + "N thread replies". Practical pattern to keep the channel clean:
  - Set `attach_to_session=true` on the cron job → each run opens a **dedicated thread** in the target channel and seeds the brief into it.
  - Structuring the final response so **line 1 = the short thread-open post** — `🗓️ <Day> <Date> <Year> Sydney — <one-sentence day summary>` (no cards) — then a blank line, then the full per-task cards. The thread's top is then the scannable summary. (Preference evolved during the session: the date is now a **big header** — `# 🗓️ <Day> <Date> <Year> Sydney` on line 1, emitted EXACTLY once — and every day's message ends with a blank line + a `──────────────` full-width-dash separator so consecutive daily posts are visually walled off from each other.)
  - True **OP + separate numbered replies** inside the thread can't be emitted by the single cron message; driving Discord via Composio (OAuth) is the fallback if that fidelity is a hard requirement.
- **Discord 2000-char message limit (hard, caused a real dropped card).** A single Discord message over ~2000 chars is truncated/mangled and content silently disappears — in one run a 🏋️ early-morning task card was dropped from what the user saw even though it was in the model output, purely because the full briefing ran ~3,800 chars. The ENTIRE briefing must stay under ~1950 chars. Use a **compact per-task block**: `📌 <rich context>` + a single `💻 Laptop · 📋 short steps · ▶️ start-now` line (not 4 separate sub-bullets), and **merge recurring slots** (e.g. 3× Book CH8 → one block, noting the times inline) rather than listing each. **Context is the priority** (Perth wants RICH multi-sentence context to think with — see the rich-context rule in `references/daily-discord-briefing.md`); keep the day-summary and 📋 steps minimal to spend the ~1950 chars on context. Never treat "the model wrote it" as "it was delivered" — re-read the run's output file to confirm each card and the total length.
- **Cron delivery header/footer** — Hermes prepends a `Cronjob Response: <name> (job_id: ...)` block to every cron delivery; Perth wanted it gone. Set **`cron.wrap_response: false`** (`hermes config set cron.wrap_response false`). Global setting, harmless to `deliver:local` jobs.
- **Workout / habit tasks: NO card at all (explicit user rule, refined twice).** Perth said to skip the whole 📌 Context / 📱 · 📋 · ▶️ block for workout tasks, then clarified: *"no context, device, steps, start now thing. But for other non-workout tasks, I still want to see it."* So workout (🏋️), Daily Shutdown (🌙), and similar simple GOAL/habit items render as a **bare line with ONLY the name + time — nothing else** (no `· mobile, just go`, no device tag, no description): e.g. `**🏋️ Workout** · 09:00` and `**🌙 Daily Shutdown** · 23:15`. Do NOT inflate them, and do NOT append any "· mobile…" tag. Full 4-part cards remain for ALL other (non-workout) tasks — that contrast is the point.
- **Strip agent commentary from the delivered message (hard rule)** — the model frequently wraps its cron output in process narration that gets POSTED verbatim (e.g. "I have all the data I need… now let me write the final briefing… that's the full briefing", and even a char-count self-check "The briefing is complete, verified at N characters…"). The cron delivery is the model's final text as-is. The job prompt MUST state: *the entire final response is what the user reads — no preamble, no process notes, no trailing "that's all" commentary; output only the briefing*. Plain "no meta-commentary" STILL leaked one run, so upgrade to a byte-level guardrail: **the very first character of output must be the `#` of the `# 🗓️ …` date header** — never a do-what-I-did checklist or a verification/char-count line (see `references/daily-discord-briefing.md`). Recheck the last run's output file (`~/.hermes/cron/output/<jobid>/<ts>.md`) for framing lines around the real briefing before trusting a delivery.
- **Composio Discord gotcha (for real OP + replies)** — the `discord` toolkit (user's personal account) only exposes read tools (`DISCORD_LIST_MY_GUILDS`, etc.). The posting/thread tools (`DISCORDBOT_CREATE_MESSAGE`, `DISCORDBOT_CREATE_THREAD`, `DISCORDBOT_LIST_GUILD_CHANNELS`) live in the separate **`discordbot` toolkit**, which requires a Discord **bot token** connection — a user account connection will NOT enable writes. If a user says they "installed a Discord Composio integration" but only a personal-account connection is active, they still need the bot-toolkit auth link. The Perth Hermes guild id is `1537787895136649298`; #dev channel is `1537826281142484992`.

## Capability boundary before recommending "remote prep"
When the user is away from home and asks what can be prepared, do not equate a task being intellectually preparable with being operationally actionable. First check whether the task requires access to a specific external system or website (e.g. tax portals, brokerage websites, New Zenler, course platforms, account dashboards). If the agent lacks that authenticated access, say so plainly and do not recommend the task as remotely doable.

Classify candidates:
- **Operationally blocked:** requires logging into an unavailable system or performing actions inside it. Defer until the user has access.
- **Draftable:** the agent can prepare a written draft, checklist, workflow, or decision memo using grounded vault/task context, while clearly separating preparation from the user's final publish/execute step.
- **Fully actionable:** the agent has the required tool and authenticated access; only call this remotely doable after verifying access.

For course migration tasks, access to notes or a migration checklist is not a substitute for New Zenler access. Do not claim to prepare the migration itself; at most, offer a checklist or draft instructions and label the platform execution as user-owned.

## Scheduling tradeoffs & modifying the schedule (reschedule / delete)
When the user asks about *fitting a new time-critical block in*, or wants to *move/cancel* existing items, this is a separate workflow from summarizing (read → reason → act):
1. **Pull the full schedule** with `entities: "all"`, `start_date`/`end_date` covering the day(s) in question (use the user's local Perth/Sydney day, per the off-by-one pitfall below). Get every task's `datetime`, `duration`, `priority`, and note which are **fixed commitments** (events with guests = do NOT touch).
2. **Name the tradeoffs explicitly** before changing anything. Enumerate exactly which existing blocks collide with the new block, labelling each with its priority and, where relevant, that it's a standing GOAL/habit item (e.g. a weekly workout). Flag what survives untouched so the user sees the full picture, and call out any event with guests as untouchable.
3. **Let the user decide the sacrifice** — don't unilaterally drop a GOAL-priority routine. Recommend folding it to an open slot (e.g. same block later in the week) and confirm before mutating. The user's standing Weekly Planning treats weekly exercise as non-negotiable, so a GOAL workout is usually the *hardest* tradeoff, not the first to cut.
4. **Reschedule** with `mcp__akiflow__edit_task` (`task_id` + `start_datetime` in user-local `YYYY-MM-DDTHH:MM:SS`; keep `duration` and let priority/status persist — moving a planned task to a day keeps GOAL/HIGH). Verify the returned `status: planned for …` reflects the new slot and that the destination day has room.
5. **Delete conflicting low-priority items** with `mcp__akiflow__delete_task` (`task_id`) — it moves to trash (recoverable), not a hard delete. Use this for lower-priority work that collides and can wait, **never** for a guest-marked event.
6. **Create a NEW planned task to claim the freed window** — after moving the old occupant out, don't just narrate the freed time: book it explicitly with `mcp__akiflow__create_task` (`status: "planned"`, `start_datetime` `YYYY-MM-DDTHH:MM:SS`, `duration`, plus `priority: "HIGH"` and `project_id` so it's protected & lands in the right bucket). Example: `Vibe Code - Finish slide creation (arvo catch-up)`. Pull the `project_id` from `mcp__akiflow__list_projects` (match by the project that already hosts the related work, e.g. the vibe-coding email task lives under `DataTH Courses`). The user benefits from seeing a real named block in the calendar, not just silence where the moved task used to be.
7. **Resolve any collision your own move creates** — before settling on where a HIGH task lands, check that the destination doesn't overlap a *different* task. If it does, nudge the lighter/sibling item to an adjacent open slot (e.g. move a 30-min admin Retro from 21:30 up to 16:30) rather than letting your move double-book the evening. Verify the final day by re-reading `get_schedule` end-to-end.
8. **Displacing a task to ANOTHER day: read the receiving day's FULL schedule first.** When the user wants several tasks moved "to the evening" and that evening is already back-to-back, the clean move is to relocate the *lowest-priority removable* task (non-HIGH, no deadline, catch-up "todos" work) to a gap on a different day — but never guess there's room. Call `get_schedule` on the target day (both entities) and pick an actual verified gap (e.g. Tech Cafe todos → tomorrow 11:00, confirmed clear between 10:00 Triage and 12:30 Prep). Parking it on a timestamp you assumed was free double-books whichever task already owns it.
9. **Merging a multi-slot task series** — when the user decides two slots of one task (e.g. "slot 2/3" + "slot 3/3") should be combined into a single occurrence: `delete_task` the redundant slot AND `edit_task` the survivor's `title` to drop the now-stale "slot N/M" suffix (e.g. → `DataTH Book CH 8 - Act on Diff`). Leaving the label on a sole remaining slot reads wrong. Deleting a slot of a series never touches its siblings.

Pitfalls: only change items the user explicitly points at ("this one"); when a task is one slot of a multi-slot series (e.g. "slot 1/3"), deleting just that slot is fine and leaves the rest intact — and if the user later consolidates the series into one block, also rename the survivor to drop the slot label (see step 9). A 3-hr block ending at **noon** means the window overlaps 09:00–12:00 — check every morning task against it, and confirm the user is okay removing anything still sitting there before/after the reschedule. Note the user may iterate several times before settling ("move this too", "keep X at its slot", "merge these") — expect re-reads and re-confirms rather than one-shot acceptance.

## Pitfalls for enrichment
- Enrichment is **grounded** — always read the referenced note(s) before asserting what a task means; never invent project context you didn't find.
- Don't grind through every vault file — target folder + keyword search first, then read 1–2 notes per task.
- Treat `is_overdue` as signal the user will want to prioritize; flag overdue HIGH tasks.
- Note the cached vault is at `~/ICloud-vault` (git-repo clone synced by cron), not the default `~/Documents/Obsidian Vault` — resolve the path before searching.

## Pitfalls & Tips
- **Date format** – Akiflow expects `YYYY-MM-DD` (zero‑padded).
- **Perth "today" off‑by‑one** – The container `date "+%Y-%m-%d"` resolves to **UTC**, which is the *previous* day relative to Perth's local day. **Perth lives in Sydney** (Australia, not US — he corrected the old "NYC/P lower-case C" profile to Sydney on 2026-08-15), so his local tz is **AEST (UTC+10)** in Aug–Sep / **AEDT (UTC+11)** in Oct–Mar daylight-saving. Compute his local day with `TZ=Australia/Sydney date "+%Y-%m-%d %A"` and use THAT as the Akiflow query date and for the diary (e.g. `Diary/<Sydney-date>.md`) — not the container UTC date nor the older Perth=UTC+8 assumption. When the user says "today (Saturday)" but `date` prints Friday, trust the **user's local Sydney day**. Sydney vs the container can differ by up to two calendar positions during AEDT; always resolve via `TZ=Australia/Sydney date`, never assume.
- **Timezone** – Dates are interpreted in the user's local timezone; no offset needed.
- **Filtering** – To show only events with guests, set `filters.with_guests_only` to `true`.
- **Avoid redundant `tool_describe`** – Assume the tool schema is known; call the tool directly.
- **Verify tool output** – After calling `mcp__akiflow__get_schedule`, check that the response contains events. If the list is empty, reply that there are no scheduled items for the weekend instead of fabricating placeholder data.

## User Preference Embedding
- Keep responses concise; avoid verbose step‑by‑step explanations unless requested.
- Do not repeat the tool description.
- For posted/scheduled briefings: **short first, detail after** — lead with `# 🗓️ date + one-sentence day summary` (big Discord header), then the cards, and end with a `──────────────` separator. One long flat wall of text was explicitly flagged as "too long" (see *Scheduled daily briefing* above).
- **Workout/habit tasks stay frictionless** — Perth wants them as BARE lines with only the name + time (`**🏋️ Workout** · 09:00`, `**🌙 Daily Shutdown** · 23:15`), never a card and never a device tag. Full cards are only for non-workout tasks. See the explicit rule under *Scheduled daily briefing*.
- **Context depth matters more than brevity** — Perth asked for *"a lot of context from second brain if available, so I can think about what to do to get it done"*. The 📌 context line should be 2–4 sentences of concrete second-brain detail (current state, blockers, prices/amounts, names, dates, links, what was decided), not a sparse clause. When the char budget tightens, cut the summary/steps first — keep the context rich.

## References
- [Akiflow schedule notes](references/akiflow_schedule_notes.md)
- `references/akiflow_schedule_notes.md` – notes on earlier over‑use of `tool_describe` and best practices.
- `references/akiflow_task_vault_map.md` – Perth's Akiflow project → Obsidian vault folder map + per-topic quick-grep terms (Vibe course, Discord access, BigMarker, R2GAI bundle, grok posts).
- `references/daily-discord-briefing.md` – the daily 7am Sydney Discord cron run: job id/schedule, ONE-message delivery model, 2000-char cap, big `# ` date header, bare-line workouts vs full cards, `──────────────` day separator, and the exact compact-card format.
