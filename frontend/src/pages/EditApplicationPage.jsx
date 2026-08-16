import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ApplicationForm } from "../components/applications/ApplicationForm";
import { Navbar } from "../components/common/Navbar";
import applicationService from "../services/applicationService";

export function EditApplicationPage() {
  const navigate = useNavigate();
  const { id } = useParams();
  const [initialData, setInitialData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadApplication = async () => {
      try {
        setIsLoading(true);
        const response = await applicationService.getApplication(id);
        setInitialData(response.data);
      } catch (err) {
        const detail =
          err.response?.data?.detail || "Unable to load application";
        setError(detail);
      } finally {
        setIsLoading(false);
      }
    };

    loadApplication();
  }, [id]);

  const handleSubmit = async (payload) => {
    setIsSubmitting(true);
    setError("");

    try {
      const response = await applicationService.updateApplication(id, payload);
      navigate(`/applications/${response.data._id}`, {
        state: { success: "Application updated successfully." },
      });
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to update application. Please try again.",
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div>
      <Navbar />
      <div className="container py-4 py-lg-5">
        <div className="mb-4">
          <h1 className="mb-1">Edit Application</h1>
          <p className="text-muted mb-0">
            Update the details for this opportunity.
          </p>
        </div>

        {error && <div className="alert alert-danger">{error}</div>}

        {isLoading ? (
          <div className="text-center py-5">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
          </div>
        ) : initialData ? (
          <div className="card shadow-sm border-0">
            <div className="card-body p-4 p-lg-5">
              <ApplicationForm
                initialData={initialData}
                onSubmit={handleSubmit}
                isSubmitting={isSubmitting}
                submitLabel="Save Changes"
                onCancel={() => navigate(`/applications/${id}`)}
              />
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
