from services.rss import filter_new_articles
import feedparser
from config import RSS_URL
import json
from datetime import datetime, timezone

from config import WEBHOOK_URL
from services.ai import evaluate_titles, inspect_article_body, write_post
from services.webhook.discord import send_post_draft
from utils.db import get_last_run_timestamp, update_last_run_timestamp, save_article_draft
from utils.web import fetch_article_body


def lambda_handler(event, context):
    # NOTE: 暫定的に定数
    account_id = "x_0011"

    last_run_ts = get_last_run_timestamp(account_id)

    # 処理の基準となる「現在時刻」を記録
    current_ts = datetime.now(timezone.utc).timestamp()

    feed = feedparser.parse(RSS_URL)
    new_articles = filter_new_articles(feed.entries, last_run_ts)

    evaluate_titles_result = evaluate_titles(new_articles)
    for title_evaluation in evaluate_titles_result.get_qualified():
        article = new_articles.get(title_evaluation.id, {})

        body = fetch_article_body(article.get("url"))
        content_evaluation = inspect_article_body(
            article_title=article.get("title"),
            article_body=body
        )

        if not content_evaluation.is_adopted:
            # 本文精査の結果不採用
            continue

        generated_post = write_post(
            article_title=article.get("title"),
            article_body=body
        )

        send_post_draft(
            webhook_url=WEBHOOK_URL,
            title=article.get("title"),
            source_url=article.get("url"),
            post_text=generated_post.post_text,
            interest_score=content_evaluation.interest_score,
            screening_reason=title_evaluation.reason,
            reply_thread_text=generated_post.reply_thread_text,
            manual_action=generated_post.manual_action
        )

        save_article_draft(
            account_id=account_id,
            source_url=article.get("url"),
            title_evaluation=title_evaluation,
            generated_post=generated_post
        )

    update_last_run_timestamp(account_id, current_ts)

    return {"statusCode": 200, "body": json.dumps("Finished")}


if __name__ == "__main__":
    # ローカル実行時のエントリーポイント
    lambda_handler(event={}, context=None)
