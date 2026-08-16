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

## Stability / borrowing analysis (DTI, servicing, CGT)
When asked "is our situation stable" / "can we service this loan" / "will we drown in debt":
- **Compute, don't hand-wave**, in code. For an AUD P&I loan, derive the REAL minimum weekly
  payment — not the posted repayment if it is an intentional overpayment (tax strategy). Formula:
  `P·r/(1−(1+r)^−n)` weekly, where `r = annual_rate/52`, `n = years·52`. The posted weekly
  payment × 52 can wildly exceed income while the true instalment is very affordable.
- Quote these metrics: **DTI** (total debt ÷ gross annual income), **servicing ratio**
  (annual repayments ÷ qualifying income), and **cash remaining** after repayments.
  Comfortable = servicing ≤ ~30–38%; a mortgage DTI up to ~4–6x is normal. Include projected
  rental income for an investment property (bank counts ~80% of rent as income, which lowers
  the ratio).
- **Rental-coverage check**: rent/week ÷ mortgage/week. Example validated this session: a
  $614K Sydney 1BR renting ~$600/wk covers ~72–81% of a 25-yr instalment at 6.14% (LVR 80–90%),
  leaving a shortfall of ~$139–232/wk which is partly principal + tax-deductible (negative
  gearing). Present the shortfall honestly as a normal holding cost, not a red flag.
- **CGT on selling shares** (AU): remind that selling 12-mo+ holdings gets the 50% CGT
  discount, use tax-loss harvesting (sell losers first), and spread sales across financial years.
  **Prefer spending from offset/redraw cash before selling shares** — avoids triggering CGT
  entirely. Order of funds: offset cash → redraw → sell losing shares → sell >12-mo shares.
- **Demographics matter**: e.g. ages 35/36, no kids, both fully employed → strong
  "prime earning" position; flag the forward risk (future kids) but don't over-alarm.

