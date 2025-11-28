# ISO Standards Platform

> An AI-powered platform for exploring and understanding global standards (ISO, IEEE, ASTM, etc.) using Retrieval Augmented Generation (RAG)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.2-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/typescript-5.0-blue.svg)](https://www.typescriptlang.org/)

---

## 🎯 Vision

The ISO Standards Platform is a comprehensive solution for accessing, searching, and understanding global standards documentation. By leveraging RAG (Retrieval Augmented Generation) with PostgreSQL's pgvector, we provide intelligent, context-aware answers about standards and their applications.

## ✨ Key Features

- **🔍 Intelligent Search** - AI-powered semantic search across all standards
- **💬 RAG-Powered Q&A** - Ask questions and get contextual answers with source citations
- **📚 Standards Repository** - Centralized access to ISO, IEEE, ASTM, IEC, and more
- **🔖 User Management** - Personal dashboard for saved standards and search history
- **⚡ Fast & Scalable** - Built on modern tech stack for optimal performance
- **🔒 Secure** - Enterprise-grade security with JWT authentication

## 🏗️ Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   React     │◄────────┤     NGINX    ├────────►│   Django    │
│  Frontend   │  HTTPS  │   (Reverse   │   HTTP  │   Backend   │
│             │         │    Proxy)    │         │             │
└─────────────┘         └──────────────┘         └──────┬──────┘
                                                         │
                                                         │
                                ┌────────────────────────┴──────────┐
                                │                                   │
                         ┌──────▼─────┐                    ┌───────▼────────┐
                         │ PostgreSQL │                    │   AWS S3       │
                         │  + pgvector│                    │  (Documents)   │
                         └────────────┘                    └────────────────┘
```

## 🛠️ Tech Stack

### Backend
- **Django 5.2** - Modern Python web framework
- **Django REST Framework** - Powerful API toolkit
- **PostgreSQL 16 + pgvector** - Vector database for embeddings
- **Python 3.13** - Latest Python with type hints
- **Pytest** - Comprehensive testing
- **Ruff** - Fast Python linter

### Frontend
- **React 18** - Modern UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Next-generation build tool
- **TailwindCSS** - Utility-first styling
- **TanStack Query** - Server state management
- **Zustand** - Client state management
- **React Router** - Navigation
- **Vitest** - Fast testing framework

### Infrastructure
- **AWS RDS** - Managed PostgreSQL
- **AWS S3** - Document storage
- **AWS EC2/ECS** - Application hosting
- **CloudFront** - CDN for static assets
- **ElastiCache** - Redis caching

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Node.js 20+
- PostgreSQL 16+ with pgvector
- AWS account (for production)

### Backend Setup

```bash
cd Backend/

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Backend will be available at `http://localhost:8000`

### Frontend Setup (Coming Soon)

```bash
cd Frontend/

# Install dependencies
npm install

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

## 📚 Documentation

Comprehensive documentation is available in the `/Docs` directory:

- **[Documentation Index](./Docs/README.md)** - Complete documentation overview
- **[Project Overview](./Docs/PROJECT_OVERVIEW.md)** - Architecture and technical details
- **[React Starter Pack](./Docs/REACT_STARTER_PACK.md)** - Frontend development guide
- **[Backend README](./Backend/README.md)** - Backend setup and usage
- **[Copilot Instructions](./.github/copilot-instructions.md)** - AI coding assistant guide

## 🧪 Testing

### Backend Tests

```bash
cd Backend/

# Run all tests
pytest

# Run with coverage
pytest --cov=config --cov=accounts

# Run specific tests
pytest accounts/tests/test_models.py

# Run with verbose output
pytest -v
```

### Frontend Tests (Coming Soon)

```bash
cd Frontend/

# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Open test UI
npm run test:ui
```

## 🎨 Code Quality

### Backend

```bash
# Lint code
ruff check .

# Format code
ruff format .

# Run pre-commit hooks
pre-commit run --all-files
```

### Frontend

```bash
# Lint code
npm run lint

# Format code
npm run format

# Type check
npm run type-check
```

## 📊 Project Status

- ✅ **Backend** - Core Django setup with custom user model
- ✅ **Testing** - Comprehensive test suite with 197 tests
- ✅ **Documentation** - Complete technical documentation
- ✅ **Code Quality** - Linting and formatting configured
- 🚧 **Frontend** - React setup in progress
- 🚧 **RAG Implementation** - Vector search with pgvector
- 🚧 **API Endpoints** - Standards and search APIs
- 📋 **Deployment** - AWS infrastructure planning

## 🗺️ Roadmap

### Phase 1: Foundation (Current)
- [x] Django backend setup
- [x] Custom user authentication
- [x] Testing infrastructure
- [x] Documentation
- [ ] React frontend setup
- [ ] Basic UI components

### Phase 2: Core Features
- [ ] Standards model and API
- [ ] Document upload and processing
- [ ] Vector embeddings with pgvector
- [ ] Basic search functionality
- [ ] User dashboard

### Phase 3: RAG Implementation
- [ ] LLM integration (OpenAI/Anthropic)
- [ ] Semantic search
- [ ] Context retrieval
- [ ] Chat interface
- [ ] Source citation

### Phase 4: Advanced Features
- [ ] Advanced filtering and sorting
- [ ] Standards comparison tool
- [ ] Version tracking
- [ ] Bookmarks and favorites
- [ ] Analytics dashboard

### Phase 5: Production
- [ ] AWS infrastructure setup
- [ ] CI/CD pipeline
- [ ] Performance optimization
- [ ] Security hardening
- [ ] Monitoring and logging

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Ensure all tests pass
5. Run linters and formatters
6. Commit your changes (`git commit -m 'feat: add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Code Style

- **Backend:** Follow PEP 8, use Black formatter (88 char line limit)
- **Frontend:** Follow ESLint + Prettier configuration
- **Types:** Use type hints (Python) and TypeScript
- **Tests:** Write tests for all new features
- **Commits:** Use conventional commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Backend Development:** Django, PostgreSQL, RAG implementation
- **Frontend Development:** React, TypeScript, UI/UX
- **DevOps:** AWS infrastructure, CI/CD
- **AI/ML:** Embeddings, LLM integration, RAG optimization

## 📧 Contact

- **GitHub Issues:** [Report bugs or request features](https://github.com/bthek1/ISO_Standards/issues)
- **Email:** support@example.com
- **Documentation:** [Full documentation](./Docs/README.md)

## 🙏 Acknowledgments

- Django and Django REST Framework teams
- React and TypeScript communities
- PostgreSQL and pgvector developers
- All open-source contributors

---

**Built with ❤️ for the standards community**

*Last Updated: November 28, 2025*
