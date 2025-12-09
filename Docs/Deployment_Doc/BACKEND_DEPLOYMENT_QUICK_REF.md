# Backend API Deployment Quick Reference

## 🚀 Quick Deploy Commands

### Using Docker on EC2 (Current Method)

```bash
# SSH to EC2
ssh -i your-key.pem ec2-user@<ec2-ip>

# Pull latest code
cd ISO_Standards/Backend
git pull

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up -d --build

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

---

## 🔗 Important URLs

### Development

- **Local Backend:** <http://localhost:8000>
- **Local Admin:** <http://localhost:8000/admin>
- **Local API:** <http://localhost:8000/api/v1/>

### Production (Update after deployment)

- **Backend API:** <https://your-ec2-ip-or-domain.com>
- **Admin Panel:** <https://your-ec2-ip-or-domain.com/admin>
- **API Docs:** <https://your-ec2-ip-or-domain.com/api/v1/docs/>
- **Health Check:** <https://your-ec2-ip-or-domain.com/health/>

### AWS Console Links

- **EC2:** <https://console.aws.amazon.com/ec2>
- **RDS:** <https://console.aws.amazon.com/rds>
- **CloudWatch Logs:** <https://console.aws.amazon.com/cloudwatch/home#logsV2:log-groups>
- **Secrets Manager:** <https://console.aws.amazon.com/secretsmanager>

---

## 🔧 Common Tasks

### Run Database Migrations

```bash
# Docker on EC2
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

### Create Superuser

```bash
# Docker on EC2
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

### Collect Static Files

```bash
# Docker on EC2
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

### View Logs

```bash
# Docker on EC2
docker-compose -f docker-compose.prod.yml logs -f web

# CloudWatch (if configured)
aws logs tail /aws/ec2/iso-standards-backend --follow
```

---

## 🔐 Environment Variables

### Required Variables

```bash
SECRET_KEY                    # Django secret key
DEBUG                         # False in production
ALLOWED_HOSTS                 # Your domain/IP
DB_HOST                       # RDS endpoint
DB_NAME                       # Database name
DB_USER                       # Database username
DB_PASSWORD                   # Database password
CORS_ALLOWED_ORIGINS          # Frontend CloudFront URL
SIMPLE_JWT_SIGNING_KEY        # JWT signing key
```

### Optional Variables

```bash
EMAIL_HOST                    # SMTP server
EMAIL_HOST_USER               # Email username
EMAIL_HOST_PASSWORD           # Email password
AWS_ACCESS_KEY_ID             # For S3 (if used)
AWS_SECRET_ACCESS_KEY         # For S3 (if used)
AWS_STORAGE_BUCKET_NAME       # S3 bucket name
REDIS_URL                     # Redis connection
DJANGO_LOG_LEVEL              # Logging level
```

---

## 📊 Monitoring

### Health Checks

```bash
# API Health
curl https://your-ec2-ip-or-domain/health/

# Database Connection
curl https://your-ec2-ip-or-domain/api/v1/health/db/
```

### Performance

```bash
# CloudWatch metrics (if EC2 monitoring enabled)
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-xxxxx \
  --start-time 2025-12-04T00:00:00Z \
  --end-time 2025-12-04T23:59:59Z \
  --period 3600 \
  --statistics Average
```

---

## 🐛 Troubleshooting

### Check Application Status

```bash
# Docker
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs -f web

# EC2 Instance
aws ec2 describe-instance-status --instance-ids i-xxxxx
  --cluster iso-standards-cluster \
  --services iso-standards-service
```

### View Error Logs

```bash
# View Docker logs
docker-compose -f docker-compose.prod.yml logs web | grep ERROR

# Continuous tail
docker-compose -f docker-compose.prod.yml logs -f web
```

### Database Connection Test

```bash
# From EC2 instance
docker-compose -f docker-compose.prod.yml exec web python manage.py dbshell

# Or direct psql connection
psql -h iso-standards-db.xxxxx.us-east-1.rds.amazonaws.com \
     -U postgres \
     -d postgres \
     -c "SELECT version();"
```

### Test JWT Authentication

```bash
# Login
curl -X POST https://your-ec2-ip-or-domain/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"yourpassword"}'

# Use token
curl https://your-ec2-ip-or-domain/api/v1/standards/ \
  -H "Authorization: Bearer <access-token>"
```

---

## 🔄 Deployment Process

### Manual Deployment (Current)

**Note:** Automated CI/CD will be configured later.

1. **SSH to EC2 instance**

```bash
ssh -i your-key.pem ec2-user@<ec2-ip>
```

1. **Pull latest changes**

```bash
cd ISO_Standards/Backend
git pull origin main
```

1. **Rebuild and restart**

```bash
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build
```

1. **Check status**
gh workflow run deploy-backend.yml

```

---

## 📋 Pre-Deployment Checklist
```bash
docker-compose -f docker-compose.prod.yml ps
curl https://your-ec2-ip-or-domain/health/
```

---

## 📋 Pre-Deployment Checklist

- [ ] All tests passing locally
- [ ] Environment variables configured in .env.production
- [ ] Database migrations created
- [ ] Static files collected
- [ ] CORS origins updated
- [ ] SSL certificate ready (if using custom domain)
- [ ] Health check endpoint working
- [ ] RDS security group configured
- [ ] EC2 security group configured
- [ ] Backup strategy in place
- [ ] Docker images built and tested locally

---

## 🆘 Emergency Rollback

### Docker on EC2

```bash
# Use previous image tag or commit
cd ISO_Standards/Backend
git checkout <previous-commit>
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build

# Or restore from backup
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --force-recreate
```

---

## 📞 Support Resources

- **AWS Support:** <https://console.aws.amazon.com/support>
- **Django Docs:** <https://docs.djangoproject.com/>
- **Docker Docs:** <https://docs.docker.com/>
- **Project Docs:** `/home/bthek1/ISO_Standards/Docs/`
- **GitHub Issues:** <https://github.com/bthek1/ISO_Standards/issues>

---

**Last Updated:** December 4, 2025
**Deployment Method:** EC2 + Docker Compose (Manual)
