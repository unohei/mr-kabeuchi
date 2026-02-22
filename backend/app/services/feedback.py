# Day2で実装: Claude / GPT に文字起こしを渡しフィードバックJSONを生成
# from openai import AsyncOpenAI
# client = AsyncOpenAI()
from typing import Dict, Any, Optional

# フィードバックJSON生成に使うプロンプトテンプレート（Day2で完成）
_SYSTEM_PROMPT_PRESENTATION = """
あなたはプレゼンテーションコーチです。
ユーザーの発話を分析し、以下のJSONスキーマで必ず返答してください。
スキーマ外の文字列は一切含めないこと。
{schema}
"""

_SYSTEM_PROMPT_ENGLISH = """
You are an English conversation coach.
Analyze the user's speech and respond ONLY with the following JSON schema.
{schema}
"""


async def generate_feedback(transcript: str, mode: str) -> Optional[Dict[str, Any]]:
    """
    文字起こしテキストとモードを受け取りフィードバックdictを返す。
    Day1はスタブ（Noneを返す）。
    Day2実装予定:
      1. modeに応じてシステムプロンプトを選択
      2. openai.chat.completions.create() with response_format={"type": "json_object"}
      3. JSONをパースして返す
    """
    return None
