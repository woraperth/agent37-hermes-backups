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

## Moosend discovery and draft workflow

- The initial `GET /lists.json` response returned only 10 lists. The documented complete-list endpoint is `GET /lists/{Page}/{PageSize}.json`; `GET /lists/1/100.json` returned 54 active lists and page 2 was empty.
- The general audience was `DataTH Blog Subscribers` with 7,031 active members at verification time. Do not confuse it with course-interest, student, or webinar-registrant lists.
- Approved sender observed: `perth@datath.com` (sender name: `แอดเพิร์ธ Data Science ชิลชิล`).
- A previous branded DataTH campaign contained two image elements and the `#unsubscribeLink#` token. Its HTML had four responsive copies of the main text block; all four must be replaced when reusing the layout.
- Directly creating/updating large HTML through the API was rejected in this account. The working approach was: fetch the prior campaign HTML, replace all four content blocks while preserving the outer template, host the non-sensitive HTML at a public `WebLocation`, create a new draft using `WebLocation`, and re-fetch to verify.
- The verified draft checks were: status `0`, no `ScheduledFor`, no `DeliveredOn`, target mailing-list ID, sender/reply-to, article URL, image count, author string `แอดเพิร์ธ`, and unsubscribe token.
- Leave prior drafts in place unless the user explicitly confirms deletion; draft cleanup is a separate destructive action.
- No test, schedule, or send endpoint should be called during this workflow.
