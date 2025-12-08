# AWS RDS PostgreSQL Setup for Development

## Overview

This document outlines the plan to set up AWS RDS PostgreSQL for the ISO Standards project development environment, replacing the current SQLite database.

## Current State

- **Development**: Using SQLite (`db.sqlite3`)
- **Django Version**: 5.2+
- **Python Version**: 3.13

## Goals

1. Set up AWS RDS PostgreSQL instance for development
2. Update Django settings for development environment
3. Migrate existing data from SQLite
4. Update development workflow and documentation
5. Configure secure access via AWS SSO

## Phase 1: AWS RDS Setup for Development

### 1.1 Prerequisites

Before creating the RDS instance:

1. **AWS SSO Access**: Ensure you're logged in
   ```bash
   aws sso login --profile ben-sso
   export AWS_PROFILE=ben-sso
   ```

2. **Check VPC and Subnets**: Identify your VPC
   ```bash
   # List VPCs
   aws ec2 describe-vpcs --region ap-southeast-2

   # List subnets in your VPC
   aws ec2 describe-subnets \
     --filters "Name=vpc-id,Values=vpc-xxxxx" \
     --region ap-southeast-2
   ```

3. **Get Your Public IP**: For security group configuration
   ```bash
   curl -s https://checkip.amazonaws.com
   ```

### 1.2 Create Development RDS Instance

