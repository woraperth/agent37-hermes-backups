---
name: family-finance-tracking
description: Track family finances from banking apps, separated by owner.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [finance, obsidian, accounting, screenshots, currency, ocr]
---

# Family Finance Tracking (screenshots → Obsidian vault)

Track a household's accounts from financial-app screenshots, keeping every account
attributed to its owner. Recurring task (users keep sending more account screenshots).

## When to Use
User sends financial-app screenshots (AMP banking, Revolut, CommSec Pocket, Betashares,
UniSuper, etc.) and wants balances recorded, accounts classified/separated by owner,
currency-converted, or family-finance stability assessed. Recurring: the user keeps sending
more accounts over time. Data is stored in an Obsidian vault (`Family Finances/`).

## Workflow
1. **OCR the screenshots** — model usually lacks vision, so `vision_analyze` fails with
   "This model does not support image inputs". Do NOT loop it. Load `image-ocr-tesseract`
   skill and OCR locally with tesseract: `tesseract <img>.png stdout -l eng --psm 6`.
   - For banking/investment app UI use `--psm 6` (uniform block) or `--psm 4`; try both
     if output is jumbled. Cross-check ambiguous digits by re-running with another PSM.
2. **Classify by owner** per the user's rule: named accounts go to that person
   (Nat/Perth), **unlabelled accounts belong to the family (ครอบครัว)**. Tag each row with
   an owner emoji (👤 Nat / 👤 Perth / 👪 ครอบครัว).
3. **Reconcile before trusting** — this is the critical step. Sum the per-owner/account
   figures in code and check against the app's stated subtotals (e.g. current value =
   sum of holdings; contributed + unrealised gain = current value). Flag mismatches rather
   than trusting raw OCR digits (1↔l, 0↔O, .↔,). CommSec-style apps even show the
   reconciliation explicitly.
4. **Store in the vault** at `<vault>/Family Finances/`:
   - Update the **README.md** overview table (per-owner rows + per-account tables).
   - Write a **snapshot** `Snapshots/YYYY-MM-DD[-account-label].md` per new data batch.
   - Withholding own totals: keep **ใช้ได้ทันที (accessible)** vs **เกษียณ (super)**
     separate; mortgage balance is listed with the family row.
   - `git add -A && git commit && git push origin` (vault is a git repo with deploy-key remote).
5. **Currency conversion** (e.g. AUD→THB): fetch a rate from `open.er-api.com/v6/latest/AUD`
   (rates.THB) and cross-check with a second source if possible. Compute per-line and total.
   State the rate + date used and that figures move with the rate.

## Pitfalls
- **Digit fidelity is the weak point.** Always recompute totals from transcribed figures and
  reconcile against cross-referenced values before acting or storing.
- **Be honest about contradictions** when analyzing stability. If the contracted mortgage
  payment (weekly×52) exceeds stated household income, that's likely an OCR over-read or the
  figure includes aggressive extra repays — say so and ask for the real "Contracted payment"
  rather than presenting an alarming conclusion as fact.
- **Superannuation** is retirement money (`เงินเกษียณ`), not liquid savings — present it as a
  separate bucket, never lump it with spendable cash.
- **Snapshot filenames**: keep `YYYY-MM-DD.md` for the main day snapshot; use
  `-revolut.md`, `-commsec-pocket.md`, `-betashares.md`, `-unisuper.md` suffixes for
  per-account snapshots on the same date.

## Support files
- `references/account-conventions.md` — per-platform parsing conventions (AMP, Revolut,
  CommSec Pocket, Betashares, UniSuper) and the owner-classification rule.
