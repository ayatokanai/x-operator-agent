import time


def filter_new_articles(feed_entries, last_run_ts):
    """前回実行時より後に公開された記事だけを抽出する"""
    new_articles = []
    for entry in feed_entries:
        # RSSの日付データをUNIXタイムスタンプに変換して比較
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            article_ts = time.mktime(entry.published_parsed)
            if article_ts > last_run_ts:
                new_articles.append(entry)
    return new_articles
