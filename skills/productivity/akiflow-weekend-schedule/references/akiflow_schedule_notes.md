# Akiflow schedule notes

During a recent session the assistant repeatedly called `tool_describe` for `mcp__akiflow__get_schedule`, which added unnecessary latency and clutter. The updated skill now:

- Calls the tool directly.
- Checks for an empty result set and reports “no events” instead of fabricating data.
- Includes a brief pitfall reminding developers to avoid redundant `tool_describe` calls.

Following this pattern keeps the interaction fast and the output concise, matching the user’s preference for brevity.
