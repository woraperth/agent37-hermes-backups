# "Process your Inputs" digest — frontmatter-tracked pattern

Validated recipe (Perth, Aug 2026) for a recurring digest that tells the user which
captured notes still need action, using a per-note Obsidian frontmatter toggle
instead of folder presence.

## The stateful model
Each note in the watched folder(s) carries a frontmatter boolean:
```yaml
---
processed: false
---
```
- `processed: true` → done; hidden from the digest.
- `processed: false` → backlog; shown.
- **Missing property** → treated as `false` (unprocessed), so a brand-new capture
  with no frontmatter is auto-included.

Why boolean and not a string enum: in Obsidian a boolean frontmatter property
renders as a **clickable checkbox** in the Properties panel — the user just taps it
to mark something done. A `status: unprocessed|processed` enum forces typing and is
fiddly. (User explicitly requested the boolean.)

## Keep the LOGIC in a script, not an LLM (the reliable path)
An LLM cron agent given "your response must start at `#`" will still leak a
working-narration line above the heading (Perth pushed back repeatedly: "It still
has header before #"). The durable fix is **`no_agent=true` + a deterministic
script** whose stdout is the digest and is delivered verbatim:

- Cron config: `no_agent=true`, `script=<path>` (relative → `~/.hermes/scripts/`),
  keep `schedule` + `deliver` on the job. Non-empty stdout is posted verbatim;
  empty stdout = silent.
- Script reads each note's YAML `processed:` value manually; skips
  `processed: true`; treats missing/`false` as unprocessed.
- Classify with simple keyword rules (`CONTENT_HINTS`/`ARCHIVE_HINTS` arrays)
  instead of a model — enough to group into Keep / Turn-into-content / Archive.
- **Never mutate** — the script must not change `processed` or move/delete notes.
- Scan only the target folders; skip index/attachment/image files
  (e.g. `Books.md`, `CleanShot*`, `.space/`).
- See `scripts/sunday_inputs_digest.py` (the working no_agent script) for a
  copyable template.

### frontmatter parsing pitfalls (the script will hit these)
- The closing `---` may have no trailing newline — Obsidian/make.md files often
  end the block inline (`finished?\n---![[image.png]]`). Match
  `^---\s*\n(.*?)\n---` (DOTALL), NOT `\n---\s*\n`.
- Take the body from `text[match.end():]`, not `text.splitlines()[:N]` — slicing
  the raw text keeps YAML keys, so summaries come back as `processed: false`.

## Output shape (Perth's final preference)
Start DIRECTLY at the `#` heading, then groups of single-line items:
`📌 Keep / process it` · `✨ Turn into content` · `📦 Archive it` (omit empty
groups). **Keep the two closing sections** — Perth explicitly wanted them back:
- `**How to process:**` — reminder to flip the `processed` toggle in Obsidian.
- `**Tackle this first:**` — the one highest-value item to do now.

What is stripped is the *opening* preamble: no framing sentence, no "here's the
digest", no narration above the `#`. Nothing after the closing sections either.
Perth's flow: act on an item → tick `processed` in Obsidian → it vanishes next run.

## Backfill on setup
When first converting existing notes, inspect what's already finished:
- If a note already carries a done-flag (e.g. `Finished?: true` on books), set
  `processed: true` so it won't clutter the first digest.
- Mark the real backlog `processed: false`.
- Add/rewrite the frontmatter line in-place per note, preserving all other
  properties (sticker, dates, speakers, banners). For a note with no frontmatter,
  prepend a minimal block.
- Migrating a prior string enum: `status: <v>` → `processed: true|false`
  (done→true, else→false). Use a targeted line rewrite, not a full-file edit.

## Delivery
- `deliver='discord:<channel_id>'` (not thread) once the user designates a dedicated
  home channel for the digest.
- Sydney timezone: for a Sunday-morning Sydney digest use `0 22 * * 6` (Sat 22:00 UTC
  = Sun 08:00 UTC+10). Always verify with `TZ=Australia/Sydney date`.

## Verification before declaring done
Trigger `cronjob action=run` and confirm:
1. The delivered post starts at `#` with no framing line above it.
2. It ends after the "Tackle this first" line — nothing after.
3. Only `processed: false` items listed; finished notes absent.
4. The script runs clean standalone (`python3 <script>`) before trusting the cron.
