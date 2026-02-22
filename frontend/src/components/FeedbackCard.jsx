// Day2で完成予定: AIフィードバックJSONを表示するカード

const DETAIL_LABELS = {
  clarity: '明瞭さ',
  structure: '構成',
  delivery: '話し方',
  vocabulary: '語彙',
}

export function FeedbackCard({ feedback }) {
  if (!feedback) {
    return (
      <div className="placeholder">
        フィードバックはまだありません。<br />
        文字起こし・AI評価はDay2で実装予定です。
      </div>
    )
  }

  return (
    <div>
      <div className="feedback-score">
        <span className="feedback-score-num">{feedback.overall_score}</span>
        <span className="feedback-score-unit">点</span>
      </div>

      <p style={{ marginBottom: 20 }}>{feedback.summary}</p>

      <div className="feedback-section">
        <h3>良かった点</h3>
        <div className="tag-list">
          {feedback.strengths.map((s, i) => (
            <span key={i} className="tag tag-green">{s}</span>
          ))}
        </div>
      </div>

      <div className="feedback-section">
        <h3>改善点</h3>
        <div className="tag-list">
          {feedback.improvements.map((s, i) => (
            <span key={i} className="tag tag-orange">{s}</span>
          ))}
        </div>
      </div>

      {feedback.details && (
        <div className="feedback-section">
          <h3>詳細スコア</h3>
          <div className="detail-grid">
            {Object.entries(feedback.details).map(([key, val]) => (
              <div key={key} className="detail-item">
                <div className="detail-label">{DETAIL_LABELS[key] ?? key}</div>
                <div className="detail-score">{val.score}</div>
                <div className="detail-comment">{val.comment}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="feedback-section">
        <h3>次のアクション</h3>
        <p style={{ fontSize: '0.95rem' }}>{feedback.next_action}</p>
      </div>
    </div>
  )
}
