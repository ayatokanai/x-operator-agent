from google import genai
from pydantic import BaseModel, Field

from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


# 1件ごとの投稿ドラフトデータ
class PostDraft(BaseModel):
    url: str = Field(description="元記事のURL")
    reason: str = Field(description="なぜこの記事を選んだのかの選定理由")
    expected_score: int = Field(description="エンゲージメントの期待値（1〜10の整数）")
    draft_text: str = Field(
        description="X向けの投稿文（140文字程度、ハッシュタグ含む）"
    )


# 投稿ドラフト全体のレスポンス構造（リストを内包する親クラス）
class CurationResult(BaseModel):
    selected_posts: list[PostDraft] = Field(description="選定された投稿リスト")


def evaluate_and_generate(articles) -> CurationResult:
    """AIに新着記事を渡し、価値の高いものを最大3件選んで投稿文を作成させる"""
    articles_text = ""
    for article in articles:
        articles_text += f"タイトル: {article.title}\nURL: {article.link}\n要約: {article.get('summary', '')}\n\n"

    prompt = f"""
        あなたはITニュースの専門キュレーターです。以下の最新ニュースから、X（旧Twitter）で共有する価値が高いニュースを【最大3件】選び、投稿文を作成してください。

        【ニュース一覧】
        {articles_text}
        ---
    """
    chat = client.chats.create(
        model="gemini-3.6-flash",
        config=genai.types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=CurationResult,
            temperature=0.2,
        ),
    )
    response = chat.send_message(prompt)
    return response.parsed
