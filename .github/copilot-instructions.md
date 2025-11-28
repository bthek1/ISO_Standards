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

### TypeScript/React

- Strict TypeScript configuration
- Functional components with hooks only
- Use arrow functions for components
- Props interfaces must be explicitly typed
- Prefer composition over inheritance
- Keep components small and focused

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
5. Run linters (Ruff for Python, ESLint for TS)
6. Format code (Black for Python, Prettier for TS)
7. Create PR with descriptive title
8. Pass CI/CD checks
9. Code review
10. Merge to main

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
- Deploy static files to CDN
- Configure CORS properly
- Use environment variables for API URLs

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

## AI/Copilot Specific Tips

- When suggesting Django models, include migrations consideration
- When suggesting React components, include accessibility attributes
- Suggest performance optimizations when appropriate
- Recommend security best practices
- Provide alternative approaches when multiple solutions exist
- Include error handling in all code suggestions
- Consider scalability in architectural decisions
