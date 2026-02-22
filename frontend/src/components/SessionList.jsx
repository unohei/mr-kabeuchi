import { Link } from 'react-router-dom'

const MODE_LABEL = { presentation: 'プレゼン', english: '英会話' }

function formatDate(iso) {
  return new Date(iso).toLocaleString('ja-JP', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function formatDuration(sec) {
  if (sec == null) return '--:--'
  const m = String(Math.floor(sec / 60)).padStart(2, '0')
  const s = String(sec % 60).padStart(2, '0')
  return `${m}:${s}`
}

export function SessionList({ sessions }) {
  if (sessions.length === 0) {
    return <p className="empty">まだセッションがありません。<br />ホームから練習を始めましょう。</p>
  }

  return (
    <ul className="session-list">
      {sessions.map((s) => (
        <li key={s.id}>
          <Link to={`/feedback/${s.id}`} className="session-item">
            <span className={`mode-badge mode-${s.mode}`}>
              {MODE_LABEL[s.mode] ?? s.mode}
            </span>
            <span className="session-date">{formatDate(s.created_at)}</span>
            <span className="session-duration">{formatDuration(s.duration_sec)}</span>
            <span className="session-score">
              {s.overall_score != null ? `${s.overall_score}点` : '---'}
            </span>
          </Link>
        </li>
      ))}
    </ul>
  )
}
