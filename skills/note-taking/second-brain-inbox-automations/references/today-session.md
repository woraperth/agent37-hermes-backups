# Session reference: Sunday Inputs digest (Perth's vault)

Working details from the session that established this pattern, so future
maintenance of the same automation has exact anchors.

## Automation live (final state)

- Cron job `050b8aeec814` — "Sunday Inputs digest (keep/archive/content)".
- **Mode: `no_agent=true` + deterministic script** `sunday_inputs_digest.py`
  (in `~/hermes/scripts/`; a copy lives in the `cron-scheduling-automations` skill as
  `scripts/sunday_inputs_digest.py`). stdout is delivered verbatim → the post starts at
  `#` by construction. This was chosen AFTER the LLM-agent version kept leaking a
  narration line above the heading (Perth: "It still has header before #").
- Schedule `0 22 * * 6` UTC = **Sunday 08:00 Australia/Sydney** (UTC+10 in Aug).
- **Delivered to Discord channel `1538108392940376155`** (a dedicated channel Perth
  designated; was originally the thread `1538106787327381504`, then moved). Guild
  `1537787895136649298`.
- The script reads `processed:` frontmatter, lists only unprocessed notes, classifies
  each Keep/Archive/Turn-into-content (by keyword rules), never mutates files.

## Output shape Perth settled on
Starts directly at `# 📥 Sunday Inputs Digest — <Sydney date>`, then grouped single-line
items (`✨ Turn into content` / `📌 Keep / process it` / `📦 Archive it`, empty groups
omitted), then **KEEPS** two closing sections:
- `**How to process:**` — flip the `processed` toggle in Obsidian to mark done.
- `**Tackle this first:**` — one highest-value item.
Only the OPENING preamble is stripped (<em>no</em> framing sentence above the `#`); the
closing sections are wanted.

## Vault layout being tracked

Root: `/home/node/ICloud-vault/Projects/Inputs/`

- `Books/` — `Book - Effortless.md`, `Book - Meditation.md` (both `processed: true`;
  they already carried a legacy `Finished?: true` flag).
- `Videos/` — 8 captures, all `processed: false`:
  - 2026 Life OS by Ali Abdaal
  - 2026 Thumbnail Masterclass - AHQ Framework
  - 2026.07 AI Prompt Photographer - P How
  - 2026.07 AI video - K Panjapat - Warroom
  - 2026.07 How to Perfect Sleep 101 - Whoop Lab by Golf
  - 2026.07 Local Model - WARROOM พี่โดม พี่เอ๋อ
  - 2026.08 Vibe Coding - WARROOM - P Kaowrote
  - Matt Pocock - AI Coding Workflow
- Index files to skip: `Books.md`, `Videos.md`, `Input.md`, `Inputs.md`.
- Also skip `.space/` and `Attachments/` (incl. `CleanShot*`, `Pasted image*`).

## Notes on the migration

- Some videos had NO frontmatter initially → a fresh `---\nprocessed: false\n---`
  block was prepended.
- Some already had YAML frontmatter (e.g. `banner`, `type`, `Date`, `source`,
  `speakers`, `topic`) → `processed:` was inserted right after the opening `---`,
  leaving all existing keys intact.
- Books previously used `Finished?: true` as the "done" marker; that mapped to
  `processed: true`.
- **Parser pitfall hit while scripting it:** a closing `---` with no trailing newline
  (`---![[image.png]]`) breaks `/^---\s*\n(.*?)\n---\s*\n/`. Use
  `/^---\s*\n(.*?)\n---/` and slice the body from `match.end()`.

## History / design reasoning

- First pass used a string enum `status: unprocessed|processed`. Perth asked for the
  simpler boolean `processed: true|false` (Obsidian tick/untick in the Properties
  panel) instead — so the boolean is now the canonical convention.
- Scheduling pitfall hit: an initial `0 20 * * 0` (Sunday 20:00 UTC) would have
  delivered MONDAY 06:00 Sydney. Corrected to `0 22 * * 6` to land Sunday 8am Sydney.
