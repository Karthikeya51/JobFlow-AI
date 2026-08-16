export function MatchScoreCard({ score, summary }) {
  const clampedScore = Math.max(0, Math.min(100, Number(score) || 0));

  return (
    <div className="card border-0 shadow-sm h-100">
      <div className="card-body p-4">
        <div className="d-flex justify-content-between align-items-center mb-3">
          <h5 className="mb-0">AI Match Score</h5>
          <span className="badge bg-primary-subtle text-primary">
            Based on resume + job
          </span>
        </div>

        <div className="display-3 fw-bold mb-2">{clampedScore}%</div>
        <div
          className="progress mb-3"
          role="progressbar"
          aria-label="AI match score"
        >
          <div
            className="progress-bar"
            style={{ width: `${clampedScore}%` }}
          ></div>
        </div>

        <p className="text-muted mb-0">
          {summary ||
            "AI-generated analysis based on the information provided."}
        </p>
      </div>
    </div>
  );
}
