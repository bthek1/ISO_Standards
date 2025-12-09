# React + TypeScript + Vite Starter Pack

A comprehensive guide for modern React development with TypeScript, designed for the ISO Standards frontend.

## Table of Contents

1. [Core React Concepts](#core-react-concepts)
2. [Project Setup](#project-setup)
3. [Styling with Tailwind CSS](#styling-with-tailwind-css)
4. [Routing with React Router](#routing-with-react-router)
5. [Data Fetching with TanStack Query](#data-fetching-with-tanstack-query)
6. [State Management](#state-management)
7. [Form Management](#form-management)
8. [Testing](#testing)
9. [Best Practices](#best-practices)

---

## Core React Concepts

### 1. Components

Components are the building blocks of React applications. Use functional components with TypeScript.

**Basic Component:**

```typescript
// Button.tsx
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  label,
  onClick,
  variant = 'primary',
  disabled = false
}) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`btn btn-${variant}`}
    >
      {label}
    </button>
  );
};
```

**Component with Children:**

```typescript
// Card.tsx
interface CardProps {
  title: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

export const Card: React.FC<CardProps> = ({ title, children, footer }) => {
  return (
    <div className="card">
      <div className="card-header">
        <h3>{title}</h3>
      </div>
      <div className="card-body">
        {children}
      </div>
      {footer && (
        <div className="card-footer">
          {footer}
        </div>
      )}
    </div>
  );
};
```

### 2. Props

Props are how data flows from parent to child components.

```typescript
// Types for props
interface UserProfileProps {
  user: {
    id: string;
    name: string;
    email: string;
    avatar?: string;
  };
  onEdit?: (userId: string) => void;
}

export const UserProfile: React.FC<UserProfileProps> = ({ user, onEdit }) => {
  return (
    <div className="user-profile">
      {user.avatar && <img src={user.avatar} alt={user.name} />}
      <h2>{user.name}</h2>
      <p>{user.email}</p>
      {onEdit && (
        <button onClick={() => onEdit(user.id)}>Edit Profile</button>
      )}
    </div>
  );
};
```

### 3. State (useState)

State is data that changes over time within a component.

```typescript
import { useState } from 'react';

export const Counter: React.FC = () => {
  const [count, setCount] = useState<number>(0);
  const [history, setHistory] = useState<number[]>([]);

  const increment = () => {
    setCount(prev => prev + 1);
    setHistory(prev => [...prev, count + 1]);
  };

  const decrement = () => {
    setCount(prev => prev - 1);
    setHistory(prev => [...prev, count - 1]);
  };

  return (
    <div>
      <h2>Count: {count}</h2>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
      <p>History: {history.join(', ')}</p>
    </div>
  );
};
```

### 4. Effects (useEffect)

Effects let you synchronize with external systems.

```typescript
import { useState, useEffect } from 'react';

export const DocumentTitle: React.FC<{ title: string }> = ({ title }) => {
  useEffect(() => {
    // Update document title
    document.title = title;

    // Cleanup function (optional)
    return () => {
      document.title = 'ISO Standards';
    };
  }, [title]); // Re-run when title changes

  return <h1>{title}</h1>;
};

// Fetching data with useEffect
export const UserData: React.FC<{ userId: string }> = ({ userId }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        setLoading(true);
        const response = await fetch(`/api/users/${userId}`);
        const data = await response.json();
        setUser(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!user) return <div>No user found</div>;

  return <div>{user.name}</div>;
};
```

### 5. Custom Hooks

Extract reusable logic into custom hooks.

```typescript
// useLocalStorage.ts
import { useState, useEffect } from 'react';

export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });

  const setValue = (value: T) => {
    try {
      setStoredValue(value);
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(error);
    }
  };

  return [storedValue, setValue];
}

// Usage
const [theme, setTheme] = useLocalStorage<'light' | 'dark'>('theme', 'light');
```

### 6. Context API

Share data across the component tree without prop drilling.

```typescript
// AuthContext.tsx
import { createContext, useContext, useState, ReactNode } from 'react';

interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  const login = async (email: string, password: string) => {
    // API call
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    const userData = await response.json();
    setUser(userData);
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        logout,
        isAuthenticated: !!user
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

// Usage in component
const Profile = () => {
  const { user, logout } = useAuth();

  return (
    <div>
      <h1>Welcome, {user?.name}</h1>
      <button onClick={logout}>Logout</button>
    </div>
  );
};
```

---

## Project Setup

### 1. Initialize Project

```bash
# Create new Vite project with React + TypeScript
npm create vite@latest iso-standards-frontend -- --template react-ts

cd iso-standards-frontend
npm install
```

### 2. Project Structure

```
src/
├── components/
│   ├── ui/                  # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Card.tsx
│   │   └── index.ts
│   ├── layout/             # Layout components
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   ├── Sidebar.tsx
│   │   └── MainLayout.tsx
│   └── features/           # Feature-specific components
│       ├── standards/
│       ├── search/
│       └── auth/
├── pages/                  # Route pages
│   ├── Home.tsx
│   ├── StandardDetail.tsx
│   ├── Search.tsx
│   └── Dashboard.tsx
├── hooks/                  # Custom hooks
│   ├── useAuth.ts
│   ├── useDebounce.ts
│   └── useLocalStorage.ts
├── services/               # API services
│   ├── api.ts
│   ├── standards.ts
│   └── auth.ts
├── stores/                 # Zustand stores
│   ├── authStore.ts
│   └── themeStore.ts
├── types/                  # TypeScript types
│   ├── standard.ts
│   ├── user.ts
│   └── api.ts
├── utils/                  # Utility functions
│   ├── format.ts
│   ├── validation.ts
│   └── constants.ts
├── styles/                 # Global styles
│   └── global.css
├── App.tsx
├── main.tsx
└── vite-env.d.ts
```

### 3. Install Core Dependencies

```bash
# Routing
npm install react-router-dom

# Data fetching
npm install @tanstack/react-query
npm install axios

# State management
npm install zustand

# Form management
npm install react-hook-form @hookform/resolvers zod

# UI/Styling
npm install tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Icons
npm install lucide-react

# Utilities
npm install clsx tailwind-merge
npm install date-fns
```

### 4. Install Dev Dependencies

```bash
npm install -D @types/node

# Testing
npm install -D vitest @vitest/ui
npm install -D @testing-library/react @testing-library/jest-dom
npm install -D @testing-library/user-event
npm install -D jsdom

# Linting & Formatting
npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
npm install -D prettier eslint-config-prettier eslint-plugin-prettier
npm install -D eslint-plugin-react eslint-plugin-react-hooks
```

### 5. TypeScript Configuration

**tsconfig.json:**

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,

    /* Path aliases */
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/pages/*": ["./src/pages/*"],
      "@/hooks/*": ["./src/hooks/*"],
      "@/utils/*": ["./src/utils/*"],
      "@/types/*": ["./src/types/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### 6. ESLint Configuration

**.eslintrc.cjs:**

```javascript
module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
    'plugin:react/recommended',
    'plugin:react/jsx-runtime',
    'prettier',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parser: '@typescript-eslint/parser',
  plugins: ['react-refresh', '@typescript-eslint', 'react'],
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    'react/prop-types': 'off',
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
};
```

### 7. Prettier Configuration

**.prettierrc:**

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 88,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "avoid",
  "endOfLine": "lf"
}
```

### 8. Vite Configuration

**vite.config.ts:**

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@/components': path.resolve(__dirname, './src/components'),
      '@/pages': path.resolve(__dirname, './src/pages'),
      '@/hooks': path.resolve(__dirname, './src/hooks'),
      '@/utils': path.resolve(__dirname, './src/utils'),
      '@/types': path.resolve(__dirname, './src/types'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/tests/setup.ts',
  },
});
```

---

## Styling with Tailwind CSS

### 1. Tailwind Setup

**tailwind.config.js:**

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
          950: '#172554',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
```

**src/styles/global.css:**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
    font-feature-settings: "rlig" 1, "calt" 1;
  }
}

@layer components {
  .btn {
    @apply px-4 py-2 rounded-md font-medium transition-colors;
  }

  .btn-primary {
    @apply bg-primary-600 text-white hover:bg-primary-700;
  }

  .btn-secondary {
    @apply bg-gray-200 text-gray-900 hover:bg-gray-300;
  }

  .card {
    @apply bg-white rounded-lg shadow-md p-6;
  }

  .input {
    @apply w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500;
  }
}
```

### 2. Utility Function for Class Names

**src/utils/cn.ts:**

```typescript
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### 3. Example Components

**Button Component:**

```typescript
import { ButtonHTMLAttributes, forwardRef } from 'react';
import { cn } from '@/utils/cn';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', isLoading, children, disabled, ...props }, ref) => {
    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={cn(
          'inline-flex items-center justify-center rounded-md font-medium transition-colors',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
          'disabled:pointer-events-none disabled:opacity-50',
          {
            'bg-primary-600 text-white hover:bg-primary-700': variant === 'primary',
            'bg-gray-200 text-gray-900 hover:bg-gray-300': variant === 'secondary',
            'border border-gray-300 bg-transparent hover:bg-gray-100': variant === 'outline',
            'hover:bg-gray-100': variant === 'ghost',
          },
          {
            'h-8 px-3 text-sm': size === 'sm',
            'h-10 px-4': size === 'md',
            'h-12 px-6 text-lg': size === 'lg',
          },
          className
        )}
        {...props}
      >
        {isLoading && <span className="mr-2">Loading...</span>}
        {children}
      </button>
    );
  }
);
```

---

## Routing with React Router

### 1. Setup Routes

**src/App.tsx:**

```typescript
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { MainLayout } from '@/components/layout/MainLayout';
import { Home } from '@/pages/Home';
import { StandardDetail } from '@/pages/StandardDetail';
import { Search } from '@/pages/Search';
import { Dashboard } from '@/pages/Dashboard';
import { Login } from '@/pages/Login';
import { NotFound } from '@/pages/NotFound';
import { ProtectedRoute } from '@/components/ProtectedRoute';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Home />} />
          <Route path="search" element={<Search />} />
          <Route path="standards/:id" element={<StandardDetail />} />

          {/* Protected routes */}
          <Route element={<ProtectedRoute />}>
            <Route path="dashboard" element={<Dashboard />} />
          </Route>

          <Route path="login" element={<Login />} />
          <Route path="404" element={<NotFound />} />
          <Route path="*" element={<Navigate to="/404" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
```

### 2. Layout Component

**src/components/layout/MainLayout.tsx:**

```typescript
import { Outlet } from 'react-router-dom';
import { Header } from './Header';
import { Footer } from './Footer';

export const MainLayout: React.FC = () => {
  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <main className="flex-1">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
};
```

### 3. Protected Route

**src/components/ProtectedRoute.tsx:**

```typescript
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';

export const ProtectedRoute: React.FC = () => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};
```

### 4. Navigation

**src/components/layout/Header.tsx:**

```typescript
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';

export const Header: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="border-b bg-white">
      <div className="container mx-auto flex items-center justify-between px-4 py-4">
        <Link to="/" className="text-2xl font-bold">
          ISO Standards
        </Link>

        <nav className="flex items-center gap-4">
          <Link to="/search" className="hover:text-primary-600">
            Search
          </Link>

          {user ? (
            <>
              <Link to="/dashboard" className="hover:text-primary-600">
                Dashboard
              </Link>
              <button onClick={handleLogout} className="btn btn-secondary">
                Logout
              </button>
            </>
          ) : (
            <Link to="/login" className="btn btn-primary">
              Login
            </Link>
          )}
        </nav>
      </div>
    </header>
  );
};
```

### 5. Programmatic Navigation

```typescript
import { useNavigate, useSearchParams } from 'react-router-dom';

export const SearchPage: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  const query = searchParams.get('q') || '';

  const handleSearch = (newQuery: string) => {
    setSearchParams({ q: newQuery });
  };

  const handleViewStandard = (id: string) => {
    navigate(`/standards/${id}`);
  };

  return (
    <div>
      <input
        value={query}
        onChange={(e) => handleSearch(e.target.value)}
        placeholder="Search standards..."
      />
    </div>
  );
};
```

---

## Data Fetching with TanStack Query

### 1. Setup Query Client

**src/main.tsx:**

```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import App from './App';
import './styles/global.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  </React.StrictMode>
);
```

### 2. API Service Layer

**src/services/api.ts:**

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for handling errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Handle token refresh or redirect to login
      localStorage.removeItem('accessToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

**src/services/standards.ts:**

```typescript
import api from './api';
import { Standard, StandardsResponse } from '@/types/standard';

export const standardsService = {
  getAll: async (params?: {
    page?: number;
    search?: string;
    category?: string;
  }): Promise<StandardsResponse> => {
    const { data } = await api.get('/standards/', { params });
    return data;
  },

  getById: async (id: string): Promise<Standard> => {
    const { data } = await api.get(`/standards/${id}/`);
    return data;
  },

  search: async (query: string): Promise<Standard[]> => {
    const { data } = await api.post('/search/', { query });
    return data;
  },

  create: async (standard: Partial<Standard>): Promise<Standard> => {
    const { data } = await api.post('/standards/', standard);
    return data;
  },

  update: async (id: string, standard: Partial<Standard>): Promise<Standard> => {
    const { data } = await api.put(`/standards/${id}/`, standard);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/standards/${id}/`);
  },
};
```

### 3. Custom Query Hooks

**src/hooks/useStandards.ts:**

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { standardsService } from '@/services/standards';
import { Standard } from '@/types/standard';

// Fetch all standards
export const useStandards = (params?: {
  page?: number;
  search?: string;
  category?: string;
}) => {
  return useQuery({
    queryKey: ['standards', params],
    queryFn: () => standardsService.getAll(params),
  });
};

// Fetch single standard
export const useStandard = (id: string) => {
  return useQuery({
    queryKey: ['standards', id],
    queryFn: () => standardsService.getById(id),
    enabled: !!id,
  });
};

// Search standards
export const useSearchStandards = (query: string) => {
  return useQuery({
    queryKey: ['standards', 'search', query],
    queryFn: () => standardsService.search(query),
    enabled: query.length > 0,
  });
};

// Create standard mutation
export const useCreateStandard = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (standard: Partial<Standard>) =>
      standardsService.create(standard),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['standards'] });
    },
  });
};

