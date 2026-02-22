import uuid

from fastapi import HTTPException, UploadFile

from ..config import settings
from ..db import get_supabase

# 許可する音声MIMEタイプ
ALLOWED_CONTENT_TYPES = {
    "audio/webm",
    "audio/ogg",
    "audio/wav",
    "audio/mpeg",
    "audio/mp4",
    "audio/x-m4a",
}
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB（Whisper上限）


async def upload_audio(file: UploadFile, user_id: str) -> str:
    """音声ファイルをSupabase Storageにアップロードして公開URLを返す"""
    content_type = file.content_type or "audio/webm"
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported audio type: {content_type}",
        )

    body = await file.read()
    if len(body) > MAX_FILE_SIZE:
        raise HTTPException(status_code=422, detail="File too large (max 25MB)")

    ext = _ext_from_content_type(content_type)
    path = f"{user_id}/{uuid.uuid4()}.{ext}"

    supabase = get_supabase()
    supabase.storage.from_(settings.STORAGE_BUCKET).upload(
        path=path,
        file=body,
        file_options={"content-type": content_type},
    )

    public_url: str = supabase.storage.from_(settings.STORAGE_BUCKET).get_public_url(path)
    return public_url


def _ext_from_content_type(content_type: str) -> str:
    mapping = {
        "audio/webm": "webm",
        "audio/ogg": "ogg",
        "audio/wav": "wav",
        "audio/mpeg": "mp3",
        "audio/mp4": "mp4",
        "audio/x-m4a": "m4a",
    }
    return mapping.get(content_type, "webm")
