---
name: hermes-gateway-operations
description: "Use when operating Hermes messaging gateway settings."
version: 1.0.0
license: MIT
author: Hermes Agent
metadata:
  hermes:
    tags: [hermes, gateway, discord, messaging, home-channel, cron-delivery]
---

# Hermes Gateway Operations

## When to Use

Use this skill for Hermes gateway configuration, platform routing, home-channel setup, and verification of scheduled-message destinations.

Use when a user asks to configure or verify a Hermes messaging-gateway behavior (especially setting a Discord/Telegram home channel, routing scheduled deliveries, or checking gateway state). Prefer the gateway's native slash-command path and verify persisted state after any change.

## Workflow

1. **Load Hermes guidance first.** For Hermes-specific work, consult the bundled `hermes-agent` skill. Its `references/slash-commands.md` is the authoritative reference for gateway-only commands such as `/sethome`; it is not duplicated in this skill. Treat live `/help` and installed source/docs as authoritative when they differ.
2. **Classify the request.** Gateway commands are platform-side commands. An instruction such as “use `/sethome`” is not the same as an agent reply containing `/sethome`; the latter does not reliably re-enter the gateway command dispatcher.
3. **Prefer the native command.** In the target chat, send the exact command `/sethome` (or `/set-home` where supported). Do not invent a standalone CLI subcommand unless `hermes --help` confirms one.
4. **If the command arrived as ordinary text and the user explicitly authorized the action, use the installed gateway implementation rather than hand-editing YAML.** Resolve the active Hermes home/profile, construct the platform’s `HomeChannel`, call the installed persistence helper, and preserve any legacy environment variables required by the running version. Use the platform/chat identifier and user provenance supplied by the gateway event; do not guess IDs.
5. **Verify.** Confirm the active config contains the expected platform, `home_channel.chat_id`, and (when applicable) thread/user/scope provenance. Check gateway logs or status if delivery behavior matters. Avoid exposing secrets or dumping raw config into chat.
6. **Report concisely.** State what changed and the destination in a user-safe form; do not paste raw YAML, tokens, or verbose tool output.

## Safety and pitfalls

- Never hand-edit `config.yaml` for routine Hermes changes; use the supported command, config CLI, or installed persistence helper.
- A Discord thread is itself a channel target in many gateway events. Preserve the event's `chat_id` and thread semantics exactly; do not silently replace it with a parent channel ID.
- Do not persist a synthetic per-message thread as the home target. The installed handler's thread-normalization logic is platform-specific; reuse it instead of duplicating assumptions.
- Keep platform enablement and home-channel persistence separate: setting a home target should not accidentally disable the platform.
- A successful local write is not proof that the running gateway has reloaded it. If the gateway is long-lived, ensure its in-memory configuration is refreshed or restart it only when appropriate and authorized.

## Reference

- See `references/sethome-fallback.md` for the verified fallback pattern used when a user's natural-language request reaches the agent instead of the gateway dispatcher.