// Update standard mutation
export const useUpdateStandard = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Standard> }) =>
      standardsService.update(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['standards'] });
      queryClient.invalidateQueries({ queryKey: ['standards', variables.id] });
    },
  });
};

// Delete standard mutation
export const useDeleteStandard = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => standardsService.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['standards'] });
    },
  });
};
```

### 4. Using Queries in Components

```typescript
import { useStandards, useDeleteStandard } from '@/hooks/useStandards';

export const StandardsList: React.FC = () => {
  const [page, setPage] = useState(1);
  const { data, isLoading, error } = useStandards({ page });
  const deleteMutation = useDeleteStandard();

  const handleDelete = async (id: string) => {
    if (confirm('Are you sure?')) {
      await deleteMutation.mutateAsync(id);
    }
  };

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <h1>Standards</h1>
      {data?.results.map((standard) => (
        <div key={standard.id}>
          <h3>{standard.title}</h3>
          <button onClick={() => handleDelete(standard.id)}>
            Delete
          </button>
        </div>
      ))}

      <button onClick={() => setPage(p => p - 1)} disabled={!data?.previous}>
        Previous
      </button>
      <button onClick={() => setPage(p => p + 1)} disabled={!data?.next}>
        Next
      </button>
    </div>
  );
};
```

### 5. Optimistic Updates

```typescript
export const useToggleFavorite = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, isFavorite }: { id: string; isFavorite: boolean }) =>
      standardsService.toggleFavorite(id, isFavorite),

    // Optimistic update
    onMutate: async ({ id, isFavorite }) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['standards', id] });

      // Snapshot previous value
      const previousStandard = queryClient.getQueryData(['standards', id]);

      // Optimistically update
      queryClient.setQueryData(['standards', id], (old: Standard) => ({
        ...old,
        isFavorite,
      }));

      return { previousStandard };
    },

    // Rollback on error
    onError: (err, variables, context) => {
      if (context?.previousStandard) {
        queryClient.setQueryData(
          ['standards', variables.id],
          context.previousStandard
        );
      }
    },

    // Always refetch after error or success
    onSettled: (data, error, variables) => {
      queryClient.invalidateQueries({ queryKey: ['standards', variables.id] });
    },
  });
};
```

---

## State Management

### 1. Local State (useState)

Use for component-specific state:

```typescript
const [count, setCount] = useState(0);
const [isOpen, setIsOpen] = useState(false);
const [formData, setFormData] = useState({ name: '', email: '' });
```

### 2. Context API (useContext)

Use for theme, auth, or moderate shared state:

```typescript
// ThemeContext.tsx
import { createContext, useContext, useState, ReactNode } from 'react';

