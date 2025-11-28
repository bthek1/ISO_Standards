# ISO Standards Project - Complete Overview

## Vision

A comprehensive platform for exploring, understanding, and accessing global standards documentation (ISO, IEEE, ASTM, etc.) powered by AI-driven search and retrieval augmented generation (RAG).

## Purpose

This application serves as:
1. **Standards Repository** - Centralized access to global standards documentation
2. **Intelligent Search** - AI-powered semantic search across standards
3. **Context-Aware Assistance** - RAG-based Q&A about specific standards
4. **Educational Platform** - Learn about standards and their applications
5. **Comparison Tool** - Compare similar standards across different organizations

## Technical Architecture

### High-Level Architecture

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
                         │            │                    │                │
                         └────────────┘                    └────────────────┘
```

### Backend Stack (Django)

**Framework:** Django 5.2+ with Python 3.13
- **API:** Django REST Framework
- **Authentication:** django-allauth (email-based)
- **Database ORM:** Django ORM with type hints
- **ASGI:** Uvicorn for async support
- **Task Queue:** Celery (for document processing)
- **Caching:** Redis

**Key Features:**
- Custom User model with email authentication
- RESTful API with proper serialization
- PostgreSQL with pgvector for embeddings
- Document upload and processing pipeline
- RAG implementation for intelligent search
- Admin interface for content management

### Frontend Stack (React + TypeScript)

**Core:**
- React 18+ with TypeScript
- Vite for build tooling
- TailwindCSS for styling

**State Management:**
- TanStack Query for server state
- Zustand for global client state
- React Context for theme/auth

**Routing & Navigation:**
- React Router DOM v6

**Forms & Validation:**
- react-hook-form
- Zod schema validation

**Testing:**
- Vitest as test runner
- React Testing Library
- Mock Service Worker (MSW)

### Database Schema (PostgreSQL)

#### Core Tables

**Users**
```sql
users
- id (PK)
- email (unique)
- password_hash
- first_name
- last_name
- is_active
- is_staff
- date_joined
- last_login
```

**Standards**
```sql
standards
- id (PK)
- code (e.g., "ISO-9001")
- title
- organization (ISO, IEEE, ASTM, etc.)
- version
- published_date
- revision_date
- status (active, superseded, withdrawn)
- category_id (FK)
- description (text)
- document_url
- created_at
- updated_at
```

**Categories**
```sql
categories
- id (PK)
- name
- slug
- parent_id (FK, self-referential)
- description
```

**Documents**
```sql
documents
- id (PK)
- standard_id (FK)
- file_path
- file_type (PDF, DOCX, etc.)
- file_size
- upload_date
- processed (boolean)
```

**Embeddings** (for RAG)
```sql
embeddings
- id (PK)
- document_id (FK)
- chunk_text (text)
- chunk_index (int)
- embedding (vector(1536))  -- pgvector
- metadata (jsonb)
- created_at
```

**Search History**
```sql
search_history
- id (PK)
- user_id (FK)
- query (text)
- results_count
- clicked_standard_id (FK, nullable)
- timestamp
```

### RAG Implementation

#### Document Processing Pipeline

1. **Upload** - Admin uploads standard document (PDF/DOCX)
2. **Extraction** - Extract text content using PyPDF2/python-docx
3. **Chunking** - Split into semantic chunks (~500 tokens each)
4. **Embedding** - Generate embeddings using OpenAI/Cohere API
5. **Storage** - Store chunks + embeddings in PostgreSQL
6. **Indexing** - Create pgvector index for fast similarity search

#### Search Flow

```
User Query
    ↓
Generate Query Embedding
    ↓
Vector Similarity Search (pgvector)
    ↓
Retrieve Top-K Relevant Chunks
    ↓
Construct Context + Query
    ↓
Send to LLM (OpenAI GPT-4)
    ↓
