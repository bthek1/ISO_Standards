# AWS Deployment Guide - ISO Standards Full-Stack Application

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Users/Browsers                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              AWS CloudFront (CDN + SSL/HTTPS)                   │
│              Distribution ID: E2494N0PGM4KTG                    │
│              URL: https://d1pjttps83iyey.cloudfront.net         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   AWS S3 Bucket (Frontend)                      │
│                   iso-standards-frontend                         │
│                   React + Vite + TypeScript                      │
│                   Static files (HTML/CSS/JS)                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ JWT Auth via HTTPS
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              AWS ALB/API Gateway (Backend API)                  │
│              HTTPS endpoint for Django REST API                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Django Backend API                           │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  Django REST Framework + SimpleJWT                      │  │
│  │  - JWT token generation/validation                      │  │
│  │  - Business logic & data processing                     │  │
│  │  - RAG implementation                                   │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Deployment Method:                                            │
│  • AWS EC2 with Docker Compose                                 │
│  • Manual deployment (documented below)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              AWS RDS PostgreSQL 16 (Database)                   │
│              - User data & authentication                        │
│              - ISO standards documents                           │
│              - pgvector extension for RAG                        │
└─────────────────────────────────────────────────────────────────┘
```

## 🔐 Authentication Flow (JWT)

```
Frontend (React)              Backend (Django)              Database (RDS)
     │                              │                            │
     │  POST /api/v1/auth/login/   │                            │
     │  { email, password }         │                            │
     ├────────────────────────────>│                            │
     │                              │  Verify credentials        │
     │                              ├─────────────────────────>  │
     │                              │  <─────────────────────────┤
     │                              │  Generate JWT tokens       │
     │                              │  (access + refresh)        │
     │  { access, refresh, user }   │                            │
     │ <────────────────────────────┤                            │
     │                              │                            │
     │  Store in localStorage       │                            │
     │  - accessToken               │                            │
     │  - refreshToken              │                            │
     │                              │                            │
     │  API Request with JWT        │                            │
     │  Authorization: Bearer <token>│                           │
     ├────────────────────────────>│                            │
     │                              │  Validate JWT              │
     │                              │  Process request           │
     │                              ├─────────────────────────>  │
     │  Response with data          │  <─────────────────────────┤
     │ <────────────────────────────┤                            │
```

---

## 📋 Prerequisites

- AWS Account with appropriate permissions
- AWS CLI installed and configured
- Docker installed (for containerized deployment)
- Domain name (optional, for custom domain)
- GitHub account (for CI/CD)

---

## 🚀 Deployment Steps

**Deployment Method:** EC2 + Docker Compose (Manual)

**Note:** This guide focuses on deploying to an EC2 instance using Docker. Automated CI/CD deployment will be configured later.

### Phase 1: Database Setup (AWS RDS)

#### 1.1 Create RDS PostgreSQL Instance

**Option A: AWS Console**
1. Navigate to RDS → Create database
2. Configuration:
   - Engine: PostgreSQL 16.x
   - Template: Production (or Dev/Test for development)
   - DB instance identifier: `iso-standards-db`
   - Master username: `postgres`
   - Master password: `<secure-password>`
   - Instance class: `db.t3.micro` (can scale up later)
   - Storage: 20 GB (with autoscaling enabled)
   - VPC: Default or create new
   - Public access: Yes (for initial setup, restrict later)
   - Security group: Create new (allow PostgreSQL port 5432)

**Option B: AWS CLI**
```bash
aws rds create-db-instance \
  --db-instance-identifier iso-standards-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 16.1 \
  --master-username postgres \
  --master-user-password YOUR_SECURE_PASSWORD \
  --allocated-storage 20 \
  --storage-type gp3 \
  --vpc-security-group-ids sg-xxxxx \
  --backup-retention-period 7 \
  --preferred-backup-window "03:00-04:00" \
  --preferred-maintenance-window "mon:04:00-mon:05:00" \
  --multi-az \
  --publicly-accessible \
  --tags Key=Project,Value=ISO-Standards Key=Environment,Value=Production
