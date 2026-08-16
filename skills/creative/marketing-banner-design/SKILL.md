---
name: marketing-banner-design
description: "Use for promotional banners with localized, legible copy."
category: creative
trigger: "Use when creating an email, course, discount, launch, or social promotional banner from supplied copy."
summary: "Turn marketing copy into a concise visual composition, preserve exact offer details, render with glyph-safe fonts, and inspect the final image before delivery."
---

# Marketing Banner Design

Use this skill for static promotional graphics: course launches, student discounts, email headers, social cards, event promotions, and similar conversion-oriented banners.

## Core principle

A promotional banner is a **decide-now** surface, not an infographic. The viewer should understand the offer in a few seconds:

1. Who is eligible?
2. What is the benefit?
3. What is the final price or action?
4. What code or CTA is required?
5. When does it expire?

Do not trade legibility for decoration. The offer hierarchy is more important than an elaborate illustration.

## Workflow

1. **Extract locked facts**
   - Copy exact prices, discount amount, URLs, dates, times, eligibility, and placeholder codes.
   - Never invent a coupon code or silently change a deadline.
   - Mark unfinished values visibly as placeholders, e.g. `XXXX` or `[โค้ดส่วนลด]`.

2. **Choose a practical canvas**
   - Default email/social landscape: 1200×628 px.
   - Use 16:9 for video/social thumbnails, 1:1 for square feeds, or 9:16 for stories.
   - Keep the main offer within a safe central area so crops do not remove the price or deadline.

3. **Commit to one composition**
   - Use a clear promotional composition: eligibility label → offer headline → price card → coupon/CTA → deadline.
   - Make one number dominant: usually the final price or discount amount.
   - Avoid equal visual weight for every line.
   - Use a small amount of decorative context (course, code, interface, or abstract technical motif), never decoration that competes with the offer.

4. **Write or place the copy**
   - Preserve the user's language and relaxed tone.
   - Prefer short lines and natural Thai phrasing.
   - Keep the banner copy shorter than the email body; the banner is a scan aid, not the full explanation.
   - Use a struck-through original price next to a larger final price when communicating a discount.

5. **Handle localized typography deliberately**
   - Before rendering, confirm that the selected font and renderer contain glyphs for the target language, especially Thai.
   - Do not trust an SVG preview if text appears missing or reduced to blank space.
   - If the SVG/browser renderer lacks glyph support, render text through a raster workflow (for example, Pillow with a confirmed Thai-capable font) or embed a known-good web/local font.
   - Check that tone marks, vowels, numerals, currency symbols, and punctuation all render correctly.

6. **Render and verify the actual output**
   - Produce the requested image file, not only a prompt or design description.
   - Inspect the rendered PNG/JPG visually.
   - Verify every locked fact: headline, discount, old/new price, code placeholder, launch date, expiry date/time, and URL.
   - Check contrast, clipping, line wrapping, and small-text readability at the intended display size.
   - If any text is missing or unreadable, fix the font/rendering path and render again before delivery.

7. **Deliver with a useful note**
   - Attach the actual image.
   - State which values remain placeholders.
   - Mention the image dimensions and any important caveat, but avoid narrating the whole production process.

## Recommended promotional hierarchy

```text
[Eligibility / exclusive label]

[Main offer: what the viewer gets]
[Discount amount or strongest benefit]

[Original price] → [Final price]

[Coupon code / CTA]
[Expiry date and time]
[URL]
```

## Copy and tone guidance

For Thai course promotions, use conversational but direct phrasing. For example:

- `นักเรียน DataTH รับส่วนลดคอร์ส Vibe Coding เพิ่มอีก 400 บาท`
- `จาก 4,900 บาท เหลือเพียง 4,500 บาท`
- `ใช้โค้ด: XXXX`
- `หมดเขต 23:59 น. ศุกร์ 21 สิงหาคม 2026`

Avoid overclaiming, fake urgency, unexplained jargon, or excessive copy on the image. If urgency is real, state the concrete deadline rather than using vague phrases like “รีบด่วน”.

## Quality checklist

- [ ] Eligibility is explicit.
- [ ] Discount and final price agree mathematically and visually.
- [ ] Original price is visibly secondary to final price.
- [ ] Placeholder code is unmistakable and easy to replace.
- [ ] Deadline includes the correct date and time.
- [ ] URL is readable and not clipped.
- [ ] Thai glyphs, tone marks, and numerals render correctly.
- [ ] Contrast is sufficient for every important line.
- [ ] Final image was inspected, not merely generated.
- [ ] No extra claims or invented details were added.

## Reference

See `references/thai-promotional-banner-checklist.md` for the condensed Thai-copy and rendering checklist used for course discount banners.

## Pitfalls

- A design that looks correct in source SVG/HTML can still lose Thai text during rasterization; always inspect the final PNG/JPG.
- Do not use the renderer's default font for Thai without checking glyph coverage.
- Do not let decorative code windows, gradients, or illustrations compete with the price and deadline.
- Do not present a placeholder code as if it were final.
- Do not claim the asset is complete until the rendered file exists and has been visually checked.
