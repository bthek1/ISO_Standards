import { useAuthStore } from '@/stores/authStore';

export const useAuth = () => {
  const {
    user,
    accessToken,
    isAuthenticated,
    isLoading,
    error,
    login,
    register,
    logout,
    setUser,
    setTokens,
    clearError,
    checkAuth,
  } = useAuthStore();

  return {
    user,
    accessToken,
    isAuthenticated,
    isLoading,
    error,
    login,
    register,
    logout,
    setUser,
    setTokens,
    clearError,
    checkAuth,
  };
};