```

#### 1.2 Configure Security Group

```bash
# Get your IP address
MY_IP=$(curl -s https://checkip.amazonaws.com)

# Add inbound rule for PostgreSQL
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 5432 \
  --cidr $MY_IP/32

# For production, also add backend server IPs/security groups
```

#### 1.3 Enable pgvector Extension

```bash
# Connect to RDS instance
psql -h iso-standards-db.xxxxx.us-east-1.rds.amazonaws.com \
     -U postgres \
     -d postgres

# Inside psql:
CREATE EXTENSION IF NOT EXISTS vector;

# Verify installation
SELECT * FROM pg_extension WHERE extname = 'vector';
```

#### 1.4 Run Django Migrations

```bash
# Set environment variables
export DB_HOST=iso-standards-db.xxxxx.us-east-1.rds.amazonaws.com
export DB_NAME=postgres
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_PORT=5432

# Run migrations
cd /home/bthek1/ISO_Standards/Backend
python manage.py migrate --settings=config.settings.production
```

---

### Phase 2: Backend API Deployment (EC2 + Docker)

**Deployment Method:** AWS EC2 with Docker Compose

**Pros:**
- Full control over deployment
- Cost-effective for small to medium deployments
- Familiar Docker workflow
- Easy to debug and maintain

**Note:** Automated CI/CD deployment will be configured later. For now, deployment is manual using Docker Compose.

**Steps:**

```bash
# 1. Launch an EC2 instance (via AWS Console)
# - Instance Type: t3.small or t3.medium
# - AMI: Amazon Linux 2023 or Ubuntu 22.04
# - Security Group: Allow SSH (22), HTTP (80), HTTPS (443), Django (8000)
# - Key Pair: Create or use existing for SSH access

# 2. SSH to EC2 instance
ssh -i your-key.pem ec2-user@<ec2-public-ip>

# 3. Install Docker and Docker Compose
sudo yum update -y
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 4. Clone repository
git clone https://github.com/bthek1/ISO_Standards.git
cd ISO_Standards/Backend

# 5. Create production environment file
cat > .env.production << 'EOF'
DJANGO_ENV=production
DEBUG=False
SECRET_KEY=your-generated-secret-key
ALLOWED_HOSTS=your-ec2-ip-or-domain,.cloudfront.net
CORS_ALLOWED_ORIGINS=https://d1pjttps83iyey.cloudfront.net

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=iso-standards-db.xxxxx.us-east-1.rds.amazonaws.com
DB_PORT=5432

# JWT
SIMPLE_JWT_SIGNING_KEY=your-jwt-signing-key
EOF

# 6. Build and start services
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# 7. Run migrations and create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# 8. Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# 9. Check logs
docker-compose -f docker-compose.prod.yml logs -f
```

**Optional: Configure Domain and HTTPS**

```bash
# Install Certbot for Let's Encrypt SSL
sudo yum install -y certbot python3-certbot-nginx

# Get SSL certificate (after pointing domain to EC2)
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Update ALLOWED_HOSTS and CORS_ALLOWED_ORIGINS in .env.production
# Restart services
docker-compose -f docker-compose.prod.yml restart
```

```bash
# 1. Create ECR repository
aws ecr create-repository \
  --repository-name iso-standards-backend \
  --region us-east-1

# 2. Build and push Docker image
cd /home/bthek1/ISO_Standards/Backend

# Get ECR login
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build production image
docker build -t iso-standards-backend:latest \
  -f Dockerfile.prod .

# Tag image
docker tag iso-standards-backend:latest \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com/iso-standards-backend:latest

```

---

### Phase 3: Configure CORS & JWT for Frontend-Backend Communication

#### 3.1 Update Django Settings for CORS

Add to `Backend/config/settings/production.py`:

```python
# CORS Configuration
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    'https://d1pjttps83iyey.cloudfront.net'
).split(',')

CORS_ALLOW_CREDENTIALS = True

# JWT Configuration
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'SIGNING_KEY': os.environ.get('SIMPLE_JWT_SIGNING_KEY', SECRET_KEY),
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# Update REST_FRAMEWORK settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

#### 3.2 Update Frontend Environment Variables

Update `Frontend/.env.production`:

```bash
# Backend API URL (replace with your EC2 IP or domain)
VITE_API_URL=https://your-ec2-ip-or-domain/api/v1

# Or if using custom domain:
# VITE_API_URL=https://api.yourdomain.com/api/v1
```

---

### Phase 4: Secrets Management with AWS Secrets Manager

```bash
# 1. Create secret for production credentials
aws secretsmanager create-secret \
  --name iso-standards/prod \
  --description "Production secrets for ISO Standards app" \
  --secret-string '{
    "SECRET_KEY": "your-django-secret-key",
    "DB_PASSWORD": "your-database-password",
    "SIMPLE_JWT_SIGNING_KEY": "your-jwt-signing-key",
    "EMAIL_HOST_PASSWORD": "your-email-password"
  }'

# 2. Grant access to backend service
# (Attach IAM policy to EC2 instance role or ECS task role)
```

**IAM Policy for Secrets Access:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": "arn:aws:secretsmanager:us-east-1:account-id:secret:iso-standards/prod-*"
    }
  ]
}
```

---

### Phase 5: Set Up Application Load Balancer & SSL

#### 5.1 Request SSL Certificate (AWS Certificate Manager)

```bash
# Request certificate for your domain
aws acm request-certificate \
  --domain-name api.yourdomain.com \
  --subject-alternative-names "*.yourdomain.com" \
  --validation-method DNS \
  --region us-east-1

