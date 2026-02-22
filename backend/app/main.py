from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import sessions

app = FastAPI(
    title="Mr.壁打ち API",
    version="0.1.0",
    description="プレゼン/英会話練習の音声フィードバックAPI",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:4173",  # Vite preview
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions.router)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}
