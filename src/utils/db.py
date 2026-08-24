from datetime import datetime, timedelta, timezone

import boto3

from config import DYNAMODB_TABLE, REGION

dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table(DYNAMODB_TABLE)


def get_last_run_timestamp():
    """DynamoDBから前回の実行日時（UNIXタイムスタンプ）を取得する"""
    # TODO: 動作確認用に落としているのでコミット前に戻す
    # try:
    #     response = table.get_item(Key={"id": "SYSTEM:LAST_RUN"})
    #     if "Item" in response:
    #         return float(response["Item"]["timestamp"])
    # except Exception as e:
    #     print(f"DB読み込みエラー: {e}")

    # 初回実行時やデータがない場合は、24時間前をデフォルト値とする
    return (datetime.now(timezone.utc) - timedelta(days=1)).timestamp()


def update_last_run_timestamp(now_timestamp):
    """今回の実行日時をDynamoDBに記録する"""
    table.put_item(
        Item={
            "id": "SYSTEM:LAST_RUN",
            "type": "config",
            "timestamp": str(now_timestamp),
        }
    )
