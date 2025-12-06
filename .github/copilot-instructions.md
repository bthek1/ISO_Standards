# GitHub Copilot Instructions for ISO Standards Project

## Project Overview

This is a full-stack application for explaining ISO standards and various global standards. The project implements RAG (Retrieval Augmented Generation) with PostgreSQL for intelligent document search and information retrieval.

### Tech Stack

**Backend:**

- Django 5.2+ with Python 3.13
- Django REST Framework for API endpoints
- PostgreSQL database with RAG capabilities
- django-allauth for authentication
- Custom user model (email-based authentication)

**Frontend:**

- React 18+ with TypeScript
- Vite as build tool
- TailwindCSS for styling
- React Router for navigation
- TanStack Query for server state
- Zustand for global state management
- react-hook-form + zod for forms

**Infrastructure:**

- AWS RDS for production database
- ASGI for async support
- Docker for containerization

## Project Structure

```
ISO_Standards/
├── Backend/
│   ├── accounts/          # Custom user authentication
│   ├── config/            # Django settings & configuration
│   ├── templates/         # Django templates
│   ├── static/            # Static files
│   └── manage.py
├── Frontend/              # React application (TBD)
├── Docs/                  # Project documentation
└── README.md
```

## Code Style & Conventions

### Python/Django

- Follow PEP 8 with 88 character line limit (Black formatter)
- Use type hints for all function signatures
- Prefer dataclasses for structured data
- Write comprehensive docstrings for classes and functions
- All code must pass Ruff linting
- Test coverage required for new features

**Linting & Formatting Tools:**

- **Ruff**: Primary linter and formatter (replaces flake8, isort, pyupgrade)
  - Auto-fix imports and common issues
  - Django-specific checks enabled
  - Security checks via Bandit integration
  - Complexity limit: max 10 (McCabe)
- **Black**: Code formatter (88 char line length)
- **mypy**: Static type checker with django-stubs
- **Pre-commit hooks**: Auto-run checks before commits

**Quick Commands:**

```bash
make format        # Auto-format code
make lint          # Run linter with auto-fix
make check-lint    # Check without auto-fix
make check-types   # Run mypy type checking
make check-all     # Run all checks
```

**Enabled Ruff Rules:**

- `E/F` - PyCodeStyle errors and Pyflakes
- `W` - PyCodeStyle warnings
- `UP` - PyUpgrade (modern Python syntax)
- `I` - Import sorting
- `B` - Bugbear (common bugs)
- `C4` - Comprehensions
- `C90` - McCabe complexity
- `DJ` - Django-specific checks
- `N` - PEP8 naming conventions
- `PLE/PLW` - Pylint errors/warnings
- `S` - Security (Bandit)
- `SIM` - Code simplification
- `T10/T20` - No debugger/print statements
- `RUF` - Ruff-specific rules

**Ignoring Rules:**

```python
# ruff: noqa  # Ignore entire file
import os  # noqa: F401  # Ignore specific rule
```

### TypeScript/React

- Strict TypeScript configuration
- Functional components with hooks only
- Use arrow functions for components
- Props interfaces must be explicitly typed
- Prefer composition over inheritance
- Keep components small and focused

**Linting & Formatting Tools:**

- **ESLint**: TypeScript and React linting
  - `@eslint/js` recommended config
  - `typescript-eslint` for TypeScript
  - `eslint-plugin-react-hooks` for hooks rules
  - `eslint-plugin-react-refresh` for Vite HMR
- **Prettier**: Code formatter (integrated with ESLint)
- **TypeScript Compiler**: Strict mode enabled

**Quick Commands:**

```bash
npm run lint        # Run ESLint
npm run lint:fix    # Auto-fix ESLint issues
npm run format      # Format with Prettier
npm run type-check  # TypeScript type checking
```

**ESLint Configuration:**

- Files: `**/*.{ts,tsx}`
- ECMAScript: 2020
- Environment: Browser globals
- Extends recommended configs for JS, TS, and React

### Markdown

**Markdownlint Configuration (`.markdownlint.json`):**

- Default rules enabled
- `MD013`: Disabled (line length)
- `MD041`: Disabled (first line heading)
- `MD033`: Disabled (inline HTML)
- `MD036`: Disabled (emphasis as heading)

### Testing

- Write tests for all new features
- Use pytest for backend (pytest-django)
- Use Vitest + React Testing Library for frontend
- Maintain >80% code coverage
- Test files should mirror source structure

## Django Specific Guidelines

### Models

- Always use custom managers with type hints
- Include `__str__` method for all models
- Add comprehensive field validation
- Use `blank=True, null=True` consistently
- Document model relationships

Example:

```python
from typing import Any
from django.db import models
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager["CustomUser"]):
    def create_user(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> "CustomUser":
        # Implementation
        pass
```

### Views & APIs

- Use class-based views for REST endpoints
- Implement proper permission classes
- Return appropriate HTTP status codes
- Validate all input data
- Use serializers for data transformation

