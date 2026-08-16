import { Link } from "react-router-dom";

export function EmptyApplications({
  message = "No applications yet",
  subtitle,
  showButton = true,
}) {
  return (
    <div className="card border-0 shadow-sm">
      <div className="card-body text-center py-5">
        <div className="mb-3">
          <i className="bi bi-briefcase fs-1 text-muted"></i>
        </div>
        <h4 className="mb-2">{message}</h4>
        {subtitle && <p className="text-muted mb-4">{subtitle}</p>}
        {showButton && (
          <Link to="/applications/new" className="btn btn-primary">
            + Add Application
          </Link>
        )}
      </div>
    </div>
  );
}
