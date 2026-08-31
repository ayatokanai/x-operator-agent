import requests


def send_post_draft(
    webhook_url: str,
    title: str,
    source_url: str,
    post_text: str,
    interest_score: int,
    screening_reason: str,
    reply_thread_text: str | None = None,
    manual_action: str | None = None,
    affiliate_potential: str | None = None,
) -> bool:
    """
    生成したX投稿ドラフトをDiscordへEmbed形式で通知する関数
    """
    # 手動アクションの有無に応じて色（バーの色）を切り替える
    # 手動アクションあり: オレンジ(0xFFA500), 通常: 青(0x1DA1F2)
    embed_color = 0xFFA500 if manual_action else 0x1DA1F2

    # 基本のフィールド定義
    fields = [
        {
            "name": "🎯 スコア / 採用理由",
            "value": f"★ **{interest_score}/10**\n{screening_reason}",
            "inline": True,
        },
    ]

    # ツリー投稿がある場合に追加
    if reply_thread_text:
        fields.append({
            "name": "🧵 ツリー",
            "value": reply_thread_text,
            "inline": False,
        })

    # 人手による対応が必要な場合（スクショ添付など）
    if manual_action:
        fields.append({
            "name": "⚠️ 要手動アクション",
            "value": manual_action,
            "inline": False,
        })

    # アフィリエイトにつなげるポテンシャルがある場合
    if affiliate_potential:
        fields.append({
            "name": "💰 アフィリエイト",
            "value": affiliate_potential,
            "inline": False,
        })

    # Discord Webhookペイロード組み立て
    payload = {
        "content": post_text,
        "embeds": [
            {
                "title": f"📰 {title}",
                "url": source_url,
                "color": embed_color,
                "fields": fields,
                # "footer": {
                #     "text": "X Auto Poster • DynamoDB 保存完了"
                # }
            }
        ]
    }

    # 送信リクエスト
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        print("✅ Discordへの通知が成功しました。")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Discord通知エラー: {e}")
        return False