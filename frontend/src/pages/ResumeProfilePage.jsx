import { useEffect, useState } from "react";
import { Navbar } from "../components/common/Navbar";
import api from "../services/api";

export function ResumeProfilePage() {
  const [resumeText, setResumeText] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [updatedAt, setUpdatedAt] = useState(null);

  useEffect(() => {
    const fetchResume = async () => {
      try {
        const response = await api.get("/api/resume");
        setResumeText(response.data.resume_text || "");
        setUpdatedAt(response.data.updated_at);
      } catch (err) {
        if (err.response?.status !== 404) {
          setError(
            err.response?.data?.detail || "Unable to load resume profile.",
          );
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchResume();
  }, []);

  const handleSave = async () => {
    try {
      setIsSaving(true);
      setError("");
      setSuccess("");
      const response = await api.put("/api/resume", {
        resume_text: resumeText,
      });
      setUpdatedAt(response.data.updated_at);
      setSuccess("Resume saved successfully.");
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to save resume.");
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async () => {
    try {
      setIsSaving(true);
      setError("");
      setSuccess("");
      await api.delete("/api/resume");
      setResumeText("");
      setUpdatedAt(null);
      setSuccess("Resume profile removed.");
    } catch (err) {
      setError(
        err.response?.data?.detail || "Unable to delete resume profile.",
      );
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="bg-light min-vh-100">
      <Navbar />
      <div className="container py-4 py-lg-5">
        <div className="mb-4">
          <p className="text-primary fw-semibold mb-1">Resume Profile</p>
          <h1 className="mb-2">Resume Profile</h1>
          <p className="text-muted mb-0">
            Save your resume content once and use it to analyze your fit for
            future opportunities.
          </p>
        </div>

        {error && <div className="alert alert-danger">{error}</div>}
        {success && <div className="alert alert-success">{success}</div>}

        <div className="card border-0 shadow-sm">
          <div className="card-body p-4">
            <div className="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
              <div className="small text-muted">
                {resumeText.length} characters
              </div>
              <div className="small text-muted">
                {updatedAt
                  ? `Last updated: ${new Date(updatedAt).toLocaleString()}`
                  : "Not saved yet"}
              </div>
            </div>

            <textarea
              className="form-control mb-3"
              rows={18}
              value={resumeText}
              onChange={(event) => setResumeText(event.target.value)}
              placeholder="Paste your resume text here..."
              disabled={isLoading || isSaving}
            />

            <div className="text-muted small mb-3">
              Include your skills, education, experience, projects and
              achievements for better AI matching.
            </div>

            <div className="d-flex gap-2 flex-wrap">
              <button
                className="btn btn-primary"
                onClick={handleSave}
                disabled={isSaving || isLoading}
              >
                {isSaving ? "Saving..." : "Save Resume"}
              </button>
              <button
                className="btn btn-outline-danger"
                onClick={handleDelete}
                disabled={isSaving || isLoading}
              >
                Clear / Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
