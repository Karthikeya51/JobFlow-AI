import { useEffect, useState } from "react";

const defaultFormState = {
  company: "",
  job_title: "",
  location: "",
  job_url: "",
  salary: "",
  status: "Saved",
  applied_date: "",
  job_description: "",
  notes: "",
};

const statusOptions = ["Saved", "Applied", "Interview", "Offer", "Rejected"];

export function ApplicationForm({
  initialData = null,
  onSubmit,
  isSubmitting,
  submitLabel,
  onCancel,
}) {
  const [formData, setFormData] = useState(defaultFormState);
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (initialData) {
      setFormData({
        ...defaultFormState,
        ...initialData,
        applied_date: initialData.applied_date
          ? initialData.applied_date.slice(0, 10)
          : "",
      });
    }
  }, [initialData]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    setErrors((prev) => ({ ...prev, [name]: "" }));
  };

  const validateForm = () => {
    const nextErrors = {};

    if (!formData.company?.trim()) nextErrors.company = "Company is required";
    if (!formData.job_title?.trim())
      nextErrors.job_title = "Job title is required";
    if (!formData.job_description?.trim())
      nextErrors.job_description = "Job description is required";
    if (formData.job_url && !/^https?:\/\//i.test(formData.job_url)) {
      nextErrors.job_url = "Job URL must start with http:// or https://";
    }

    if (formData.status && !statusOptions.includes(formData.status)) {
      nextErrors.status = "Invalid status";
    }

    setErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!validateForm()) return;

    const payload = {
      ...formData,
      company: formData.company.trim(),
      job_title: formData.job_title.trim(),
      location: formData.location?.trim() || null,
      job_url: formData.job_url?.trim() || null,
      salary: formData.salary?.trim() || null,
      applied_date: formData.applied_date || null,
      notes: formData.notes?.trim() || null,
      job_description: formData.job_description.trim(),
    };

    onSubmit(payload);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="row g-3">
        <div className="col-md-6">
          <label htmlFor="company" className="form-label">
            Company *
          </label>
          <input
            id="company"
            name="company"
            className={`form-control ${errors.company ? "is-invalid" : ""}`}
            value={formData.company}
            onChange={handleChange}
            disabled={isSubmitting}
          />
          {errors.company && (
            <div className="invalid-feedback d-block">{errors.company}</div>
          )}
        </div>

        <div className="col-md-6">
          <label htmlFor="job_title" className="form-label">
            Job Title *
          </label>
          <input
            id="job_title"
            name="job_title"
            className={`form-control ${errors.job_title ? "is-invalid" : ""}`}
            value={formData.job_title}
            onChange={handleChange}
            disabled={isSubmitting}
          />
          {errors.job_title && (
            <div className="invalid-feedback d-block">{errors.job_title}</div>
          )}
        </div>

        <div className="col-md-6">
          <label htmlFor="location" className="form-label">
            Location
          </label>
          <input
            id="location"
            name="location"
            className="form-control"
            value={formData.location}
            onChange={handleChange}
            disabled={isSubmitting}
          />
        </div>

        <div className="col-md-6">
          <label htmlFor="job_url" className="form-label">
            Job URL
          </label>
          <input
            id="job_url"
            name="job_url"
            type="url"
            className={`form-control ${errors.job_url ? "is-invalid" : ""}`}
            value={formData.job_url}
            onChange={handleChange}
            disabled={isSubmitting}
          />
          {errors.job_url && (
            <div className="invalid-feedback d-block">{errors.job_url}</div>
          )}
        </div>

        <div className="col-md-4">
          <label htmlFor="salary" className="form-label">
            Salary
          </label>
          <input
            id="salary"
            name="salary"
            className="form-control"
            value={formData.salary}
            onChange={handleChange}
            disabled={isSubmitting}
          />
        </div>

        <div className="col-md-4">
          <label htmlFor="status" className="form-label">
            Status
          </label>
          <select
            id="status"
            name="status"
            className={`form-select ${errors.status ? "is-invalid" : ""}`}
            value={formData.status}
            onChange={handleChange}
            disabled={isSubmitting}
          >
            {statusOptions.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
          {errors.status && (
            <div className="invalid-feedback d-block">{errors.status}</div>
          )}
        </div>

        <div className="col-md-4">
          <label htmlFor="applied_date" className="form-label">
            Applied Date
          </label>
          <input
            id="applied_date"
            name="applied_date"
            type="date"
            className="form-control"
            value={formData.applied_date}
            onChange={handleChange}
            disabled={isSubmitting}
          />
        </div>

        <div className="col-12">
          <label htmlFor="job_description" className="form-label">
            Job Description *
          </label>
          <textarea
            id="job_description"
            name="job_description"
            rows="6"
            className={`form-control ${errors.job_description ? "is-invalid" : ""}`}
            value={formData.job_description}
            onChange={handleChange}
            disabled={isSubmitting}
          />
          {errors.job_description && (
            <div className="invalid-feedback d-block">
              {errors.job_description}
            </div>
          )}
        </div>

        <div className="col-12">
          <label htmlFor="notes" className="form-label">
            Notes
          </label>
          <textarea
            id="notes"
            name="notes"
            rows="3"
            className="form-control"
            value={formData.notes}
            onChange={handleChange}
            disabled={isSubmitting}
          />
        </div>
      </div>

      <div className="d-flex justify-content-end gap-2 mt-4">
        {onCancel && (
          <button
            type="button"
            className="btn btn-outline-secondary"
            onClick={onCancel}
            disabled={isSubmitting}
          >
            Cancel
          </button>
        )}
        <button
          type="submit"
          className="btn btn-primary"
          disabled={isSubmitting}
        >
          {isSubmitting ? (
            <>
              <span
                className="spinner-border spinner-border-sm me-2"
                role="status"
                aria-hidden="true"
              ></span>
              {submitLabel}
            </>
          ) : (
            submitLabel
          )}
        </button>
      </div>
    </form>
  );
}
