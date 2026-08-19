# YouTube source fallback

## Evidence boundary

When transcript retrieval fails because the request is blocked, do not infer that captions are disabled and do not write a detailed summary. Use a verified public metadata endpoint such as YouTube oEmbed to establish only:

- video title;
- channel/author and channel URL;
- video ID and canonical watch URL;
- thumbnail URL, if useful.

## Draft behavior

Create a source scaffold with verified metadata, investigation questions, and a clearly labeled tentative editorial angle. Add a note that transcript-level details remain unverified. If the user later supplies a transcript or asks for manual review, replace the scaffold with grounded notes and preserve the original source link.

## Example oEmbed request

```text
https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=VIDEO_ID&format=json
```

Treat the response as source metadata, not as evidence of the video's spoken content.
