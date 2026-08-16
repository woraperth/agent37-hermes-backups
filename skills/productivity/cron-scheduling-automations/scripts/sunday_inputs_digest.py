#!/usr/bin/env python3
"""Sunday Inputs digest generator — validated no_agent cron script (Perth, Aug 2026).

Copy and modify for any recurring "process your inbox/vault" digest delivered to
Discord. Uses frontmatter `processed: true|false` per note; emits a heading-first
digest on stdout. Wired to a cron job with `no_agent=true` + `script=` so stdout
is delivered VERBATIM — the first byte is ALWAYS `#`, so no preamble/narration can
leak in (an LLM agent cannot be trusted to guarantee this).

Edit the paths / hints / group order to taste. Run standalone to preview:
    python3 sunday_inputs_digest.py
"""
import datetime
import os
import re
import sys
from pathlib import Path

VAULT = "/home/node/ICloud-vault"
INPUT_DIRS = [
    Path(VAULT) / "Projects/Inputs/Books",
    Path(VAULT) / "Projects/Inputs/Videos",
]
INDEX_FILES = {"Books.md", "Videos.md", "Input.md", "Inputs.md"}

# ---- frontmatter helpers -------------------------------------------------
# NOTE: the closing `---` may have NO trailing newline (e.g. `---![[img]]`),
# so anchor only on the opening + `\n---` close, not `\n---\s*\n`.
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def frontmatter_dict(text):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        out[key.strip().lower()] = val.strip().strip('"').strip("'")
    return out


def is_processed(fm):
    raw = (fm.get("processed") or "").lower().strip()
    return raw in {"true", "yes", "1"}  # anything else (false/no/missing) = unprocessed


# ---- classification -------------------------------------------------------
# Simple keyword rules approximate the keep / content / archive judgement.
CONTENT_HINTS = ["skool", "series", "vibe coding", "coding", "workflow",
                 "framework", "app", "pipeline", "prompt", "thumbnail", "tool",
                 "build", "warroom", "local model", "rss", "second brain"]
ARCHIVE_HINTS = ["sleep", "perfect sleep", "circadian", "reference"]


def classify(fname, first_lines):
    blob = (fname + "\n" + first_lines).lower()
    content = sum(1 for h in CONTENT_HINTS if h in blob)
    archive = sum(1 for h in ARCHIVE_HINTS if h in blob)
    if archive and not content:
        return "archive"
    if content:
        return "content"
    return "keep"


def clean_fname(name):
    return name[:-3].replace("_", " ") if name.endswith(".md") else name


def summarize(first_lines):
    """First substantive body line as a one-sentence snippet (strip markdown)."""
    lines = [l.strip() for l in first_lines.splitlines() if l.strip()]
    lines = [l for l in lines
             if not l.startswith("![[") and not l.startswith("https://")
             and not set(l) <= {"-", "*", "=", "#"} and not l.startswith("---")]
    if lines:
        text = re.sub(r"[#*_`>]", "", lines[0]).strip()
        if not text and len(lines) > 1:
            text = re.sub(r"[#*_`>]", "", lines[1]).strip()
        if text:
            return text[:107].rstrip() + "…" if len(text) > 110 else text
    return ""


# ---- gather notes (body ALWAYS sliced AFTER the frontmatter match) --------
notes = []  # {name, summary, cat}
for d in INPUT_DIRS:
    if not d.exists():
        continue
    for p in sorted(d.glob("*.md")):
        if p.name in INDEX_FILES:
            continue
        text = p.read_text(encoding="utf-8")
        if is_processed(frontmatter_dict(text)):
            continue
        m = FRONTMATTER_RE.match(text)
        body = text[m.end():] if m else text
        first = "\n".join(body.splitlines()[:30])
        notes.append({"name": clean_fname(p.name), "summary": summarize(first),
                      "cat": classify(p.stem, first)})

# ---- Sydney date ----------------------------------------------------------
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=10)))
date_label = now.strftime("%-d %b %Y") if os.name != "nt" else now.strftime("%d %b %Y")

# ---- build output (heading FIRST byte, closing sections kept) -------------
out = [f"# 📥 Sunday Inputs Digest — {date_label}", ""]
if not notes:
    out += ["(no unprocessed items)", "", "---", "",
            "**How to process:** To mark any done, open the note in Obsidian → in the frontmatter flip the `processed` toggle from `false` to `true`.",
            "", "**Tackle this first:** 🎯 All Inputs are processed ✅ — nothing to do this week."]
    print("\n".join(out)); sys.exit(0)

labels = {"content": "✨ Turn into content", "keep": "📌 Keep / process it", "archive": "📦 Archive it"}
for key in ("content", "keep", "archive"):  # content first = highest value
    group = [n for n in notes if n["cat"] == key]
    if group:
        out.append(f"**{labels[key]}**")
        for n in group:
            what = n["summary"] or n["name"]
            out.append(f"- **{n['name']}** — {what}")
        out.append("")

out += ["---", "",
        "**How to process:** To mark any of these done, open the note in Obsidian → in the frontmatter (top of the note), flip the `processed` toggle from `false` to `true` — it vanishes from next week's digest. No files were touched; this is suggestions only.",
        ""]

pick = next((n for cat in ("content", "keep", "archive") for n in notes if n["cat"] == cat), notes[0])
why = ("it's the one closest to shipping and maps directly onto your build/series work"
       if pick["cat"] == "content" else
       "it's the most actionable item still sitting in your Inputs" if pick["cat"] == "keep" else
       "it's the oldest / least active, so clear it to shrink the backlog")
out.append(f"**Tackle this first:** 🎯 **{pick['name']}** — {why}.")

print("\n".join(out))
