export interface ApiResponse<T> {
  data: T;
  meta?: {
    page?: number;
    total?: number;
    per_page?: number;
  };
  errors?: string[];
}

export interface ApiError {
  detail?: string;
  message?: string;
  status?: number;
}