type Theme = 'light' | 'dark';

interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [theme, setTheme] = useState<Theme>('light');

  const toggleTheme = () => {
    setTheme(prev => (prev === 'light' ? 'dark' : 'light'));
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
};
```

### 3. Zustand (Recommended for Complex State)

**src/stores/authStore.ts:**

```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthState {
  user: User | null;
  accessToken: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  setUser: (user: User) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      isAuthenticated: false,

      login: async (email, password) => {
        const response = await fetch('/api/auth/login', {
          method: 'POST',
          body: JSON.stringify({ email, password }),
        });
        const { user, accessToken } = await response.json();

        set({
          user,
          accessToken,
          isAuthenticated: true,
        });
      },

      logout: () => {
        set({
          user: null,
          accessToken: null,
          isAuthenticated: false,
        });
      },

      setUser: (user) => set({ user }),
    }),
    {
      name: 'auth-storage',
    }
  )
);
```

**src/stores/uiStore.ts:**

```typescript
import { create } from 'zustand';

interface UIState {
  sidebarOpen: boolean;
  theme: 'light' | 'dark';
  toggleSidebar: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
}

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: false,
  theme: 'light',

  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setTheme: (theme) => set({ theme }),
}));
```

**Usage:**

```typescript
import { useAuthStore } from '@/stores/authStore';

