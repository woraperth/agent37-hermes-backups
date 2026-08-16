# DataTH / Moosend RSS findings

## Verified RSS endpoint

- Blog: `https://blog.datath.com`
- Working feed: `https://blog.datath.com/feed/`
- Response content type: `application/rss+xml`
- Feed contained 10 items during verification on 2026-08-16.
- Latest observed item: `AI Second brain EP 1 – สมองไม่ได้มีไว้ “เก็บข้อมูล”`
- Latest observed publication date: 29 July 2026.
- WordPress `guid` values were available and are suitable as deduplication keys, with canonical article URLs as fallback.

## Moosend campaign organization

Moosend documentation states that campaigns can have labels for internal organization by topic, audience, purpose, or other internal use. Recommended labels:

- `Newsletter` — RSS-driven article emails
- `Marketing` — discounts, launches, sales
- `Event` — webinars and live sessions
- `Transactional` — operational messages

Recommended name: `[Newsletter] YYYY-MM-DD — <article title>`.

Keep campaign labels separate from subscriber tags and custom fields. Use mailing lists or segments to control audience; use subscriber tags/custom fields to describe contacts.

## Operational boundary

The working session only verified the public feed and updated a local workflow draft. It did not connect to Moosend, create a campaign, test an email, schedule delivery, or send anything.
