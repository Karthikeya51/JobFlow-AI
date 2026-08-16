export function ApplicationFilters({
  search,
  onSearchChange,
  status,
  onStatusChange,
  sort,
  onSortChange,
  totalCount,
}) {
  return (
    <div className="card shadow-sm border-0 mb-4">
      <div className="card-body">
        <div className="row g-3 align-items-center">
          <div className="col-lg-5">
            <label
              htmlFor="application-search"
              className="form-label visually-hidden"
            >
              Search
            </label>
            <div className="input-group">
              <span className="input-group-text">
                <i className="bi bi-search"></i>
              </span>
              <input
                id="application-search"
                type="search"
                className="form-control"
                placeholder="Search company, role, location"
                value={search}
                onChange={(event) => onSearchChange(event.target.value)}
              />
            </div>
          </div>

          <div className="col-md-3 col-lg-2">
            <label
              htmlFor="status-filter"
              className="form-label visually-hidden"
            >
              Status
            </label>
            <select
              id="status-filter"
              className="form-select"
              value={status}
              onChange={(event) => onStatusChange(event.target.value)}
            >
              <option value="">All</option>
              <option value="Saved">Saved</option>
              <option value="Applied">Applied</option>
              <option value="Interview">Interview</option>
              <option value="Offer">Offer</option>
              <option value="Rejected">Rejected</option>
            </select>
          </div>

          <div className="col-md-3 col-lg-2">
            <label htmlFor="sort-filter" className="form-label visually-hidden">
              Sort
            </label>
            <select
              id="sort-filter"
              className="form-select"
              value={sort}
              onChange={(event) => onSortChange(event.target.value)}
            >
              <option value="created_at_desc">Newest</option>
              <option value="created_at_asc">Oldest</option>
              <option value="company_asc">Company A-Z</option>
              <option value="company_desc">Company Z-A</option>
              <option value="applied_date_desc">Recently Applied</option>
            </select>
          </div>

          <div className="col-md-3 col-lg-3 text-md-end">
            <div className="text-muted small fw-semibold">
              {totalCount} {totalCount === 1 ? "application" : "applications"}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
