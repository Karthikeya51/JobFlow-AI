export function StatsCard({ label, value, icon, accentClass = "primary" }) {
  return (
    <div className="card border-0 shadow-sm h-100">
      <div className="card-body">
        <div className="d-flex justify-content-between align-items-start gap-3">
          <div>
            <div className="text-muted small fw-semibold text-uppercase">
              {label}
            </div>
            <div className="display-6 fs-3 fw-bold mt-2">{value}</div>
          </div>
          <div
            className={`rounded-circle p-2 bg-${accentClass}-subtle text-${accentClass}`}
          >
            <span className="fs-5">{icon}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