const Profile = () => {
  const { user, logout } = useAuthStore();

  return (
    <div>
      <h1>{user?.name}</h1>
      <button onClick={logout}>Logout</button>
    </div>
  );
};
```

### 4. Server State (TanStack Query)

**Never duplicate server state in global state!** Use TanStack Query:

```typescript
// ❌ Bad - duplicating server state
const [standards, setStandards] = useState([]);
useEffect(() => {
  fetchStandards().then(setStandards);
}, []);

// ✅ Good - use React Query
const { data: standards } = useQuery({
  queryKey: ['standards'],
  queryFn: fetchStandards,
});
```

---

## Form Management

### 1. Setup react-hook-form + zod

**src/schemas/standardSchema.ts:**

```typescript
import { z } from 'zod';

export const standardSchema = z.object({
  code: z.string().min(1, 'Code is required'),
  title: z.string().min(3, 'Title must be at least 3 characters'),
  organization: z.enum(['ISO', 'IEEE', 'ASTM', 'IEC']),
  description: z.string().optional(),
  publishedDate: z.string().datetime(),
  category: z.string().min(1, 'Category is required'),
});

export type StandardFormData = z.infer<typeof standardSchema>;
```

### 2. Form Component

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { standardSchema, StandardFormData } from '@/schemas/standardSchema';
import { useCreateStandard } from '@/hooks/useStandards';

export const StandardForm: React.FC = () => {
  const createMutation = useCreateStandard();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<StandardFormData>({
    resolver: zodResolver(standardSchema),
    defaultValues: {
      code: '',
      title: '',
      organization: 'ISO',
      description: '',
    },
  });

  const onSubmit = async (data: StandardFormData) => {
    try {
      await createMutation.mutateAsync(data);
      reset();
      // Show success message
    } catch (error) {
      // Handle error
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="code" className="block text-sm font-medium">
          Code
        </label>
        <input
          id="code"
          type="text"
          {...register('code')}
          className="input"
        />
        {errors.code && (
          <p className="mt-1 text-sm text-red-600">{errors.code.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="title" className="block text-sm font-medium">
          Title
        </label>
        <input
          id="title"
          type="text"
          {...register('title')}
          className="input"
        />
        {errors.title && (
          <p className="mt-1 text-sm text-red-600">{errors.title.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="organization" className="block text-sm font-medium">
          Organization
        </label>
        <select
          id="organization"
          {...register('organization')}
          className="input"
        >
          <option value="ISO">ISO</option>
          <option value="IEEE">IEEE</option>
          <option value="ASTM">ASTM</option>
          <option value="IEC">IEC</option>
        </select>
        {errors.organization && (
          <p className="mt-1 text-sm text-red-600">
            {errors.organization.message}
          </p>
        )}
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium">
          Description
        </label>
        <textarea
          id="description"
          {...register('description')}
          className="input"
          rows={4}
        />
        {errors.description && (
          <p className="mt-1 text-sm text-red-600">
            {errors.description.message}
          </p>
        )}
      </div>

      <button
        type="submit"
        disabled={isSubmitting || createMutation.isPending}
        className="btn btn-primary"
      >
        {isSubmitting ? 'Creating...' : 'Create Standard'}
      </button>
    </form>
  );
};
```