**Instance Specifications:**
- **Engine**: PostgreSQL 16.x (latest stable)
- **Instance Class**: `db.t3.micro` (Free tier eligible, ~$12/month after free tier)
- **Storage**: 20 GB GP3 (Free tier: 20 GB)
- **Multi-AZ**: No (development doesn't need high availability)
- **Backup Retention**: 1 day (minimal backups for dev)
- **Public Access**: Yes (for direct development access)
- **Region**: `ap-southeast-2` (Sydney)

**Step 1: Create Security Group**

```bash
# Set AWS profile
export AWS_PROFILE=ben-sso

# Get default VPC (or use your specific VPC)
VPC_ID=$(aws ec2 describe-vpcs \
  --filters "Name=isDefault,Values=true" \
  --query 'Vpcs[0].VpcId' \
  --output text \
  --region ap-southeast-2)

echo "Using VPC: $VPC_ID"

# Create security group for RDS
SG_ID=$(aws ec2 create-security-group \
  --group-name iso-standards-dev-rds-sg \
  --description "Security group for ISO Standards Development RDS" \
  --vpc-id $VPC_ID \
  --region ap-southeast-2 \
  --output text \
  --query 'GroupId')

echo "Created Security Group: $SG_ID"

# Get your public IP
MY_IP=$(curl -s https://checkip.amazonaws.com)

# Add inbound rule for PostgreSQL from your IP
aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --protocol tcp \
  --port 5432 \
  --cidr $MY_IP/32 \
  --region ap-southeast-2

echo "Added PostgreSQL access from: $MY_IP"
```

**Step 2: Create RDS Instance**

```bash
# Create development RDS instance with public access
aws rds create-db-instance \
  --db-instance-identifier iso-standards-dev \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 16.1 \
  --master-username postgres \
  --master-user-password "DevPassword123!" \
  --allocated-storage 20 \
  --storage-type gp3 \
  --vpc-security-group-ids $SG_ID \
  --backup-retention-period 1 \
  --publicly-accessible \
  --no-multi-az \
  --storage-encrypted \
  --region ap-southeast-2 \
  --tags Key=Environment,Value=Development Key=Project,Value=ISO_Standards

echo "Creating RDS instance... This will take 5-10 minutes"

# Wait for instance to be available
aws rds wait db-instance-available \
  --db-instance-identifier iso-standards-dev \
  --region ap-southeast-2

echo "✓ RDS instance is ready!"

# Get endpoint information
RDS_ENDPOINT=$(aws rds describe-db-instances \
  --db-instance-identifier iso-standards-dev \
  --query 'DBInstances[0].Endpoint.Address' \
  --output text \
  --region ap-southeast-2)

echo "RDS Endpoint: $RDS_ENDPOINT"
echo "Username: postgres"
echo "Password: DevPassword123!"
echo "Port: 5432"
```

### 1.3 Verify Connection

```bash
# Install PostgreSQL client if not already installed
# Ubuntu/Debian:
# sudo apt-get install postgresql-client

# macOS:
# brew install postgresql

# Test connection
psql -h $RDS_ENDPOINT \
  -U postgres \
  -d postgres \
  -c "SELECT version();"

# Create application database
psql -h $RDS_ENDPOINT \
  -U postgres \
  -c "CREATE DATABASE iso_standards;"

echo "✓ Database created successfully"
```

## Phase 2: PostgreSQL Extensions Setup

Install required PostgreSQL extensions for the application.

### 2.1 Connect to RDS and Enable Extensions

```bash
# Get RDS endpoint
export AWS_PROFILE=ben-sso
RDS_ENDPOINT=$(aws rds describe-db-instances \
  --db-instance-identifier iso-standards-dev \
  --query 'DBInstances[0].Endpoint.Address' \
  --output text \
  --region ap-southeast-2)

# Connect to the database
psql -h $RDS_ENDPOINT -U postgres -d iso_standards

# Run these commands in psql:
# Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";     -- For text search
CREATE EXTENSION IF NOT EXISTS "vector";      -- For pgvector (RAG)

# Verify extensions
\dx

# Exit psql
\q
```

**Note**: If the `vector` extension is not available, you may need to use a different RDS instance class or install it separately. For development, you can skip it initially and add it later when implementing RAG features.

## Phase 3: Django Settings Configuration

### 3.1 Update Base Settings

**File**: `Backend/config/settings/base.py`

```python
import os
from pathlib import Path

# Database helper function
def get_database_config():
    """Get database configuration based on environment."""
    env = os.environ.get("DJANGO_ENV", "development")

    if env == "development":
        # Option 1: Local Docker PostgreSQL
        if os.environ.get("USE_DOCKER_DB", "false").lower() == "true":
            return {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": os.environ.get("DB_NAME", "iso_standards"),
                "USER": os.environ.get("DB_USER", "postgres"),
                "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
## Phase 3: Django Settings Configuration

### 3.1 Update Development Settings

**File**: `Backend/config/settings/development.py`

```python
from .base import *  # noqa: F403

DEBUG = True

# Allow all hosts in development
ALLOWED_HOSTS = ["*"]

# AWS RDS PostgreSQL Database Configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "iso_standards"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "DevPassword123!"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "CONN_MAX_AGE": 0,  # Don't persist connections in dev
        "OPTIONS": {
            "connect_timeout": 10,
        },
    }
}

# Optional: Enable SQL query logging in development
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}
```

### 3.2 Keep Test Settings with Local PostgreSQL

**File**: `Backend/config/settings/test.py`

Tests will continue to use the PostgreSQL service in GitHub Actions.

```python
from .base import *  # noqa: F403

# Use PostgreSQL for tests (matches CI/CD)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "test_iso_standards",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# Speed up tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
```PORT=5432

# Database Option 3: AWS RDS Development
# USE_RDS_DEV=true
# AWS credentials configured via SSO

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 4.2 Production .env

**File**: `Backend/.env.production` (Never commit this file!)

```bash
# Environment
DJANGO_ENV=production
DEBUG=False
SECRET_KEY=your-production-secret-key

# Database - Retrieved from AWS Secrets Manager
# AWS credentials configured via IAM role or SSO

# Allowed Hosts
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# AWS Settings
AWS_STORAGE_BUCKET_NAME=iso-standards-static
AWS_S3_REGION_NAME=ap-southeast-2
```

## Phase 5: Install PostgreSQL Dependencies

### 5.1 Update pyproject.toml

**File**: `Backend/pyproject.toml`

Add PostgreSQL adapter to dependencies:

```toml
[project]
dependencies = [
    # ... existing dependencies
    "psycopg2-binary>=2.9.9",  # PostgreSQL adapter
]
```

### 5.2 Install Dependencies

```bash
cd Backend

