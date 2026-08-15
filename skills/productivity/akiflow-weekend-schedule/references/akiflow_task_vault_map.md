# Akiflow task → Obsidian vault mapping (Perth's workspace)

Resolved vault root: `~/ICloud-vault` (git clone, cron-synced; NOT ~/Documents/Obsidian Vault).

Current task→folder map (verified for DataTH / Tech Cafe / Vibe Coding work):

| Akiflow project_name | Vault location(s) | Notes |
|---|---|---|
| DataTH Courses / DataTH - Vibe Coding 26 | `Projects/DataTH - Vibe Coding 26/จ/ุ/` | Course run-sheets: `Day2-Curriculum.md`, `Day4-Curriculum.md`, `Launch-Live.md`, `Bundle.md`, launch/live posts |
| Tech Cafe | `Archive/Tech Cafe Weekly AI Updates/` | `Tech Cafe Overview.md`; `wiki/updates/Update N — …md`; `raw/updateN.md`; `raw/postN.md` (TG-ready post templates) |
| PTE Winner (Main Projects) | `Projects/PTE Winner Payout/` | Quarterly payout SOP + checklist |
| Life Routines | `Diary/YYYY-MM-DD.md` | Daily planner + shutdown/planning habit |
| R2DE - Bag Prize (DataTH) | `Projects/DataTH - R2DE 26 Bag Prize/main.md` | Bag giveaway: blog-to-win rule, `submitters`, cost/price wait on SV Support |
| DataTH Book / Writing | `Projects/Writing Materials/` | Full book chapter + materials ("Act on Diff" CH 8) — checklist lives in a **Claude project** (task desc says "See Claude project"), *not* the vault |
| 🏋️ Workout / 🏙️ Life | `Projects/Health.md/Health/2026/*.csv` | Per-session workout logs (2026-07-xx / 2026-08-xx) |
| R2DE course (archive)` | `Archive/DataTH - R2DE 26/` | `DataTH Overview.md`, `R2DE 2026 Live Sessions.md`, launch-sales summaries, retro sources |

## Known content by topic (quick grep terms)
- **Vibe Coding course** — run-sheets describe the "ร้านเรา" coffee-shop workshop (3 builds on one `orders` Sheet). Course prep = confirm `orders` Sheet (~400 rows, 3mo, fictional customer names) + 3 demo builds.
- **Vibe access finish** — `Projects/DataTH Dev/Discord Access Automation/README.md`: auto-grant Discord role on enrollment (Pabbly→Sheets→Cloud Function `/claim`). Open items: Pabbly integration, claim command.
- **BigMarker** — webinar/live-class platform for DataTH bonus classes; created frequently (Jan/Jun/Aug diaries). Duplicate a prior event to reuse settings.
- **R2GAI / bundle** — `Bundle.md`: standalone prices (Vibe 6,900 / GenAI Weekend 6,900 / R2GAI 10,900); bundle A=Vibe+R2GAI 14,900 (hero), B=Vibe+GW 11,900, C=All-in 19,900. R2GAI page: go.datath.com/r2gai. Access-duration differs per course (flag it).
- **Grok bot / tech cafe posts** — `raw/post17.md` + `wiki/updates/Update 17` cover SpaceXAI Grok 4.5 (trained on Cursor session data, ~5× cheaper than GPT-5.6, in Cursor + Grok Build). Weekly-update structure: เกิดอะไรขึ้น → ทำไมคุณควรสนใจ.

## Search tip
Exact-case searches often return 0; use a case-insensitive regex prefix (`(?i)term`) in `search_files` and check the case-insensitive match count before concluding "not found."
- **Multi-token patterns mislead** – `search_files` regex on phrases with spaces/digits (e.g. `CH 8`, `Act on Diff`, applied via `(?i)Act on Diff`) frequently returns `0 exact, N case-insensitive` and lists unrelated hits. When a phrase/project isn't surfacing cleanly, fall back to `rg -l -i "phrase" <folder>` in the terminal and inspect the candidate files directly; the Vault diary (`Diary/YYYY-MM-DD.md`) is the most reliable cross-check for whether a task already ran today.
