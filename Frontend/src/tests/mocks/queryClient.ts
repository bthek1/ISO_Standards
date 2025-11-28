import { vitest } from 'vitest';

export const mockQueryClient = {
  prefetchQuery: vitest.fn(),
  setQueryData: vitest.fn(),
  getQueryData: vitest.fn(),
};
