# Inference-config drift and cron pinning

## Observed failure pattern

An unattended LLM-driven cron job can be skipped before making any inference call when its creation-time inference configuration differs from the current global configuration. The scheduler reports a safety error similar to:

> global inference config drifted since this job was created ... and this job is unpinned

This is intentional spend protection, not a model/provider outage.

## Recovery procedure

1. Read the active resolved settings:
   ```bash
   hermes config get model.provider
   hermes config get model.default
   ```
2. List jobs and identify jobs with `no_agent` false / no script-only mode.
3. Pin each LLM-driven job to the active pair:
   ```bash
   hermes cron edit <job_id> --provider <provider> --model <model>
   ```
4. Verify through the cron job tool/API listing that each relevant job reports the expected `model` and `provider`. Script-only jobs should report both as null.
5. Treat old `last_status: error` entries as historical; do not trigger an immediate delivered run just to validate the pin unless the user asks.

## Important distinction

A job may have a simple shell-oriented prompt but still be LLM-driven if it was not created in `no_agent` mode. Pin it or convert it to a deterministic script intentionally; do not infer execution mode from prompt wording alone.
