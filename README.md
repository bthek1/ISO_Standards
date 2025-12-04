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

### Production Deployment (AWS)

```
┌─────────────────────────────────────────────────────────────────┐
│                     Users / Browsers                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              AWS CloudFront (CDN + SSL/HTTPS)                   │
│              ✅ DEPLOYED & ACTIVE                              │
│              URL: https://d1pjttps83iyey.cloudfront.net        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   AWS S3 (Frontend)                             │
│                   React + Vite + TypeScript                     │
│                   ✅ DEPLOYED & ACTIVE                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ JWT Authentication
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              Django REST API Backend                            │
│              ⏳ Ready for Deployment                           │
│              (Elastic Beanstalk / ECS / EC2)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              AWS RDS PostgreSQL 16 + pgvector                   │
│              ⏳ To Be Created                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Development Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   React     │◄────────┤   Vite Dev   ├────────►│   Django    │
│  Frontend   │  HTTPS  │    Server    │   HTTP  │   Backend   │
│  (Port 5173)│         │              │         │  (Port 8000)│
└─────────────┘         └──────────────┘         └──────┬──────┘
                                                         │
                                                         │
                                ┌────────────────────────┴──────────┐
                                │                                   │
                         ┌──────▼─────┐                    ┌───────▼────────┐
                         │ PostgreSQL │                    │   Local Files  │
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
- **Axios** - HTTP client with JWT interceptors
- **✅ Deployed to AWS S3 + CloudFront**

### Infrastructure
- **AWS RDS** - Managed PostgreSQL with pgvector
- **AWS S3** - Static file hosting (frontend deployed ✅)
- **AWS CloudFront** - CDN for frontend (active ✅)
- **AWS Elastic Beanstalk** - Backend API (ready to deploy ⏳)
- **GitHub Actions** - CI/CD pipeline (frontend active ✅, backend ready ⏳)
- **JWT** - Stateless authentication between frontend & backend

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
### Frontend Setup

```bash
cd Frontend/

# Install dependencies
npm install

# Setup environment
cp .env.example .env
# Edit .env with your backend API URL

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:5173`

**Production:** Frontend is deployed at https://d1pjttps83iyey.cloudfront.net

### Full-Stack Development
## 📚 Documentation

Comprehensive documentation is available in the `/Docs` directory:

### Getting Started
- **[Documentation Index](./Docs/DOCUMENTATION_INDEX.md)** - Complete documentation overview
- **[Project Overview](./Docs/PROJECT_OVERVIEW.md)** - Architecture and technical details
- **[Quick Start](./Docs/QUICK_START.md)** - Quick reference guide

### Deployment
- **[Architecture Summary](./Docs/Deployment_Doc/ARCHITECTURE_SUMMARY.md)** - Full-stack architecture overview
- **[AWS Deployment Guide](./Docs/Deployment_Doc/AWS_DEPLOYMENT_GUIDE.md)** - Complete backend deployment guide
- **[Backend Quick Reference](./Docs/Deployment_Doc/BACKEND_DEPLOYMENT_QUICK_REF.md)** - Common deployment commands
- **[JWT Authentication](./Docs/Deployment_Doc/JWT_AUTHENTICATION.md)** - Authentication setup and usage
- **[Frontend Deployment](./Docs/FRONTEND_READY.md)** - Frontend deployment status

### Development
- **[Backend README](./Backend/README.md)** - Backend setup and usage
- **[Copilot Instructions](./.github/copilot-instructions.md)** - AI coding assistant guide
- **[Linting Guide](./Docs/LINTING.md)** - Code quality tools
npm run dev
```

Backend: `http://localhost:8000` | Frontend: `http://localhost:5173`
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
### Frontend Tests

```bash
cd Frontend/

# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Open test UI
npm run test:ui
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

## 📊 Project Status

### Deployed ✅
- **Frontend** - React app deployed to AWS S3 + CloudFront
- **CI/CD** - GitHub Actions deploying frontend automatically
- **Authentication** - JWT implementation ready
- **Testing** - Comprehensive test suite (Backend: 197 tests, Frontend: configured)
- **Documentation** - Complete deployment guides

### Ready for Deployment ⏳
- **Backend API** - Django REST API with JWT auth
- **Docker** - Production Dockerfile and docker-compose
- **CI/CD** - Backend GitHub Actions workflow ready

### In Progress 🚧
- **RDS Database** - PostgreSQL with pgvector (to be created)
- **Backend Deployment** - Elastic Beanstalk / ECS / EC2 setup
- **RAG Implementation** - Vector search and embeddings
- **API Endpoints** - Standards CRUD operations

### Planned 📋
- **Advanced Search** - Semantic search with RAG
- **User Dashboard** - Personal standards library
- **Analytics** - Usage tracking and insights
### Phase 1: Foundation
- [x] Django backend setup
- [x] Custom user authentication (email-based)
- [x] Testing infrastructure
- [x] Documentation
- [x] React frontend setup
- [x] Frontend deployment (S3 + CloudFront)
- [x] JWT authentication implementation
- [x] CI/CD for frontend

### Phase 2: Backend Deployment (Current)
- [ ] AWS RDS PostgreSQL setup with pgvector
- [ ] Backend deployment (Elastic Beanstalk)
- [ ] Environment variables & secrets management
- [ ] SSL/HTTPS configuration
- [ ] Backend CI/CD activation
- [ ] Full-stack integration testing

### Phase 3: Core Features
- [ ] Standards model and API
- [ ] Document upload and processing
- [ ] Vector embeddings with pgvector
- [ ] Basic search functionality
- [ ] User dashboard
### Phase 1: Foundation (Current)
- [x] Django backend setup
- [x] Custom user authentication
- [x] Testing infrastructure
- [x] Documentation
### Phase 5: Production & Optimization
- [ ] Performance optimization
- [ ] Security hardening
- [ ] Monitoring and logging (CloudWatch)
- [ ] Custom domain setup
- [ ] CDN optimization
- [ ] Backup and disaster recoveryocessing
## 🚀 Quick Deploy

### Frontend (Deployed)
```bash
# Automatic deployment on push to main
git push origin main  # GitHub Actions handles deployment
```

### Backend (Ready to Deploy)
```bash
# 1. Set up RDS database
aws rds create-db-instance --db-instance-identifier iso-standards-db ...

# 2. Deploy to Elastic Beanstalk
cd Backend/
eb init -p python-3.13 iso-standards-backend
eb create iso-standards-prod
eb setenv SECRET_KEY=xxx DB_HOST=xxx ...
eb deploy

# See full guide: Docs/Deployment_Doc/AWS_DEPLOYMENT_GUIDE.md
```

---

## 🤝 Contributingdings with pgvector
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
## 📧 Contact & Resources

- **Live Demo (Frontend):** https://d1pjttps83iyey.cloudfront.net
- **GitHub Issues:** [Report bugs or request features](https://github.com/bthek1/ISO_Standards/issues)
- **Documentation:** [Complete documentation](./Docs/DOCUMENTATION_INDEX.md)
- **Deployment Guide:** [AWS Deployment](./Docs/Deployment_Doc/AWS_DEPLOYMENT_GUIDE.md)

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
---

**Built with ❤️ for the standards community**

**Status:** Frontend Deployed ✅ | Backend Ready for Deployment ⏳

*Last Updated: December 3, 2025*
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
