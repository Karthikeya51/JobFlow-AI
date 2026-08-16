import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Navbar } from "../components/common/Navbar";
import { StatsCard } from "../components/dashboard/StatsCard";
import { StatusDistributionChart } from "../components/dashboard/StatusDistributionChart";
import { ApplicationTrendChart } from "../components/dashboard/ApplicationTrendChart";
import { useAuth } from "../hooks/useAuth";
import dashboardService from "../services/dashboardService";

export function DashboardPage() {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    summary: {
      total: 0,
      saved: 0,
      applied: 0,
      interview: 0,
      offer: 0,
      rejected: 0,
    },
    conversion: { interview_rate: 0, offer_rate: 0 },
    status_distribution: [],
    monthly_trend: [],
    recent_applications: [],
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadStats = async () => {
      try {
        setIsLoading(true);
        const response = await dashboardService.getDashboardStats();
        setStats(response.data);
      } catch (err) {
        setError(
          err.response?.data?.detail || "Unable to load dashboard data.",
        );
      } finally {
        setIsLoading(false);
      }
    };

    loadStats();
  }, []);

  return (
    <div className="bg-light min-vh-100">
      <Navbar />
      <div className="container py-4 py-lg-5">
        <div className="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-4">
          <div>
            <p className="text-primary fw-semibold mb-1">Overview</p>
            <h1 className="mb-1">Welcome back, {user?.name || "there"}</h1>
            <p className="text-muted mb-0">
              Track hiring momentum and conversion at a glance.
            </p>
          </div>
          <Link to="/applications/new" className="btn btn-primary">
            + Add Application
          </Link>
        </div>

        {error && (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        )}

        {isLoading ? (
          <div className="text-center py-5">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
          </div>
        ) : (
          <>
            <div className="row g-3 mb-4">
              <div className="col-md-6 col-xl-3">
                <StatsCard
                  label="Total"
                  value={stats.summary.total}
                  icon="📊"
                  accentClass="primary"
                />
              </div>
              <div className="col-md-6 col-xl-3">
                <StatsCard
                  label="Saved"
                  value={stats.summary.saved}
                  icon="💾"
                  accentClass="secondary"
                />
              </div>
              <div className="col-md-6 col-xl-3">
                <StatsCard
                  label="Applied"
                  value={stats.summary.applied}
                  icon="📨"
                  accentClass="info"
                />
              </div>
              <div className="col-md-6 col-xl-3">
                <StatsCard
                  label="Interviews"
                  value={stats.summary.interview}
                  icon="🎯"
                  accentClass="warning"
                />
              </div>
            </div>

            <div className="row g-4 mb-4">
              <div className="col-xl-4">
                <StatusDistributionChart data={stats.status_distribution} />
              </div>
              <div className="col-xl-8">
                <ApplicationTrendChart data={stats.monthly_trend} />
              </div>
            </div>

            <div className="card border-0 shadow-sm">
              <div className="card-body">
                <div className="d-flex justify-content-between align-items-center mb-3">
                  <h5 className="card-title mb-0">Recent activity</h5>
                  <Link
                    to="/applications"
                    className="btn btn-link p-0 text-decoration-none"
                  >
                    View all applications
                  </Link>
                </div>

                {stats.recent_applications.length === 0 ? (
                  <div className="text-muted py-4 text-center">
                    No recent applications yet. Add your first job to start
                    tracking progress.
                  </div>
                ) : (
                  <div className="table-responsive">
                    <table className="table table-hover align-middle mb-0">
                      <thead>
                        <tr>
                          <th>Company</th>
                          <th>Role</th>
                          <th>Status</th>
                          <th>Applied</th>
                        </tr>
                      </thead>
                      <tbody>
                        {stats.recent_applications.map((application) => (
                          <tr key={application._id}>
                            <td>{application.company}</td>
                            <td>{application.job_title}</td>
                            <td>
                              <span className="badge bg-light text-dark border">
                                {application.status}
                              </span>
                            </td>
                            <td>
                              {application.applied_date
                                ? new Date(
                                    application.applied_date,
                                  ).toLocaleDateString()
                                : "—"}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
