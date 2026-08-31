import uuid
import time
from datetime import datetime, timedelta, timezone

import boto3

from config import DYNAMODB_TABLE, REGION
from services.ai.schemas import GeneratedPost
from services.ai.schemas import TitleEvaluation

dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table(DYNAMODB_TABLE)


def get_last_run_timestamp():
    """DynamoDBから前回の実行日時（UNIXタイムスタンプ）を取得する"""
    try:
        response = table.get_item(Key={"id": "SYSTEM:LAST_RUN"})
        if "Item" in response:
            return float(response["Item"]["timestamp"])
    except Exception as e:
        print(f"DB読み込みエラー: {e}")

    # 初回実行時やデータがない場合は、24時間前をデフォルト値とする
    return (datetime.now(timezone.utc) - timedelta(days=1)).timestamp()


def update_last_run_timestamp(account_id, now_timestamp):
    """今回の実行日時をDynamoDBに記録する"""
    table.put_item(
        Item={
            "PK": f"ACCOUNT#{account_id}",
            "SK": "SYSTEM:LAST_RUN",
            "type": "config",
            "timestamp": str(now_timestamp),
        }
    )


def save_article_draft(account_id: str,
                       source_url: str,
                       title_evaluation: TitleEvaluation,
                       generated_post: GeneratedPost):
    now_iso = datetime.now(timezone.utc).isoformat()

    id = uuid.uuid4()
    pk = f"ACCOUNT#{account_id}"
    sk = f"POST#{id}"
    
    # 90日後に自動削除するTTL（Unix Timestamp）
    ttl_timestamp = int(time.time()) + (90 * 24 * 60 * 60)

    item = {
        "PK": pk,
        "SK": sk,
        "GSI1PK": "STATUS#DRAFT_PENDING",
        "GSI1SK": f"CREATED_AT#{now_iso}",
        "status": "DRAFT_PENDING",
        "source_url": source_url,
        "interest_score": title_evaluation.interest_score,
        "screening_reason": title_evaluation.reason,
        "post_text": generated_post.post_text,
        "reply_thread_text": generated_post.reply_thread_text,
        "manual_action": generated_post.manual_action,
        "affiliate_potential": generated_post.affiliate_potential,
        "created_at": now_iso,
        "updated_at": now_iso,
        "ttl": ttl_timestamp,
    }
    
    table.put_item(Item=item)