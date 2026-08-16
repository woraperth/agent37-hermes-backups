---
name: cron-scheduling-automations
description: "Use when setting up recurring cron digests; fix timezone."
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [cron, scheduling, automation, timezone, digests, recurring]
    related_skills: [obsidian, weekly-review-planning, akiflow-weekend-schedule]
---

# Cron Scheduling for Recurring Automations

Stand up recurring Hermes cron jobs — daily/weekly briefings, watchdogs, "process your inbox" digests — and get the timing, delivery, and failure semantics right the first time. The hard parts are not the tool calls; they are timezone conversion, delivery targeting, and keeping a recurring job safe to run unattended.

## When to Use

- "Set this up to run every day / Sunday / hour."
- "Create a cron job that digests X and pings me."
- "Schedule a recurring automation based on my second brain / vault / calendar."
- Any request to build a scheduled job backed by files, an API, or a recurring workflow.

For a concrete, validated "process your Inputs/inbox" digest (frontmatter `processed` toggle, backfill on setup, heading-first output shape), see `references/inputs-digest-frontmatter-pattern.md`. A working, copyable `no_agent` digest script lives at `scripts/sunday_inputs_digest.py` — the reliable way to guarantee a preamble-free delivered message. For token-usage and API-vs-subscription reviews, use `references/usage-audit-and-cost-review.md`; it defines the cron-only scope, jq aggregation, and cost-comparison guardrails.

## Core Rules

### 1. Timezone conversion is the #1 failure mode
Hermes cron schedules run in **UTC**. If the user lives in a non-UTC timezone (e.g. Australia/Sydney, UTC+10 in summer / UTC+11 in winter), a naive weekday does NOT do what they asked.

- Always convert the user's *local* target time to UTC before writing the schedule.
- A 20:00–23:59 UTC slot crosses midnight and lands on the **next** local day. "Sunday morning Sydney" is *not* any Sunday UTC schedule — it is `Saturday 22:00 UTC` = `0 22 * * 6`.
- Verify with `TZ=Australia/Sydney date` and reason out the resulting calendar weekday before creating the job. A wrong day is a silent recurring miss, hardest to notice because the job runs "successfully" on the wrong day.
- Handle DST: Sydney flips UTC offset over the year, so re-check the offset when the season changes rather than assuming a fixed value.

### 2. Deliver to the exact destination
- For Discord threads, target `discord:<channel_id>:<thread_id>` so the recurring job lands inside the thread the user is watching, not the main channel.
- Use `deliver='local'` for silent data/sync jobs that shouldn't message anyone.
- `origin` is fine when the job's purpose is to reply in the conversation that created it.

### 3. Recurring digests must be safe to run unattended (read-only)
A digest that "proposes next actions" should:
- Read / classify / suggest, but **never mutate** source files (no moving, editing, or deleting vault notes, tasks, or records).
- Say clearly in the cron prompt that it must not write — so a future agent run can't accidentally act on its own suggestions.
- Present output that collapses tool noise: concise prose, bullets/emoji, no raw file dumps (matches how users consume Discord delivery).

### 3b. Track "processed" state with a frontmatter *boolean*, not folder presence
For a "process your inputs/inbox" digest, don't treat *presence in a folder* as "still unprocessed" — that re-flags finished notes forever. Instead put a per-note frontmatter property the user ticks:
- **Use a boolean key** (e.g. `processed: true|false`), not a string enum (`status: unprocessed|processed`). A boolean renders as a **clickable checkbox in Obsidian's Properties panel** — zero typing for the user. (User explicitly preferred this.)
- **Treat a missing property as the default** (`false` = unprocessed), so a newly captured note with no frontmatter is picked up automatically rather than silently skipped.
- The digest lists only `processed: false` and **must never** flip the property itself (read-only; the user ticks it when done).
- Backfill on setup: mark already-finished items `true`, the real backlog `false`. When migrating an existing string enum, rewrite the line in-place (`status: X` → `processed: true|false`), preserving the rest of each note's frontmatter.

### 3c. Strip the preamble from cron-delivered messages (Perth Discord style)
Perth wants recurring digest/briefing posts to start **directly at the `#` heading** with the content underneath — no framing sentence, no narration before or after. State this explicitly in the cron prompt: "final message must begin with `# <title>` and contain only the heading + grouped items; omit any group with no items; end on the last item."

