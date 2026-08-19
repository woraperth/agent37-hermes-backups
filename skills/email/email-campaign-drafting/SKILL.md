---
name: email-campaign-drafting
description: Use when drafting marketing email campaigns safely.
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [email, campaigns, marketing, drafting, verification]
---

# Email Campaign Drafting

Use this class-level workflow when turning approved copy and assets into a marketing email campaign draft in a provider such as Moosend. The objective is a verifiable draft, not an assumed send.

## Workflow

1. **Confirm the brief.** Identify campaign type (Marketing vs Newsletter), subject, preview text/subtitle, approved body copy, CTA URL, sender/reply-to, audience, and whether the user supplied a banner or other assets.
2. **Inspect account resources first.** Validate credentials, approved sender, target lists, and any existing campaign whose audience/layout should be reused. Never guess a mailing list from a similar name when the provider can enumerate it.
3. **Prepare email HTML.** Use mobile-friendly, table-safe/simple inline styles where appropriate; include an absolute HTTPS asset URL, meaningful image alt text, a clear CTA, and the provider's unsubscribe placeholder. Preserve approved copy and distinguish the internal campaign name from the customer-facing subject.
4. **Create only a draft.** Drafting, testing, scheduling, and sending are separate operations. Do not schedule or send unless the applicable account policy explicitly allows it and the user separately requests it. For draft-only accounts, never schedule/send.
5. **Verify the created resource.** Confirm the returned campaign ID, exact subject, internal name, sender/confirmation address, campaign status, selected lists, and that delivery counters are still zero. If a provider's single-resource endpoint is ambiguous, query its collection endpoint with pagination and locate the returned ID instead of claiming success from the create response alone.
6. **Report concretely.** Give the campaign ID, draft status, subject, audience selection, and whether test/schedule/send occurred. Do not expose API keys.

## Provider-specific support

For Moosend API field shapes and the validated collection-based verification workaround, see `references/moosend-api-quirks.md`.

## Pitfalls

- Do not pass mailing-list IDs as bare strings if the provider expects form objects.
- Do not use a local filesystem path in email HTML; recipients and provider renderers need an absolute public HTTPS URL.
- Do not infer that `HTTP 200` means success; inspect the provider's JSON code/error fields.
- Do not report recipient totals from a fresh draft's delivery counters; they normally remain zero until delivery.
- Do not call a test endpoint merely because a draft was created; testing needs its own explicit recipient/content approval.
