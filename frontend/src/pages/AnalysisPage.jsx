import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { Navbar } from "../components/common/Navbar";
import { MatchScoreCard } from "../components/analysis/MatchScoreCard";
import applicationService from "../services/applicationService";
import analysisService from "../services/analysisService";

export function AnalysisPage() {
  const { applicationId } = useParams();
  const [application, setApplication] = useState(null);
  const [analysis, setAnalysis] = useState({
    job_analysis: null,
    resume_match: null,
  });
  const [isLoading, setIsLoading] = useState(true);
  const [isAnalyzingJob, setIsAnalyzingJob] = useState(false);
  const [isAnalyzingMatch, setIsAnalyzingMatch] = useState(false);
  const [error, setError] = useState("");

  const loadData = async () => {
    try {
      setIsLoading(true);
      const response = await applicationService.getApplication(applicationId);
      setApplication(response.data);
      const analysisResponse =
        await analysisService.getApplicationAnalysis(applicationId);
      setAnalysis(
        analysisResponse.data || { job_analysis: null, resume_match: null },
      );
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load analysis.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [applicationId]);

  const handleJobAnalysis = async () => {
    try {
      setIsAnalyzingJob(true);
      setError("");
      const response = await analysisService.analyzeJob(applicationId);
      setAnalysis((prev) => ({ ...prev, job_analysis: response.data }));
    } catch (err) {
      setError(
        err.response?.data?.detail || "Unable to analyze job description.",
      );
    } finally {
      setIsAnalyzingJob(false);
    }
  };

  const handleResumeMatch = async () => {
    try {
      setIsAnalyzingMatch(true);
      setError("");
      const response = await analysisService.analyzeResumeMatch(applicationId);
      setAnalysis((prev) => ({ ...prev, resume_match: response.data }));
    } catch (err) {
      const detail =
        err.response?.data?.detail ||
        "Unable to compare resume with this role.";
      if (detail.toLowerCase().includes("resume")) {
        setError(detail + " Please add your resume profile first.");
      } else {
        setError(detail);
      }
    } finally {
      setIsAnalyzingMatch(false);
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

  if (!application) {
    return (
      <div>
        <Navbar />
        <div className="container py-5">
          <div className="alert alert-danger">
            {error || "Application not found."}
          </div>
          <Link to="/applications" className="btn btn-primary">
            Back to applications
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div>
      <Navbar />
      <div className="container py-4 py-lg-5">
        <div className="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-4">
          <div>
            <p className="text-uppercase text-secondary small fw-semibold mb-1">
              AI Analysis
            </p>
            <h1 className="mb-1">{application.company}</h1>
            <div className="text-muted">{application.job_title}</div>
          </div>
          <div className="d-flex gap-2 flex-wrap">
            <button
              className="btn btn-primary"
              onClick={handleJobAnalysis}
              disabled={isAnalyzingJob || isAnalyzingMatch}
            >
              {isAnalyzingJob ? "Analyzing job..." : "Analyze Job"}
            </button>
            <button
              className="btn btn-outline-primary"
              onClick={handleResumeMatch}
              disabled={isAnalyzingJob || isAnalyzingMatch}
            >
              {isAnalyzingMatch
                ? "Comparing resume..."
                : "Analyze Resume Match"}
            </button>
            <Link
              to={`/applications/${applicationId}`}
              className="btn btn-outline-secondary"
            >
              Back to Application
            </Link>
          </div>
        </div>

        {error && <div className="alert alert-danger">{error}</div>}

        <div className="row g-4">
          {analysis.job_analysis && (
            <div className="col-lg-6">
              <div className="card border-0 shadow-sm h-100">
                <div className="card-body p-4">
                  <h4 className="mb-3">Job Analysis</h4>
                  <p className="text-muted">{analysis.job_analysis.summary}</p>

                  <div className="mb-3">
                    <h6>Required Skills</h6>
                    <div className="d-flex flex-wrap gap-2">
                      {analysis.job_analysis.required_skills?.map((skill) => (
                        <span key={skill} className="badge text-bg-primary">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="mb-3">
                    <h6>Preferred Skills</h6>
                    <div className="d-flex flex-wrap gap-2">
                      {analysis.job_analysis.preferred_skills?.map((skill) => (
                        <span key={skill} className="badge text-bg-secondary">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="mb-3">
                    <h6>Responsibilities</h6>
                    <ul className="mb-0 ps-3">
                      {analysis.job_analysis.responsibilities?.map((item) => (
                        <li key={item}>{item}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="mb-3">
                    <h6>Experience Requirements</h6>
                    <p className="mb-0">
                      {analysis.job_analysis.experience_requirements}
                    </p>
                  </div>

                  <div>
                    <h6>Important Keywords</h6>
                    <div className="d-flex flex-wrap gap-2">
                      {analysis.job_analysis.keywords?.map((keyword) => (
                        <span
                          key={keyword}
                          className="badge text-bg-light border"
                        >
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {analysis.resume_match && (
            <div className="col-lg-6">
              <MatchScoreCard
                score={analysis.resume_match.match_score}
                summary={analysis.resume_match.summary}
              />
              <div className="card border-0 shadow-sm mt-4">
                <div className="card-body p-4">
                  <h5 className="mb-3">Your Strengths</h5>
                  <ul className="mb-3 ps-3">
                    {analysis.resume_match.strengths?.map((strength) => (
                      <li key={strength}>{strength}</li>
                    ))}
                  </ul>

                  <h5 className="mb-3">Skills to Improve</h5>
                  <ul className="mb-3 ps-3">
                    {analysis.resume_match.missing_skills?.map((skill) => (
                      <li key={skill}>{skill}</li>
                    ))}
                  </ul>

                  <h5 className="mb-3">Recommendations</h5>
                  <ul className="mb-0 ps-3">
                    {analysis.resume_match.recommendations?.map((rec) => (
                      <li key={rec}>{rec}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}
        </div>

        {!analysis.job_analysis && !analysis.resume_match && !error && (
          <div className="card border-0 shadow-sm mt-4">
            <div className="card-body p-4 text-center text-muted">
              Use AI to understand this opportunity and compare it with your
              saved resume profile.
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
