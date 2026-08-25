from google import genai

from config import GEMINI_API_KEY

from .schemas import PromptConfig, TitleScreeningResult

client = genai.Client(api_key=GEMINI_API_KEY)
screening_config = PromptConfig.load("screening")


def evaluate_articles(articles) -> TitleScreeningResult:
    """AIに新着記事を渡し、価値の高いものを選んで投稿文を作成させる"""
    articles_text = ""
    for article in articles:
        articles_text += f"タイトル: {article.title}\nURL: {article.link}\n要約: {article.get('summary', '')}\n\n"

    prompt = screening_config.template.format(articles_text=articles_text)

    chat = client.chats.create(
        model=screening_config.model_name,
        config=genai.types.GenerateContentConfig(
            system_instruction=screening_config.system_instruction,
            response_mime_type="application/json",
            response_schema=TitleScreeningResult,
            temperature=screening_config.temperature,
        ),
    )
    response = chat.send_message(prompt)
    return response.parsed
