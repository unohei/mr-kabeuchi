import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile

from ..auth import get_current_user
from ..db import get_supabase
from ..models import SessionListItem, SessionListResponse, SessionResponse
from ..services.feedback import generate_feedback
from ..services.storage import upload_audio
from ..services.transcribe import transcribe_audio

router = APIRouter(prefix="/sessions", tags=["sessions"])

VALID_MODES = {"presentation", "english"}


@router.post("", response_model=SessionResponse, status_code=201)
async def create_session(
    audio_file: UploadFile = File(...),
    mode: str = Form(...),
    duration_sec: Optional[int] = Form(None),
    user_id: str = Depends(get_current_user),
):
    """
    音声ファイルを受け取り、Storage保存→文字起こし→フィードバック生成→DB保存を行う。
    Day1: 文字起こし/フィードバックはスタブ（空/None）。
    """
    if mode not in VALID_MODES:
        raise HTTPException(
            status_code=422,
            detail=f"mode must be one of {sorted(VALID_MODES)}",
        )

    # 1. Supabase Storage にアップロード
    audio_url = await upload_audio(audio_file, user_id)

    # 2. 文字起こし（Day1はスタブ、空文字を返す）
    transcript = await transcribe_audio(audio_url)

    # 3. フィードバック生成（Day1はスタブ、Noneを返す）
    feedback = await generate_feedback(transcript, mode) if transcript else None

    # 4. DB に保存
    supabase = get_supabase()
    session_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    payload = {
        "id": session_id,
        "user_id": user_id,
        "mode": mode,
        "audio_url": audio_url,
        "transcript": transcript or None,
        "feedback": feedback,
        "duration_sec": duration_sec,
        "created_at": now,
    }

    result = supabase.table("sessions").insert(payload).execute()

    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to save session to DB")

    return SessionResponse(**result.data[0])


@router.get("", response_model=SessionListResponse)
async def list_sessions(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    mode: Optional[str] = Query(None),
    user_id: str = Depends(get_current_user),
):
    """ログイン中ユーザーのセッション一覧を返す（新しい順）"""
    supabase = get_supabase()

    query = (
        supabase.table("sessions")
        .select("id, mode, feedback, duration_sec, created_at")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .range(offset, offset + limit - 1)
    )
    if mode:
        query = query.eq("mode", mode)

    result = query.execute()

    # 件数取得
    count_query = (
        supabase.table("sessions")
        .select("id", count="exact")
        .eq("user_id", user_id)
    )
    if mode:
        count_query = count_query.eq("mode", mode)
    count_result = count_query.execute()

    items = [
        SessionListItem(
            id=row["id"],
            mode=row["mode"],
            overall_score=(row["feedback"] or {}).get("overall_score"),
            duration_sec=row.get("duration_sec"),
            created_at=row["created_at"],
        )
        for row in result.data
    ]

    return SessionListResponse(items=items, total=count_result.count or 0)


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    user_id: str = Depends(get_current_user),
):
    """セッション詳細（自分のものだけ取得可能）"""
    supabase = get_supabase()

    result = (
        supabase.table("sessions")
        .select("*")
        .eq("id", session_id)
        .eq("user_id", user_id)
        .maybe_single()
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="Session not found")

    return SessionResponse(**result.data)
