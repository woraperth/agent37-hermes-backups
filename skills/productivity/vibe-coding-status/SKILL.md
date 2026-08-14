---
name: vibe-coding-status
description: Summarize Vibe Coding course status from Obsidian.
trigger: "User asks for current status of the Vibe Coding course or any progress update."
---
# Overview
Provides a concise, structured status report for the Vibe Coding course by aggregating information from the Obsidian vault (notes, project files, diary entries).

## Steps
1. **Locate core files** in `~/ICloud-vault/Projects/DataTH - Vibe Coding 26/`:
   - `Course-Info.md` – course definition, pricing, audience.
   - `Launch-Live.md` – launch‑day live event script and checklist.
   - `Day1-Curriculum.md` / `Day2-Curriculum.md` – curriculum details.
   - `Diary/` entries for recent actions (promotion, prep sync).
2. **Extract key sections**:
   - Title, tagline, instructor bios.
   - Schedule dates/times.
   - Pricing tiers & active promos.
   - Launch‑day live event date, run‑of‑show outline, promotion checklist.
   - Recent marketing actions from diary.
3. **Assemble a status table** with columns: Area, What’s ready/decided, Recent actions, Next steps.
4. **Add pending items** noted in diary or TODOs in the launch script.
5. **Return the report** formatted in markdown for easy copy‑paste into Slack/Discord or Obsidian.

## Pitfalls & Tips
- Verify the vault path `~/ICloud-vault` is correct.
- Files may contain Thai characters; keep UTF‑8 encoding.
- Dates are in Thai timezone – mention the timezone.
- If a referenced file is missing, fall back to the most recent diary entry.

## References
- `references/vibe-coding-status-notes.md` – session‑specific excerpts used to build the report.
