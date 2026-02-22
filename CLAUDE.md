# Mr.壁打ち — プロジェクト概要

プレゼン/英会話の音声録音→文字起こし→AIフィードバックアプリ。3日MVP。

## 技術スタック

| レイヤー | 技術 |
|---|---|
| フロントエンド | React 18 + Vite + react-router-dom v6 |
| バックエンド | FastAPI (Python 3.9) + uvicorn |
| 認証 | Supabase Auth（ES256 JWT / JWKS検証） |
| DB | Supabase PostgreSQL（RLS有効） |
| Storage | Supabase Storage（`audio` バケット） |
| 文字起こし | OpenAI Whisper API |
| AIフィードバック | OpenAI GPT-4o（JSON固定出力） |

## ディレクトリ構成

```
mr-kabedachi/
├── frontend/src/
│   ├── api/sessions.js        # バックエンドAPIラッパー（JWT自動付与）
│   ├── components/
│   │   ├── AudioRecorder.jsx  # 録音UI（MediaRecorder）
│   │   ├── FeedbackCard.jsx   # フィードバックJSON表示
│   │   ├── NavBar.jsx
│   │   └── SessionList.jsx    # 履歴一覧
│   ├── hooks/useRecorder.js   # MediaRecorder抽象化（Safari対応）
│   ├── lib/
│   │   ├── AuthContext.jsx    # Supabase session管理
│   │   └── supabase.js
│   └── pages/
│       ├── LoginPage.jsx
│       ├── HomePage.jsx       # モード選択
│       ├── SessionPage.jsx    # 録音セッション
│       ├── HistoryPage.jsx
│       └── FeedbackPage.jsx
├── backend/app/
│   ├── main.py               # FastAPI + CORS
│   ├── auth.py               # JWKS/ES256 JWT検証
│   ├── config.py             # pydantic-settings
│   ├── db.py                 # Supabaseクライアント（service key）
│   ├── models.py             # Pydanticスキーマ
│   ├── routers/sessions.py   # POST/GET /sessions
│   └── services/
│       ├── storage.py        # Supabase Storageアップロード
│       ├── transcribe.py     # Whisper API（Day2実装）
│       └── feedback.py       # GPT-4o フィードバック生成（Day2実装）
└── supabase/migrations/001_initial.sql
```

## DB スキーマ（sessions テーブル）

```sql
id           UUID PRIMARY KEY
user_id      UUID REFERENCES auth.users
mode         TEXT CHECK (mode IN ('presentation', 'english'))
audio_url    TEXT        -- Supabase Storage 公開URL
transcript   TEXT        -- Whisper文字起こし結果
feedback     JSONB       -- AIフィードバック（固定スキーマ）
duration_sec INT
created_at   TIMESTAMPTZ
```

## feedback JSONB 固定スキーマ

```json
{
  "overall_score": 78,
  "summary": "...",
  "strengths": ["..."],
  "improvements": ["..."],
  "details": {
    "clarity":    { "score": 80, "comment": "..." },
    "structure":  { "score": 75, "comment": "..." },
    "delivery":   { "score": 70, "comment": "..." },
    "vocabulary": { "score": 85, "comment": "..." }
  },
  "next_action": "..."
}
```

## API エンドポイント

| Method | Path | 説明 |
|---|---|---|
| POST | `/sessions` | 音声アップロード→文字起こし→フィードバック→DB保存 |
| GET | `/sessions` | 履歴一覧（?limit&offset&mode） |
| GET | `/sessions/{id}` | 詳細取得 |
| GET | `/health` | ヘルスチェック |

## コーディング規約

- Python: 3.9互換（`X | Y` 型ヒント禁止 → `Optional[X]`, `Union[X, Y]` を使う）
- 非同期: FastAPIのエンドポイントは `async def`
- エラー: `HTTPException` で返す。詳細は `detail` フィールドに
- フロント: ESモジュール、React関数コンポーネント、hooks優先

## 環境変数

### backend/.env
```
SUPABASE_URL=
SUPABASE_SERVICE_KEY=   # service_role key（RLSバイパス用）
OPENAI_API_KEY=
STORAGE_BUCKET=audio
```

### frontend/.env.local
```
VITE_SUPABASE_URL=
VITE_SUPABASE_ANON_KEY=
VITE_API_URL=http://localhost:8000
```

## 起動コマンド

```bash
# バックエンド
cd backend && source .venv/bin/activate && uvicorn app.main:app --reload

# フロントエンド
cd frontend && npm run dev
```

## Day 進捗

- [x] Day1: 設計・骨格・録音→Storage保存→一覧表示
- [ ] Day2: Whisper文字起こし + GPT-4oフィードバック生成
- [ ] Day3: UI polish + エラーハンドリング + デプロイ
