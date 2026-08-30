import trafilatura


def fetch_article_body(url: str) -> str:
    """Webページから広告等を除去して本文テキストを抽出"""
    if not url:
        return ""

    downloaded = trafilatura.fetch_url(url)
    if downloaded:
        text = trafilatura.extract(downloaded)
        return text if text else ""
    return ""
