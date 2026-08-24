import json
from datetime import datetime, timezone

import feedparser

from config import RSS_URL, WEBHOOK_URL
from services.ai import evaluate_and_generate
from services.rss import filter_new_articles
from utils.db import get_last_run_timestamp, update_last_run_timestamp


def lambda_handler(event, context):
    print("=== 1. 前回実行日時の取得 ===")
    last_run_ts = get_last_run_timestamp()
    print(f"前回実行日時: {datetime.fromtimestamp(last_run_ts, timezone.utc)}")

    # 処理の基準となる「現在時刻」を記録
    current_ts = datetime.now(timezone.utc).timestamp()

    print("#" * 100)
    print(RSS_URL)
    feed = feedparser.parse(RSS_URL)
    new_articles = filter_new_articles(feed.entries, last_run_ts)

    for entry in new_articles:
        article_url = entry.link
        title = entry.title
        summary = entry.get("summary", "")
        print("=" * 40)
        print(f"Processed successfully: {title}")
        print(f"Processed successfully: {article_url}")
        print(f"Processed successfully: {summary}")
        # break  # 1回の実行で1件処理して終了

    print("=== 3. AIによる価値評価と選定 ===")
    ai_result = evaluate_and_generate(new_articles)

    print("\n【AIの出力結果】\n")
    print(ai_result)
    print("\n")

    print("=== 投稿履歴と実行日時の保存 ===")
    print(current_ts)
    # save_posted_history(new_articles, ai_result, current_ts)
    update_last_run_timestamp(current_ts)

    return {"statusCode": 200, "body": json.dumps("Finished")}


def send_webhook(title, url, draft):
    print("WEBHOOK SEND TODO")

    if not WEBHOOK_URL:
        print("WEBHOOK_URL is not configured.")
        return

    # payload = {
    #     "content": f"📢 **【X投稿 下書き案】**\n\n{draft}\n\n🔗 元記事: {url}"
    # }
    # req = urllib.request.Request(
    #     WEBHOOK_URL,
    #     data=json.dumps(payload).encode("utf-8"),
    #     headers={"Content-Type": "application/json", "User-Agent": "Lambda-Bot"}
    # )
    # urllib.request.urlopen(req)


if __name__ == "__main__":
    # ローカル実行時のエントリーポイント
    lambda_handler(event={}, context=None)
