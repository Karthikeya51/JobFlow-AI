const STATUS_CLASS_MAP = {
  Saved: "bg-secondary-subtle text-secondary-emphasis border",
  Applied: "bg-primary-subtle text-primary-emphasis border",
  Interview: "bg-warning-subtle text-warning-emphasis border",
  Offer: "bg-success-subtle text-success-emphasis border",
  Rejected: "bg-danger-subtle text-danger-emphasis border",
};

export function ApplicationStatusBadge({ status }) {
  const badgeClass = STATUS_CLASS_MAP[status] || "bg-light text-dark border";

  return (
    <span className={`badge rounded-pill ${badgeClass}`}>
      {status || "Saved"}
    </span>
  );
}
