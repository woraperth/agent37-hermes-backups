# Daily 7am Discord briefing cron (Perth's Akiflow → second-brain → #dev)

Job: `1f1ccad8dac5` "Daily 7am Sydney Akiflow schedule + second brain briefing".
Fires `0 21 * * *` UTC = 7:00 Australia/Sydney (Sydney is UTC+10 Aug–Sep; DST +11 from first Sun Oct). Delivers to Discord channel `1537826281142484992` (#dev), one dedicated thread per day, via native cron `deliver:"discord:<channel_id>"` + `attach_to_session:true`. Attached skill: `akiflow-weekend-schedule`.

## Delivery model (learned the hard way)
- **Hermes cron posts ONE message per run** — the agent's final response, verbatim. It CANNOT natively post a thread OP then separate reply messages. The composio/bot-token route was abandoned by the user as "not worth it". Keep using native delivery.
- **The model's final response may leak process commentary** ("I have all the data I need… let me write… that's the full briefing"; also "The briefing is complete, verified at N characters, properly formatted with…"). Instruct it bluntly: final output = ONLY the posted briefing, no preamble/meta/trailer. The cron output file's `## Response` section is exactly what posts.
- **Hard guardrail vs commentary: the output MUST start with the `#` of the date header as character #1.** "no meta-commentary" alone was still violated once (a run led with "The briefing is complete, verified at 1968 characters…" which posted verbatim). Upgrade the instruction to a hard rule: *the very first character of your output must be the `#` of `# 🗓️ …`; never start with a checklist of what you did or a char-count / verification line.* Because `wrap_response:false` (and even the default wrapper) expose the model's own first line, any leading narration becomes the top of the post — so a byte-level first-char rule is the reliable fix.
- **Cron "response wrapping" header/footer** — by default Hermes prepends a block to every cron delivery:  `Cronjob Response: <name> (job_id: ...) ---------------------------------------------`. Perth wanted it gone. Set **`cron.wrap_response: false`** (`hermes config set cron.wrap_response false`) so the delivery is the raw briefing with no wrapper. It's global but harmless to `deliver:local` jobs.

## Discord formatting constraints
- **2000-char hard limit.** A normal 4-part card per task + 8-9 tasks blows past it and Discord truncates/drops cards. Root cause of a "missing" task card in the user's view (cards near the top were in the file but the deliverable was mangled). Enforce a hard 1950-char cap in the prompt and use a tight card format.
- **Big text** = markdown `# ` prefix on the line (no HTML headings). Date header renders as: `# 🗓️ <Day> <D> <Mon> <Year> Sydney`.

## Perth's preferred format (final, user-confirmed)
Message = one Discord message:
1. Line 1: BIG date header exactly once: `# 🗓️ Saturday 15 Aug 2026 Sydney` (no space issues after `#`).
2. Line 2: one-sentence day summary: `— <summary>`.
3. Blank line.
4. **Two categories of task, handled differently:**
   - **WORKOUT + simple habit tasks (🏋️ Workout, 🌙 Daily Shutdown): render as a BARE one-liner — ONLY the name + time, nothing else.** NO context, NO 📱/💻, NO steps, NO start-now, NO "· mobile, just go". E.g. `**🏋️ Workout** · 09:00`. The user was explicit: "no context, device, steps, start now thing".
   - **ALL other tasks: keep the FULL 4-part card** (context, device, steps, start-now), compact; flag overdue HIGH with 🚨 + missed date; merge recurring slots (3× Book CH8) into one block.
5. LAST line: blank line then `──────────────` separator, so consecutive days are visually distinct.

Compact card format (fits under the char cap):
```
**<emoji> <Task name>** · <time>
📌 <RICH multi-sentence context>
💻 Laptop · 📋 steps→short · ▶️ start-now action
```
(Mobile variants use 📱. Combine device/steps/start-now onto one line.)

### Context is the STAR (user correction — richer context over brevity)
Perth explicitly asked for MORE context: *"Make it multiple sentences if possible. I want a lot of context from second brain if available. So I can think about what to do to get it done."* So the 📌 context line is **NOT a clipped 1-clause — write 2–4 short sentences of real substance**: background/why it matters, current state + blockers, key specifics from the notes (names, amounts, prices, dates, links like vibe.datath.com), what was decided last time, and the actual open question to resolve today. Spend MOST of the ~1950-char budget here.
- To free space: keep the day-summary line and the 📋 steps line to absolute minimum (steps can be 2-3 words); the device tag stays one token.
- Ground it in the actual vault notes (READ 2-3 notes/task: run-sheets, bundle/pricing, project main.md, diary, meeting notes) and pull concrete specifics — never fabricate. If a note is thin, say only what's confident and keep short.
- Workout/habit tasks STILL get bare one-liners regardless (separate rule above).

## Recipe for the job prompt
Ground every card in the vault (search `(?i)term` in the mapped project folder + `Diary/<today-sydney>.md`, READ before writing, never invent). Exclude the standing "Week priorities" task (PTE Winner project). Compute today via `TZ=Australia/Sydney date "+%Y-%m-%d %A"` — never the plain UTC `date` (it's the prior day). Check the job's output in `~/.hermes/cron/output/<job_id>/` via the `## Response` block to verify what actually posted.