# Activate virtual environment if not already active
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"
## Phase 6: Database Migration

### 6.1 Backup SQLite Data (if you have existing data)

```bash
cd Backend

# Backup SQLite database
cp db.sqlite3 db.sqlite3.backup

# Export data as JSON
python manage.py dumpdata \
  --exclude auth.permission \
  --exclude contenttypes \
  --exclude sessions \
  --indent 2 \
  > data_backup.json

echo "✓ SQLite data backed up to data_backup.json"
```

### 6.2 Run Migrations on RDS

```bash
# Ensure your .env has the correct RDS settings
# Activate virtual environment
source .venv/bin/activate

# Run migrations
python manage.py migrate

echo "✓ Database migrations completed"
```

### 6.3 Create Superuser

```bash
# Create a new superuser for the PostgreSQL database
python manage.py createsuperuser

# Or create with command
python manage.py createsuperuser \
  --email your.email@example.com \
  --username admin
```

### 6.4 Import Data (if you backed up SQLite data)

```bash
# Load data from backup
python manage.py loaddata data_backup.json

echo "✓ Data imported successfully"
```

### 6.5 Verify Database

```bash
# Test database connection
python manage.py dbshell

# In psql, run:
# \dt  -- List all tables
# \q   -- Exit

# Or use Django shell
python manage.py shell
```

```python
# In Django shell:
from accounts.models import CustomUser
print(f"Total users: {CustomUser.objects.count()}")

# Test query
users = CustomUser.objects.all()
for user in users:
    print(f"User: {user.email}")
```ile**: `Backend/.env.example`

Update the example file for other developers:

```bash
# Environment
DJANGO_ENV=development
DEBUG=True
SECRET_KEY=your-secret-key-here

# AWS RDS PostgreSQL Database
DB_NAME=iso_standards
DB_USER=postgres
DB_PASSWORD=your-password-here
DB_HOST=your-rds-endpoint.ap-southeast-2.rds.amazonaws.com
DB_PORT=5432

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1
```ate the PostgreSQL service to match RDS version:

```yaml
services:
  postgres:
    image: postgres:16-alpine
    env:
      POSTGRES_DB: test_iso_standards
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - 5432:5432
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
## Phase 8: Development Workflow

### 8.1 Daily Development Workflow

```bash
# 1. Login to AWS SSO (if session expired)
aws sso login --profile ben-sso

# 2. Navigate to Backend directory
cd Backend

# 3. Activate virtual environment
source .venv/bin/activate

# 4. Verify database connection
python scripts/test_db_connection.py

# 5. Run migrations (if needed)
python manage.py migrate

# 6. Start development server
python manage.py runserver
```

### 8.2 Managing the RDS Instance

**Check instance status:**
```bash
export AWS_PROFILE=ben-sso
aws rds describe-db-instances \
  --db-instance-identifier iso-standards-dev \
  --query 'DBInstances[0].[DBInstanceStatus,Endpoint.Address,Endpoint.Port]' \
  --region ap-southeast-2
```

**Stop instance to save costs (when not developing):**
```bash
# Stop the instance
aws rds stop-db-instance \
  --db-instance-identifier iso-standards-dev \
  --region ap-southeast-2

echo "RDS instance stopped. It will auto-start after 7 days."
```

**Start instance:**
```bash
# Start the instance
aws rds start-db-instance \
  --db-instance-identifier iso-standards-dev \
  --region ap-southeast-2

# Wait for it to be available
aws rds wait db-instance-available \
  --db-instance-identifier iso-standards-dev \
  --region ap-southeast-2

echo "RDS instance is running"
```

### 8.3 Database Management

**Create database backup:**
```bash
# Manual snapshot
aws rds create-db-snapshot \
  --db-instance-identifier iso-standards-dev \
  --db-snapshot-identifier iso-standards-dev-snapshot-$(date +%Y%m%d) \
  --region ap-southeast-2
