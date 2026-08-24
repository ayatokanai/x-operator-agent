import os
import time
import json
import urllib.request
import feedparser
import boto3

# 環境変数の読み込み
# DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE", "x-operator-agent-table")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
LLM_API_KEY = os.environ.get("LLM_API_KEY")
RSS_URL = "https://news.yahoo.co.jp/rss/topics/it.xml"

# dynamodb = boto3.resource("dynamodb")
# table = dynamodb.Table(DYNAMODB_TABLE)

def lambda_handler(event, context):
    print("#"*100)
    print(RSS_URL)
    feed = feedparser.parse(RSS_URL)
    
    for entry in feed.entries[:5]:
        article_url = entry.link
        title = entry.title
        summary = entry.get("summary", "")
        
        # # 1. DynamoDBで重複チェック
        # res = table.get_item(
        #     Key={"PK": "ACCOUNT#tech_news_ja", "SK": f"ARTICLE#{article_url}"}
        # )
        # if "Item" in res:
        #     continue
        
        # # 2. 投稿ドラフト生成 (検証用フォーマット)
        # post_draft = f"【注目ニュース】\n{title}\n\n要約: {summary[:80]}...\n#TechNews"
        
        # # 3. Discord / Slack へWebhook通知
        # send_webhook(title, article_url, post_draft)
        
        # # 4. DynamoDBに履歴保存 (30日TTL)
        # ttl_expire = int(time.time()) + (30 * 24 * 60 * 60)
        # table.put_item(
        #     Item={
        #         "PK": "ACCOUNT#tech_news_ja",
        #         "SK": f"ARTICLE#{article_url}",
        #         "post_draft": post_draft,
        #         "created_at": int(time.time()),
        #         "ttl": ttl_expire
        #     }
        # )
        print("="*40)
        print(f"Processed successfully: {title}")
        print(f"Processed successfully: {article_url}")
        print(f"Processed successfully: {summary}")
        print("="*40)
        break  # 1回の実行で1件処理して終了

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
