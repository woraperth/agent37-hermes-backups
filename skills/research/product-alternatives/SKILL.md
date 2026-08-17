---
name: product-alternatives
description: Suggest cheaper alternatives with prices and retailer links.
trigger: When a user asks for cheaper or alternative products.
---
# Product Alternatives Skill

## Goal
Provide concise, region-specific product options or alternatives grounded in live supplier/retailer evidence. This also covers custom corporate gifts and souvenirs when the user wants available items rather than a cost comparison.

## Procedure
1. **Extract constraints before searching:** country/market, product class, personalisation method, maximum/minimum quantity, budget if given, and exclusions such as size-dependent apparel.
2. **Search locally in the user's language** where possible. For Thailand, use Thai queries such as `ของพรีเมี่ยม สกรีนโลโก้`, `ของชำร่วย สกรีนโลโก้`, and category-specific terms (แก้ว, ปากกา, สมุด, พวงกุญแจ, etc.).
3. **Collect supplier evidence, not just generic category ideas:** product title/category, personalisation method (print/engrave/emboss), supplier URL, and any explicit MOQ. Prefer supplier pages with a visible product catalogue or service description.
4. **Treat MOQ carefully:** only label an item as confirmed for the requested quantity when the source explicitly states the MOQ. If the site lists the item but does not publish MOQ, label it `MOQ not stated—confirm with supplier`; never infer that a low advertised minimum applies to every product category.
5. **Filter physical constraints early:** remove size-dependent apparel when the user has no sizing information. Prioritise size-free gifts such as pens, notebooks, bottles, mugs, keychains, USB drives, umbrellas, phone stands, and gift sets.
6. **If prices are absent, do not invent ranges.** The user may explicitly request an availability-only list; in that case omit prices and say that the supplier should confirm price, setup fee, and MOQ.
7. **Compose a compact table:**
   | Item | Customisation | MOQ evidence | Supplier/source |
   Use grouped rows where several items come from the same supplier, and include direct links.
8. **Add a short verification note:** ask suppliers to confirm whether they accept the exact quantity, artwork/setup fees, production time, and whether the quoted minimum applies to the selected item.

### Custom corporate-gift research reference
See `references/thailand-custom-gifts.md` for supplier/category evidence and the distinction between catalogue availability and verified MOQ.

## Original cheaper-alternative workflow
For ordinary alternatives, search `<product name> cheaper alternative <region>`, collect visible prices and reputable retailer URLs, and include a brief price-variation disclaimer. If no usable entries exist, use a category-specific reference file.

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
