# Cloud-hosted YouTube transcript access

## Observed access signatures

For a public YouTube video, cloud hosting can return `RequestBlocked`/`IpBlocked` from `youtube-transcript-api`; `yt-dlp` may instead report “Sign in to confirm you’re not a bot”. These errors identify the access path as the problem; they do not prove the video has no captions. Stop retrying the same cloud IP.

## Decision tree

1. Use a rotating residential/ISP proxy with `youtube-transcript-api` (`WebshareProxyConfig` or `GenericProxyConfig`) for server-side automation. Static/free proxies are less reliable and may be blocked.
2. Use a hosted transcript provider with an API key, such as [TranscriptAPI](https://transcriptapi.com/) or [Supadata](https://supadata.ai/youtube-transcript-api). Verify the target video and require a non-empty transcript before accepting it.
3. Run `yt-dlp` locally on the user's own machine with `--cookies-from-browser` and subtitle options. Browser cookies are session credentials: never ask users to upload them through chat.
4. Do not recommend the official `captions.list` endpoint for arbitrary third-party videos: Google's docs require OAuth authorization and caption-resource access.

## Evidence and source links

- `youtube-transcript-api` documents cloud-provider IP blocking and recommends rotating residential proxies: https://github.com/jdepoix/youtube-transcript-api#working-around-ip-bans-requestblocked-or-ipblocked-exception
- `yt-dlp` documents browser-cookie loading and current YouTube extractor options: https://github.com/yt-dlp/yt-dlp#cookies
- YouTube Data API captions authorization requirements: https://developers.google.com/youtube/v3/docs/captions/list
- Hosted API endpoint checks without credentials returned authentication errors during the research session; do not describe them as free/no-key solutions.

## Evidence boundary

If no authenticated or proxy-backed path is available and no transcript was actually retrieved, preserve only verified metadata (title, channel, URL) and say that transcript-level claims are unverified.
