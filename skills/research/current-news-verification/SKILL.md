---
name: current-news-verification
description: "Use for current news and exact-time verification."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Research, News, Verification, RSS, Current Events]
    related_skills: [grounded-citations, blocked-page-recovery]
---

# Current-News Verification

## When to Use

Use when a user asks about a current event, public itinerary, visit, appearance,
meeting, or exact time—especially when “today” or “tomorrow” is involved.

Use this skill for questions about breaking/current events, schedules,
visits, itineraries, public appearances, and exact times. The goal is not
merely to find a plausible headline: distinguish what is publicly confirmed
from what is missing, stale, or inferred.

## Procedure

1. Establish the reference date and timezone with a system time lookup. State
   the date explicitly when “today” or “tomorrow” is involved.
2. Search broadly using the available web-search tool. Try both the relevant
   local language and English, plus the named person, organization, place, and
   date.
3. If ordinary search is unavailable or returns client-rendered/noisy HTML,
   use Google News RSS through `terminal` as a discovery fallback. The
   reproducible recipe is in `references/rss-discovery.md`.
4. Extract the headline, publisher, publication date, and any literal details
   actually present in each result. Do not upgrade “will meet businesses” into
   an exact time or venue.
5. Follow the publisher URL where possible. If a publisher is blocked, use the
   blocked-page-recovery skill’s archive/API routes, preserving provenance.
6. Cross-check important itinerary or timing claims against a second
   independent source. Prefer official government, organization, or event
   schedules when available.
7. Answer at the precision supported by the evidence. If an exact time is not
   published, say that directly; do not infer it from arrival time, article
   timestamps, or a generic “tomorrow” reference.
8. Cite every externally sourced claim inline and include a concise Sources
   list. Search/RSS results may support only what their item literally states;
   cite the full publisher page for body-level details.

## Evidence ladder

- **Strong:** official itinerary/calendar, direct statement from the host or
  government, or two independent reports that state the same time.
- **Moderate:** one reputable publisher’s article with an explicit time.
- **Weak:** RSS/search headline or snippet without the requested detail.
- **Insufficient:** inference from timezone, travel schedule, article timestamp,
  or an uncited social-media repost.

## Response style

Lead with the answer in one or two sentences. Then add the relevant date,
qualification, and sources. For a missing exact detail, use wording such as:
“I confirmed the event, but I could not find a publicly published exact time.”
Avoid burying the answer under retrieval mechanics.

## Pitfalls

- Do not present a search snippet as if you read the linked article.
- Do not guess a time from a broad itinerary or convert a publication time into
  an event time.
- Do not treat a blocked page as evidence merely because it returned HTTP 200;
  validate the body and preserve snapshot/live provenance.
- Do not repeat the same failed search endpoint in a loop; pivot language,
  source, format, or route.
- “No exact time found” means no exact time was found in the checked public
  sources, not that the event has no scheduled time.

## Verification checklist

Before sending: reference date/timezone checked; named person and event
identity checked; every exact figure/time traced to literal source text;
uncertainty stated; citations and URLs match the sources actually consulted.