## Committed / recurring expense analysis (insurance + fixed support)
Distinct consultative task from OCR tracking: the user LISTS committed annual costs (not
screenshots) and asks how to handle them — typically anxious that a premium "ประกันเลิกไม่ได้
จ่ายมานานแล้ว, can't stop, paid for years". Don't just total them; **reframe by whether the
money is truly spent or holds value**:
- **จ่ายทิ้ง (sunk outflow)** — pure cost, no cash value returned: term/major-medical health
  insurance, monthly support to family (e.g. mother's living costs ฿15,000/mo).
- **สะสม / คุ้มครอง (value-holding)** — the premium is effectively forced savings + protection
  that returns money or pays a guaranteed lump sum: critical-illness and endowment/savings
  policies that accumulate to a stated age (e.g. age 50, guaranteed ฿4M payout on claim).
- Present the split explicitly: "เทียบรายได้ได้สบาย / only ~X% of total is really spent". For
  Nat the true annual outflow is the sunk bucket (health + support), NOT the full total — the
  savings-type premiums are her own money locked up plus protection.
- Normalize to a monthly blended figure (฿/year ÷ 12) so she can relate it to income and to the
  withdrawable Thai fund.
- Identify the **largest single driver** (usually recurring support, e.g. 72% of the total) —
  that is what drains liquid Thai cash (her ฿200K ran ~13 months), not the small insurance
  premiums. Recommend a separate "ใครงบ/แม่งบ" budget bucket and phased plan rather than
  touching the savings-type policies.

## Additional-property purchase and rental-yield analysis
When the user asks how much to borrow for a second/investment property:
1. Clarify or state the assumption that the quoted amount is the **purchase price**, not the loan amount. If rent is quoted weekly, annualise it as `weekly_rent × 52`; show gross yield as `annual_rent ÷ purchase_price`.
2. Do not treat gross rent as spendable cash. Stress-test at least 50 rental weeks/year and subtract a clearly labelled allowance for strata/body corporate, council/water, landlord insurance, property management, maintenance, vacancy, and possible special levies. Apartment strata and special-levy risk should be highlighted.
3. Compare multiple LVRs (usually 50%, 60%, 70%) and interest-rate scenarios (base around the current investor rate and a higher stress rate). For interest-only screening, annual interest is `loan × rate`; say explicitly that principal-and-interest repayments will produce worse cash flow.
4. Present the result as pre-tax cash flow, not guaranteed profit. Mention that tax treatment/negative gearing and depreciation need an Australian tax adviser; lender serviceability is separate from actual cash flow.
5. Include upfront acquisition costs: NSW transfer duty, conveyancing/inspection/loan costs, and a repair/special-levy buffer. Do not imply that offset cash is free: withdrawing from an offset may increase interest on the existing home loan and may have tax/security implications.
6. Give a cautious recommendation range rather than a precise approval claim. For a $600K apartment renting at $600/week (5.2% gross yield), a 50–60% LVR is the sensible initial comparison; do not recommend 70–80% without actual strata, existing-debt, serviceability, and buffer data. Ask for those figures before finalising.
7. Quote sources for current rate and NSW duty when browsing is available, and label all numerical assumptions/date. Use code for arithmetic and reconcile totals.

## Pitfalls
- **Do NOT assume currency.** A user may quote different figures in different currencies on
  the same day: bank/investment apps in AUD (AMP, Revolut, CommSec, Betashares, UniSuper), but
  a *computed* summary (net worth by owner, an Excel-style table) may be in THB. Twice this
  session a net-worth table was first mis-recorded as AUD when it was actually THB — always
  confirm/label the currency unit (฿ vs $ / AUD) explicitly in stored tables and in the reply,
  and when there's any doubt (a round integer like `8,995,330` with no `$`/`A$` suffix), ask
  rather than assume. Patch the vault immediately if you get it wrong.
- **Income, super, and net-worth figures also get stored per-owner.** Beyond account balances,
  a user may provide: annual income per person, superannuation per person, and a year-by-year
  net-worth table. Record all of these attributed to the owner, in the same README + snapshot
  pattern. A full-house net worth "without debt" ≈ sum of the per-owner rows, and it can far
  exceed the AMP account-list total because it aggregates off-system assets (property, external
  deposits). Present that distinction honestly.
- **Digit fidelity is the weak point.** Always recompute totals from transcribed figures and
  reconcile against cross-referenced values before acting or storing.
- **Second / additional properties are assets, not liabilities until a loan closes.** A
  property "not yet mortgaged" (e.g. a family 1BR condo at A$614,000 with a 0.9% deposit
  paid = $5,526) records at FULL value on the asset side, with no debt. Record owner +
  property type explicitly and ask if it's the user's personal or family-owned — a "Nat's
  house" label was once corrected to family. Distinguish it from the current residence
  (the one whose mortgage shows in AMP).\n- **Net-worth accounting** (user asks how a remaining mortgage fits in): `Net worth =
  total assets − total debts`. Include the home's FULL value as an asset and the FULL
  remaining mortgage as a liability — never count the home twice and never offset it as a
  partial. Two scenarios differ by whether the quoted "without debt" total already includes
  the home's full value: (A) if yes → net worth = that total − remaining loan; (B) if no →
  net worth = total + full home value − loan. When a spreadsheet shows both "without debt"
  and "with debt" rows, the difference equals the total debt subtracted. Check the units are
  consistent (AUD vs THB) before explaining.\n- **Be honest about contradictions** when analyzing stability. If the contracted mortgage
  payment (weekly×52) exceeds stated household income, that's likely an OCR over-read or the
  figure includes aggressive extra repays — say so and ask for the real "Contracted payment"
  rather than presenting an alarming conclusion as fact.
- **Superannuation** is retirement money (`เงินเกษียณ`), not liquid savings — present it as a
  separate bucket, never lump it with spendable cash.
- **Snapshot filenames**: keep `YYYY-MM-DD.md` for the main day snapshot; use
  `-revolut.md`, `-commsec-pocket.md`, `-betashares.md`, `-unisuper.md`, `-net-worth-full-house.md`,
  `-income-and-perth-super.md` suffixes for per-account snapshots on the same date.
- **Ownership-filter queries are recurring.** The user repeatedly asks variations of "how much
  is [owner/subset] worth" (e.g. "Perth AMP offset", "Nat spending/saving/salary", "family AMP
  others excluding Perth, Nat, Emergency, and Credit Card"). Maintain one master owner-tagged
  table and recompute the requested subtotal in code each time — apply the exact exclusions the
  user names, show which accounts remained, and give the ฿ conversion.

## Support files
- `references/account-conventions.md` — per-platform parsing conventions (AMP, Revolut,
  CommSec Pocket, Betashares, UniSuper) and the owner-classification rule.
- `references/nat-thailand-committed-expenses.md` — Nat's recurring annual Thai line items and
  the sunk-vs-value reframe (health ฿20K, CI ฿25K, endowment ฿25K, mother ฿180K/yr = ฿250K/yr).
- `references/investment-property-screening.md` — conservative Australian second-property
  LVR, rent-yield, expense, interest-rate, and cash-flow screening template.
