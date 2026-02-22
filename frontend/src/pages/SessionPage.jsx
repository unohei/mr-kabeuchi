import { useState } from 'react'
import { useLocation, useNavigate, Link } from 'react-router-dom'
import { AudioRecorder } from '../components/AudioRecorder'
import { createSession } from '../api/sessions'

const MODE_LABEL = { presentation: 'プレゼン練習', english: '英会話練習' }

export function SessionPage() {
  const navigate = useNavigate()
  const { state } = useLocation()
  const mode = state?.mode ?? 'presentation'

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (audioBlob, durationSec) => {
    setError('')
    setLoading(true)
    try {
      const session = await createSession({ audioBlob, mode, durationSec })
      navigate(`/feedback/${session.id}`, { state: { session } })
    } catch (err) {
      setError(err.message || '送信に失敗しました。')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <nav className="nav">
        <Link to="/" className="nav-link">← ホーム</Link>
        <span className={`mode-badge mode-${mode}`}>{MODE_LABEL[mode]}</span>
      </nav>

      <div className="page-header">
        <h1>{MODE_LABEL[mode]}</h1>
        <p>録音ボタンを押してスタートしてください</p>
      </div>

      {error && <p className="error-msg">{error}</p>}

      <div className="card">
        <AudioRecorder onSubmit={handleSubmit} loading={loading} />
      </div>
    </>
  )
}
