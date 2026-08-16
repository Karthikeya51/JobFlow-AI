import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { ApplicationForm } from "../components/applications/ApplicationForm";
import { Navbar } from "../components/common/Navbar";
import applicationService from "../services/applicationService";

export function CreateApplicationPage() {
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (payload) => {
    setIsSubmitting(true);
    setError("");

    try {
      const response = await applicationService.createApplication(payload);
      navigate(`/applications/${response.data._id}`, {
        state: { success: "Application created successfully." },
      });
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to create application. Please try again.",
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
          <h1 className="mb-1">Create Application</h1>
          <p className="text-muted mb-0">
            Add a new role to track in your job search.
          </p>
        </div>

        {error && <div className="alert alert-danger">{error}</div>}

        <div className="card shadow-sm border-0">
          <div className="card-body p-4 p-lg-5">
            <ApplicationForm
              onSubmit={handleSubmit}
              isSubmitting={isSubmitting}
              submitLabel="Create Application"
              onCancel={() => navigate("/applications")}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
