# Frontend Setup Plan - ISO Standards Platform

## Project Overview

Create a modern React + TypeScript frontend for the ISO Standards platform with Material-UI (MUI), enabling users to search, explore, and interact with global standards using AI-powered RAG capabilities.

---

## Phase 1: Project Initialization

### 1.1 Create Vite + React + TypeScript Project

```bash
# From Frontend directory
npm create vite@latest . -- --template react-ts

# Install dependencies
npm install
```

### 1.2 Install Core Dependencies

```bash
# UI Framework - Material-UI
npm install @mui/material @mui/icons-material @emotion/react @emotion/styled

# Routing
npm install react-router-dom

# Data Fetching & Server State
npm install @tanstack/react-query @tanstack/react-query-devtools
npm install axios

# Global State Management
npm install zustand

# Form Management & Validation
npm install react-hook-form @hookform/resolvers zod

# Utilities
npm install date-fns
npm install clsx
```

### 1.3 Install Dev Dependencies

```bash
# TypeScript Types
npm install -D @types/node

# Testing
npm install -D vitest @vitest/ui jsdom
npm install -D @testing-library/react @testing-library/jest-dom @testing-library/user-event
npm install -D happy-dom

# Linting & Formatting
npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
npm install -D prettier eslint-config-prettier eslint-plugin-prettier
npm install -D eslint-plugin-react eslint-plugin-react-hooks eslint-plugin-react-refresh

# MSW for API mocking
npm install -D msw
```

---

## Phase 2: Project Structure Setup

### 2.1 Create Directory Structure

```text
src/
├── components/
│   ├── ui/                     # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Input.tsx
│   │   ├── LoadingSpinner.tsx
│   │   └── index.ts
│   ├── layout/                 # Layout components
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   ├── Sidebar.tsx
│   │   ├── MainLayout.tsx
│   │   └── index.ts
│   └── features/               # Feature-specific components
│       ├── standards/
│       │   ├── StandardCard.tsx
│       │   ├── StandardsList.tsx
│       │   ├── StandardDetail.tsx
│       │   └── StandardFilters.tsx
│       ├── search/
│       │   ├── SearchBar.tsx
│       │   ├── SearchResults.tsx
│       │   └── SearchFilters.tsx
│       ├── rag/
│       │   ├── ChatInterface.tsx
│       │   ├── ChatMessage.tsx
│       │   └── SourceCitation.tsx
│       └── auth/
│           ├── LoginForm.tsx
│           ├── RegisterForm.tsx
│           └── ProtectedRoute.tsx
├── pages/
│   ├── Home.tsx
│   ├── Search.tsx
│   ├── StandardDetail.tsx
│   ├── RAGChat.tsx
│   ├── Dashboard.tsx
│   ├── Login.tsx
│   ├── Register.tsx
│   └── NotFound.tsx
├── hooks/
│   ├── useAuth.ts
│   ├── useDebounce.ts
│   ├── useLocalStorage.ts
│   └── useMediaQuery.ts
├── services/
│   ├── api.ts
│   ├── standards.ts
│   ├── search.ts
│   ├── auth.ts
│   └── rag.ts
├── stores/
│   ├── authStore.ts
│   ├── uiStore.ts
│   └── searchStore.ts
├── types/
│   ├── standard.ts
│   ├── user.ts
│   ├── api.ts
│   └── index.ts
├── utils/
│   ├── constants.ts
│   ├── format.ts
│   ├── validation.ts
│   └── helpers.ts
├── theme/
│   ├── theme.ts
│   ├── colors.ts
│   └── typography.ts
├── tests/
│   ├── setup.ts
│   ├── mocks/
│   └── utils/
├── App.tsx
├── main.tsx
└── vite-env.d.ts
```

### 2.2 Create Configuration Files

**tsconfig.json** - TypeScript configuration with path aliases
**vite.config.ts** - Vite configuration with path resolution
**.eslintrc.cjs** - ESLint configuration
**.prettierrc** - Prettier configuration
**vitest.config.ts** - Vitest configuration

---

## Phase 3: Core Configuration

