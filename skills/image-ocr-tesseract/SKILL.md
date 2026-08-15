---
name: image-ocr-tesseract
description: OCR screenshots with tesseract when the model lacks vision.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [OCR, Images, Screenshots, Text-Extraction, Tesseract, Vision]
    related_skills: [ocr-and-documents]
---

# Image OCR with Tesseract (vision-less fallback)

Use when the USER sends an image (screenshot, photo, bank-app screenshot, PDF page render) and the active model cannot "see" it — `vision_analyze` fails with an error like:

```
Error analyzing image: Error code: 400 - {'error': {'message': 'This model does not support image inputs'}}
```

That error is a dead end with the current model. Do NOT loop retrying `vision_analyze`. Instead, OCR the image text locally with `tesseract`. This handles phone/bank-app screenshots, scanned pages rendered to PNG, and photos containing text.

Related: `ocr-and-documents` (bundled) covers PDF/scans via pymupdf/marker-pdf; `image-ocr-tesseract` covers the separate case of raw image files.

## When to Use
- User sends images (screenshots, bank-app shots, photo of a document) and `vision_analyze` returns "This model does not support image inputs" / "does not support vision".
- Any task needing to read text or numbers out of an image when no vision-capable model is active: transcribe a statement, fill a tracker, analyze account balances, digitize a hand note.
- Do NOT use when a vision model is available — `vision_analyze` is higher fidelity there.

## Workflow

1. **Confirm the files exist and are images** (a `vision_analyze` failure alone doesn't tell you the path is bad):
   ```bash
   ls -la /path/to/img_*.png
   file /path/to/img_*.png   # prints e.g. "PNG image data, 1080 x 2400"
   ```

2. **Install tesseract + language packs** (once per machine):
   ```bash
   sudo apt-get install -y tesseract-ocr tesseract-ocr-eng
   # add languages the content may be in, e.g.:
   # sudo apt-get install -y tesseract-ocr-tha        # Thai
   tesseract --list-langs                              # confirm installed packs
   ```

3. **Run OCR** — combine the languages you expect and pick a PSM mode:
   ```bash
   tesseract screenshot.png stdout -l eng --psm 4
   tesseract screenshot.png stdout -l tha+eng --psm 4
   ```
   - `--psm 4` (assume a single column of text of variable sizes) is a good default for UI / banking-app screenshots.
   - `--psm 3` (default, fully automatic) for page-like scans.
   - `--psm 11` for sparse single-line text.
   - For multi-line account lists / tables, `--psm 4` or `6` (uniform block) reads best.

4. **Sanity-check the numbers before acting on them.** OCR misreads digits (1↔l, 0↔O, `.` ↔ `,`). For financial/accounting data, recompute totals in code from the transcribed figures and reconcile against anything cross-referenced — flag mismatches rather than trusting raw OCR blindly.

## Pitfalls
- **Do not loop the same failing `vision_analyze` call.** One diagnostic attempt, then pivot to tesseract.
- **`--lang` matters for non-Latin scripts** (Thai, etc.). Without the right pack you get garbage or blank output.
- **PSM mode changes results dramatically.** If output is a jumble, try a different `--psm` before assuming OCR failed.
- **Digit fidelity is the weak point.** Financial screenshots need a verification pass (recompute totals, cross-check account names vs. expected).
- **Busy screenshots with app UI chrome** produce stray text; strip it mentally and keep the account names + values.

## Support files
- `scripts/ocr_image.py` — re-runnable OCR helper: `python ocr_image.py shot.png --lang tha+eng --psm 4 [--out file]`.
