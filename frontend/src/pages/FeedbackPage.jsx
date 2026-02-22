import { useEffect, useState } from 'react'
import { Link, useLocation, useParams } from 'react-router-dom'
import { FeedbackCard } from '../components/FeedbackCard'
import { getSession } from '../api/sessions'

const MODE_LABEL = { presentation: 'プレゼン', english: '英会話' }

function formatDate(iso) {
  return new Date(iso).toLocaleString('ja-JP', {
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit',
  })
}

function formatDuration(sec) {
  if (sec == null) return '--:--'
  const m = String(Math.floor(sec / 60)).padStart(2, '0')
  const s = String(sec % 60).padStart(2, '0')
  return `${m}:${s}`
}

export function FeedbackPage() {
  const { id } = useParams()
  const { state } = useLocation()

  const [session, setSession] = useState(state?.session ?? null)
  const [loading, setLoading] = useState(!state?.session)
  const [error, setError] = useState('')

  useEffect(() => {
    if (state?.session) return
    getSession(id)
      .then(setSession)
      .catch((err) => setError(err.message || '取得に失敗しました。'))
      .finally(() => setLoading(false))
  }, [id, state?.session])

  return (
    <>
      <nav className="nav">
        <Link to="/history" className="nav-link">← 履歴</Link>
        <Link to="/" className="nav-link">ホーム</Link>
      </nav>

      {loading && <p className="spinner">読み込み中...</p>}
      {error && <p className="error-msg">{error}</p>}

      {session && (
        <>
          <div className="card">
            <div className="meta-list">
              <div className="meta-item">
                <span className="meta-label">モード</span>
                <span className={`mode-badge mode-${session.mode}`}>
                  {MODE_LABEL[session.mode] ?? session.mode}
                </span>
              </div>
              <div className="meta-item">
                <span className="meta-label">日時</span>
                <span className="meta-value">{formatDate(session.created_at)}</span>
              </div>
              <div className="meta-item">
                <span className="meta-label">時間</span>
                <span className="meta-value">{formatDuration(session.duration_sec)}</span>
              </div>
            </div>

            {session.audio_url && (
              <audio src={session.audio_url} controls style={{ width: '100%', marginTop: 8 }} />
            )}
          </div>

          <div className="card">
            <h2 style={{ marginBottom: 16, fontSize: '1.1rem', fontWeight: 700 }}>
              フィードバック
            </h2>
            <FeedbackCard feedback={session.feedback} />
          </div>

          {session.transcript && (
            <div className="card">
              <h2 style={{ marginBottom: 12, fontSize: '1.1rem', fontWeight: 700 }}>
                文字起こし
              </h2>
              <p style={{ fontSize: '0.95rem', lineHeight: 1.8, color: '#374151' }}>
                {session.transcript}
              </p>
            </div>
          )}
        </>
      )}
    </>
  )
}
