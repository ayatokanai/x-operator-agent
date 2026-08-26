import time


def filter_new_articles(feed_entries, last_run_ts):
    """前回実行時より後に公開された記事だけを抽出する"""
    new_articles = {}
    for idx, entry in enumerate(feed_entries, start=1):
        if idx > 3: break
        # RSSの日付データをUNIXタイムスタンプに変換して比較
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            article_ts = time.mktime(entry.published_parsed)
            if article_ts > last_run_ts:
                id = f"art_{idx}"
                new_articles[id] = {
                    "title": entry.title,
                    "summary": entry.get("summary", ""),
                    "url": entry.link
                }
    return new_articles
