from google import genai

from config import GEMINI_API_KEY

from .schemas import (
    PromptConfig,
    TitleEvaluationResult,
    ContentEvaluation,
    GeneratedPost
)

client = genai.Client(api_key=GEMINI_API_KEY)


def evaluate_titles(articles: dict) -> TitleEvaluationResult:
    """AIに新着記事を渡し、価値の高いものを選ばせる"""
    prompt_config = PromptConfig.load("evaluate_title_draft")

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


def inspect_article_body(article_title: str,
                         article_body: str) -> ContentEvaluation:
    """AIに記事URLを渡して本文を確認させ、投稿価値とXリサーチ価値を検討させる"""
    prompt_config = PromptConfig.load("inspect_article")

    prompt = prompt_config.template.format(
        title=article_title,
        body=article_body
    )

    chat = client.chats.create(
        model=prompt_config.model_name,
        config=genai.types.GenerateContentConfig(
            system_instruction=prompt_config.system_instruction,
            response_mime_type="application/json",
            response_schema=ContentEvaluation,
            temperature=prompt_config.temperature,
        ),
    )
    response = chat.send_message(prompt)
    return response.parsed


def fetch_x_sentiments(prompt: str):
    ...

def write_post(article_title: str,
               article_body: str) -> GeneratedPost:
    """AIに記事URLを渡して本文を確認させ、投稿価値とXリサーチ価値を検討させる"""
    prompt_config = PromptConfig.load("write_post")

    prompt = prompt_config.template.format(
        title=article_title,
        body=article_body,
        research_section=""
    )

    chat = client.chats.create(
        model=prompt_config.model_name,
        config=genai.types.GenerateContentConfig(
            system_instruction=prompt_config.system_instruction,
            response_mime_type="application/json",
            response_schema=GeneratedPost,
            temperature=prompt_config.temperature,
        ),
    )
    response = chat.send_message(prompt)
    return response.parsed
