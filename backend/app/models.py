from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel


# ---------- Feedback JSON（固定スキーマ） ----------

class FeedbackDetail(BaseModel):
    score: int
    comment: str


class FeedbackDetails(BaseModel):
    clarity: FeedbackDetail
    structure: FeedbackDetail
    delivery: FeedbackDetail
    vocabulary: FeedbackDetail


class Feedback(BaseModel):
    overall_score: int
    summary: str
    strengths: List[str]
    improvements: List[str]
    details: FeedbackDetails
    next_action: str


# ---------- API レスポンス ----------

class SessionResponse(BaseModel):
    id: str
    mode: str
    audio_url: str
    transcript: Optional[str] = None
    feedback: Optional[Any] = None  # Day2でFeedbackに厳格化
    duration_sec: Optional[int] = None
    created_at: datetime


class SessionListItem(BaseModel):
    id: str
    mode: str
    overall_score: Optional[int] = None
    duration_sec: Optional[int] = None
    created_at: datetime


class SessionListResponse(BaseModel):
    items: List[SessionListItem]
    total: int
