# Per-platform account conventions (Nat / Perth / ครอบครัว)

These conventions were derived from recording Nat & Perth's accounts (AMP bank, Revolut,
CommSec Pocket, Betashares, UniSuper) into the nat-hermes-second-brain vault. Reuse for
parsing the same apps quickly.

## Owner-classification rule (user's explicit instruction)
- Account named with a person → belongs to that person.
- Account with NO person in the name (Household Expenses, House Utility, Travel saving,
  Salary and Emergencies, Credit Card, the home loan) → **ครอบครัว (family)**.
- Tag rows: `👤 Nat`, `👤 Perth`, `👪 ครอบครัว`.

## AMP Banking (BSB 939200)
- Account list screenshots show: name, `$xxx.xx Balance Available`, `BSB 939200 ACC nnnnnn`.
  Keep account number alongside the balance.
- "ProfVarPI" = the home loan (Professional Pack Variable Rate Loan, P&I), in both owners'
  names (Woratana & Kessurang) → family debt. Fields: Current balance (negative),
  Available redraw, Interest rate p.a., Contracted payment + frequency (usually Weekly).
- Offset note: the family "Salary and Emergencies" balance is large and offsets the loan.

## Revolut Investing
- Top card: `Total portfolio value`, `+$gain (+%)` = unrealised profit overall, stock
  subtotal, commodities subtotal, cash balance.
- Per-holding lines: ticker, shares qty, price, `+%` unrealised. App shows % per holding,
  NOT a per-holding dollar gain — only the portfolio-level gain is in dollars.

## CommSec Pocket
- `CURRENT VALUE`, then a `+$gain (+%)` line, `CONTRIBUTED` (money put in), and
  `LAST INVESTMENT` date. Ready-made reconciliation: contributed + gain = current value.
- Funds listed with per-fund `+$gain (+%)`. Vault: current value A$18,954.28,
  contributed $11,329.92, last investment 31 Jul 2026.

## Betashares
- `Total investments` + `+%` and `+$gain`. Holdings split into HOLDING (e.g. A200 ETF)
  and PORTFOLIO (e.g. All Growth). Per-holding shows `+%` only.

## UniSuper
- `Overview → Accumulation 1` shows the balance + "As at <date>". Contributions listed with
  date, `+$amt`, and type (Member Voluntary Before-Tax / Employer Contribution).

## Currency conversion (AUD → THB)
- Open endpoint (no key): `https://open.er-api.com/v6/latest/AUD` → `rates.THB`.
- Cross-check with a second source (e.g. frankfurter.app needs `/latest?from=AUD&to=THB`).
- State the rate and date used; figures move with the rate.
