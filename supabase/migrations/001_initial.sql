-- =============================================
-- Mr.壁打ち: 初期スキーマ
-- Supabase SQL Editor に貼り付けて実行する
-- =============================================

-- セッションテーブル（1録音 = 1セッション）
CREATE TABLE IF NOT EXISTS sessions (
  id           UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id      UUID        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  mode         TEXT        NOT NULL CHECK (mode IN ('presentation', 'english')),
  audio_url    TEXT        NOT NULL,
  transcript   TEXT,
  feedback     JSONB,
  duration_sec INT,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- RLS: 自分のセッションのみ操作可能
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "users_own_sessions"
  ON sessions
  FOR ALL
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- インデックス: 履歴一覧の高速化
CREATE INDEX IF NOT EXISTS idx_sessions_user_created
  ON sessions (user_id, created_at DESC);

-- =============================================
-- Supabase Storage: バケット作成
-- ダッシュボード > Storage > New Bucket で手動作成してもOK
-- =============================================
-- INSERT INTO storage.buckets (id, name, public)
-- VALUES ('audio', 'audio', true)
-- ON CONFLICT DO NOTHING;
--
-- CREATE POLICY "auth_upload_audio"
--   ON storage.objects FOR INSERT
--   TO authenticated
--   WITH CHECK (bucket_id = 'audio' AND auth.uid()::text = (storage.foldername(name))[1]);
--
-- CREATE POLICY "auth_read_audio"
--   ON storage.objects FOR SELECT
--   TO authenticated
--   USING (bucket_id = 'audio' AND auth.uid()::text = (storage.foldername(name))[1]);