### 3.1 TypeScript Configuration (tsconfig.json)

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/pages/*": ["./src/pages/*"],
      "@/hooks/*": ["./src/hooks/*"],
      "@/services/*": ["./src/services/*"],
      "@/stores/*": ["./src/stores/*"],
      "@/types/*": ["./src/types/*"],
      "@/utils/*": ["./src/utils/*"],
      "@/theme/*": ["./src/theme/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### 3.2 Vite Configuration (vite.config.ts)

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
      '@/services': path.resolve(__dirname, './src/services'),
      '@/stores': path.resolve(__dirname, './src/stores'),
      '@/types': path.resolve(__dirname, './src/types'),
      '@/utils': path.resolve(__dirname, './src/utils'),
      '@/theme': path.resolve(__dirname, './src/theme'),
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
    css: true,
  },
});
```

### 3.3 Environment Variables (.env)

```bash
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME=ISO Standards Platform
VITE_ENABLE_DEVTOOLS=true
```

---

## Phase 4: Material-UI Theme Setup

### 4.1 Create Theme Configuration

**src/theme/theme.ts:**

```typescript
import { createTheme } from '@mui/material/styles';
import { colors } from './colors';
import { typography } from './typography';

export const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: colors.primary[600],
      light: colors.primary[400],
      dark: colors.primary[800],
    },
    secondary: {
      main: colors.secondary[600],
      light: colors.secondary[400],
      dark: colors.secondary[800],
    },
    error: {
      main: colors.error[600],
    },
    warning: {
      main: colors.warning[600],
    },
    success: {
      main: colors.success[600],
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography,
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        },
      },
    },
  },
});
```

**src/theme/colors.ts:**

```typescript
export const colors = {
  primary: {
    50: '#e3f2fd',
    100: '#bbdefb',
    200: '#90caf9',
    300: '#64b5f6',
    400: '#42a5f5',
    500: '#2196f3',
    600: '#1e88e5',
    700: '#1976d2',
    800: '#1565c0',
    900: '#0d47a1',
  },
  secondary: {
    50: '#f3e5f5',
    100: '#e1bee7',
    200: '#ce93d8',
    300: '#ba68c8',
    400: '#ab47bc',
    500: '#9c27b0',
    600: '#8e24aa',
    700: '#7b1fa2',
    800: '#6a1b9a',
    900: '#4a148c',
  },
  // Add more color definitions
};
```

### 4.2 Wrap App with MUI ThemeProvider

**src/main.tsx:**

```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { theme } from '@/theme/theme';
import App from './App';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <App />
        <ReactQueryDevtools initialIsOpen={false} />
      </ThemeProvider>
    </QueryClientProvider>
  </React.StrictMode>
);
```

---

## Phase 5: Core Features Implementation

### 5.1 API Service Layer

**src/services/api.ts:**

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
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

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('accessToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

### 5.2 Authentication Store (Zustand)

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
        // Implement login logic
      },

      logout: () => {
        set({ user: null, accessToken: null, isAuthenticated: false });
        localStorage.removeItem('accessToken');
      },

      setUser: (user) => set({ user }),
    }),
    {
      name: 'auth-storage',
    }
  )
);
```

### 5.3 Router Setup

**src/App.tsx:**

```typescript
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { MainLayout } from '@/components/layout/MainLayout';
import { Home } from '@/pages/Home';
import { Search } from '@/pages/Search';
import { StandardDetail } from '@/pages/StandardDetail';
import { RAGChat } from '@/pages/RAGChat';
import { Dashboard } from '@/pages/Dashboard';
import { Login } from '@/pages/Login';
import { Register } from '@/pages/Register';
import { NotFound } from '@/pages/NotFound';
import { ProtectedRoute } from '@/components/features/auth/ProtectedRoute';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Home />} />
          <Route path="search" element={<Search />} />
          <Route path="standards/:id" element={<StandardDetail />} />
          <Route path="rag" element={<RAGChat />} />

          <Route element={<ProtectedRoute />}>
            <Route path="dashboard" element={<Dashboard />} />
          </Route>

          <Route path="login" element={<Login />} />
          <Route path="register" element={<Register />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
```

---

## Phase 6: Key Components Development

### 6.1 Layout Components

- **Header** - Navigation bar with logo, search, user menu
- **Footer** - Links, copyright, social media
- **Sidebar** - Category navigation, filters (optional)
- **MainLayout** - Wrapper combining Header + Content + Footer

### 6.2 Standards Feature Components

- **StandardCard** - Display standard summary in grid/list
- **StandardsList** - Paginated list of standards
- **StandardDetail** - Full standard information
- **StandardFilters** - Organization, category, date filters

### 6.3 Search Feature Components

- **SearchBar** - Input with autocomplete
- **SearchResults** - Display search results
- **SearchFilters** - Advanced search filters

### 6.4 RAG Chat Feature Components

- **ChatInterface** - Chat UI container
- **ChatMessage** - Individual message component
- **SourceCitation** - Show document sources
- **ChatInput** - Message input with file upload

### 6.5 UI Components (MUI-based)

- **Button** - Customized MUI Button
- **Card** - Standard card component
- **Input** - Form input fields
- **LoadingSpinner** - Loading indicator
- **ErrorBoundary** - Error handling

---

## Phase 7: Data Fetching with TanStack Query

### 7.1 Create Custom Hooks

**src/hooks/useStandards.ts:**

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { standardsService } from '@/services/standards';

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

export const useStandard = (id: string) => {
  return useQuery({
    queryKey: ['standards', id],
    queryFn: () => standardsService.getById(id),
    enabled: !!id,
  });
};

export const useSearchStandards = (query: string) => {
  return useQuery({
    queryKey: ['standards', 'search', query],
    queryFn: () => standardsService.search(query),
    enabled: query.length > 2,
  });
};
```

---

## Phase 8: Testing Setup

### 8.1 Configure Vitest

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

### 8.2 Test Setup File

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

### 8.3 Example Component Test

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
});
```

---

## Phase 9: Additional Features

### 9.1 Dark Mode Support

Use MUI's theme mode switching:

```typescript
const [mode, setMode] = useState<'light' | 'dark'>('light');
const theme = createTheme({
  palette: {
    mode,
  },
});
```

### 9.2 Responsive Design

Use MUI's breakpoints and responsive props:

```typescript
<Grid container spacing={2}>
  <Grid item xs={12} sm={6} md={4}>
    <StandardCard />
  </Grid>
</Grid>
```

### 9.3 Internationalization (Future)

```bash
npm install i18next react-i18next
```

---

## Phase 10: Package.json Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "lint:fix": "eslint . --ext ts,tsx --fix",
    "format": "prettier --write \"src/**/*.{ts,tsx,json,css,md}\"",
    "type-check": "tsc --noEmit"
  }
}
```

---

## Implementation Checklist

### Phase 1: Foundation ✓

- [ ] Initialize Vite + React + TypeScript project
- [ ] Install all dependencies
- [ ] Setup directory structure
- [ ] Configure TypeScript, ESLint, Prettier
- [ ] Setup Vite config with path aliases

### Phase 2: Core Setup

- [ ] Configure Material-UI theme
- [ ] Setup React Router
- [ ] Configure TanStack Query
- [ ] Setup Zustand stores
- [ ] Create API service layer
- [ ] Setup environment variables

### Phase 3: Layout Components

- [ ] Header component
- [ ] Footer component
- [ ] MainLayout component
- [ ] Sidebar component (optional)

### Phase 4: Authentication

- [ ] Login page
- [ ] Register page
- [ ] Auth store (Zustand)
- [ ] Protected routes
- [ ] Auth service

### Phase 5: Standards Features

- [ ] Home page with featured standards
- [ ] Search page with filters
- [ ] Standard detail page
- [ ] Standards list component
- [ ] Standard card component
- [ ] Standards service & hooks

### Phase 6: RAG Features

- [ ] RAG chat page
- [ ] Chat interface component
- [ ] Message components
- [ ] Source citation component
- [ ] RAG service & hooks

### Phase 7: User Dashboard

- [ ] Dashboard page
- [ ] Saved standards
- [ ] Search history
- [ ] User preferences

### Phase 8: Testing

- [ ] Setup Vitest
- [ ] Write component tests
- [ ] Write hook tests
- [ ] Setup MSW for API mocking
- [ ] Integration tests

### Phase 9: Polish

- [ ] Error boundaries
- [ ] Loading states
- [ ] Empty states
- [ ] 404 page
- [ ] Responsive design
- [ ] Accessibility (ARIA labels)
- [ ] Dark mode support

### Phase 10: Deployment

- [ ] Build optimization
- [ ] Environment configuration
- [ ] Docker configuration
- [ ] CI/CD setup

---

## Key Technologies Summary

| Category | Technology | Purpose |
| -------- | ---------- | ------- |
| Framework | React 18 | UI library |
| Language | TypeScript | Type safety |
| Build Tool | Vite | Fast development & building |
| UI Library | Material-UI (MUI) | Component library |
| Routing | React Router v6 | Navigation |
| Server State | TanStack Query | Data fetching & caching |
| Client State | Zustand | Global state management |
| Forms | react-hook-form + zod | Form handling & validation |
| HTTP Client | Axios | API requests |
| Testing | Vitest + RTL | Unit & integration tests |
| Linting | ESLint + Prettier | Code quality |

---

## Development Workflow

1. **Start Development Server**

   ```bash
   npm run dev
   ```

2. **Run Tests in Watch Mode**

   ```bash
   npm test
   ```

3. **Check Types**

   ```bash
   npm run type-check
   ```

4. **Lint & Format**

   ```bash
   npm run lint:fix
   npm run format
   ```

5. **Build for Production**

   ```bash
   npm run build
   npm run preview
   ```

---

## Next Steps After Setup

1. **Create UI Component Library** - Build reusable MUI-based components
2. **Implement Authentication Flow** - Login, register, password reset
3. **Build Standards Browser** - List, search, filter, detail views
4. **Develop RAG Chat Interface** - Real-time chat with AI
5. **Add User Dashboard** - Personal workspace
6. **Implement Dark Mode** - Theme switching
7. **Optimize Performance** - Code splitting, lazy loading
8. **Add Analytics** - Track user behavior
9. **Deploy to Production** - AWS S3 + CloudFront

---

## Estimated Timeline

- **Phase 1-2 (Setup):** 1-2 days
- **Phase 3-4 (Layout & Auth):** 2-3 days
- **Phase 5 (Standards Features):** 3-5 days
- **Phase 6 (RAG Features):** 3-5 days
- **Phase 7 (Dashboard):** 2-3 days
- **Phase 8-9 (Testing & Polish):** 3-5 days
- **Phase 10 (Deployment):** 1-2 days

**Total:** 15-25 days for MVP

---

## Resources

- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)
- [Material-UI Documentation](https://mui.com/)
- [TanStack Query Documentation](https://tanstack.com/query/)
- [React Router Documentation](https://reactrouter.com/)
- [Zustand Documentation](https://github.com/pmndrs/zustand)
- [Vitest Documentation](https://vitest.dev/)

---

**Last Updated:** November 28, 2025
