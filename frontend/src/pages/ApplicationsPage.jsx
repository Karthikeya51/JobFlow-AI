import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { ApplicationFilters } from "../components/applications/ApplicationFilters";
import { ApplicationCard } from "../components/applications/ApplicationCard";
import { ApplicationTable } from "../components/applications/ApplicationTable";
import { DeleteApplicationModal } from "../components/applications/DeleteApplicationModal";
import { EmptyApplications } from "../components/applications/EmptyApplications";
import { Navbar } from "../components/common/Navbar";
import applicationService from "../services/applicationService";

const debounce = (func, delay = 300) => {
  let timeoutId;
  return (...args) => {
    if (timeoutId) clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
};

export function ApplicationsPage() {
//   const navigate = useNavigate();
  const [applications, setApplications] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");
  const [sort, setSort] = useState("created_at_desc");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedApplication, setSelectedApplication] = useState(null);
  const [isDeleting, setIsDeleting] = useState(false);

  const loadApplications = useMemo(() => {
    return debounce(async (nextSearch, nextStatus, nextSort, nextPage) => {
      try {
        setIsLoading(true);
        setError("");

        const [sortBy, sortOrder] = nextSort.includes("_")
          ? nextSort.split("_")
          : ["created_at", "desc"];

        const response = await applicationService.getApplications({
          page: nextPage,
          limit: 10,
          search: nextSearch,
          status: nextStatus,
          sort_by: sortBy,
          sort_order: sortOrder,
        });

        setApplications(response.data.items || []);
        setTotal(response.data.total || 0);
        setTotalPages(response.data.pages || 0);
      } catch (err) {
        const detail =
          err.response?.data?.detail || "Unable to load applications.";
        setError(detail);
      } finally {
        setIsLoading(false);
      }
    }, 250);
  }, []);

  useEffect(() => {
    loadApplications(search, status, sort, page);
  }, [search, status, sort, page, loadApplications]);

  const handleDeleteClick = (application) => {
    setSelectedApplication(application);
  };

  const handleDelete = async () => {
    if (!selectedApplication) return;
    setIsDeleting(true);

    try {
      await applicationService.deleteApplication(selectedApplication._id);
      setSelectedApplication(null);
      await loadApplications(search, status, sort, page);
    } catch (err) {
      const detail =
        err.response?.data?.detail || "Unable to delete application.";
      setError(detail);
    } finally {
      setIsDeleting(false);
    }
  };

  const handleRetry = () => {
    loadApplications(search, status, sort, page);
  };

  return (
    <div>
      <Navbar />
      <div className="container py-4 py-lg-5">
        <div className="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-4">
          <div>
            <h1 className="mb-1">Job Applications</h1>
            <p className="text-muted mb-0">
              Track and manage your job search in one place.
            </p>
          </div>
          <Link to="/applications/new" className="btn btn-primary">
            + Add Application
          </Link>
        </div>

        <ApplicationFilters
          search={search}
          onSearchChange={setSearch}
          status={status}
          onStatusChange={setStatus}
          sort={sort}
          onSortChange={setSort}
          totalCount={total}
        />

        {error && (
          <div
            className="alert alert-danger d-flex justify-content-between align-items-center"
            role="alert"
          >
            <span>{error}</span>
            <button
              className="btn btn-sm btn-outline-danger"
              type="button"
              onClick={handleRetry}
            >
              Retry
            </button>
          </div>
        )}

        {isLoading ? (
          <div className="text-center py-5">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
          </div>
        ) : applications.length === 0 ? (
          <EmptyApplications
            message={
              search || status
                ? "No applications match your filters."
                : "No applications yet"
            }
            subtitle={
              search || status
                ? "Try adjusting your search or filters."
                : "Start tracking your job search by adding your first application."
            }
          />
        ) : (
          <>
            <div className="d-none d-lg-block">
              <div className="card shadow-sm border-0">
                <ApplicationTable
                  applications={applications}
                  onDelete={handleDeleteClick}
                />
              </div>
            </div>

            <div className="d-lg-none row g-3">
              {applications.map((application) => (
                <div key={application._id} className="col-12">
                  <ApplicationCard
                    application={application}
                    onDelete={handleDeleteClick}
                  />
                </div>
              ))}
            </div>

            {totalPages > 1 && (
              <div className="d-flex justify-content-center mt-4">
                <nav aria-label="Application pagination">
                  <ul className="pagination">
                    <li className={`page-item ${page === 1 ? "disabled" : ""}`}>
                      <button
                        type="button"
                        className="page-link"
                        onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
                      >
                        Previous
                      </button>
                    </li>
                    <li className="page-item disabled">
                      <span className="page-link">
                        {page} / {totalPages}
                      </span>
                    </li>
                    <li
                      className={`page-item ${page >= totalPages ? "disabled" : ""}`}
                    >
                      <button
                        type="button"
                        className="page-link"
                        onClick={() =>
                          setPage((prev) => Math.min(prev + 1, totalPages))
                        }
                      >
                        Next
                      </button>
                    </li>
                  </ul>
                </nav>
              </div>
            )}
          </>
        )}
      </div>

      <DeleteApplicationModal
        show={Boolean(selectedApplication)}
        onClose={() => setSelectedApplication(null)}
        onConfirm={handleDelete}
        isDeleting={isDeleting}
      />
    </div>
  );
}
