# ISO Standards Project Documentation

## 📚 Documentation Index

Welcome to the ISO Standards project documentation. This platform enables intelligent exploration and access to global standards (ISO, IEEE, ASTM, etc.) using AI-powered semantic search and RAG.

---

## Core Documentation

### 1. [Project Overview](./PROJECT_OVERVIEW.md)
Complete technical architecture, database schema, API structure, and deployment guide.

**Contents:**
- Vision and purpose
- Technical architecture (Backend + Frontend)
- Database schema with PostgreSQL + pgvector
- RAG implementation details
- API endpoint specifications
- Development and deployment setup
- Security and performance considerations

### 2. [React Starter Pack](./REACT_STARTER_PACK.md)
Comprehensive guide for React + TypeScript + Vite frontend development.

**Contents:**
- Core React concepts (components, hooks, props, state)
- Project setup with Vite + TypeScript
- Styling with Tailwind CSS
- Routing with React Router
- Data fetching with TanStack Query
- State management (Zustand)
- Form management (react-hook-form + zod)
- Testing with Vitest + React Testing Library
- Best practices and patterns

### 3. [Copilot Instructions](../.github/copilot-instructions.md)
GitHub Copilot configuration for code generation assistance.

**Contents:**
- Code style and conventions
- Django-specific guidelines
- React-specific guidelines
- API design patterns
- Security best practices
- Testing requirements

---

## Backend Documentation

### Setup & Configuration

**[Backend README](../Backend/README.md)**
- Installation instructions
- Environment setup
- Running the development server
- Database migrations

**[Environment Configuration](./Refactor/env_refactor.md)**
- Environment variables reference
- Settings configuration
- Development vs Production setup

### Testing

**[Pytest Guide](../Backend/PYTEST_GUIDE.md)**
- Test structure and organization
- Running tests
- Coverage requirements
- Best practices

**[Linting Guide](../Backend/LINTING.md)**
- Ruff configuration
- Code formatting with Black
- Pre-commit hooks

---

## Frontend Documentation (Coming Soon)

### Setup & Configuration
- Installation guide
- Environment setup
- Development workflow

### Component Library
- UI components documentation
- Component patterns
- Accessibility guidelines

### API Integration
- API client setup
- Authentication flow
- Error handling

---

## Architecture Diagrams

### System Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   React     │◄────────┤     NGINX    ├────────►│   Django    │
│  Frontend   │  HTTPS  │   (Reverse   │   HTTP  │   Backend   │
│  (Port 3000)│         │    Proxy)    │         │  (Port 8000)│
└─────────────┘         └──────────────┘         └──────┬──────┘
                                                         │
                                                         │
                                ┌────────────────────────┴──────────┐
                                │                                   │
                         ┌──────▼─────┐                    ┌───────▼────────┐
                         │ PostgreSQL │                    │   AWS S3       │
                         │  + pgvector│                    │  (Documents)   │
                         │ (Port 5432)│                    │                │
                         └────────────┘                    └────────────────┘
```

### RAG Pipeline

```
Document Upload
    ↓
Text Extraction (PyPDF2/python-docx)
    ↓
Chunking (LangChain)
    ↓
Embedding Generation (OpenAI/Cohere)
    ↓
Store in PostgreSQL with pgvector
    ↓
Index for Vector Similarity Search
```

### User Query Flow

```
User Search Query
    ↓
Generate Query Embedding
    ↓
Vector Similarity Search (pgvector)
    ↓
Retrieve Top-K Relevant Chunks
    ↓
Construct Context + Original Query
    ↓
Send to LLM (GPT-4/Claude)
    ↓