### Settings

- Environment-specific settings (development/production/test)
- Never commit secrets to version control
- Use environment variables via `.env` file
- Keep sensitive data in AWS Secrets Manager (production)

## React Specific Guidelines

### Component Structure

```typescript
interface ComponentProps {
  title: string;
  onSubmit: (data: FormData) => void;
}

export const Component: React.FC<ComponentProps> = ({ title, onSubmit }) => {
  // Hooks at the top
  const [state, setState] = useState<string>("");

  // Event handlers
  const handleClick = () => {
    // Implementation
  };

  // Render
  return <div className="container">{/* JSX */}</div>;
};
```

### Hooks Best Practices

- Extract custom hooks for reusable logic
- Use `useMemo` and `useCallback` judiciously
- Keep hooks pure and predictable
- Name custom hooks with `use` prefix

### Data Fetching

- Use TanStack Query for all server requests
- Implement proper error boundaries
- Show loading states
- Handle optimistic updates

```typescript
const { data, isLoading, error } = useQuery({
  queryKey: ["standards", id],
  queryFn: () => fetchStandard(id),
});
```

### State Management

- Local state: `useState` for component-specific data
- Shared state: `useContext` for theme, auth
- Complex state: Zustand for global app state
- Server state: TanStack Query (never duplicate in local state)

### Forms

```typescript
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const schema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
});

type FormData = z.infer<typeof schema>;

const MyForm = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  const onSubmit = (data: FormData) => {
    // Handle submission
  };

  return <form onSubmit={handleSubmit(onSubmit)}>{/* Form fields */}</form>;
};
```

## RAG & AI Features

### Vector Search

- PostgreSQL with pgvector extension
- Embeddings stored alongside standards documents
- Semantic search capabilities
- Context retrieval for LLM prompts

### Standards Documents

- Each standard stored with metadata
- Full-text search + vector similarity
- Category/tag system for organization
- Version tracking for standards updates

## API Design

### REST Endpoints

- `/api/v1/standards/` - List and search standards
- `/api/v1/standards/{id}/` - Standard details
- `/api/v1/search/` - RAG-powered search
- `/api/v1/auth/` - Authentication endpoints

### Response Format

```json
{
  "data": {
    /* response data */
  },
  "meta": {
    "page": 1,
    "total": 100,
    "per_page": 20
  },
  "errors": []
}
```

## Development Workflow

1. Create feature branch from `main`
2. Write tests first (TDD)
3. Implement feature
4. Ensure all tests pass
5. **Run linters and formatters:**
   - Backend: `make check-all` or `make format && make lint && make check-types`
   - Frontend: `npm run lint:fix && npm run type-check`
6. **Verify pre-commit hooks pass** (if installed)
7. Create PR with descriptive title
8. Pass CI/CD checks
9. Code review
10. Merge to main

**Pre-commit Setup:**

```bash
# Backend (one-time setup)
cd Backend
make pre-commit-install

# Hooks run automatically on git commit
# To skip (not recommended): git commit --no-verify
```

## AWS CLI Access

### Authentication

This project uses **AWS SSO** for authentication. To access AWS services via CLI:

```bash
# Login with SSO profile
aws sso login --profile ben-sso

# Verify access
aws sts get-caller-identity --profile ben-sso
```

### Using AWS CLI Commands

Option 1 - Add profile to each command:
```bash
aws s3 ls --profile ben-sso
aws rds describe-db-instances --profile ben-sso
```

Option 2 - Set as default profile for session:
```bash
export AWS_PROFILE=ben-sso
aws s3 ls  # Now uses ben-sso by default
```

### SSO Session Management

- SSO sessions expire after a period of inactivity
- Re-authenticate when needed: `aws sso login --profile ben-sso`
- Check current session: `aws sts get-caller-identity --profile ben-sso`

### Common AWS Operations

```bash
# List S3 buckets
aws s3 ls --profile ben-sso

# List RDS instances
aws rds describe-db-instances --profile ben-sso

# Access CloudFront distributions
aws cloudfront list-distributions --profile ben-sso

# View Secrets Manager secrets
aws secretsmanager list-secrets --profile ben-sso
```

## Environment Variables

### Backend (.env)

```bash
DJANGO_ENV=development
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost/dbname
ALLOWED_HOSTS=localhost,127.0.0.1

# AWS (Production)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
```

### Frontend (.env)

```bash
VITE_API_URL=http://localhost:8000/api/v1
VITE_ENABLE_DEVTOOLS=true
```

## Testing Commands

### Backend

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=config --cov=accounts

# Run specific test file
pytest accounts/tests/test_models.py

# Run with verbose output
pytest -v
```

### Frontend

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch
```

## Common Tasks

### Adding a New Django App

1. Create app: `python manage.py startapp app_name`
2. Add to `INSTALLED_APPS` in `settings/base.py`
3. Create models with type hints
4. Create migrations: `python manage.py makemigrations`
5. Apply migrations: `python manage.py migrate`
6. Create tests in `app_name/tests/`
7. Register in admin if needed