```

**Access database directly:**
```bash
## Phase 9: Monitoring (Optional for Development)

### 9.1 View RDS Metrics in AWS Console

Access the RDS console to view basic metrics:
- CPU Utilization
- Database Connections
- Free Storage Space
- Read/Write Latency

```bash
# Open RDS console (if using a browser on the server)
export AWS_PROFILE=ben-sso
aws rds describe-db-instances \
  --db-instance-identifier iso-standards-dev \
  --region ap-southeast-2
```

### 9.2 Check Database Size

```bash
# Connect to database
psql -h $RDS_ENDPOINT -U postgres -d iso_standards

# Run in psql:
SELECT
    pg_database.datname,
    pg_size_pretty(pg_database_size(pg_database.datname)) AS size
FROM pg_database
ORDER BY pg_database_size(pg_database.datname) DESC;

# Check table sizes
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```torage space alarm
aws cloudwatch put-metric-alarm \
  --alarm-name iso-standards-rds-storage-low \
  --alarm-description "Alert when free storage < 2GB" \
  --metric-name FreeStorageSpace \
  --namespace AWS/RDS \
  --statistic Average \
  --period 300 \
  --threshold 2000000000 \
  --comparison-operator LessThanThreshold \
  --evaluation-periods 1 \
  --dimensions Name=DBInstanceIdentifier,Value=iso-standards-prod \
  --region ap-southeast-2 \
  --profile ben-sso
```

### 9.3 Backup Strategy

- **Automated Backups**: Enabled with 7-day retention
- **Manual Snapshots**: Before major changes
- **Point-in-Time Recovery**: Enabled automatically

```bash
# Create manual snapshot
aws rds create-db-snapshot \
  --db-instance-identifier iso-standards-prod \
  --db-snapshot-identifier iso-standards-prod-$(date +%Y%m%d-%H%M%S) \
  --region ap-southeast-2 \
  --profile ben-sso

# List snapshots
aws rds describe-db-snapshots \
  --db-instance-identifier iso-standards-prod \
  --region ap-southeast-2 \
  --profile ben-sso
```

## Phase 10: Documentation Updates

### 10.1 Update README.md

Add database setup instructions for new developers.

### 10.2 Update .env.example

Provide template with all database options.

### 10.3 Create Runbook

Document common operations:
## Phase 10: Documentation Updates

### 10.1 Update Backend README.md

Add a "Database Setup" section with RDS connection instructions.

### 10.2 Create Quick Reference Card

**File**: `Backend/RDS_QUICK_REFERENCE.md`

```markdown
# AWS RDS Quick Reference

## Connection Details
- Instance: iso-standards-dev
- Database: iso_standards
- User: postgres
- Port: 5432

## Get Endpoint
```bash
export AWS_PROFILE=ben-sso
aws rds describe-db-instances \
  --db-instance-identifier iso-standards-dev \
  --query 'DBInstances[0].Endpoint.Address' \
  --output text \
  --region ap-southeast-2
```

## Stop/Start Instance
```bash
# Stop (saves costs when not developing)
aws rds stop-db-instance --db-instance-identifier iso-standards-dev --region ap-southeast-2

# Start
aws rds start-db-instance --db-instance-identifier iso-standards-dev --region ap-southeast-2
```

## Connect with psql
```bash
psql -h YOUR_ENDPOINT -U postgres -d iso_standards
```
```

## Troubleshooting

### Common Issues

**1. Cannot connect to RDS**
- Verify AWS SSO is logged in: `aws sts get-caller-identity --profile ben-sso`
- Check security group allows your IP
- Verify RDS instance is running: `aws rds describe-db-instances --db-instance-identifier iso-standards-dev --region ap-southeast-2`

**2. "Password authentication failed"**
- Verify password in `.env` file matches RDS password
- Check `DB_HOST` is correct endpoint

**3. "Connection timeout"**
- Check RDS instance is publicly accessible
- Verify security group inbound rules allow port 5432 from your IP
- Your IP may have changed (update security group)

**Update security group with new IP:**
```bash
# Get current security group
SG_ID=$(aws rds describe-db-instances \
  --db-instance-identifier iso-standards-dev \
  --query 'DBInstances[0].VpcSecurityGroups[0].VpcSecurityGroupId' \
  --output text \
  --region ap-southeast-2)

