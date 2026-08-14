---
name: hermes-agent-display
description: "Change the display name (agent name) shown by Hermes Agent."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, display, configuration]
    related_skills: [hermes-agent]
---

# Change Hermes Agent Display Name

This skill provides the canonical workflow for renaming the Hermes Agent that appears in greetings, status lines, and UI elements.

## When to use
- You want the agent to introduce itself with a custom name (e.g., "Perth Bot").
- You need to persist the name across sessions and restarts.
- You tried `hermes config set display.agent_name …` and saw a warning that the key is unrecognized.

## Steps
1. **Create a personal skin**
   ```bash
   mkdir -p ~/.hermes/skins
   cp ~/.hermes/skills/autonomous-ai-agents/hermes-agent/templates/skin.yaml \
      ~/.hermes/skins/<your-skin>.yaml   # replace <your-skin> with a short name
   ```
2. **Edit the `agent_name` field**
   Open the copied skin and change the line:
   ```yaml
   agent_name: Your Desired Name
   ```
   Example:
   ```yaml
   agent_name: Perth Bot
   ```
3. **Activate the skin**
   ```bash
   hermes config set display.skin <your-skin>
   ```
   Replace `<your-skin>` with the filename without the `.yaml` extension.
4. **Restart / reset Hermes**
   - Either start a new Hermes session (`hermes`), or inside a running session type `/reset`.
   - The new name will appear in all subsequent greetings.

## Pitfalls & Gotchas
- **Do not use** `hermes config set display.agent_name …`. This key is not recognized and Hermes will ignore it (you’ll get a warning). The correct way is via the skin’s `agent_name` field.
- Editing the built‑in skin (`templates/skin.yaml` inside the `hermes-agent` skill) will be overwritten on skill updates. Always copy it to `~/.hermes/skins/` first.
- After changing the skin, a running session won’t pick up the change until you reset or start a new session.

## Reference
- See the full reference file `references/rename-agent.md` for a concise cheat‑sheet.
