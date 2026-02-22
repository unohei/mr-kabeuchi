import io

import httpx
from fastapi import HTTPException
from openai import AsyncOpenAI

from ..config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def transcribe_audio(audio_url: str) -> str:
    """
    音声URL（Supabase Storage）から音声をダウンロードし、Whisper で文字起こしする。
    言語は自動検出（日本語・英語どちらも対応）。
    """
    if not audio_url:
        return ""

    try:
        async with httpx.AsyncClient(timeout=30) as http_client:
            response = await http_client.get(audio_url)
            response.raise_for_status()
            audio_bytes = response.content
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"音声のダウンロードに失敗しました: {e}")

    try:
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "audio.webm"

        transcription = await client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )
        return transcription.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文字起こしに失敗しました: {e}")
