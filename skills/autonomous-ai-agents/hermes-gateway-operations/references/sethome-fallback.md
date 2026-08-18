# `/sethome` fallback: verified pattern

## Trigger

Use this only when the user explicitly asks to set the current gateway chat as home, but the inbound message reached the agent as ordinary text instead of being dispatched as the native `/sethome` command.

## Verified sequence

1. Read the current event metadata from the session context/logs: logical platform, `chat_id`, chat name, user ID, scope ID, and thread ID. Never infer an ID from a display name.
2. Inspect the installed Hermes gateway implementation for the current version. The handler constructs `gateway.config.HomeChannel`, calls `persist_home_channel(home, enabled_if_new=...)`, preserves legacy home environment variables, and updates the running gateway config.
3. Reuse the installed helper and its thread-normalization logic rather than hand-editing YAML or reproducing platform-specific assumptions.
4. Verify the resulting active config has the expected `platforms.<platform>.home_channel` fields. Keep secrets and raw config out of the user-facing response.

## Discord note

For a Discord thread, the gateway event may expose the thread ID as the chat target. Preserve the event's exact `chat_id` and do not silently substitute the parent channel. Whether a thread ID belongs in `home_channel.thread_id` is determined by the installed handler; do not guess.

## What not to do

- Do not claim that an assistant response containing `/sethome` will execute the gateway command.
- Do not invent `hermes gateway sethome` without checking the installed CLI help.
- Do not edit `config.yaml` with a text editor for this operation.
- Do not report success until the persisted target is verified.
