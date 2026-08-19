# YouTube metadata fallback

When transcript retrieval is unavailable, a public YouTube oEmbed request can verify basic metadata without claiming to have reviewed the full video.

Example:

```python
import requests
url = "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=VIDEO_ID&format=json"
r = requests.get(url, timeout=30)
r.raise_for_status()
metadata = r.json()
print(metadata["title"], metadata["author_name"], metadata["author_url"])
```

Use the returned title, channel, channel URL, thumbnail, and canonical video URL as source metadata. Treat any interpretation of the video's argument as a proposed editorial angle unless the transcript or another reliable content source was actually retrieved. Keep the original user URL in the draft when that is their established citation style.