### 3. Reusable Form Components

**FormField Component:**

```typescript
import { UseFormRegister, FieldError } from 'react-hook-form';

interface FormFieldProps {
  label: string;
  name: string;
  type?: string;
  register: UseFormRegister<any>;
  error?: FieldError;
  placeholder?: string;
  required?: boolean;
}

export const FormField: React.FC<FormFieldProps> = ({
  label,
  name,
  type = 'text',
  register,
  error,
  placeholder,
  required,
}) => {
  return (
    <div>
      <label htmlFor={name} className="block text-sm font-medium">
        {label} {required && <span className="text-red-500">*</span>}
      </label>
      <input
        id={name}
        type={type}
        {...register(name)}
        placeholder={placeholder}
        className="input"
      />
      {error && (
        <p className="mt-1 text-sm text-red-600">{error.message}</p>
      )}
    </div>
  );
};
```

---

## Testing

### 1. Vitest Setup

**vitest.config.ts:**

```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/tests/setup.ts',
    css: true,
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

**src/tests/setup.ts:**

```typescript
import '@testing-library/jest-dom';
import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';

expect.extend(matchers);

afterEach(() => {
  cleanup();
});
```

### 2. Component Testing

**src/components/ui/Button.test.tsx:**

```typescript
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('applies variant class', () => {
    render(<Button variant="secondary">Button</Button>);
    const button = screen.getByText('Button');
    expect(button).toHaveClass('btn-secondary');
  });

  it('disables when disabled prop is true', () => {
    render(<Button disabled>Button</Button>);
    expect(screen.getByText('Button')).toBeDisabled();
  });

  it('shows loading state', () => {
    render(<Button isLoading>Button</Button>);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });
});
```

### 3. Hook Testing

**src/hooks/useDebounce.test.ts:**

```typescript
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useDebounce } from './useDebounce';