Return Enhanced Response
```

#### Technologies

- **Vector Database:** PostgreSQL with pgvector extension
- **Embeddings:** OpenAI `text-embedding-3-small` or Cohere
- **LLM:** OpenAI GPT-4 or Anthropic Claude
- **Chunking:** LangChain text splitters
- **Orchestration:** LangChain or LlamaIndex

### API Structure

#### Base URL
```
https://api.isostandards.example.com/api/v1/
```

#### Endpoints

**Authentication**
- `POST /auth/register/` - User registration
- `POST /auth/login/` - User login (returns JWT)
- `POST /auth/logout/` - User logout
- `POST /auth/refresh/` - Refresh access token
- `GET /auth/me/` - Current user info

**Standards**
- `GET /standards/` - List standards (with pagination, filters)
- `GET /standards/{id}/` - Standard details
- `GET /standards/{id}/download/` - Download document
- `POST /standards/` - Create standard (admin only)
- `PUT /standards/{id}/` - Update standard (admin only)
- `DELETE /standards/{id}/` - Delete standard (admin only)

**Search**
- `POST /search/` - Standard search (text or semantic)
- `POST /search/rag/` - RAG-powered Q&A
- `GET /search/history/` - User's search history
- `GET /search/suggestions/` - Search suggestions

**Categories**
- `GET /categories/` - List all categories
- `GET /categories/{slug}/standards/` - Standards in category

**Organizations**
- `GET /organizations/` - List standard organizations
- `GET /organizations/{slug}/` - Organization details

### Frontend Architecture

#### Project Structure
```
frontend/
├── src/
│   ├── components/         # Reusable UI components
│   │   ├── ui/            # Base components (Button, Input, etc.)
│   │   ├── layout/        # Layout components (Header, Footer)
│   │   └── features/      # Feature-specific components
│   ├── pages/             # Route pages
│   │   ├── Home.tsx
│   │   ├── Search.tsx
│   │   ├── StandardDetail.tsx
│   │   └── Dashboard.tsx
│   ├── hooks/             # Custom React hooks
│   ├── services/          # API calls
│   ├── stores/            # Zustand stores
│   ├── types/             # TypeScript types
│   ├── utils/             # Utility functions
│   ├── styles/            # Global styles
│   ├── App.tsx
│   └── main.tsx
├── public/
├── tests/
└── package.json
```

#### Key Features

**1. Standards Browser**
- Grid/List view toggle
- Advanced filtering (organization, category, date)
- Sorting options
- Infinite scroll or pagination

**2. Semantic Search**
- Real-time search with debouncing
- Search suggestions/autocomplete
- Recent searches
- Filter by relevance/date/organization

**3. RAG Chat Interface**
- Chat-style Q&A about standards
- Context highlighting (show source chunks)
- Follow-up questions
- Export conversation

**4. Standard Detail View**
- Full metadata display
- Related standards
- Version history
- Download document
- Share functionality

**5. User Dashboard**
- Saved/bookmarked standards
- Search history
- Recent activity
- Preferences

## Development Setup

### Prerequisites
- Python 3.13+
- Node.js 20+
- PostgreSQL 16+ with pgvector
- Redis
- AWS account (for production)

### Backend Setup

```bash
cd Backend/

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata fixtures/standards.json

# Run development server
python manage.py runserver
```

### Frontend Setup

```bash
cd Frontend/

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your settings

# Run development server
npm run dev
```

### PostgreSQL pgvector Setup

```bash
# Install pgvector extension
CREATE EXTENSION vector;

# Create index for embeddings
CREATE INDEX ON embeddings USING ivfflat (embedding vector_cosine_ops);
```

## Deployment

### AWS Infrastructure

**Compute:**
- EC2 instances (or ECS/Fargate)
- Application Load Balancer

**Database:**
- AWS RDS PostgreSQL with pgvector

**Storage:**
- S3 for document storage
- CloudFront CDN for static assets

**Caching:**
- ElastiCache Redis

**Other:**
- Route 53 for DNS
- ACM for SSL certificates
- CloudWatch for monitoring

### Environment Configuration

**Development:** SQLite, local files, console email
**Testing:** In-memory database, mock services
**Production:** RDS, S3, SES email, CloudWatch logs

## Security Considerations

1. **Authentication:** JWT tokens with refresh rotation
2. **Authorization:** Role-based access control (RBAC)
3. **Data Protection:** Encryption at rest and in transit
4. **API Security:** Rate limiting, CORS configuration
5. **Input Validation:** Strict validation on all endpoints
6. **Document Access:** Signed URLs for document downloads
7. **Secrets Management:** AWS Secrets Manager
8. **Audit Logging:** Track all data modifications

## Future Enhancements

### Phase 1 (MVP)
- [x] Basic Django backend with custom user
- [x] PostgreSQL database
- [ ] React frontend with TypeScript
- [ ] Basic search functionality
- [ ] Standard detail pages
- [ ] User authentication

### Phase 2
- [ ] RAG implementation
- [ ] Vector embeddings
- [ ] Semantic search
- [ ] Chat interface
- [ ] Document upload pipeline

### Phase 3
- [ ] Advanced filtering
- [ ] Comparison tool
- [ ] Version tracking
- [ ] User dashboard
- [ ] Bookmarks/favorites

### Phase 4
- [ ] Mobile app (React Native)
- [ ] API for third-party integrations
- [ ] Analytics dashboard
- [ ] Automated standard updates
- [ ] Multi-language support

## Performance Targets

- **Page Load:** < 2 seconds
- **Search Response:** < 500ms
- **RAG Query:** < 3 seconds
- **Document Upload:** < 30 seconds (processing)
- **API Response:** < 200ms (p95)
- **Uptime:** 99.9%

## Monitoring & Analytics

**Application Metrics:**
- Request/response times
- Error rates
- Cache hit rates
- Database query performance

**Business Metrics:**
- Daily active users
- Search queries per user
- Most viewed standards
- Document downloads
- User engagement time

**Tools:**
- AWS CloudWatch
- Sentry for error tracking
- Google Analytics
- Custom analytics dashboard

## Team & Responsibilities

**Backend Developer:**
- Django API development
- Database schema design
- RAG implementation
- DevOps & deployment

**Frontend Developer:**
- React UI/UX implementation
- State management
- API integration
- Performance optimization

**AI/ML Engineer:**
- Embedding generation
- RAG optimization
- LLM prompt engineering
- Model evaluation

## License

[Specify License]

## Contributing

[Link to CONTRIBUTING.md]

## Support

For issues and questions:
- GitHub Issues: [repository URL]
- Email: support@example.com
- Documentation: [docs URL]
