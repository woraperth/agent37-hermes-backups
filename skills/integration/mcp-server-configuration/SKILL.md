---
name: mcp-server-configuration
description: "Use when managing Hermes MCP server connections."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [mcp, hermes, integrations, configuration, authentication]
---

# MCP Server Configuration

Use this skill when a user asks Hermes Agent to connect to an MCP server, test an MCP connection, authenticate an MCP server, or remove a previously configured server.

## Workflow

1. **Inspect the available CLI before acting.** Run `hermes mcp --help` and, when needed, `hermes mcp add --help`, `hermes mcp test --help`, or `hermes mcp remove --help`. Prefer the native `hermes mcp` commands over hand-editing YAML.
2. **Use a stable, descriptive server name.** Names become configuration keys and tool prefixes. For example, use `lenny`, not a URL or a temporary label.
3. **Add the server with the correct transport.** For a remote HTTP/Streamable HTTP endpoint, use:
   ```bash
   hermes mcp add <name> --url <endpoint> --connect-timeout <seconds>
   ```
   For stdio servers, use `--command`, followed by `--args` as the final option. Do not put secrets in command-line history when a safer supported auth/config path exists.
4. **Handle authentication explicitly.** A `401 Unauthorized` means the endpoint requires credentials. Do not guess, fabricate, or silently reuse a token. Ask the user for the supported credential or OAuth direction. If the user has not provided credentials, do not claim the server was connected.
5. **Verify state after any add/remove attempt.** Run `hermes mcp list`. A server is configured only if it appears in the list. If it appears, run `hermes mcp test <name>` when the user wants connection verification.
6. **Honor cancellation immediately.** If the user changes their mind, first run `hermes mcp list`; remove the named server only if it is present, using `hermes mcp remove <name>` (or `rm`). Then verify with `hermes mcp list` again. If it is absent, report that no removal was needed rather than inventing a removal result.
7. **Restart Hermes when required by the active implementation.** MCP discovery is generally performed at startup; after configuration changes, restart the relevant Hermes process before expecting newly discovered tools in an already-running session.

## Safety and reporting

- Never hand-edit `config.yaml` for the user when a native CLI command exists.
- Distinguish among: add command attempted, configuration saved, connection authenticated, and tools discovered. These are separate states.
- If an interactive add command reaches an auth or save prompt, treat the resulting configuration as unknown until `hermes mcp list` confirms it.
- Report the exact verified state concisely, especially after a cancellation.

## Reference

See `references/remote-mcp-auth-and-cancellation.md` for a concise reproduction and reporting checklist based on a remote endpoint that returned 401 during setup.