describe('useDebounce', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('returns initial value immediately', () => {
    const { result } = renderHook(() => useDebounce('test', 500));
    expect(result.current).toBe('test');
  });

  it('debounces value updates', async () => {
    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      {
        initialProps: { value: 'initial', delay: 500 },
      }
    );

    expect(result.current).toBe('initial');

    rerender({ value: 'updated', delay: 500 });
    expect(result.current).toBe('initial');

    vi.advanceTimersByTime(500);
    await waitFor(() => {
      expect(result.current).toBe('updated');
    });
  });
});
```

### 4. Testing with React Query

**src/hooks/useStandards.test.tsx:**

```typescript
import { describe, it, expect, vi } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useStandards } from './useStandards';
import * as standardsService from '@/services/standards';

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};

describe('useStandards', () => {
  it('fetches standards successfully', async () => {
    const mockData = {
      results: [{ id: '1', title: 'ISO 9001' }],
      count: 1,
    };

    vi.spyOn(standardsService, 'getAll').mockResolvedValue(mockData);

    const { result } = renderHook(() => useStandards(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toEqual(mockData);
  });

  it('handles errors', async () => {
    vi.spyOn(standardsService, 'getAll').mockRejectedValue(
      new Error('Failed to fetch')
    );

    const { result } = renderHook(() => useStandards(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => expect(result.current.isError).toBe(true));
    expect(result.current.error).toEqual(new Error('Failed to fetch'));
  });
});
```

### 5. Integration Testing

```typescript
import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { StandardsList } from './StandardsList';

const createTestWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });

  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>{children}</BrowserRouter>
    </QueryClientProvider>
  );
};

