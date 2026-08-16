---
name: second-brain-inbox-automations
description: Digest unprocessed Obsidian inbox notes via a boolean flag.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Obsidian, Cron, Inbox, Digest, Frontmatter, Automation]
    related_skills: [obsidian, akiflow-weekend-schedule]
---

# Second-Brain Inbox Automations

Use when designing a recurring (cron) automation that walks an Obsidian inbox folder
(e.g. `Projects/Inputs/Books`, `Projects/Inputs/Videos`) and periodically surfaces
"unprocessed" captures for the user to keep / archive / turn into content — the classic
capture-but-never-process trap. Covers how to track per-note state and how to wire the
cron so it fires at the RIGHT local time.

## Core pattern: flag state in frontmatter, not by folder presence

Do NOT judge "unprocessed" by *presence* in the Inputs folder or by note age. A note can
sit in Inputs long after the user acted on it, and re-flagging finished notes is noise.
Instead give every inbox note an explicit boolean frontmatter property.

### Use a boolean, NOT a string enum (user preference)

Perth's vault convention: a single boolean key that renders as an Obsidian clickable
toggle in the Properties panel — no typing to maintain.

```yaml
---
processed: false   # unticked = still in backlog
---
```

- `processed: true`  → done, hidden from the digest
- `processed: false` → in backlog, listed in the digest
- property ABSENT     → treat as `false`/unprocessed (be forgiving on new/old notes)

Prefer this over a string enum like `status: unprocessed|processed`. The user explicitly
pushed back on the string enum and asked for the `processed` tick/untick boolean — encode
that preference from the start. A new note that has no `processed` line must be treated
as unprocessed, never skipped.

## Machine-auditing state

The digest reads each note's YAML `processed:` value and lists ONLY the unprocessed
ones. Running this as a plain LLM cron agent works, BUT an LLM is unreliable at
guaranteeing a clean, preamble-free delivered post ("start at `#`" gets violated by a
narration line). Perth pushed back on this repeatedly. The durable fix is a
**deterministic script** wired with `no_agent=true`, whose stdout (starting at `#`) is
delivered verbatim. A validated, copyable template lives in the cron umbrella skill:
`cron-scheduling-automations/scripts/sunday_inputs_digest.py`.

Whether LLM or script, encode this intent:
- Skip index files (`Books.md`, `Videos.md`, `Input.md`, `Inputs.md`), `.space/`, and
  `Attachments/` or image files (`CleanShot*`, `Pasted image*`).
- Read the first ~15 lines of each unprocessed note to classify it (Keep/Archive/Turn into content).
- **Never edit, move, or delete files, and never change the `processed` value** — the digest
  is a suggestion list only. The user ticks the box in Obsidian themselves.
- Tell the user HOW to mark something done: open the note's frontmatter and flip
  `processed: false` → `true`.

## Bulk frontmatter editing (preserving existing properties)

When adding the flag to many notes at once, do NOT rewrite files by hand. Use `execute_code`
with a regex over the YAML frontmatter block so existing keys survive:

- Match the frontmatter with `/^---\s*\n(.*?)\n---/s` (DOTALL). **Do NOT force
  `\s*\n` after the closing `---`** — Obsidian/make.md files often end the block inline
  (`finished?\n---![[image.png]]`) with no trailing newline, which breaks the stricter
  pattern. Anchoring only on the opening + `\n---` close handles both cases.
- To read a note's body (for summarising), slice from `text[match.end():]` — if you
  slice `text.splitlines()[:N]` from the raw text you keep the YAML keys, so summaries
  come back as `processed: false` instead of real content.
- If the note already has a frontmatter block, insert `processed: <val>` right after the
  opening `---` (prepend to the block body) — do not touch other keys.
- If the note has NO frontmatter, prepend a fresh block `---\nprocessed: <val>\n---\n`.
- Convert legacy tags when migrating map cleanly (e.g. an old `Finished?: true` → `processed: true`).
- After the bulk edit, `head` a couple of files to verify the frontmatter parses correctly.

## Scheduling the cron for the user's timezone (critical)

The cron engine runs on UTC. To land a job on a specific LOCAL day/time you must compute
the UTC offset yourself — a naive local-looking cron string silently fires a day off.

Example: a Sunday-morning digest in Australia/Sydney (UTC+10 in Aug). "Sunday 8am Sydney"
= Saturday 22:00 UTC → cron `0 22 * * 6`. A first guess of `0 20 * * 0` (Sunday 20:00 UTC)
would actually land MONDAY 06:00 Sydney — wrong day. Always verify with:
`TZ=Australia/Sydney date` and mentally/re-derive the UTC offset before setting `schedule`.

Perth's rule: always think in Australia/Sydney local time; the system clock is UTC and
UTC+10 (or UTC+11 in DST).

## References

- `references/today-session.md` — working session details: Perth's Inputs layout, the exact
  notes retrofitted with `processed`, and the cron deliver target used.
