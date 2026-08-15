---
name: api-secret-hygiene
description: "Use when API keys leak: host safely, purge Hermes DB/FTS."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [secrets, api-keys, credentials, security, cleanup, database]
    related_skills: [github-auth]
---

# Third-Party API Secret Handling in Hermes

## When to Use
- A user pastes a third-party API key / OAuth token into chat (BigMarker, Stripe, Twilio, any REST provider)
  and you need to connect to that provider safely.
- A pasted secret leaked into Hermes persistence (logs, state DB, FTS search, session history) and needs purging.

Use when a user pastes a third-party API key/token (BigMarker, Stripe, Twilio, any REST provider) into the
Hermes chat and you need to connect to that provider, host the secret safely on this instance, and/or scrub
the secret after it leaked into a chat-facing artifact.

Two distinct jobs this skill covers:
1. **Safe hosting** — store the pasted secret so it isn't re-exposed.
2. **Leak purge** — when a secret was typed into chat, remove it from Hermes' persistence.

## Safe hosting (do this as soon as you hold a real key)

Never keep a pasted key in chat-derived logs or in shell history as the working copy. Move it into an
owner-only, git-ignored file under a persistent path, then read it via env/flag for every call.

```bash
# Persistent, owner-only, git-ignored secret store on this machine
mkdir -p ~/<project>            # under $HOME (survives restarts on Agent37; $HOME is persistent)
umask 077
cat > ~/<project>/.env.<provider> <<EOF
<PROVIDER>_API_KEY=<the-key>
EOF
chmod 600 ~/<project>/.env.<provider>
echo '.env' > ~/<project>/.gitignore   # never commit the secret
```

- **Persistent path:** on Agent37 only `$HOME` (`/home/node` here) and `/home/linuxbrew` survive
  container restarts; anything elsewhere (e.g. `/tmp`) is wiped. Keep the secret in `$HOME`.
- **Call pattern:** `KEY=$(grep '^PROVIDER_API_KEY=' ~/<project>/.env.<provider> | cut -d= -f2)` then
  `curl -sS -H "API-KEY: $KEY" ...`. Prefer env var / reading the file over pasting the literal into
  commands that land in process listings.
- **Rotate advice:** once a secret has been pasted into a chat platform (Discord/Telegram log persists), tell
  the user it's technically compromised and recommend rotating it in the provider dashboard. It's cheap
  insurance even after you scrub local copies.

## Leak purge: the key is already in Hermes persistence

When a user pastes a secret into chat, it automatically lands in Hermes' SQLite state DB — the `messages`
table (columns `content`, `tool_calls`, `api_content`) AND the two Full-Text-Search indexes
(`messages_fts`, `messages_fts_trigram`). It also appears in `~/.hermes/logs/gateway.log` and `agent.log`
because those capture the raw message stream.

