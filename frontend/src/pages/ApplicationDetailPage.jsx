import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { Navbar } from "../components/common/Navbar";
import { DeleteApplicationModal } from "../components/applications/DeleteApplicationModal";
import { ApplicationStatusBadge } from "../components/applications/ApplicationStatusBadge";
import applicationService from "../services/applicationService";

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

export function ApplicationDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [application, setApplication] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const loadApplication = async () => {
    try {
      setIsLoading(true);
      setError("");
      const response = await applicationService.getApplication(id);
      setApplication(response.data);
    } catch (err) {
      const detail =
        err.response?.data?.detail || "Unable to load application details.";
      setError(detail);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadApplication();
  }, [id]);

  const handleDelete = async () => {
    setIsDeleting(true);
    try {
      await applicationService.deleteApplication(id);
      navigate("/applications", {
        state: { success: "Application deleted successfully." },
      });
    } catch (err) {
      const detail =
        err.response?.data?.detail || "Unable to delete application.";
      setError(detail);
    } finally {
      setIsDeleting(false);
      setShowDeleteModal(false);
    }
  };

  if (isLoading) {
    return (
      <div>
        <Navbar />
        <div className="container py-5 text-center">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div>
        <Navbar />
        <div className="container py-5">
          <div className="alert alert-danger">{error}</div>
          <Link to="/applications" className="btn btn-primary">
            Back to Applications
          </Link>
        </div>
      </div>
    );
  }

  if (!application) return null;

  return (
    <div>
      <Navbar />
      <div className="container py-4 py-lg-5">
        <div className="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-4">
          <div>
            <p className="text-uppercase text-secondary small fw-semibold mb-1">
              Application
            </p>
            <h1 className="mb-1">{application.company}</h1>
            <div className="text-muted">{application.job_title}</div>
          </div>
          <div className="d-flex gap-2 flex-wrap">
            <Link to="/applications" className="btn btn-outline-secondary">
              Back to Applications
            </Link>
            <Link
              to={`/analysis/${application._id}`}
              className="btn btn-primary"
            >
              AI Analysis
            </Link>
            <Link
              to={`/applications/${application._id}/edit`}
              className="btn btn-outline-primary"
            >
              Edit
            </Link>
            <button
              type="button"
              className="btn btn-outline-danger"
              onClick={() => setShowDeleteModal(true)}
            >
              Delete
            </button>
          </div>
        </div>

        <div className="row g-4">
          <div className="col-lg-8">
            <div className="card shadow-sm border-0">
              <div className="card-body p-4">
                <div className="d-flex align-items-center gap-3 mb-4">
                  <ApplicationStatusBadge status={application.status} />
                  <span className="text-muted small">
                    Updated {formatDate(application.updated_at)}
                  </span>
                </div>

                <div className="row g-3 mb-4">
                  <div className="col-md-6">
                    <div className="text-muted small">Location</div>
                    <div className="fw-semibold">
                      {application.location || "—"}
                    </div>
                  </div>
                  <div className="col-md-6">
                    <div className="text-muted small">Salary</div>
                    <div className="fw-semibold">
                      {application.salary || "—"}
                    </div>
                  </div>
                  <div className="col-md-6">
                    <div className="text-muted small">Applied Date</div>
                    <div className="fw-semibold">
                      {formatDate(application.applied_date)}
                    </div>
                  </div>
                  <div className="col-md-6">
                    <div className="text-muted small">Job URL</div>
                    {application.job_url ? (
                      <a
                        href={application.job_url}
                        target="_blank"
                        rel="noreferrer"
                        className="fw-semibold text-decoration-none"
                      >
                        View Job Posting
                      </a>
                    ) : (
                      <span className="fw-semibold">—</span>
                    )}
                  </div>
                </div>

                <div className="mb-4">
                  <h5 className="mb-3">Job Description</h5>
                  <div
                    className="text-body-secondary"
                    style={{ whiteSpace: "pre-wrap" }}
                  >
                    {application.job_description}
                  </div>
                </div>

                <div>
                  <h5 className="mb-3">Notes</h5>
                  <div
                    className="text-body-secondary"
                    style={{ whiteSpace: "pre-wrap" }}
                  >
                    {application.notes || "No notes added."}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="col-lg-4">
            <div className="card shadow-sm border-0">
              <div className="card-body p-4">
                <h5 className="mb-3">Overview</h5>
                <dl className="row mb-0">
                  <dt className="col-sm-5">Created</dt>
                  <dd className="col-sm-7">
                    {formatDate(application.created_at)}
                  </dd>
                  <dt className="col-sm-5">Updated</dt>
                  <dd className="col-sm-7">
                    {formatDate(application.updated_at)}
                  </dd>
                  <dt className="col-sm-5">Status</dt>
                  <dd className="col-sm-7">
                    <ApplicationStatusBadge status={application.status} />
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <DeleteApplicationModal
        show={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        onConfirm={handleDelete}
        isDeleting={isDeleting}
      />
    </div>
  );
}