Return Enhanced Response with Sources
```

---

## API Documentation

### Base URL
```
Development: http://localhost:8000/api/v1/
Production: https://api.isostandards.example.com/api/v1/
```

### Key Endpoints

**Authentication**
- `POST /auth/register/` - User registration
- `POST /auth/login/` - User login (returns JWT)
- `POST /auth/logout/` - User logout
- `GET /auth/me/` - Current user info

**Standards**
- `GET /standards/` - List standards (paginated)
- `GET /standards/{id}/` - Standard details
- `POST /search/` - Standard search
- `POST /search/rag/` - RAG-powered Q&A

For complete API documentation, see [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md#api-structure)

---

## Development Guides

### Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/bthek1/ISO_Standards.git
   cd ISO_Standards
   ```

2. **Setup Backend**
   ```bash
   cd Backend
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your settings
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

3. **Setup Frontend** (when available)
   ```bash
   cd Frontend
   npm install
   cp .env.example .env
   # Edit .env with your settings
   npm run dev
   ```

### Testing

**Backend:**
```bash
cd Backend
pytest                          # Run all tests
pytest --cov                    # With coverage
pytest accounts/tests/          # Specific app
```

**Frontend:**
```bash
cd Frontend
npm test                        # Run all tests
npm run test:coverage           # With coverage
npm run test:ui                 # Open test UI
```

### Code Quality

**Backend:**
```bash
ruff check .                    # Lint
ruff format .                   # Format
pytest --cov                    # Test coverage
```

**Frontend:**
```bash
npm run lint                    # ESLint
npm run format                  # Prettier
npm run type-check              # TypeScript
```

---

## Database Schema

### Core Models

**CustomUser**
- Email-based authentication
- Fields: email, first_name, last_name, is_active, is_staff

**Standard**
- code, title, organization, version
- published_date, revision_date, status
- description, document_url

**Embedding**
- document_id, chunk_text, chunk_index
- embedding (vector), metadata

For complete schema, see [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md#database-schema-postgresql)

---

## Technology Stack

### Backend
- **Framework:** Django 5.2 + Python 3.13
- **API:** Django REST Framework
- **Database:** PostgreSQL 16 + pgvector
- **Authentication:** django-allauth (email-based)
- **ASGI:** Uvicorn for async support
- **Testing:** pytest + pytest-django

### Frontend
- **Framework:** React 18 + TypeScript
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **Routing:** React Router v6
- **State:** TanStack Query + Zustand
- **Forms:** react-hook-form + zod
- **Testing:** Vitest + React Testing Library

### Infrastructure
- **Database:** AWS RDS (PostgreSQL)
- **Storage:** AWS S3
- **Hosting:** AWS EC2/ECS
- **CDN:** CloudFront
- **Cache:** ElastiCache (Redis)

---

## Contributing

### Code Style
- Backend: PEP 8, Black formatter (88 char line limit)
- Frontend: ESLint + Prettier
- Type hints required for all functions
- Comprehensive tests for new features

### Git Workflow
1. Create feature branch from `main`
2. Write tests first (TDD)
3. Implement feature
4. Run linters and tests
5. Create PR with descriptive title
6. Code review
7. Merge to main

### Commit Messages
```
feat: add RAG search endpoint
fix: resolve authentication token refresh
docs: update API documentation
test: add tests for standard creation
refactor: optimize database queries
```

---

## Resources

### Django
- [Django Documentation](https://docs.djangoproject.com/)
- [DRF Documentation](https://www.django-rest-framework.org/)
- [django-allauth](https://django-allauth.readthedocs.io/)

### React
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [TanStack Query](https://tanstack.com/query/)
- [React Router](https://reactrouter.com/)

### Tools
- [Tailwind CSS](https://tailwindcss.com/)
- [Vitest](https://vitest.dev/)
- [PostgreSQL pgvector](https://github.com/pgvector/pgvector)

---

## Support

- **Issues:** [GitHub Issues](https://github.com/bthek1/ISO_Standards/issues)
- **Email:** [Contact](mailto:support@example.com)
- **Documentation:** This repository

---

## License

[Specify License]

---

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version history and updates.

---

**Last Updated:** November 28, 2025
