import feedparser
from bs4 import BeautifulSoup

RSS_URL = "https://techcrunch.com/feed/"

def fetch_latest_news():
    """
    Fetches the latest 3 articles from TechCrunch RSS feed.
    """
    feed = feedparser.parse(RSS_URL)
    articles = []

    # Loop through the first 3 entries
    for entry in feed.entries[:3]:
        # Clean HTML tags from the summary (RSS often has <p> tags)
        summary_text = BeautifulSoup(entry.summary, "html.parser").get_text()
        
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "summary": summary_text,
            "published": entry.published
        })
    
    return articles