export const constants = {
  API_TIMEOUT: 30000,
  DEBOUNCE_DELAY: 500,
  CACHE_TIME: 5 * 60 * 1000, // 5 minutes
  STALE_TIME: 1 * 60 * 1000, // 1 minute
  RETRY_COUNT: 3,
  PAGE_SIZE: 20,
  MAX_TAG_LENGTH: 50,
  MAX_SEARCH_LENGTH: 200,
};

export const routes = {
  HOME: '/',
  SEARCH: '/search',
  STANDARDS: '/standards',
  STANDARD_DETAIL: (id: string) => `/standards/${id}`,
  RAG_CHAT: '/rag',
  DASHBOARD: '/dashboard',
  LOGIN: '/login',
  REGISTER: '/register',
  PROFILE: '/profile',
  NOT_FOUND: '/404',
};

export const messages = {
  SUCCESS: 'Operation completed successfully',
  ERROR: 'An error occurred. Please try again.',
  LOADING: 'Loading...',
  NO_DATA: 'No data available',
  UNAUTHORIZED: 'Please log in to continue',
  FORBIDDEN: 'You do not have permission to access this',
  NOT_FOUND: 'The requested resource was not found',
};