### Adding a New React Component

1. Create component file: `ComponentName.tsx`
2. Export from index: `export { ComponentName } from './ComponentName'`
3. Create test file: `ComponentName.test.tsx`
4. Write component with TypeScript types
5. Add Storybook story if applicable

### Database Migrations

```bash
# Create migration
python manage.py makemigrations

# View migration SQL
python manage.py sqlmigrate app_name 0001

# Apply migrations
python manage.py migrate

# Rollback migration
python manage.py migrate app_name 0001
```

## Security Best Practices

1. Never commit `.env` files
2. Use parameterized queries (Django ORM does this)
3. Validate all user input
4. Use CSRF protection (enabled by default)
5. Implement rate limiting on API endpoints
6. Use HTTPS in production
7. Regular dependency updates
8. SQL injection prevention via ORM
9. XSS prevention via React's auto-escaping

## Performance Guidelines

### Backend

- Use `select_related()` and `prefetch_related()` for query optimization
- Implement database indexing for frequently queried fields
- Use caching for expensive operations
- Paginate large querysets
- Use async views for I/O-bound operations

### Frontend

- Code splitting with lazy loading
- Optimize images (WebP, lazy loading)
- Use React.memo for expensive components
- Debounce search inputs
- Implement virtual scrolling for long lists
- Bundle size monitoring

## Deployment

### Backend (Django)

- Use Gunicorn/Uvicorn as WSGI/ASGI server
- Configure static files with WhiteNoise
- Use AWS RDS for database
- Environment-specific settings
- Health check endpoint: `/health/`

### Frontend (React)

- Build: `npm run build`
- Deploy to AWS S3 + CloudFront
- Automatic deployment on successful tests
- Configure CORS properly
- Use environment variables for API URLs

## CI/CD Workflows

### GitHub Actions

**CI Pipeline (`ci.yml`):**
- Runs on every push to `main`/`develop` and all PRs
- Backend: Python 3.13, PostgreSQL 16, pytest with coverage
- Frontend: Node.js 20, Vitest, TypeScript type-checking, ESLint
- Both jobs must pass for PR approval
- Coverage reports uploaded to Codecov

**Backend Tests (`test-backend.yml`):**
- Triggers on Backend file changes
- Runs Ruff linting, Black formatting, mypy type checking
- Executes all Django tests with PostgreSQL
- Matrix testing across Python versions

**Frontend Tests (`test-frontend.yml`):**
- Triggers on Frontend file changes
- Runs TypeScript type-check, ESLint, Vitest tests
- Matrix testing on Node.js 20 and 22
- Production build verification

**Frontend Deployment (`deploy-frontend.yml`):**
- Only runs after `test-frontend.yml` succeeds
- Builds production bundle
- Deploys to AWS S3 (`iso-standards-frontend`)
- Invalidates CloudFront cache (Distribution: `E2494N0PGM4KTG`)
- URL: https://d1pjttps83iyey.cloudfront.net

**Workflow Dependencies:**
1. Push to `main` → `test-frontend.yml` runs
2. Tests pass → `deploy-frontend.yml` auto-triggers
3. Tests fail → deployment blocked

### Pre-commit Checks

**Before committing:**
```bash
# Backend
cd Backend
make format      # Black + Ruff auto-fix
make lint        # Check linting
make check-types # mypy
pytest           # Run tests

# Frontend
cd Frontend
npm run format   # Prettier
npm run lint     # ESLint
npm run type-check
npm test
```

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [TanStack Query](https://tanstack.com/query/)
- [Tailwind CSS](https://tailwindcss.com/)
- [PostgreSQL pgvector](https://github.com/pgvector/pgvector)

## When Generating Code

1. **Always include type hints** (Python) or **TypeScript types** (React)
2. **Write tests** alongside implementation
3. **Add docstrings/comments** for complex logic
4. **Follow existing patterns** in the codebase
5. **Consider edge cases** and error handling
6. **Optimize for readability** over cleverness
7. **Ask for clarification** if requirements are ambiguous
8. **Ensure code passes linting:**
   - Python: Must pass Ruff checks (no debugger/print statements, proper imports, complexity ≤10)
   - TypeScript: Must pass ESLint checks (proper hooks usage, React best practices)
   - All: Proper formatting with Black/Prettier

## AI/Copilot Specific Tips

- When suggesting Django models, include migrations consideration
- When suggesting React components, include accessibility attributes
- Suggest performance optimizations when appropriate
- Recommend security best practices
- Provide alternative approaches when multiple solutions exist
- Include error handling in all code suggestions
- Consider scalability in architectural decisions
- **Always generate code that passes linting without manual fixes**
- **Use proper type annotations for all Python functions**
- **Avoid using `print()` or `debugger` statements in production code**
- **Keep function complexity low (McCabe ≤10)**
- **Follow import sorting conventions (stdlib → third-party → local)**
