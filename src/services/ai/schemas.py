import os

import yaml
from pydantic import BaseModel, Field


class PromptConfig(BaseModel):
    model_name: str = Field(default="gemini-3.5-flash-lite")
    temperature: float = Field(default=0.7)
    system_instruction: str | None = Field(default=None)
    template: str = Field(description="変数を埋め込む前のプロンプト")

    @classmethod
    def load(
        cls, task_name: str, yaml_file_name: str = "prompts.yaml"
    ) -> "PromptConfig":
        base_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_path = os.path.join(base_dir, yaml_file_name)

        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if task_name not in data:
            raise ValueError(f"Task '{task_name}' not found in {yaml_file_name}")

        return cls(**data[task_name])


# 1件ごとの選別結果データ
class TitleEvaluation(BaseModel):
    id: str = Field(description="記事のID")
    interest_score: int = Field(description="インプレッション期待度（1〜10）")
    reason: str = Field(description="インプレッション期待度の理由・根拠")
    is_duplicate: bool = Field(description="一覧内の他の記事と同一のトピック・発表・後追いニュースである場合に True（先に登場した方を残し、後から出てきた方を True にする）")


# 選別結果全体のレスポンス構造（結果一覧を内包する親クラス）
class TitleEvaluationResult(BaseModel):
    result_list: list[TitleEvaluation] = Field(description="記事評価リスト")

    def get_qualified(self,
                      passing_score: int = 8,
                      max_count: int = 5,
                      remove_duplicates: bool = True) -> list[TitleEvaluation]:
        candidates = self.result_list
        if remove_duplicates:
            candidates = [c for c in self.result_list if not c.is_duplicate]

        passed = [c for c in candidates if c.interest_score >= passing_score]

        if len(passed) >= max_count:
            return passed

        # スコア8以上の記事が不足している場合はスコア7の記事から不足分補充
        # スコア7以上でも不足している場合もスコア6以下の記事は含めない
        needed_count = max_count - len(passed)
        waitlist_score = passing_score - 1
        waitlist = [c for c in candidates if c.interest_score == waitlist_score]
        return passed + waitlist[:needed_count]


# 1件ごとの選別結果データ
class ContentEvaluation(BaseModel):
    # url: str = Field(description="元記事のURL")
    is_adopted: bool = Field(description="採否判定")
    reason: str = Field(description="採否判定の理由")
    interest_score: int = Field(description="本文確認後の注目度・期待値（1〜10）")
    needs_x_research: bool = Field(description="Xリサーチ要否")
    x_research_query: str | None = Field(description="X検索キーワード")


# # 選別結果全体のレスポンス構造（結果一覧を内包する親クラス）
# class ContentEvaluationResult(BaseModel):
#     result_list: list[ContentEvaluation] = Field(description="選定された投稿リスト")
