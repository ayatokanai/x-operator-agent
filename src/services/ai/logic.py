from google import genai

from config import GEMINI_API_KEY

from .schemas import PromptConfig, TitleEvaluationResult

client = genai.Client(api_key=GEMINI_API_KEY)


def evaluate_titles(articles: dict) -> TitleEvaluationResult:
    """AIに新着記事を渡し、価値の高いものを選ばせる"""
    prompt_config = PromptConfig.load("evaluate_title")

    articles_text = ""
    for id, article in articles.items():
        articles_text += f"ID: {id}\nタイトル: {article.get('title')}\n要約: {article.get('summary', '')}\n---\n"

    prompt = prompt_config.template.format(articles_text=articles_text)

    chat = client.chats.create(
        model=prompt_config.model_name,
        config=genai.types.GenerateContentConfig(
            system_instruction=prompt_config.system_instruction,
            response_mime_type="application/json",
            response_schema=TitleEvaluationResult,
            temperature=prompt_config.temperature,
        ),
    )
    response = chat.send_message(prompt)
    return response.parsed

