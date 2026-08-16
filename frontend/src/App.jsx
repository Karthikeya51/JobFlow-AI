import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { ProtectedRoute } from "./components/ProtectedRoute";
import { LoginPage } from "./pages/LoginPage";
import { RegisterPage } from "./pages/RegisterPage";
import { ApplicationsPage } from "./pages/ApplicationsPage";
import { CreateApplicationPage } from "./pages/CreateApplicationPage";
import { ApplicationDetailPage } from "./pages/ApplicationDetailPage";
import { EditApplicationPage } from "./pages/EditApplicationPage";
import { DashboardPage } from "./pages/DashboardPage";
import { ResumeProfilePage } from "./pages/ResumeProfilePage";
import { AnalysisPage } from "./pages/AnalysisPage";

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/resume"
            element={
              <ProtectedRoute>
                <ResumeProfilePage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/analysis/:applicationId"
            element={
              <ProtectedRoute>
                <AnalysisPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/applications"
            element={
              <ProtectedRoute>
                <ApplicationsPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/applications/new"
            element={
              <ProtectedRoute>
                <CreateApplicationPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/applications/:id"
            element={
              <ProtectedRoute>
                <ApplicationDetailPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/applications/:id/edit"
            element={
              <ProtectedRoute>
                <EditApplicationPage />
              </ProtectedRoute>
            }
          />

          <Route path="/" element={<Navigate to="/applications" replace />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