# Follow DNS validation steps in AWS Console
```

#### 5.2 Create Application Load Balancer

**Via AWS Console:**
1. EC2 → Load Balancers → Create Load Balancer
2. Choose Application Load Balancer
3. Configure:
   - Name: `iso-standards-alb`
   - Scheme: Internet-facing
   - Listeners: HTTP (80) and HTTPS (443)
   - Availability Zones: Select at least 2
4. Configure Security Settings:
   - Select SSL certificate from ACM
5. Configure Target Group:
   - Target type: Instance/IP (depending on deployment)
   - Protocol: HTTP
   - Port: 8000
   - Health check path: `/health/` or `/api/v1/health/`
6. Register targets (your EC2 instance or ECS tasks)

#### 5.3 Update DNS Records

```bash
# Add CNAME record for API subdomain
# api.yourdomain.com → iso-standards-alb-xxxxx.us-east-1.elb.amazonaws.com
```

---

### Phase 6: Health Checks & Monitoring

#### 6.1 Create Health Check Endpoint

Add to `Backend/config/urls.py`:

```python
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    """Health check endpoint for load balancer."""
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return JsonResponse({
            "status": "healthy",
            "database": "connected"
        })
    except Exception as e:
        return JsonResponse({
            "status": "unhealthy",
            "error": str(e)
        }, status=503)

urlpatterns = [
    path('health/', health_check, name='health'),
    # ... other URLs
]
```

#### 6.2 Configure CloudWatch Alarms

```bash
# Create alarm for high error rate
aws cloudwatch put-metric-alarm \
  --alarm-name iso-standards-high-error-rate \
  --alarm-description "Alert when error rate exceeds 5%" \
  --metric-name HTTPCode_Target_5XX_Count \
  --namespace AWS/ApplicationELB \
  --statistic Sum \
  --period 300 \
  --evaluation-periods 2 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold

# Create alarm for low health
aws cloudwatch put-metric-alarm \
  --alarm-name iso-standards-unhealthy-targets \
  --metric-name UnHealthyHostCount \
  --namespace AWS/ApplicationELB \
  --statistic Average \
  --period 60 \
  --evaluation-periods 2 \
  --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold
```

---

## 🔧 Production Checklist

### Django Backend
- [ ] `DEBUG=False` in production
- [ ] `SECRET_KEY` from environment/secrets manager
- [ ] `ALLOWED_HOSTS` configured correctly
- [ ] CORS origins include frontend CloudFront URL
- [ ] JWT signing key configured
- [ ] Database connection to RDS working
- [ ] pgvector extension enabled in RDS
- [ ] Static files configured (WhiteNoise or S3)
- [ ] Migrations applied
- [ ] Superuser created
- [ ] Health check endpoint working
- [ ] SSL/HTTPS enabled
- [ ] Security headers configured
- [ ] Logging to CloudWatch configured
- [ ] Gunicorn configured for production

### Frontend (Already Deployed)
- [ ] S3 bucket created and configured
- [ ] CloudFront distribution set up
- [ ] `VITE_API_URL` points to backend API
- [ ] CORS headers allowing CloudFront origin
- [ ] JWT tokens stored securely (httpOnly if possible)
- [ ] Error handling for 401 responses
- [ ] Token refresh logic implemented

### Database (RDS)
- [ ] PostgreSQL 16 instance created
- [ ] Security group allows backend access
- [ ] pgvector extension installed
- [ ] Automated backups enabled
- [ ] Multi-AZ for high availability (optional)
- [ ] Performance Insights enabled
- [ ] Connection pooling configured

### Security
- [ ] SSL/TLS certificates installed
- [ ] Security groups restrict access appropriately
- [ ] Secrets stored in AWS Secrets Manager
- [ ] IAM roles with least privilege
- [ ] HSTS headers enabled
- [ ] Rate limiting configured
- [ ] SQL injection protection (Django ORM)
- [ ] XSS protection (React auto-escaping)

### Monitoring & Logging
- [ ] CloudWatch Logs configured
- [ ] CloudWatch Alarms set up
- [ ] Application metrics tracked
- [ ] Error tracking (Sentry/Rollbar optional)
- [ ] Uptime monitoring

---

## 🚦 Testing the Deployment

### 1. Test Health Check
```bash
curl https://api.yourdomain.com/health/
# Expected: {"status": "healthy", "database": "connected"}
```

### 2. Test JWT Authentication
```bash
# Login
curl -X POST https://api.yourdomain.com/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# Expected response with access and refresh tokens
```

### 3. Test Protected Endpoint
```bash
curl https://api.yourdomain.com/api/v1/standards/ \
  -H "Authorization: Bearer <access-token>"
