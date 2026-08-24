from google import genai

from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def evaluate_and_generate(articles):
    """AIに新着記事を渡し、価値の高いものを最大3件選んで投稿文を作成させる"""
    articles_text = ""
    for article in articles:
        articles_text += f"タイトル: {article.title}\nURL: {article.link}\n要約: {article.get('summary', '')}\n\n"

    prompt = f"""
        あなたはITニュースの専門キュレーターです。以下の最新ニュースから、X（旧Twitter）で共有する価値が高いニュースを【最大3件】選び、投稿文を作成してください。

        【ニュース一覧】
        {articles_text}

        【出力要件】
        選んだニュースそれぞれについて、以下の形式で出力してください。
        ---
        URL: [選んだニュースのURL]
        投稿ドラフト: [140文字以内のX向け投稿文。ハッシュタグ含む]
        ---
    """
    chat = client.chats.create(model="gemini-3.6-flash")
    response = chat.send_message(prompt)
    return response.text.strip()
