import { useEffect, useState } from 'react'
import { NavBar } from '../components/NavBar'
import { SessionList } from '../components/SessionList'
import { listSessions } from '../api/sessions'

export function HistoryPage() {
  const [sessions, setSessions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    listSessions()
      .then((data) => setSessions(data.items))
      .catch((err) => setError(err.message || '取得に失敗しました。'))
      .finally(() => setLoading(false))
  }, [])

  return (
    <>
      <NavBar />
      <div className="page-header">
        <h1>練習履歴</h1>
        <p>これまでの練習セッション一覧</p>
      </div>

      {error && <p className="error-msg">{error}</p>}
      {loading && <p className="spinner">読み込み中...</p>}
      {!loading && !error && <SessionList sessions={sessions} />}
    </>
  )
}
