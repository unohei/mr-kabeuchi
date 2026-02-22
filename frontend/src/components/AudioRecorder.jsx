import { useState } from 'react'
import { useRecorder } from '../hooks/useRecorder'

function formatDuration(sec) {
  const m = String(Math.floor(sec / 60)).padStart(2, '0')
  const s = String(sec % 60).padStart(2, '0')
  return `${m}:${s}`
}

export function AudioRecorder({ onSubmit, loading }) {
  const { isRecording, duration, start, stop } = useRecorder()
  const [audioBlob, setAudioBlob] = useState(null)
  const [audioUrl, setAudioUrl] = useState(null)
  const [error, setError] = useState('')

  const handleStart = async () => {
    setError('')
    setAudioBlob(null)
    setAudioUrl(null)
    try {
      await start()
    } catch {
      setError('マイクへのアクセスを許可してください。')
    }
  }

  const handleStop = async () => {
    const blob = await stop()
    if (blob) {
      setAudioBlob(blob)
      setAudioUrl(URL.createObjectURL(blob))
    }
  }

  const handleReset = () => {
    setAudioBlob(null)
    setAudioUrl(null)
  }

  const handleSubmit = () => {
    if (audioBlob) onSubmit(audioBlob, duration)
  }

  return (
    <div className="recorder">
      {error && <p className="error-msg">{error}</p>}

      {/* 録音前 */}
      {!isRecording && !audioBlob && (
        <button className="btn btn-primary btn-lg" onClick={handleStart}>
          録音開始
        </button>
      )}

      {/* 録音中 */}
      {isRecording && (
        <div className="recording-ui">
          <div className="recording-indicator">
            <span className="rec-dot" />
            REC
          </div>
          <div className="timer">{formatDuration(duration)}</div>
          <button className="btn btn-danger" onClick={handleStop}>
            停止
          </button>
        </div>
      )}

      {/* 録音済み・レビュー */}
      {audioBlob && !isRecording && (
        <div className="review-ui">
          <audio src={audioUrl} controls />
          <div className="review-actions">
            <button
              className="btn btn-secondary"
              onClick={handleReset}
              disabled={loading}
            >
              やり直す
            </button>
            <button
              className="btn btn-primary"
              onClick={handleSubmit}
              disabled={loading}
            >
              {loading ? '送信中...' : '送信する'}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
