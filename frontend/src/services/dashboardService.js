import api from './api';

export const dashboardService = {
  getDashboardStats: () => api.get('/api/dashboard/stats'),
};

export default dashboardService;
