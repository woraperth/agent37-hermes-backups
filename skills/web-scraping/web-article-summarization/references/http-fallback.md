# HTTP fallback for blocked browser extraction

Use this fallback when browser navigation is unavailable, returns a harness/setup error, or a public article rejects the default Python user-agent.

```bash
curl -L --fail --retry 2 -A 'Mozilla/5.0' -o /tmp/article.html 'https://example.com/article'
```

Then parse the saved UTF-8 HTML using the same selector priority as the browser path: `article`, `.elementor-widget-theme-post-content`, `.post-content`, `.entry-content`, and `main`. If no HTML parser dependency is available, use Python's stdlib `html.parser` and ignore `script`, `style`, `noscript`, and `svg` content. Prefer the candidate with the most text. This worked for a public DataTH WordPress article that returned HTTP 403 to `urllib` but succeeded with `curl` and a browser-like user-agent.
