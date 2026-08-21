---
name: image-concept-generation
description: "Use for AI-generated product concepts from reference images."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [image-generation, product-concepts, reference-image, gpt-image, mockups, branding]
    related_skills: [comfyui, marketing-banner-design, sketch]
---

# Image Concept Generation

Use this skill when the user wants a generated visual concept, product mockup, fashion/product design, or multiple visual variations based on an attached reference image.

## Core rule: honor the requested generation method

If the user explicitly asks for GPT Image, DALL-E, or another image model, produce the result with that actual image-generation capability. Do not silently substitute a hand-drawn SVG, Pillow/vector mockup, HTML screenshot, or text-only prompt. Those can be offered as fallback alternatives only after clearly stating that the requested generator is unavailable.

## Workflow

1. Inspect the attached reference image for silhouette, camera angle, materials, lighting, typography placement, and branding placement.
2. Identify any exact brand assets needed. If an official logo file is not provided, say that generated logos and text may be inaccurate and ask for the logo asset when fidelity matters.
3. Translate the request into a generation prompt that explicitly preserves:
   - the product shape and viewpoint from the reference;
   - exact requested text, spelling, color, and placement;
   - the number of variants and the color list;
   - consistent lighting/background across the set;
   - no extra text or invented branding.
4. Generate at least one real image output, then inspect it for legibility, spelling, logo fidelity, and whether all requested variants are present.
5. If the generator supports image references or editing, pass the original reference image rather than relying only on a prose description.
6. If generation is unavailable in the active runtime, verify that limitation before responding. State it plainly, do not claim an image was generated, and provide the exact next enablement requirement or a clearly labeled non-generative fallback.

## Product/fashion concept boards

For apparel or accessories, prefer a clean product-board composition with consistent three-quarter views so front and side details are visible. Keep typography large enough to inspect. For embroidered text, specify realistic thread texture, slight irregularity, and white stitching with contrast against every colorway.

## Quality gate

Before delivery, verify:
- output is actually from the requested image generator;
- every requested colorway is represented;
- exact text is readable and correctly spelled;
- the official logo is used when supplied, or the output is labeled as a logo approximation;
- no claims are made about a generated artifact without a real output path or media result.

## Pitfalls

- Never present a deterministic Pillow/SVG board as GPT Image output.
- Never invent access to an image-generation endpoint or API key.
- Do not over-explain implementation details when the user simply wants the visual result.
- If the user corrects the method, switch methods rather than defending the previous artifact.

See `references/gpt-image-product-concepts.md` for a reusable prompt structure and verification checklist.
