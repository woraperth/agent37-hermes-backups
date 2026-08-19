# Moosend API quirks captured from a verified campaign draft

## MailingLists payload

For `POST /v3/campaigns/create.json`, pass mailing lists as form objects:

```json
"MailingLists": [
  {"MailingListID": "<list-id>"}
]
```

Passing bare IDs such as `["<list-id>"]` returns HTTP 200 with `Code: 501` and a validation error saying strings cannot be converted to `CampaignMailingListForm`.

## Verification

The create endpoint returned `Code: 0`, `Error: null`, and the campaign ID in `Context`. The attempted `GET /campaigns/<id>.json` and guessed subpaths were interpreted by this API as collection pagination parameters. A reliable verification path was:

1. `GET /v3/campaigns.json?apikey=...&page=N&pageSize=100`
2. Search the returned `Context.Campaigns` for the created ID or unique internal name.
3. Confirm exact `Name`, `Subject`, `ConfirmationTo`, list memberships, and `Status: 0` (draft), with delivery counters at zero.

Keep API keys out of logs and reports. The verified campaign used a fresh absolute HTTPS asset URL for the banner, not a local filesystem path.