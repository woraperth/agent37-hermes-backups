# GPT Image product-concept prompt and QA reference

## Prompt structure

```text
Create a realistic product concept board based on the attached reference image.
Preserve the reference product's silhouette, camera angle, proportions, materials,
and lighting. Show [N] consistent variants in these exact colorways: [list].
Place the exact text "[TEXT]" in [COLOR] embroidered/stencilled/printed on
[LOCATION]. Place the supplied official [BRAND] logo on [LOCATION]. Keep the
text and logo large, readable, correctly spelled, and free of invented symbols.
Use a clean neutral background, consistent three-quarter views, realistic
materials, and no extra text.
```

## Product-board checks

- Is the requested number of colorways visible?
- Are front and side branding details visible in the same view?
- Is every word spelled correctly and readable at normal size?
- Is the supplied logo asset used rather than a generated approximation?
- Are lighting, angle, scale, and background consistent across variants?
- Is the final output genuinely from the requested image-generation tool?

## If the requested generator is unavailable

State the limitation plainly. Do not call a Pillow/SVG/HTML output GPT Image.
Offer either: (a) enabling the requested image tool/API, or (b) a clearly labeled
non-generative layout mockup as a fallback. Preserve the user's requested
method if they explicitly corrected the workflow.
