---
name: extract-x-tweets
description: "Extract recent X tweets via browser or Composio API."
version: 1.0.0
author: Hermes Agent
license: MIT
---
# Overview
This skill explains two reliable ways to obtain recent tweet texts from a public X/Twitter profile:

* **Browser automation** – works without authentication for the latest ~20 tweets.
* **Composio X/Twitter API** – preferred for larger batches (up to 100+ tweets) and when headless browsers are blocked.

---
## Browser automation
```text
1. Install Chromium and symlink it as `google-chrome` for the browser harness:
   sudo apt-get update && sudo apt-get install -y chromium
   sudo ln -s /usr/bin/chromium /usr/local/bin/google-chrome
2. Open the profile:
   new_tab('https://x.com/@USERNAME')
   wait_for_load()
3. Wait for tweet elements `[data-testid="tweetText"]` to appear – use a retry loop.
4. Extract texts:
   js('Array.from(document.querySelectorAll("[data-testid=\"tweetText\"]")).map(e=>e.innerText);')
5. Scroll down (`js('window.scrollBy(0, window.innerHeight);')`) and repeat until the desired number of tweets is collected.
6. Save to JSON.
```
### Pitfalls
- Dynamic loading may return empty results immediately; retry.
- X may display a login wall or CAPTCHA for headless browsers – fall back to the API.
- Without authentication only the most recent ~20 tweets are visible.

---
## Composio X/Twitter API
1. Discover the tool:
   ```json
   {"queries":[{"use_case":"fetch recent tweets for a X user","known_fields":"username:USERNAME,limit:100"}],"session":{"generate_id":true}}
   ```
   Call `COMPOSIO_SEARCH_TOOLS`.
2. Retrieve the tool slug (e.g., `X_TWITTER_GET_TWEETS`) and its input schema via `COMPOSIO_GET_TOOL_SCHEMAS`.
3. If no active connection exists, run `COMPOSIO_MANAGE_CONNECTIONS` for the `x_twitter` toolkit and have the user complete the OAuth flow.
4. Execute the fetch tool with `username` and `limit`.
5. Extract the `text` field from each tweet object and store as JSON.

### Pitfalls
- Requires user‑authorised connection on first use.
- Respect API rate limits.
- Always fetch the latest schema before invoking.

---
## Choosing a method
- Use **browser automation** for quick checks of ≤20 recent tweets when you cannot obtain a Composio connection.
- Use **Composio API** for reliable, larger batches or automated pipelines.

---
# References
- `references/chromium-setup.md`
- `references/typefully-mcp.md`
