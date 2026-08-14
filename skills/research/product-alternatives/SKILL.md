---
name: product-alternatives
description: Suggest cheaper alternatives with prices and retailer links.
trigger: When a user asks for cheaper or alternative products.
---
# Product Alternatives Skill

## Goal
Provide concise, region‑specific suggestions for lower‑priced alternatives to a product the user is considering buying.

## Procedure
1. **Extract the target product name** from the user request.
2. **Compose a search query**: `<product name> cheaper alternative <region>` (e.g., "Satechi Slim EX1 cheaper alternative Australia").
3. **Run a web search** with `brave_web_search` (request up to 10 results).
4. **Collect results** that contain:
   - Product title
   - Price (AU$) visible in the snippet
   - A reputable retailer URL (Amazon AU, Kmart, Officeworks, JB Hi‑Fi, etc.)
5. **If the search yields no usable entries**, fall back to the reference file `references/keyboard-alternatives-au.md` (or another category‑specific reference under `references/`).
6. **Compose the reply** as a markdown table:
   | Alternative | Approx. AU price | Key feature | Link |
   |---|---|---|---|
   (populate rows)
7. **Add a brief disclaimer** that prices may vary and the user should verify current listings.

## Pitfalls & Work‑arounds
- **Amazon blocks scraping** – avoid loading the product page directly; rely on search results.
- **Missing price in snippets** – discard those entries; look for other retailers.
- **Region‑specific pricing** – always include the region (AU) in the query.

## References
- `references/keyboard-alternatives-au.md` – curated list of common wireless multi‑device keyboards and typical AU price ranges.
- `references/gaming-mouse-alternatives-au.md` – example for another product class.

## Example
User: *"I am about to buy the Satechi Slim EX1 keyboard on Amazon AU. Is there a cheaper alternative?"*
Assistant runs the skill and replies with a table of alternatives (Logitech K380, K780, Microsoft Surface Keyboard, etc.) showing AU price ranges and retailer links.