```

### 4. Test CORS
```javascript
// In browser console on CloudFront URL
fetch('https://api.yourdomain.com/api/v1/standards/', {
  headers: {
    'Authorization': 'Bearer <token>'
  }
}).then(r => r.json()).then(console.log)
```

---

## 📊 Cost Estimation

### Monthly AWS Costs (Approximate)

| Service | Configuration | Estimated Cost |
|---------|--------------|----------------|
| **RDS PostgreSQL** | db.t3.micro, 20GB | $15-25/month |
| **EC2 Instance** | t3.small (backend) | $15-20/month |
| **S3 (Frontend)** | 1GB storage, 10k requests | $1-2/month |
| **CloudFront** | 10GB transfer | $1-5/month |
| **Data Transfer** | Outbound | $5-15/month |
| **Secrets Manager** | 2 secrets (optional) | $1/month |
| **CloudWatch** | Basic metrics | $3-5/month |
| **SSL Certificate (Let's Encrypt)** | Free | $0 |
| **Route 53 (DNS)** | Hosted zone (optional) | $0.50/month |

**Total: $40-75/month** (cost-optimized setup)

### Cost Optimization Tips
- Use Reserved Instances for long-term savings (up to 40% off)
- Use Spot Instances for non-critical workloads
- Downgrade RDS to db.t4g.micro for additional savings
- Monitor unused resources with AWS Cost Explorer
- Use S3 lifecycle policies for old data
- Consider AWS Free Tier eligibility (first 12 months)
- Use Fargate Spot for non-critical workloads
- Cache API responses with CloudFront

---

## 🔄 CI/CD with GitHub Actions

Update `.github/workflows/deploy-backend.yml`:

```yaml
name: Deploy Backend to AWS

on:
  push:
    branches: [main]
    paths:
      - 'Backend/**'
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to EC2 via SSH
        run: |
          echo "${{ secrets.EC2_SSH_KEY }}" > ec2_key.pem
          chmod 600 ec2_key.pem
          ssh -o StrictHostKeyChecking=no -i ec2_key.pem ec2-user@${{ secrets.EC2_HOST }} << 'EOF'
            cd ISO_Standards/Backend
            git pull origin main
            docker-compose -f docker-compose.prod.yml build
            docker-compose -f docker-compose.prod.yml up -d
            docker-compose -f docker-compose.prod.yml exec -T web python manage.py migrate
            docker-compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput
          EOF
```

**Note:** CI/CD workflow will be set up later. For now, deployment is manual via SSH to EC2.

---

## 🆘 Troubleshooting

### Issue: CORS errors in browser console
**Solution:** Ensure `CORS_ALLOWED_ORIGINS` in Django includes CloudFront URL

### Issue: 401 Unauthorized on API calls
**Solution:**
- Check JWT token is being sent in Authorization header
- Verify token hasn't expired
- Check `SIMPLE_JWT` settings in Django

### Issue: Database connection refused
**Solution:**
- Verify RDS security group allows backend IP/security group
- Check `DB_HOST` environment variable
- Ensure RDS instance is publicly accessible (or use VPC peering)

### Issue: Static files not loading
**Solution:**
- Run `docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic`
- Check WhiteNoise configuration
- Verify STATIC_ROOT and STATIC_URL settings

### Issue: Health check failing
**Solution:**
- Check database connectivity
- Verify health check endpoint returns 200
- Review Docker logs: `docker-compose -f docker-compose.prod.yml logs -f`

### Issue: Docker container not starting
**Solution:**
- Check logs: `docker-compose -f docker-compose.prod.yml logs web`
- Verify .env.production has all required variables
- Check port 8000 is not already in use

---

## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Django on Docker Best Practices](https://docs.docker.com/samples/django/)
- [Django REST Framework JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [AWS RDS Best Practices](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_BestPractices.html)
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [AWS EC2 Security Best Practices](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security.html)

---

## 🎯 Next Steps

1. Set up EC2 instance with Docker and Docker Compose
2. Set up RDS PostgreSQL database with pgvector
3. Deploy backend API to EC2
4. Configure CORS and JWT
5. Test authentication flow end-to-end
6. Set up monitoring and alerts (CloudWatch)
7. Configure custom domain and HTTPS (optional)
8. Implement CI/CD pipeline (future)
9. Load test application
10. Set up backup and disaster recovery

---

**Last Updated:** December 4, 2025
**Maintainer:** Benedict Thekkel
**Project:** ISO Standards Full-Stack Application
