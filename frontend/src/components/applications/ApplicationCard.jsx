import { Link } from "react-router-dom";
import { ApplicationStatusBadge } from "./ApplicationStatusBadge";

const formatDate = (value) => {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "—";
  return date.toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
};

export function ApplicationCard({ application, onDelete }) {
  return (
    <div className="card shadow-sm border-0 h-100">
      <div className="card-body">
        <div className="d-flex justify-content-between align-items-start gap-3 mb-3">
          <div>
            <h5 className="mb-1">{application.company}</h5>
            <div className="text-muted">{application.job_title}</div>
          </div>
          <ApplicationStatusBadge status={application.status} />
        </div>

        <div className="small text-muted mb-2">
          <div>
            <strong>Location:</strong> {application.location || "—"}
          </div>
          <div>
            <strong>Applied:</strong> {formatDate(application.applied_date)}
          </div>
        </div>

        <div className="d-flex gap-2 flex-wrap mt-3">
          <Link
            to={`/applications/${application._id}`}
            className="btn btn-sm btn-primary"
          >
            View
          </Link>
          <Link
            to={`/applications/${application._id}/edit`}
            className="btn btn-sm btn-outline-secondary"
          >
            Edit
          </Link>
          <button
            type="button"
            className="btn btn-sm btn-outline-danger"
            onClick={() => onDelete(application)}
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}
