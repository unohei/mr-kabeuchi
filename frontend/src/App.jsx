import { Navigate, Route, Routes } from 'react-router-dom'
import { useAuth } from './lib/AuthContext'
import { LoginPage } from './pages/LoginPage'
import { HomePage } from './pages/HomePage'
import { SessionPage } from './pages/SessionPage'
import { HistoryPage } from './pages/HistoryPage'
import { FeedbackPage } from './pages/FeedbackPage'

function ProtectedRoute({ children }) {
  const { session } = useAuth()
  if (session === undefined) return <p className="spinner">読み込み中...</p>
  if (!session) return <Navigate to="/login" replace />
  return children
}

export function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/" element={<ProtectedRoute><HomePage /></ProtectedRoute>} />
      <Route path="/session" element={<ProtectedRoute><SessionPage /></ProtectedRoute>} />
      <Route path="/history" element={<ProtectedRoute><HistoryPage /></ProtectedRoute>} />
      <Route path="/feedback/:id" element={<ProtectedRoute><FeedbackPage /></ProtectedRoute>} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