**PITFALL — prompting an LLM to "start at `#`" is NOT reliable.** Even with a loud "CRITICAL OUTPUT RULE: your final response's FIRST character must be `#`", a model frequently leaks a working-narration line ("Here's the digest…", "Both books are processed…") *inside* its final response, above the heading. Perth will catch this and push back ("It still has header before #"). Do not ship an LLM-composed digest on the strength of a prompt to be clean.

**The durable fix is `no_agent=true` + a deterministic script**: write a script that computes the digest and prints it to stdout; the cron delivers stdout **verbatim**, so the first byte of the post is structurally the `#` — no model, no narration, no preamble, ever. Classify with simple keyword rules (keep / turn-into-content / archive) rather than relying on a model. This trades a bit of classification nuance for guaranteed clean output every run — the right trade once a user complains about the header.

### 3d. frontmatter regex pitfalls when scanning vault notes
When a script reads note frontmatter (to find `processed:`, classify, extract summaries):
- A closing `---` may have **no trailing newline** — Obsidian/make.md files often end the block inline (`finished?\n---![[image.png]]`). Do NOT anchor on `\n---\s*\n`; match `^---\s*\n(.*?)\n---` (DOTALL) and accept whatever follows the close.
- Extract the *body* from `text[match.end():]`, NOT `text.splitlines()[:N]` — slicing the raw text keeps the YAML keys, so summaries come back as `processed: false` instead of real content.
- Treat a missing `processed:` line as `false`/unprocessed so fresh captures are never skipped.

### 4. Scope toolsets tightly
Add `enabled_toolsets` to match exactly what the job needs (e.g. `["terminal", "file"]` for a vault-scanning digest). Shrinking the toolset cuts token overhead and reduces the blast radius of an unattended run.

### 5. Pin LLM-driven jobs against inference-config drift
Hermes protects unattended jobs from accidentally spending under a changed global provider/model. If an LLM-driven job was created with an older or implicit configuration, a later global model change can cause it to be skipped as unpinned.

- Before declaring a model change complete, read the active resolved provider and model (`hermes config get model.provider` and `hermes config get model.default`).
- For every **LLM-driven** cron job, pin that exact pair with `hermes cron edit <job_id> --provider <provider> --model <model>`.
- Do not add inference pins to `no_agent` script-only jobs; they do not call a model and should remain deterministic.
- Verify with the cron job API/tool listing, which exposes each job's `model` and `provider`. The human CLI list may show historical failures without displaying the current pin.
- Do not rerun a previously failed delivered briefing merely to test the pin unless explicitly requested; let the next scheduled run verify it without duplicate delivery or unnecessary spend.

A concise reproduction/verification note is in `references/inference-config-drift-and-cron-pinning.md`.

## Procedure

1. Confirm the **local timezone + local target time** and the desired cadence.
2. Compute the UTC cron expression from the local target (see rule 1). Dial it by hand, don't eyeball a near-match.
3. Decide the **delivery destination** — thread id, channel, or `local` (rule 2).
4. Draft a **self-contained prompt** (the job runs in a fresh session with no chat context): state the goal, the exact source paths, the read-only constraint, and the desired output shape.
5. Set `enabled_toolsets` to the minimum.
6. Create with `cronjob action=create`, then read back `next_run_at` and sanity-check the local-time interpretation before declaring it done.

## Pitfalls

- Scheduling a local-morning job on a UTC clock without shifting the weekday (the #1 silent failure).
- A digest job that mutates the very files it's supposed to only review.
- Judging "processed" by folder presence instead of an explicit frontmatter `processed: true|false` toggle (causes finished notes to be re-flagged forever).
- Using a string `status` enum instead of a boolean `processed:` key — the boolean is a one-click Obsidian checkbox; the enum forces typing.
- A cron post that starts with a framing/preamble line instead of the `#` heading, or carries trailing commentary — Perth wants the heading-first, bare-content shape.
- Delivering to a channel instead of the thread, cluttering the main chat.
- Verbose cron output that pastes raw file/API content into a chat channel.
- Forgetting the job has zero conversation context, so the prompt must fully self-describe.

## Verification

- [ ] `next_run_at` maps to the intended *local* day/time after conversion.
- [ ] Schedule survives re-creation cleanly (no off-by-one weekday on the UTC clock).
- [ ] Prompt explicitly forbids mutation if the job is a read-only digest.
- [ ] For a "process inputs" digest, per-note state is a frontmatter `processed: true|false` boolean, and the prompt treats missing as `false` (rule 3b).
- [ ] Delivered message shape verified from the output file: starts at the `#` heading, ends on the last item, no preamble/commentary (rule 3c).
- [ ] Toolsets contain no capability the job doesn't need.
