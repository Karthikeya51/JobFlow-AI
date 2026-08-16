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

export function ApplicationTable({ applications, onDelete }) {
  return (
    <div className="table-responsive">
      <table className="table table-hover align-middle mb-0">
        <thead className="table-light">
          <tr>
            <th>Company</th>
            <th>Job Title</th>
            <th>Location</th>
            <th>Status</th>
            <th>Applied Date</th>
            <th className="text-end">Actions</th>
          </tr>
        </thead>
        <tbody>
          {applications.map((application) => (
            <tr key={application._id}>
              <td>
                <div className="fw-semibold">{application.company}</div>
              </td>
              <td>{application.job_title}</td>
              <td>{application.location || "—"}</td>
              <td>
                <ApplicationStatusBadge status={application.status} />
              </td>
              <td>{formatDate(application.applied_date)}</td>
              <td className="text-end">
                <div className="btn-group btn-group-sm" role="group">
                  <Link
                    to={`/applications/${application._id}`}
                    className="btn btn-outline-primary"
                  >
                    View
                  </Link>
                  <Link
                    to={`/applications/${application._id}/edit`}
                    className="btn btn-outline-secondary"
                  >
                    Edit
                  </Link>
                  <button
                    type="button"
                    className="btn btn-outline-danger"
                    onClick={() => onDelete(application)}
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
