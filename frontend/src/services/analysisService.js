import api from './api';

export const analysisService = {
  analyzeJob: (applicationId) => api.post(`/api/analysis/job/${applicationId}`),
  analyzeResumeMatch: (applicationId) => api.post(`/api/analysis/match/${applicationId}`),
  getApplicationAnalysis: (applicationId) => api.get(`/api/analysis/application/${applicationId}`),
};

export default analysisService;
