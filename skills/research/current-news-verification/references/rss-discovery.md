# Google News RSS discovery fallback

Use this when ordinary search is unavailable, client-rendered, or too noisy.
RSS identifies recent headlines and publishers; it is discovery evidence, not
a substitute for the linked article.

```python
import urllib.parse, urllib.request
import xml.etree.ElementTree as ET

query = urllib.parse.quote('person organization event date')
url = (
    'https://news.google.com/rss/search?q=' + query
    + '&hl=en-US&gl=US&ceid=US:en'
)
root = ET.fromstring(urllib.request.urlopen(url, timeout=20).read())
for item in root.findall('./channel/item')[:10]:
    print(item.findtext('title'))
    print(item.findtext('pubDate'))
    print(item.findtext('link'))
```

Run equivalent searches in the relevant local language. Record the literal
headline, source, and date. Follow the publisher URL before claiming details
not present in the RSS item, especially exact times. If no checked source gives
the requested precision, report that limitation explicitly instead of inferring
from article timestamps, travel timing, or the word “tomorrow.”
