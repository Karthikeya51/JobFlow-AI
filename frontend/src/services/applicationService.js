import api from './api';

export const applicationService = {
  getApplications: (params = {}) => api.get('/api/applications', { params }),
  getApplication: (id) => api.get(`/api/applications/${id}`),
  createApplication: (data) => api.post('/api/applications', data),
  updateApplication: (id, data) => api.put(`/api/applications/${id}`, data),
  deleteApplication: (id) => api.delete(`/api/applications/${id}`),
};

export default applicationService;
