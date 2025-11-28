import api from './api';

interface Standard {
  id: string;
  title: string;
  code: string;
  description: string;
  category: string;
  organization: string;
  year: number;
}

interface StandardsParams {
  page?: number;
  search?: string;
  category?: string;
}

interface StandardsResponse {
  data: Standard[];
  meta: {
    page: number;
    total: number;
    per_page: number;
  };
}

export const standardsService = {
  getAll: async (params?: StandardsParams) => {
    const { data } = await api.get<StandardsResponse>(
      '/standards/',
      { params }
    );
    return data;
  },

  getById: async (id: string) => {
    const { data } = await api.get<Standard>(`/standards/${id}/`);
    return data;
  },

  search: async (query: string) => {
    const { data } = await api.get<StandardsResponse>(
      '/standards/search/',
      { params: { q: query } }
    );
    return data;
  },
};