# Get your current IP
MY_IP=$(curl -s https://checkip.amazonaws.com)

# Add new rule
aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --protocol tcp \
  --port 5432 \
  --cidr $MY_IP/32 \
  --region ap-southeast-2
```

**4. Django migrations fail**
- Ensure virtual environment is activated
- Check database name in `.env` matches created database
- Verify extensions are installed (if using pgvector)

## Rollback Plan

If you need to revert to SQLite:

1. **Keep SQLite backup**: Don't delete `db.sqlite3.backup`
2. **Comment out RDS in .env**:
   ```bash
   # DB_NAME=iso_standards
   # DB_USER=postgres
   # DB_PASSWORD=DevPassword123!
   # DB_HOST=your-endpoint
   # DB_PORT=5432
   ```
3. **Update development.py** to use SQLite:
   ```python
   DATABASES = {
       "default": {
           "ENGINE": "django.db.backends.sqlite3",
           "NAME": BASE_DIR / "db.sqlite3",
       }
   }
   ```
4. **Restore SQLite backup**: `cp db.sqlite3.backup db.sqlite3`

## Cost Estimation

### AWS RDS (db.t3.micro) - Development
- **Instance**: ~$12/month (after free tier)
- **Storage** (20GB GP3): ~$2/month
- **Backup** (1-day retention): ~$0.50/month
- **Total**: ~$14.50/month

### Cost Savings Tips
1. **Stop instance when not developing** (saves ~$12/month during stopped periods)
2. **Use smaller storage** if you don't need 20GB
3. **Consider free tier** (750 hours/month for 12 months)

## Timeline

- **Phase 1**: RDS Setup (30-45 minutes)
- **Phase 2**: Extensions Setup (10 minutes)
- **Phase 3**: Django Configuration (20-30 minutes)
- **Phase 4**: Environment Setup (10 minutes)
- **Phase 5**: Install Dependencies (5 minutes)
- **Phase 6**: Database Migration (15-30 minutes)
- **Phase 7**: Testing (15-20 minutes)
- **Phase 8**: Documentation (10 minutes)

**Total Estimated Time**: 2-3 hours

## Success Criteria

- ✅ RDS instance running and accessible
- ✅ Django connects to RDS successfully
- ✅ All migrations applied without errors
- ✅ Extensions installed (uuid-ossp, pg_trgm)
- ✅ Test script passes
- ✅ Development server runs successfully
- ✅ Can stop/start RDS instance via CLI

## Next Steps After Setup

1. Start using RDS for all development work
2. Stop RDS instance when not actively developing
3. Monitor AWS costs in billing console
4. Consider setting up CloudWatch alarms (optional)
5. Plan for production RDS setup when ready

## Cleanup (If You Want to Delete RDS)

To delete the RDS instance and associated resources:

```bash
export AWS_PROFILE=ben-sso

# Delete RDS instance (with final snapshot)
aws rds delete-db-instance \
  --db-instance-identifier iso-standards-dev \
  --final-db-snapshot-identifier iso-standards-dev-final-snapshot \
  --region ap-southeast-2

# Or delete without snapshot
# aws rds delete-db-instance \
#   --db-instance-identifier iso-standards-dev \
#   --skip-final-snapshot \
#   --region ap-southeast-2

# Delete security group (after RDS is deleted)
# aws ec2 delete-security-group \
#   --group-id sg-xxxxx \
#   --region ap-southeast-2
```

## References

- [AWS RDS PostgreSQL Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html)
- [Django PostgreSQL Notes](https://docs.djangoproject.com/en/5.0/ref/databases/#postgresql-notes)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [PostgreSQL 16 Release Notes](https://www.postgresql.org/docs/16/release-16.html)
