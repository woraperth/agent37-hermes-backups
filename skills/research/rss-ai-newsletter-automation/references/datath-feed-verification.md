# DataTH RSS feed verification

Verified during the August 16, 2026 newsletter-automation session.

## Source

- Blog: `https://blog.datath.com`
- Working feed: `https://blog.datath.com/feed/`
- Alternate working path: `https://blog.datath.com/rss`
- `/feed.xml`, `/rss.xml`, `/atom.xml`, and `/index.xml` returned 404 during the probe.
- Response status: HTTP 200
- Content type: `application/rss+xml; charset=UTF-8`
- Feed format: WordPress RSS 2.0

## Observed fields

Each item exposed:

- `title`
- `link`
- `pubDate`
- `guid`
- RSS content namespaces, including `content`

Use `guid` as the stable deduplication key and retain `link` as the article URL.

## Verification snapshot

- Channel title: `เข้าใจ Data ง่าย ๆ กับ DataTH`
- Channel link: `https://blog.datath.com`
- Items returned at verification: 10
- Latest observed title: `AI Second brain EP 1 – สมองไม่ได้มีไว้ “เก็บข้อมูล”`
- Latest observed publication time: `Wed, 29 Jul 2026 12:43:11 +0000`
- Latest observed GUID: `https://blog.datath.com/?p=9673`

## Implementation note

A scheduled poll is sufficient for the MVP; CMS webhook access is not required. On each run, parse the feed, compare GUIDs against a persistent processed-items store, and enqueue only unseen items for article fetching and AI drafting. The verified feed proves public RSS access only; it does not prove access to the user's newsletter provider, mailing list, sender identity, or campaign API.
