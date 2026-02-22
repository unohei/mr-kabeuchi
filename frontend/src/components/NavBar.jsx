import { Link } from 'react-router-dom'
import { supabase } from '../lib/supabase'

export function NavBar() {
  const handleLogout = async () => {
    await supabase.auth.signOut()
  }

  return (
    <nav className="nav">
      <Link to="/" className="nav-title">Mr.壁打ち</Link>
      <div className="nav-actions">
        <Link to="/history" className="nav-link">履歴</Link>
        <button className="nav-logout" onClick={handleLogout}>ログアウト</button>
      </div>
    </nav>
  )
}
