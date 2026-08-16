---
name: rss-newsletter-automation
description: Use for RSS newsletter automation with approval gates.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [rss, newsletters, automation, email]
    related_skills: [moosend]
---

# RSS-to-newsletter automation

## When to Use

Use when a user wants new blog posts converted into AI-assisted email newsletters, especially when the provider supports campaign labels, mailing lists, or segments.

## Core workflow

1. **Verify the source first**
   - Fetch the blog homepage and probe common feed paths (`/feed/`, `/feed`, `/rss`, `/rss.xml`, `/atom.xml`, `/feed.xml`).
   - Confirm HTTP success, an RSS/Atom content type, and parseable entries.
   - Record the canonical feed URL, item count, latest title, latest publication time, `guid`, and article link.
   - Do not assume the feed path from the CMS; verify it live.

2. **Design deduplication**
   - Use the RSS `guid` as the primary stable identifier.
   - Fall back to the canonical article URL if no GUID exists.
   - Persist processed identifiers before enabling recurring runs.
   - Never send the same article twice because a polling window overlaps.

3. **Fetch and validate article content**
   - Retrieve the article title, URL, excerpt, and main content.
   - Reject missing, duplicate, inaccessible, or non-article pages.
   - Require the AI output to be grounded only in retrieved article content.

4. **Generate the newsletter**
   - Produce subject, preview text, short opening, concise summary, practical takeaways when useful, and a read-more link.
   - Match the user's established language and editorial voice; avoid generic AI marketing copy and exaggerated claims.
   - Keep the original article URL unchanged.
   - Return `NEEDS_REVIEW` when the article is ambiguous, promotional, sensitive, or lacks enough content.

5. **Use an approval-gated MVP**
   - Start with AI draft → human approval → provider campaign creation/send.
   - Do not enable fully automatic sending until several runs have been manually reviewed.
   - Sending, scheduling, and testing are separate provider actions; creating a draft must not imply any delivery.

## Campaign taxonomy versus audience data

Keep these concepts separate:

- **Campaign labels** answer: “What kind of campaign is this?”
- **Mailing lists/segments** answer: “Who should receive it?”
- **Subscriber tags/custom fields** answer: “What do we know about this contact?”

For Moosend-style providers, use internal campaign labels such as `Newsletter`, `Marketing`, `Event`, and `Transactional`. Use a naming convention such as:

`[Newsletter] YYYY-MM-DD — <article title>`

Do not use subscriber tags merely to classify campaigns. Use lists or segments when the audience must differ.

## Safety and access boundaries

- Verify the provider account, approved sender, target list, and campaign label before creating a provider draft.
- Keep API keys in environment variables; never expose them in URLs, logs, notes, or chat.
- Do not claim access to a CMS, course platform, blog admin, subscriber list, or provider account unless a live tool confirms it.
- If the user is away from the required website, prepare the workflow, prompt, taxonomy, or draft content only; do not represent the external task as completed.
- Do not send or schedule campaigns without explicit, immediate confirmation.

## Implementation checklist

- [ ] Verified RSS/Atom endpoint
- [ ] Persistent processed-item store
- [ ] Article fetcher and content extractor
- [ ] Grounded AI prompt with `NEEDS_REVIEW` path
- [ ] Duplicate, timeout, and failure handling
- [ ] Provider list/sender confirmed
- [ ] Campaign label and naming convention confirmed
- [ ] Approval channel confirmed
- [ ] One historical article test completed
- [ ] First 3–5 campaigns manually reviewed
- [ ] Automatic sending decision made only after review

## References

- `references/datath-moosend-rss-findings.md` — verified feed and campaign-taxonomy findings from a real DataTH/Moosend investigation.
