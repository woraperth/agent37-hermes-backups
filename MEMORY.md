User's second brain is the Obsidian vault cloned at ~/ICloud-vault (GitHub https://github.com/woraperth/ICloud-vault), synced by cron sync-icloud-vault (30 min).
§
Relevant Obsidian notes should be automatically retrieved when mentioned.
§
Always express dates/times in the Australia/Sydney timezone (UTC+10/UTC+11). The system clock is likely UTC — convert when displaying or reasoning about times.
§
Akiflow uses Perth's local day (Perth UTC+8), not the container's UTC day.
§
Discord home guild: Perth Hermes (1537787895136649298); daily briefing channel 1537826281142484992.
§
For read-only access to a user's private GitHub repo (syncing a second brain, fetching data), user's preferred method is a repo-scoped DEPLOY KEY (read-only, single repo) — NOT a full-account PAT. Generate key, user pastes pubkey under repo Settings→Deploy keys with write access unchecked; push back or revert if I suggest PAT as the default.
§
Nat profile: 165cm/44kg, pilates weekly, 7-8k steps/day, cooks daily. Nat communicates in Thai and wants financial answers shown in BOTH AUD and ฿ using ~฿23.40/AUD (or net-worth ฿ figures she provides). For her 'own money', exclude family accounts (Salary&Emergencies, Credit Card, Travel, Utility, Household) AND Perth's. Family home is in Chatswood, Sydney.
§
'Sunday Inputs digest' cron (050b8aeec814, Sun 8am Sydney → Discord 1538108392940376155) = no_agent script ~/.hermes/scripts/sunday_inputs_digest.py, scans ~/ICloud-vault/Projects/Inputs, uses note `processed: true|false` (missing=false=unprocessed), outputs digest from `#` + How-to-process + Tackle-this-first. Never edits files.
§
User prefers final approved content saved in the relevant Obsidian project folder with a date in the filename, then committed and pushed to the vault GitHub repository.
§
User prefers concise, concrete explanations of Git status and uncommitted changes, naming affected files and whether changes pre-existed.