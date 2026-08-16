export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const APPLICATION_STATUS = {
  SAVED: 'Saved',
  APPLIED: 'Applied',
  INTERVIEW: 'Interview',
  OFFER: 'Offer',
  REJECTED: 'Rejected',
}

export const STATUS_COLORS = {
  SAVED: 'secondary',
  APPLIED: 'info',
  INTERVIEW: 'warning',
  OFFER: 'success',
  REJECTED: 'danger',
}
