import json
from typing import Any, Dict, Optional

from fastapi import HTTPException
from openai import AsyncOpenAI

from ..config import settings

_JSON_SCHEMA = """{
  "overall_score": <0-100の整数>,
  "summary": "<1〜2文の総評>",
  "strengths": ["<良かった点1>", "<良かった点2>"],
  "improvements": ["<改善点1>", "<改善点2>"],
  "details": {
    "clarity":    { "score": <0-100の整数>, "comment": "<コメント>" },
    "structure":  { "score": <0-100の整数>, "comment": "<コメント>" },
    "delivery":   { "score": <0-100の整数>, "comment": "<コメント>" },
    "vocabulary": { "score": <0-100の整数>, "comment": "<コメント>" }
  },
  "next_action": "<次回への具体的なアドバイス1文>"
}"""

_SYSTEM_PROMPT_PRESENTATION = (
    "あなたはプレゼンテーションコーチです。\n"
    "ユーザーの発話を分析し、以下のJSONスキーマのみで返答してください。\n"
    "スキーマ外の文字列は一切含めないこと。\n\n"
    + _JSON_SCHEMA
)

_SYSTEM_PROMPT_ENGLISH = (
    "You are an English conversation coach.\n"
    "Analyze the user's speech and respond ONLY with the following JSON schema.\n"
    "Do not include any text outside of the schema.\n\n"
    + _JSON_SCHEMA
)


async def generate_feedback(transcript: str, mode: str) -> Optional[Dict[str, Any]]:
    """
    文字起こしテキストとモードを受け取り GPT-4o でフィードバック dict を返す。

    Args:
        transcript: Whisper の文字起こし結果
        mode: "presentation" または "english"

    Returns:
        固定スキーマの dict、transcript が空の場合は None

    Raises:
        HTTPException(500): API 呼び出し失敗時
    """
    if not transcript:
        return None

    system_prompt = (
        _SYSTEM_PROMPT_ENGLISH if mode == "english" else _SYSTEM_PROMPT_PRESENTATION
    )

    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            temperature=0.3,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript},
            ],
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Feedback generation failed: {e}"
        )

    return json.loads(response.choices[0].message.content)
