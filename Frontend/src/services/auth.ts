import api from './api';

interface LoginRequest {
  email: string;
  password: string;
}

interface LoginResponse {
  access: string;
  refresh: string;
  user: {
    id: string;
    email: string;
    name: string;
  };
}

interface RegisterRequest {
  email: string;
  password: string;
  name: string;
}

interface User {
  id: string;
  email: string;
  name: string;
}

export const authService = {
  login: async (credentials: LoginRequest) => {
    const { data } = await api.post<LoginResponse>(
      '/auth/login/',
      credentials
    );
    return data;
  },

  register: async (userData: RegisterRequest) => {
    const { data } = await api.post<LoginResponse>(
      '/auth/register/',
      userData
    );
    return data;
  },

  logout: async () => {
    await api.post('/auth/logout/');
  },

  getCurrentUser: async () => {
    const { data } = await api.get<User>('/auth/me/');
    return data;
  },

  refreshToken: async (refreshToken: string) => {
    const { data } = await api.post<{ access: string }>(
      '/auth/token/refresh/',
      { refresh: refreshToken }
    );
    return data;
  },
};
