# PDF bank-statement expense analysis

Use this reference when a user uploads a bank statement PDF and asks why a month ran out of money or whether food spending spiked.

## Verified workflow

1. Read the statement period before analyzing. If the requested month is outside the period, state that explicitly and do not infer it.
2. Prefer PyMuPDF for text-based PDFs. Parse transaction date, description, amount, and running balance while preserving raw descriptions.
3. Determine debit versus credit from the running-balance movement and official statement totals. In extracted AMP-style statements, scheduled internal transfers may appear as a standalone amount but increase the balance: they are credits/funding, not expenses.
4. Reconcile parsed values against the statement's official debit/credit totals. Do not report a category breakdown until the reconciliation works.
5. Use conservative categories: groceries/ingredients, prepared food/eating out, non-food/other, and unlabelled/uncertain. Keep ambiguous rows visible.
6. Report monthly totals, a named baseline (for example, average of prior complete months), percentage deviations, and the largest transactions behind any spike.

## Reproduction note

An AMP Offset Deposit Account statement covering 1 Jan-30 Jun 2026 had six $1,100 scheduled transfers that increased the balance. The statement reported credits of $6,600 and debits of $6,751.58. Correct analysis therefore excluded the $6,600 funding credits from spending and reconciled the remaining $6,751.58 as debits. Treating the scheduled amounts as expenses would double-count flows and produce an invalid result.
