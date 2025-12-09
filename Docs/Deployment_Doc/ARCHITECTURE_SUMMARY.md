# AWS Deployment - Architecture Summary

## 📐 Full-Stack Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                          USERS / BROWSERS                            │
└──────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    AWS CloudFront (CDN + SSL)                         │
│                    Distribution: E2494N0PGM4KTG                       │
│                    URL: https://d1pjttps83iyey.cloudfront.net        │
│                    ✅ DEPLOYED & ACTIVE                              │
└──────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                   AWS S3 (Frontend Static Files)                      │
│                   Bucket: iso-standards-frontend                      │
│                   React + Vite + TypeScript                          │
│                   ✅ DEPLOYED & ACTIVE                              │
└──────────────────────────────────────────────────────────────────────┘
                                   │
                                   │ JWT Authentication
                                   │ CORS: Configured
                                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    Backend API (EC2 + Docker)                        │
│                                                                      │
│  AWS EC2 with Docker Compose                                         │
│  • Full control over deployment                                      │
│  • Cost-effective                                                    │
│  • Manual deployment (automated CI/CD later)                         │
│  ⏳ TO BE DEPLOYED                                                  │
└──────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                Django REST Framework Backend                         │
│                                                                      │
│  • Business logic & API endpoints                                    │
│  • JWT token generation/validation (SimpleJWT)                       │
│  • RAG implementation (pgvector)                                     │
│  • CORS configured for CloudFront                                    │
│  • Gunicorn WSGI server (production)                                 │
└──────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                   AWS RDS PostgreSQL 16                              │
│                                                                      │
│  • User authentication data                                          │
│  • ISO standards documents                                           │
│  • pgvector extension for RAG/embeddings                             │
│  • Automated backups (7 days)                                        │
│  • Multi-AZ for high availability                                    │
│  ⏳ TO BE CREATED                                                   │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🔐 Authentication Flow (JWT)

```
Frontend (React)              Backend API (Django)           Database (RDS)
     │                              │                            │
     │  1. POST /auth/login/       │                            │
     │     {email, password}        │                            │
     ├──────────────────────────────►                            │
     │                              │  2. Verify credentials     │
     │                              ├────────────────────────────►
     │                              │ ◄──────────────────────────┤
     │                              │  3. Generate JWT tokens    │
     │                              │     (access + refresh)     │
     │  4. Return tokens & user     │                            │
     │ ◄──────────────────────────┤                            │
     │                              │                            │
     │  5. Store in localStorage:   │                            │
     │     - accessToken (60 min)   │                            │
     │     - refreshToken (7 days)  │                            │
     │                              │                            │
     │  6. API Request              │                            │
     │     Authorization: Bearer    │                            │
     ├──────────────────────────────►                            │
     │                              │  7. Validate JWT           │
     │                              │  8. Process request        │
     │                              ├────────────────────────────►
     │  9. Response                 │ ◄──────────────────────────┤
     │ ◄──────────────────────────┤                            │
```

**Key Features:**

- Access tokens expire in 60 minutes
- Refresh tokens expire in 7 days
- Automatic token refresh via Axios interceptor
- Tokens rotated on refresh (old tokens blacklisted)
- CORS configured between CloudFront and backend
- Bearer token authentication

---

## 📁 Project Structure

```
ISO_Standards/
├── Frontend/                    # React + Vite + TypeScript
│   ├── src/
│   │   ├── services/
│   │   │   ├── api.ts          # Axios instance with JWT interceptors ✅
│   │   │   ├── auth.ts         # Authentication service ✅
│   │   │   └── standards.ts    # API endpoints
│   │   ├── stores/
│   │   │   └── authStore.ts    # Zustand auth state ✅
│   │   └── ...
│   └── ...
│   ✅ DEPLOYED TO: S3 + CloudFront
│
├── Backend/                     # Django 5.2 + Python 3.13
│   ├── config/
│   │   ├── settings/
│   │   │   ├── base.py         # Base settings ✅
│   │   │   ├── development.py  # Dev settings ✅
│   │   │   └── production.py   # Production settings ✅ (Updated with JWT)
│   │   ├── urls.py             # URL routing ✅ (Updated with JWT endpoints)
│   │   └── wsgi.py
│   ├── accounts/               # Custom user model (email-based) ✅
│   ├── Dockerfile.prod         # Production Docker image ✅ NEW
│   ├── docker-compose.prod.yml # Production Docker Compose ✅ NEW
│   ├── .env.production.example # Production env template ✅ NEW
│   └── ...
│   ⏳ TO BE DEPLOYED
│
├── .github/workflows/
│   ├── deploy-frontend.yml     # Frontend CI/CD ✅ ACTIVE
│   └── deploy-backend.yml      # Backend CI/CD ✅ NEW (Ready to activate)
│
└── Docs/
    ├── DOCUMENTATION_INDEX.md  # Main documentation index ✅ UPDATED
    └── Deployment_Doc/
        ├── AWS_DEPLOYMENT_GUIDE.md              # Complete deployment guide ✅ NEW
        ├── BACKEND_DEPLOYMENT_QUICK_REF.md      # Quick commands ✅ NEW
        └── JWT_AUTHENTICATION.md                # Auth documentation ✅ NEW
```

---

## 🎯 Deployment Status

### ✅ Completed

