---
name: rss-ai-newsletter-automation
description: Use when automating newsletters from RSS/Atom feeds.
category: research
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [RSS, Atom, newsletters, automation]
    related_skills: [blogwatcher, moosend]
trigger: "When a user wants to monitor a blog RSS/Atom feed and generate or send newsletters from new posts."
summary: "Verify the feed, identify stable item IDs, design fetch/summarise/review/send stages, and keep external sending separate from drafting."
---

# RSS → AI newsletter automation

## When to Use

Use this skill when a user wants new blog posts detected from RSS/Atom and transformed into AI-assisted newsletters, whether the delivery provider is known yet or still needs to be confirmed.

## Purpose

Design and implement a reliable pipeline that detects new blog posts from RSS/Atom, generates a newsletter draft with an LLM, and optionally sends it through an email provider. Treat feed ingestion, content generation, approval, and delivery as separate stages.

## Core workflow

1. **Verify the source first**
   - Fetch the user-provided blog URL and test likely feed paths.
   - Confirm HTTP success, XML validity, and an RSS/Atom content type.
   - Record the canonical feed URL and inspect several entries before designing the parser.
   - Do not claim a feed works from a homepage link alone.

2. **Use stable identifiers and deduplication**
   - Prefer RSS `guid`/Atom `id` as the processed-item key.
   - Fall back to the canonical article URL only when no stable feed ID exists.
   - Persist processed IDs and keep the article URL for traceability.
   - A polling run must be idempotent: rerunning it must not create another newsletter for an already processed item.

3. **Fetch article content**
   - Use the feed title, URL, excerpt, and publication date as metadata.
   - Fetch the article page when the feed does not contain enough text for a faithful summary.
   - If the page cannot be retrieved or contains insufficient content, stop and flag the item for review rather than inventing details.

4. **Generate a draft**
   - Produce subject, preview text, short opening, useful summary, optional takeaways, and a read-more link.
   - Instruct the model to use only facts supported by the article and to return `NEEDS_REVIEW` for ambiguous or overly promotional content.
   - Preserve the canonical URL exactly.
   - Match the user's established language and voice; avoid generic AI marketing phrasing.

5. **Gate quality and delivery**
   - Check URL validity, duplicate status, factual grounding, length, sender, footer, and unsubscribe content.
   - Recommend draft → human approval → send for the MVP.
   - Do not silently turn a request to "set up" or "build" into an externally visible send or schedule.
   - After several manually reviewed sends, the user may choose whether selected low-risk articles can auto-send.

6. **Handle failures**
   - Retry temporary fetch failures once.
   - Do not send when article extraction, summarisation, audience selection, or provider validation fails.
   - Record the item ID, URL, stage, and failure reason in a review queue or run log.

## Provider boundary

Keep provider-specific actions separate from the RSS workflow. Before creating a campaign, confirm the provider, approved sender, target list, and content fields. Draft creation, test sending, scheduling, and live sending are different operations. Require explicit confirmation immediately before any externally visible action.

## Practical MVP

A low-risk first implementation is:

- Scheduled RSS poll
- Stable-ID deduplication
- Article fetch
- AI draft generation
- Human approval notification
- Provider campaign creation only after approval
- Manual review of the first 3–5 sends

Do not require a webhook when polling is sufficient; RSS polling is simpler and works without CMS access.

## References

- `references/datath-feed-verification.md` — verified DataTH RSS endpoint, observed response details, and the exact feed-specific implementation notes from the initial probe.

## Pitfalls

- Do not recommend work that requires access the agent does not have (for example, a course platform or a private newsletter account).
- Do not treat a valid RSS feed as proof that the agent can access the user's subscriber list or email provider.
- Do not use publication date alone for deduplication; feeds can be republished or reordered.
- Do not auto-send during initial setup. Build and verify the draft path first.
- Do not include API keys in feed logs, campaign URLs, files, or chat output.

## Verification checklist

- [ ] Feed URL returns valid RSS/Atom
- [ ] Parser extracts title, URL, date, and stable ID
- [ ] Duplicate item is ignored on a second run
- [ ] Article content is fetched and bounded
- [ ] Generated draft cites only article-supported facts
- [ ] Broken/ambiguous article is flagged, not sent
- [ ] Approval gate is tested
- [ ] Provider campaign is verified before any send
