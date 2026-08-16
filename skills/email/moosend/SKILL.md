---
name: moosend
description: Build and manage Moosend email campaigns safely.
version: 0.1.0
author: Perth888, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [email, moosend, campaigns, newsletters]
    related_skills: []
---

# Moosend Skill

Use this skill to work with the Moosend v3 API for mailing lists, subscribers, and email campaigns. It supports campaign preparation and management; sending or scheduling is always a separate, explicit action and must not be inferred from drafting.

## When to Use

- Create or update a Moosend regular email campaign.
- Inspect mailing lists, subscribers, senders, campaigns, or campaign statistics.
- Test, schedule, unschedule, or send a campaign after explicit confirmation.

Don't use for: transactional email design or operations unless the request specifically targets Moosend transactional campaigns.

## Prerequisites

- Store the Moosend API key in the environment variable `MOOSEND_API_KEY` or in the profile's `.env`; never paste it into chat, files committed to repositories, or URLs shown in logs.
- Confirm the sender email is an approved Moosend sender.
- Confirm the target mailing-list ID before creating a campaign.
- Use the documented base URL `https://api.moosend.com/v3`.
- API authentication is the required `apikey` query parameter. Requests should use JSON and the `Accept: application/json` header.

## Quick Reference

```text
GET  /lists.json?apikey=$MOOSEND_API_KEY
GET  /campaigns.json?apikey=$MOOSEND_API_KEY
POST /campaigns/create.json?apikey=$MOOSEND_API_KEY
POST /campaigns/{CampaignID}/test.json?apikey=$MOOSEND_API_KEY
POST /campaigns/{CampaignID}/schedule.json?apikey=$MOOSEND_API_KEY
POST /campaigns/{CampaignID}/send.json?apikey=$MOOSEND_API_KEY
```

The create body commonly includes:

```json
{
  "Name": "Internal campaign name",
  "CampaignType": "Regular",
  "Subject": "Email subject",
  "SenderEmail": "approved-sender@example.com",
  "ReplyToEmail": "approved-sender@example.com",
  "ConfirmationToEmail": "owner@example.com",
  "HTMLContent": "<html>...</html>",
  "MailingLists": ["mailing-list-id"],
  "SegmentID": "optional-segment-id",
  "IsAB": false,
  "TrackInGoogleAnalytics": false
}
```

## Procedure

1. **Inspect account resources.** Use `terminal` with a short Python or curl request to list mailing lists, senders, and existing campaigns. Redact the API key from output. Completion criterion: the chosen list ID and approved sender are identified.
2. **Prepare content.** Build valid email HTML with an unsubscribe link supported by Moosend, mobile-friendly layout, and absolute URLs for images. Prefer `HTMLContent` for generated content; use `WebLocation` only when the public URL is deliberate and verified. Completion criterion: the final subject, sender, reply-to, audience, and HTML are reviewed.
3. **Create a draft.** Call `POST https://api.moosend.com/v3/campaigns/create.json?apikey=...` with the required JSON body. Completion criterion: response is HTTP 200 and returns a campaign ID; retain the ID without exposing the key.
4. **Verify the draft.** Retrieve campaign details and confirm subject, sender, content, mailing list, and campaign status. Completion criterion: all critical fields match the approved brief.
5. **Test separately.** Call the campaign test endpoint only when a test recipient and test subject/content are explicitly supplied. Completion criterion: Moosend returns success and the test result is recorded.
6. **Schedule or send only after explicit confirmation.** Scheduling uses `POST /campaigns/{CampaignID}/schedule.json` with `DateTime` and optional `Timezone`; Moosend documents that scheduling assigns a time but does not itself send, so the send endpoint is a separate operation. Completion criterion: the user explicitly chose send-now or schedule and the API response is successful.
7. **Verify delivery state.** Retrieve campaign details and, when needed, campaign summary/statistics. Completion criterion: the resulting status is reported with the campaign ID and timestamp.

## Safety Rules

- This account is draft-only: never schedule or send any campaign, even if explicitly requested later. Drafting and optional testing are the only campaign operations allowed.
- Drafting, testing, scheduling, and sending are distinct operations. Never call schedule or send because the user asked to “build” a campaign.
- Never use an API key found in conversation memory; ask the user to configure a fresh key in the environment if `MOOSEND_API_KEY` is absent.
- Do not put `apikey` in copied logs, screenshots, reports, or error messages.
- Treat campaign send, schedule, delete, subscriber removal, and list deletion as destructive or externally visible actions requiring explicit confirmation immediately before the call.
- Confirm timezone and date format against the Moosend account settings before scheduling. Prefer an explicit timezone such as `AUS Eastern Standard Time` when accepted by the account.

## Verification

- Check HTTP status and parse the JSON response.
- Treat a Moosend response with `Code: 0` and `Error: null` as the documented success shape, but still verify the returned resource or status.
- For a draft, re-fetch campaign details and compare the critical fields.
- For a scheduled or sent campaign, re-fetch campaign details and report the actual returned status; never claim success from a command that failed or timed out.
- Use `terminal` commands with environment expansion and redacted output; do not print the full request URL after adding the API key.

## Known API Details

- Base URL: `https://api.moosend.com/v3`.
- Endpoint format is `/resource.{Format}` where `Format` is `json` or `xml`; use `json`.
- Authentication is a query parameter named `apikey`, not a bearer header.
- Create draft: `POST /campaigns/create.{Format}`; required fields include `Name`, `Subject`, `SenderEmail`, `ReplyToEmail`, and `IsAB`. Content can be supplied via `HTMLContent` or `WebLocation`; `MailingLists` selects the audience.
- Send now: `POST /campaigns/{CampaignID}/send.{Format}`.
- Schedule: `POST /campaigns/{CampaignID}/schedule.{Format}` with required `DateTime` and optional `Timezone`; the guide explicitly says a subsequent send call is needed at the scheduled time.
- Rate limits, status codes, and field validation follow the current Moosend documentation; on errors, preserve the HTTP status and redacted response for diagnosis.
