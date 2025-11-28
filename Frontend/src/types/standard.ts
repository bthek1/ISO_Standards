export interface Standard {
  id: string;
  title: string;
  code: string;
  description: string;
  category: string;
  organization: string;
  year: number;
  content?: string;
  relatedStandards?: string[];
}

export interface StandardsParams {
  page?: number;
  search?: string;
  category?: string;
}

export interface StandardsResponse {
  data: Standard[];
  meta: {
    page: number;
    total: number;
    per_page: number;
  };
}
