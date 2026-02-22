import { useNavigate } from 'react-router-dom'
import { NavBar } from '../components/NavBar'

const MODES = [
  {
    id: 'presentation',
    label: 'プレゼン練習',
    desc: '発表・スピーチの構成・話し方をフィードバック',
  },
  {
    id: 'english',
    label: '英会話練習',
    desc: 'スピーキング・語彙・流暢さをフィードバック',
  },
]

export function HomePage() {
  const navigate = useNavigate()

  const handleSelect = (mode) => {
    navigate('/session', { state: { mode } })
  }

  return (
    <>
      <NavBar />
      <div className="page-header">
        <h1>今日も練習しましょう</h1>
        <p>モードを選択してください</p>
      </div>

      <div className="mode-selector">
        {MODES.map((m) => (
          <button
            key={m.id}
            className="mode-card"
            onClick={() => handleSelect(m.id)}
          >
            <div className={`mode-badge mode-${m.id}`}>{m.label}</div>
            <p className="mode-card-desc">{m.desc}</p>
          </button>
        ))}
      </div>
    </>
  )
}
