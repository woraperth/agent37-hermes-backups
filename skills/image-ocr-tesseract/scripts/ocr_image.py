#!/usr/bin/env python3
"""OCR text from static image files (PNG/JPG/WebP) with tesseract.

HANDY WHEN: the active model has no vision (vision_analyze fails with
"This model does not support image inputs") and the user sent screenshots,
photos, or any image the agent must read.

Requires tesseract. Install once:
    sudo apt-get install -y tesseract-ocr tesseract-ocr-eng
    # + languages as needed, e.g. Thai:
    #   sudo apt-get install -y tesseract-ocr-tha

Usage:
    python ocr_image.py screenshot.png                 # auto lang(s), psm 4
    python ocr_image.py shot.png --lang eng            # force English only
    python ocr_image.py shot.png --lang tha+eng        # Thai + English
    python ocr_image.py shot.png --psm 3               # manual PSM mode
    python ocr_image.py shot.png --out out.txt         # save to file

PSM tips: 4/6 for UI screenshots (account lists/tables), 3 for full pages,
11 for sparse single-line text.
"""
import sys
import subprocess


def ocr(path, lang=None, psm=4, out=None):
    cmd = ["tesseract", path, "stdout"]
    if lang:
        cmd += ["-l", lang]
    cmd += ["--psm", str(psm)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        sys.exit(result.returncode)
    if out:
        with open(out, "w") as f:
            f.write(result.stdout)
    else:
        print(result.stdout)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in {"-h", "--help"}:
        print(__doc__)
        sys.exit(0)

    path = args[0]
    lang = None
    psm = 4
    out = None

    if "--lang" in args:
        lang = args[args.index("--lang") + 1]
    if "--psm" in args:
        psm = int(args[args.index("--psm") + 1])
    if "--out" in args:
        out = args[args.index("--out") + 1]

    ocr(path, lang=lang, psm=psm, out=out)
