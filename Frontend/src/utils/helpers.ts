export const handleApiError = (error: unknown): string => {
  if (error && typeof error === 'object' && 'response' in error) {
    const axiosError = error as { response: { data: unknown } };
    // Server responded with error status
    const data = axiosError.response.data;
    if (typeof data === 'string') return data;
    if (data && typeof data === 'object') {
      if ('detail' in data && typeof data.detail === 'string')
        return data.detail;
      if ('message' in data && typeof data.message === 'string')
        return data.message;
      if ('errors' in data && Array.isArray(data.errors) && data.errors[0])
        return String(data.errors[0]);
    }
    return 'An error occurred';
  } else if (error && typeof error === 'object' && 'request' in error) {
    // Request made but no response
    return 'No response from server. Please check your connection.';
  }
  // Other errors
  if (error instanceof Error) return error.message;
  return 'An unexpected error occurred';
};

export const sleep = (ms: number): Promise<void> => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};

export const classNames = (
  ...classes: (string | undefined | false)[]
): string => {
  return classes.filter(Boolean).join(' ');
};

export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const isEmpty = (value: unknown): boolean => {
  return (
    value === undefined ||
    value === null ||
    (typeof value === 'string' && value.trim() === '') ||
    (Array.isArray(value) && value.length === 0) ||
    (typeof value === 'object' && Object.keys(value).length === 0)
  );
};
