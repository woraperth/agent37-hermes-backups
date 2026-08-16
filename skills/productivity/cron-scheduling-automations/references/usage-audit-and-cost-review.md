# Hermes usage-audit and cost review

Use this when a user asks how many tokens Hermes used or whether API billing would be cheaper than a subscription.

## What the audit means

The native `~/.hermes/cron/usage_audit.jsonl` records inference usage for audited **cron executions** (`prompt_tokens`, `completion_tokens`, `total_tokens`, model, job id, and timestamp). It is not automatically a complete accounting of interactive Discord/CLI sessions. State/session metadata may show message counts but should not be presented as token usage unless per-request usage is available.

Always label the scope explicitly: audit period, timezone, and whether the figures are cron-only or include interactive sessions.

## Aggregate without loading raw logs into chat

Use `jq` to aggregate by UTC date and job:

```bash
jq -s 'group_by(.ts[0:10]) | map({date: .[0].ts[0:10], requests:length, prompt:map(.prompt_tokens)|add, completion:map(.completion_tokens)|add, total:map(.total_tokens)|add})' ~/.hermes/cron/usage_audit.jsonl

jq -s 'group_by(.job_id) | map({job_id:.[0].job_id, requests:length, prompt:map(.prompt_tokens)|add, completion:map(.completion_tokens)|add, total:map(.total_tokens)|add})' ~/.hermes/cron/usage_audit.jsonl
```

Use `hermes cron list` to map job IDs to names before explaining the result. Keep raw JSON out of Discord; report a compact table and the main drivers.

## Interpretation and cost comparison

Separate background automation from user chat. A frequent sync or briefing can dominate prompt tokens through repeated context, even when completion output is tiny. Do not multiply token counts by an invented price: confirm the active provider/model and current pricing, and note when the active route is a subscription/OAuth path rather than API billing. Subscription limits and API token charges are different products and are not directly comparable from token totals alone.

If background jobs dominate, recommend reducing cadence/context or converting deterministic work to `no_agent` scripts before concluding that API or subscription is cheaper. Mention that the current model/provider may not have a public API price equivalent.

## Verification checklist

- [ ] Read the audit file and aggregate in code (`jq` or equivalent), not mental arithmetic.
- [ ] State the exact date range and timezone basis.
- [ ] Identify whether interactive conversations are included.
- [ ] Map job IDs to names using `hermes cron list`.
- [ ] Distinguish prompt and completion tokens; highlight repeated-context overhead.
- [ ] Avoid fabricated API cost estimates; use verified pricing or present a formula with assumptions.