- [x] Frontend deployed to S3
- [x] CloudFront distribution configured
- [x] Frontend CI/CD pipeline active
- [x] JWT authentication implemented in code
- [x] CORS configuration added
- [x] Production Dockerfile created
- [x] Docker Compose production config created
- [x] Health check endpoint added
- [x] Backend CI/CD workflow created
- [x] Documentation created

### ⏳ Pending

- [ ] RDS PostgreSQL instance created
- [ ] pgvector extension installed
- [ ] Backend deployed (choose: EB/ECS/EC2)
- [ ] Environment variables configured
- [ ] SSL certificate for backend API
- [ ] Custom domain for backend (optional)
- [ ] Secrets stored in AWS Secrets Manager
- [ ] Database migrations run on RDS
- [ ] Superuser created
- [ ] Backend CI/CD activated

---

## 🚀 Next Steps to Deploy Backend

### 1. Set Up RDS Database

```bash
# Create PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier iso-standards-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 16.1 \
  --master-username postgres \
  --master-user-password <SECURE_PASSWORD> \
  --allocated-storage 20

# Enable pgvector extension (after instance is ready)
psql -h <rds-endpoint> -U postgres -d postgres
CREATE EXTENSION vector;
```

### 2. Deploy Backend (EC2 + Docker - Manual)

```bash
# SSH to EC2 instance
ssh -i your-key.pem ec2-user@<ec2-public-ip>

# Install Docker and Docker Compose (if not already installed)
sudo yum update -y && sudo yum install -y docker
sudo systemctl start docker && sudo systemctl enable docker
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone repository
git clone https://github.com/bthek1/ISO_Standards.git
cd ISO_Standards/Backend

# Create .env.production file
cat > .env.production << 'EOF'
DJANGO_ENV=production
DEBUG=False
SECRET_KEY=<generated-secret>
ALLOWED_HOSTS=your-ec2-ip-or-domain
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=<db-password>
DB_HOST=<rds-endpoint>
DB_PORT=5432
CORS_ALLOWED_ORIGINS=https://d1pjttps83iyey.cloudfront.net
SIMPLE_JWT_SIGNING_KEY=<jwt-secret>
EOF

# Build and start services
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

### 3. Configure Frontend to Use Backend

```bash
# Update Frontend/.env.production
VITE_API_URL=https://your-ec2-ip-or-domain/api/v1

# Redeploy frontend
git add Frontend/.env.production
git commit -m "Update API URL"
git push origin main  # Auto-deploys via GitHub Actions
```

### 4. Test Full Flow

```bash
# Test health check
curl https://your-ec2-ip-or-domain/health/

# Test login
curl -X POST https://your-ec2-ip-or-domain/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"password"}'

# Test authenticated request
curl https://your-ec2-ip-or-domain/api/v1/standards/ \
  -H "Authorization: Bearer <access-token>"
```

---

## 📊 Technology Stack

### Frontend (Deployed ✅)

- **Framework:** React 18 + TypeScript
- **Build Tool:** Vite
- **Styling:** TailwindCSS
- **State:** Zustand (global) + TanStack Query (server)
- **Routing:** React Router
- **Forms:** react-hook-form + zod
- **HTTP:** Axios with JWT interceptors
- **Hosting:** AWS S3 + CloudFront

### Backend (Ready to Deploy ⏳)

- **Framework:** Django 5.2 + Python 3.13
- **API:** Django REST Framework
- **Authentication:** djangorestframework-simplejwt
- **Database:** PostgreSQL 16 (AWS RDS)
- **Vector DB:** pgvector for RAG
- **WSGI:** Gunicorn (production)
- **CORS:** django-cors-headers
- **Static Files:** WhiteNoise
- **Hosting:** AWS EC2 with Docker Compose

### Infrastructure

- **Cloud:** AWS
- **Database:** RDS PostgreSQL 16 with pgvector
- **CDN:** CloudFront
- **Storage:** S3
- **CI/CD:** GitHub Actions
- **Secrets:** AWS Secrets Manager
- **Monitoring:** CloudWatch

---

## 📚 Documentation Links

- **[Complete Deployment Guide](Deployment_Doc/AWS_DEPLOYMENT_GUIDE.md)** - Full AWS backend deployment
- **[Quick Reference](Deployment_Doc/BACKEND_DEPLOYMENT_QUICK_REF.md)** - Common commands
- **[JWT Authentication](Deployment_Doc/JWT_AUTHENTICATION.md)** - Auth setup & usage
- **[Frontend Deployment](FRONTEND_READY.md)** - Frontend status
- **[Documentation Index](DOCUMENTATION_INDEX.md)** - All documentation

---

## 💰 Estimated Monthly Costs

| Service | Configuration | Cost |
|---------|--------------|------|
| S3 (Frontend) | 1GB, 10k requests | $1-2 |
| CloudFront | 10GB transfer | $1-5 |
| RDS PostgreSQL | db.t3.micro, 20GB | $15-25 |
| EC2 Backend | t3.small | $15-20 |
| Secrets Manager | 2 secrets (optional) | $1 |
| CloudWatch | Basic | $3-5 |
| **Total** | | **$40-75/month** |

---

**Last Updated:** December 4, 2025
**Status:** Frontend deployed ✅ | Backend ready for deployment ⏳
**Deployment Method:** EC2 + Docker Compose (manual deployment, CI/CD later)
**Next Step:** Create RDS instance and deploy backend to EC2
