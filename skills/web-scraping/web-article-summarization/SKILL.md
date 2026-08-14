---
name: web-article-summarization
description: Summarize a public web article given its URL.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [web, summarization, scraping]
    related_skills: []
---

# Web Article Summarization

## When to Use
Use this skill whenever a user asks to summarise a public web article, blog post, or any publicly accessible page. It handles lazy‑loaded content and common article containers.

## Overview
Use this skill whenever a user asks to *summarize* an article, blog post, or similar public web page. The skill abstracts the extraction of the article body, handling lazy‑loaded content and common CMS structures.

## Steps
1. **Open the URL** – `new_tab(url)` then `wait_for_load()`.
2. **Allow lazy content to load** – optionally `import time; time.sleep(1-2)` for scripts that load on scroll.
3. **Try primary selectors** in order, stopping at the first non‑empty result:
   - `article`
   - `.elementor-widget-theme-post-content`
   - `.post-content`
   - `.entry-content`
   - `main`
4. **Extract text** – `js('element.innerText')` or `js('element.textContent')`.
5. **If still empty**, scroll to bottom a few times (`js('window.scrollBy(0, document.body.scrollHeight)')`) and repeat step 3.
6. **Return the extracted string** (trim whitespace, limit length if needed) for downstream summarization.

## Pitfalls & Work‑arounds
- Lazy‑loaded sections – scroll before extraction.
- Paywalls / login walls – abort and ask the user for access; do not guess credentials.
- Multiple article elements – pick the one with the most text (`len(text)`).
- Non‑English characters – ensure UTF‑8 handling; `js` returns Unicode strings.
- Heavy JavaScript pages – consider `capture_screenshot()` for manual inspection if text extraction fails.

## References
- `references/example-datath-summary.md` – concrete extraction of the DataTH "AI Second brain EP 1" article showing the selector order that succeeded.
