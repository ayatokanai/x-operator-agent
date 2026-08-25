import os
import yaml
from pydantic import BaseModel, Field

class PromptConfig(BaseModel):
    model_name: str = Field(default="gemini-3.5-flash-lite")
    temperature: float = Field(default=0.7)
    system_instruction: str | None = Field(default=None)
    template: str = Field(description="変数を埋め込む前のプロンプト")

    @classmethod
    def load(cls, task_name: str, yaml_file_name: str = "prompts.yaml") -> "PromptConfig":
        base_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_path = os.path.join(base_dir, yaml_file_name)
        
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        if task_name not in data:
            raise ValueError(f"Task '{task_name}' not found in {yaml_file_name}")
            
        return cls(**data[task_name])


# 1件ごとの投稿ドラフトデータ
class TitleScreeningDraft(BaseModel):
    url: str = Field(description="元記事のURL")
    reason: str = Field(description="なぜこの記事を選んだのかの選定理由")
    interest_score: int = Field(description="一次注目度（1〜10）")


# 投稿ドラフト全体のレスポンス構造（リストを内包する親クラス）
class TitleScreeningResult(BaseModel):
    selected_posts: list[TitleScreeningDraft] = Field(description="選定された投稿リスト")
