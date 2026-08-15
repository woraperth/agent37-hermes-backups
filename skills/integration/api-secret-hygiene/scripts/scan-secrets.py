#!/usr/bin/env python3
"""Scan Hermes persistence (logs + state.db) for LIVE credential patterns.

Use during a secret audit: after one pasted key leaks, the user may ask whether OTHER
credentials (GitHub PATs, bot/Discord tokens, Composio keys, SSH private keys, etc.)
are also sitting in logs / the message DB.

Designed to report ONLY live full-length tokens, NOT placeholders/diagnostic text.
A loose regex like "c[xoma][a-z0-9]{20,}" matches random words and hex substrings —
require a realistic provider-specific prefix AND realistic length, and ALWAYS eyeball
surrounding context before deciding something is a real secret.

Run:  python3 scan-secrets.py
"""
import sqlite3, re, glob, os

sources = {}

# All text from every text-bearing column of the messages table
con = sqlite3.connect(os.path.expanduser('~/.hermes/state.db'))
cols = [r[1] for r in con.execute('PRAGMA table_info(messages)') if not r[1].endswith('_fts')]
dbtext = ""
for c in cols:
    for (v,) in con.execute(f'SELECT {c} FROM messages'):
        if v:
            dbtext += "\n" + str(v)
sources["DB"] = dbtext

for f in glob.glob(os.path.expanduser('~/.hermes/logs/*.log')):
    try:
        sources["log:" + os.path.basename(f)] = open(f, encoding='utf-8', errors='ignore').read()
    except OSError:
        pass

# Live-token patterns. Length thresholds reject the masked/placeholder strings
# (e.g. "ghp_...", "ghp_BZaq***") that an agent's own diagnostic messages emit.
patterns = {
    "GitHub PAT (live full)":        r"gh[pousr]_[A-Za-z0-9]{30,}",
    "OpenAI sk-":                    r"sk-[A-Za-z0-9]{20,}",
    "Discord bot token":             r"[A-Za-z0-9]{24,}\.[A-Za-z0-9]{6,}\.[A-Za-z0-9]{27,}",
    "Composio cx_":                  r"cx_[A-Za-z0-9]{20,}",
    "Composio ocst. OAuth-exchange": r"ocst\.[A-Za-z0-9._-]{20,}",
    "Anthropic sk-ant":              r"sk-ant-[A-Za-z0-9]{15,}",
    "Slack xox":                     r"xox[baprs]-[0-9A-Za-z\-]{20,}",
    "Google AIza":                   r"AIza[0-9A-Za-z_\-]{30,}",
    "Stripe sk_live":                r"sk_live_[0-9a-zA-Z]{15,}",
    "AWS AKIA":                      r"AKIA[0-9A-Z]{16}",
    "SSH PRIVATE key (BEGIN ...)":   r"BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY",
}

# NOTE on SSH: a PUBLIC key line (ssh-ed25519 AAAA..., ssh-rsa AAAAB...) is designed to be
# shared and is NOT a secret — leave it alone. Only BEGIN ... PRIVATE KEY is sensitive.

hits = 0
for name, blob in sources.items():
    found = []
    for label, rx in patterns.items():
        for m in re.finditer(rx, blob):
            v = m.group(0)
            found.append(f"  {label}: {v[:10]}*** (len {len(v)})")
    if found:
        hits += 1
        print(f"\n>>> {name}: {len(found)} live-secret match(es)")
        for x in sorted(set(found)):
            print(x)

if not hits:
    print(">> No live secrets found in DB or any log. Clean.")
print("\n== sweep complete ==")