describe('StandardsList Integration', () => {
  it('displays standards and allows deletion', async () => {
    const user = userEvent.setup();

    render(<StandardsList />, { wrapper: createTestWrapper() });

    // Wait for data to load
    await waitFor(() => {
      expect(screen.getByText('ISO 9001')).toBeInTheDocument();
    });

    // Click delete button
    const deleteButton = screen.getByRole('button', { name: /delete/i });
    await user.click(deleteButton);

    // Confirm deletion
    // ... assert deletion happened
  });
});
```

### 6. Test Commands

**package.json:**

```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}
```

---

## Best Practices

### 1. Component Organization

```typescript
// ✅ Good - clear, organized, typed
interface Props {
  title: string;
  onSubmit: (data: FormData) => void;
}

export const MyComponent: React.FC<Props> = ({ title, onSubmit }) => {
  // 1. Hooks
  const [state, setState] = useState<string>('');
  const { data } = useQuery(/* ... */);

  // 2. Derived state
  const isValid = state.length > 0;

  // 3. Event handlers
  const handleClick = () => {
    setState('clicked');
  };

  // 4. Effects
  useEffect(() => {
    // side effects
  }, [state]);

  // 5. Render
  return <div>{/* JSX */}</div>;
};
```

### 2. Custom Hooks Patterns

```typescript
// Extract reusable logic
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}

// Usage
const debouncedSearch = useDebounce(searchTerm, 500);
```

### 3. Error Boundaries

```typescript
import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div>
          <h1>Something went wrong</h1>
          <pre>{this.state.error?.message}</pre>
        </div>
      );
    }

    return this.props.children;
  }
}
```

### 4. Code Splitting

```typescript
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

### 5. Performance Optimization

```typescript
import { memo, useMemo, useCallback } from 'react';

// Memoize expensive components
export const ExpensiveList = memo<{ items: Item[] }>(({ items }) => {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
});

// Memoize expensive calculations
const sortedItems = useMemo(() => {
  return items.sort((a, b) => a.name.localeCompare(b.name));
}, [items]);

// Memoize callback functions
const handleClick = useCallback((id: string) => {
  console.log('Clicked:', id);
}, []);
```

### 6. Type Safety

```typescript
// Define strict types
interface Standard {
  id: string;
  code: string;
  title: string;
  organization: Organization;
  publishedDate: Date;
}

type Organization = 'ISO' | 'IEEE' | 'ASTM' | 'IEC';

// Use discriminated unions
type Result<T> =
  | { status: 'loading' }
  | { status: 'error'; error: Error }
  | { status: 'success'; data: T };

// Type guards
function isError(result: Result<any>): result is { status: 'error'; error: Error } {
  return result.status === 'error';
}
```

### 7. Accessibility

```typescript
// Add ARIA labels
<button aria-label="Close modal" onClick={onClose}>
  <XIcon />
</button>

// Use semantic HTML
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
  </ul>
</nav>

// Keyboard navigation
<div
  role="button"
  tabIndex={0}
  onKeyDown={(e) => e.key === 'Enter' && handleClick()}
  onClick={handleClick}
>
  Click me
</div>
```

---

## Quick Reference

### Essential Commands

```bash
# Development
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview production build

# Testing
npm test            # Run tests
npm run test:ui     # Open test UI
npm run test:coverage

# Linting
npm run lint        # Run ESLint
npm run lint:fix    # Fix ESLint errors
npm run format      # Format with Prettier
```

### Folder Structure Summary

```
src/
├── components/     # Reusable UI components
├── pages/          # Route pages
├── hooks/          # Custom React hooks
├── services/       # API services
├── stores/         # Zustand stores
├── types/          # TypeScript types
├── utils/          # Utility functions
└── styles/         # Global styles
```

### Key Dependencies

- **React Router:** Navigation
- **TanStack Query:** Server state
- **Zustand:** Client state
- **react-hook-form + zod:** Forms
- **Tailwind CSS:** Styling
- **Vitest + RTL:** Testing

---

This starter pack provides everything needed to build a modern, type-safe, performant React application!
