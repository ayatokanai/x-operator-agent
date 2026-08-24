import os

# AWS関連
DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE", "x-operator-agent-table")
REGION = os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1")

# 外部API関連
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# アプリケーション設定
RSS_URL = "https://news.yahoo.co.jp/rss/categories/it.xml"