### PITFALL — the self-perpetuation loop
Every assistant message that quotes the secret's literal characters writes a NEW copy into `messages` + FTS.
So scrubbing is never "done" while you keep typing the key into your own replies/tool calls. Sequence the
scrub so that the *final* scrub runs after the last message that needs the literal, and thereafter **reference
the key only by its location/role, never by its characters** ("the key in ~/bigmarker/.env.bm", "the provider
API token"), or you will re-pollute the DB and a follow-up sweep will see it again.

### Scrub procedure (verified working)

```bash
cd ~/.hermes

# 1. Remove plaintext from the log files
for f in logs/gateway.log logs/agent.log; do
  sed -i "s/$KEY/***REDACTED***/g" "$f" 2>/dev/null
done

# 2. Scrub the messages table (every text-bearing column) + rebuild BOTH fts indexes
python3 - <<'PY'
import sqlite3
con = sqlite3.connect('state.db')
key = '...'          # the literal key, read from your .env, not typed
red = '[REDACTED]'
cols = [r[1] for r in con.execute('PRAGMA table_info(messages)')]
for c in cols:
    con.execute(f'UPDATE messages SET {c}=REPLACE(CAST({c} AS TEXT),?,?) WHERE CAST({c} AS TEXT) LIKE ?',
                (key, red, '%'+key+'%'))
con.commit()
for tbl in ('messages_fts', 'messages_fts_trigram'):   # must rebuild BOTH; trigram indexes substrings
    con.execute(f"INSERT INTO {tbl}({tbl}) VALUES('rebuild')")
con.commit()
# verify
k = '...'
print('messages:', con.execute("SELECT COUNT(*) FROM messages WHERE content LIKE ? OR tool_calls LIKE ? OR api_content LIKE ?",
      ('%'+k+'%','%'+k+'%','%'+k+'%')).fetchone()[0])
for tbl in ('messages_fts','messages_fts_trigram'):
    print(tbl, con.execute(f'SELECT COUNT(*) FROM {tbl} WHERE {tbl} MATCH ?',(k,)).fetchone()[0])
PY
```

### PITFALL — DB backups retain the key
If you took a `cp state.db state.db.bak-*` before scrubbing, that backup still holds the plaintext key and
your disk sweep will keep matching it. Delete the backup once the live DB is verified clean.

### Verification + full sweep
After the scrub, confirm the plaintext exists in exactly ONE place (the .env safe store):

```bash
grep -rpl "$KEY" "$HOME" /tmp /home/linuxbrew 2>/dev/null   # expect only the .env.<provider>
```

Note the sweep will re-match `state.db` temporarily if you then type the key into another chat message — that
is the loop above, not a failed scrub. Verify with the final no-literal message and stop there.

## Secret audit: find OTHER credentials already in persistence

When a pasted key leaks, the user often asks "are there OTHER keys sitting in here too?" (GitHub PATs, bot
tokens, Composio/OpenAI keys, SSH keys, etc.). Run an audit before or alongside the targeted purge.

Use `scripts/scan-secrets.py` (re-runnable sweep over logs + all `messages` text columns) as a starting probe,
then triage each hit.

### PITFALL — loose regexes produce false positives
A lazy catch-all like `c[xoma][a-zA-Z0-9]{20,}` matches ordinary words and hex substrings (e.g. a random
`ca38c1da...` inside an unrelated long token). Require a provider-specific prefix AND a realistic length, then
verify surrounding context before treating it as a secret to scrub.

### PITFALL — SSH keys: public half is NOT secret
`ssh-ed25519 AAAA...` / `ssh-rsa AAAAB...` lines are the PUBLIC half, deliberately shareable. Leave them
intact. Only `-----BEGIN ... PRIVATE KEY-----` is sensitive. The scan script watches only for the PRIVATE
header for this reason.

### PITFALL — ephemeral vs long-lived tokens
`ocst.<token>` prefixed strings are short-lived Composio *OAuth-exchange* tokens (transient, appear in a
tool-config snapshot), not durable user secrets. Still worth scrubbing for hygiene, but don't rank them as
equivalent to a GitHub PAT. `cx_` is the longer-lived Composio key format.

### PITFALL — audit text re-pollutes, same as scrubbing
Your own diagnostic messages that literally type `ghp_`, `ocst.`, or a masked `ghp_BZaq***` placeholder are
NOT real secrets. A strict "full-length token" regex (prefix + 30+ chars) discriminates real from these
emissions; your final reply should not retype the literal.

### Discriminating live token from placeholder
Verbatim placeholders like `ghp_…`, `ghp_...`, `ghp_BZaq***` (agent-typed while investigating) are harmless.
Confirm a real secret exists only by matching prefix + realistic length across ALL text columns and logs;
0 matched tokens == genuinely clean, regardless of placeholder strings in history.

## Non-goals / cautions
- Do NOT capture this as "the DB scrub is broken" — the reset then status 0 means the scrub worked AND new
  copies were written; the lesson is to stop emitting the literal, not that scrubbing failed.
- Logs and the public chat thread cannot be fully erased by you; say so frankly and recommend rotation.
- If the provider is in Composio's catalog, prefer the Composio OAuth connection (managed, user never pastes
  the key into chat) over key-pasting at all. Only fall back to an API key when no Composio integration exists.
