# Remote MCP Authentication and Cancellation

## Validated session pattern

For a remote server such as `https://mcp.lennysdata.com/mcp`:

1. Check the command surface with `hermes mcp --help` and `hermes mcp add --help`.
2. Attempt the native add command:
   ```bash
   hermes mcp add lenny --url https://mcp.lennysdata.com/mcp --connect-timeout 30
   ```
3. If the endpoint returns `401 Unauthorized`, the server requires authentication. Do not claim success and do not invent an API key or bearer token.
4. Because the add flow may be interactive and may offer to save configuration after a failed connection, verify actual state with:
   ```bash
   hermes mcp list
   ```
5. If the user cancels or changes their mind, only run `hermes mcp remove lenny` when `lenny` appears in that list. Otherwise report that no saved entry exists.

## Reporting states separately

- **Attempted:** the add command was invoked.
- **Saved:** the server appears in `hermes mcp list`.
- **Connected:** `hermes mcp test <name>` succeeds.
- **Available:** Hermes has restarted or rediscovered the server's tools.

Do not collapse these into a single claim such as “connected” unless each relevant state has been verified.
