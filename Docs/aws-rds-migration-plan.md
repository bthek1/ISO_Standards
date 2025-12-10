# AWS RDS PostgreSQL Setup for Development

## Overview

This guide sets up AWS RDS PostgreSQL for development, replacing SQLite. The database will be accessible from your local computer for Django development.

## Prerequisites

- AWS SSO configured with `ben-sso` profile
- PostgreSQL client installed (`psql`)
- Python 3.13 with Django 5.2+

## Goals

1. Create AWS RDS PostgreSQL instance for development
2. Configure security group for local computer access
3. Update Django settings and environment variables
4. Connect and verify database access

## Step 1: AWS RDS Instance Setup

### 1.1 Login to AWS

```bash
aws sso login --profile ben-sso
export AWS_PROFILE=ben-sso
```

### 1.2 Get Your Public IP

```bash
MY_IP=$(curl -s https://checkip.amazonaws.com)
echo "Your IP: $MY_IP"
```

### 1.3 Create Security Group

```bash
# Get default VPC
VPC_ID=$(aws ec2 describe-vpcs \
  --filters "Name=isDefault,Values=true" \
  --query 'Vpcs[0].VpcId' \
  --output text \
  --region ap-southeast-2)

# Create security group
SG_ID=$(aws ec2 create-security-group \
  --group-name iso-standards-dev-rds-sg \
  --description "Security group for ISO Standards Development RDS" \
  --vpc-id $VPC_ID \
  --region ap-southeast-2 \
  --output text \
  --query 'GroupId')

# Allow PostgreSQL access from your IP
aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --protocol tcp \
  --port 5432 \
  --cidr $MY_IP/32 \
  --region ap-southeast-2

echo "Security Group: $SG_ID"
```

### 1.4 Create RDS Instance

```bash
aws rds create-db-instance \
  --db-instance-identifier iso-standards-dev \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 16.11 \
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

echo "Creating RDS instance... (5-10 minutes)"

# Wait for instance
aws rds wait db-instance-available \
  --db-instance-identifier iso-standards-dev \
  --region ap-southeast-2

# Get endpoint
RDS_ENDPOINT=$(aws rds describe-db-instances \
  --db-instance-identifier iso-standards-dev \
  --query 'DBInstances[0].Endpoint.Address' \
  --output text \
  --region ap-southeast-2)

echo "✓ RDS Ready!"
echo "Endpoint: $RDS_ENDPOINT"
```

**Instance Details:**

- Engine: PostgreSQL 16.11
- Class: db.t3.micro (free tier eligible)
- Storage: 20GB GP3
- Region: ap-southeast-2 (Sydney)
- Public access: Yes
- Cost: ~$14.50/month (free tier: 750 hours/month for 12 months)

## Step 2: Create Database and Extensions

### 2.1 Connect and Create Database

```bash
# Test connection
psql -h $RDS_ENDPOINT -U postgres -c "SELECT version();"

# Create database
psql -h $RDS_ENDPOINT -U postgres -c "CREATE DATABASE iso_standards;"
```

### 2.2 Install Extensions

```bash
# Connect to database
psql -h $RDS_ENDPOINT -U postgres -d iso_standards

# In psql, run:
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "vector";  -- For RAG features

# Verify
\dx

# Exit
\q
```

**Note**: If `vector` extension fails, skip it for now. It's only needed for RAG features.

## Step 3: Django Configuration

### 3.1 Install PostgreSQL Adapter

```bash
cd Backend
source .venv/bin/activate
pip install psycopg2-binary
```

### 3.2 Update Environment Variables

Create/update `Backend/.env`:

```bash
# Environment
DJANGO_ENV=development
DEBUG=True
SECRET_KEY=your-secret-key-here

# AWS RDS PostgreSQL (with SSL encryption)
DB_NAME=iso_standards
DB_USER=postgres
DB_PASSWORD=DevPassword123!
DB_HOST=your-rds-endpoint.ap-southeast-2.rds.amazonaws.com
DB_PORT=5432
DATABASE_URL=postgresql://postgres:DevPassword123!@your-rds-endpoint.ap-southeast-2.rds.amazonaws.com:5432/iso_standards?sslmode=require

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1
```

Replace `DB_HOST` and the endpoint in `DATABASE_URL` with your actual RDS endpoint.

**Note**: The `?sslmode=require` parameter ensures all connections are encrypted with SSL/TLS.

### 3.3 Update Django Settings

Verify `Backend/config/settings/development.py` has:

```python
from .base import *
import os

DEBUG = True
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "iso_standards"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "CONN_MAX_AGE": 0,
        "OPTIONS": {
            "connect_timeout": 10,
            "sslmode": "require",  # Enforce SSL/TLS encryption
        },
    }
}
```

**Security Note**: The `sslmode: require` option ensures all database connections are encrypted using SSL/TLS (TLSv1.3 with AES-256-GCM).

## Step 4: Migrate Database

### 4.1 Backup SQLite (if needed)

```bash
cd Backend

# Backup existing data
cp db.sqlite3 db.sqlite3.backup

# Export data
python manage.py dumpdata \
  --exclude auth.permission \
  --exclude contenttypes \
  --exclude sessions \
  --indent 2 \
  > data_backup.json
```

### 4.2 Run Migrations

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Import old data (optional)
# python manage.py loaddata data_backup.json
```

### 4.3 Verify

```bash
# Test Django shell
python manage.py shell
```

```python
from accounts.models import CustomUser
print(f"Users: {CustomUser.objects.count()}")
```

## Step 5: Daily Workflow

### Start Development

```bash
# Login to AWS (if session expired)
aws sso login --profile ben-sso

# Navigate to Backend
cd Backend
source .venv/bin/activate

# Start server
python manage.py runserver
```

### Connect to Database

```bash
# Get endpoint
export AWS_PROFILE=ben-sso
RDS_ENDPOINT=$(aws rds describe-db-instances \
  --db-instance-identifier iso-standards-dev \
  --query 'DBInstances[0].Endpoint.Address' \
  --output text \
  --region ap-southeast-2)

# Connect with psql
psql -h $RDS_ENDPOINT -U postgres -d iso_standards
```

### Stop RDS (Save Costs)

```bash
# Stop instance when not developing
aws rds stop-db-instance \
  --db-instance-identifier iso-standards-dev \
  --region ap-southeast-2
```

### Start RDS

```bash
# Start instance
aws rds start-db-instance \
  --db-instance-identifier iso-standards-dev \
  --region ap-southeast-2

# Wait until available
aws rds wait db-instance-available \
  --db-instance-identifier iso-standards-dev \
  --region ap-southeast-2
```

## Troubleshooting

### Cannot Connect to RDS

**Issue**: Connection timeout or refused

**Solutions**:

1. Check RDS is running:

   ```bash
   aws rds describe-db-instances \
     --db-instance-identifier iso-standards-dev \
     --query 'DBInstances[0].DBInstanceStatus' \
     --region ap-southeast-2
   ```

2. Verify your IP hasn't changed:

   ```bash
   curl -s https://checkip.amazonaws.com
   ```

3. Update security group with new IP:

   ```bash
   MY_IP=$(curl -s https://checkip.amazonaws.com)
   SG_ID=$(aws rds describe-db-instances \
     --db-instance-identifier iso-standards-dev \
     --query 'DBInstances[0].VpcSecurityGroups[0].VpcSecurityGroupId' \
     --output text \
     --region ap-southeast-2)

   aws ec2 authorize-security-group-ingress \
     --group-id $SG_ID \
     --protocol tcp \
     --port 5432 \
     --cidr $MY_IP/32 \
     --region ap-southeast-2
   ```

### Password Authentication Failed

Check `.env` file has correct password: `DevPassword123!`

### Django Migration Errors

Ensure `psycopg2-binary` is installed:

```bash
pip install psycopg2-binary
```

## Quick Reference

### RDS Instance Details

- **Identifier**: iso-standards-dev
- **Database**: iso_standards
- **User**: postgres
- **Password**: DevPassword123!
- **Port**: 5432
- **Region**: ap-southeast-2

### Common Commands

```bash
# Get RDS endpoint
aws rds describe-db-instances \
  --db-instance-identifier iso-standards-dev \
  --query 'DBInstances[0].Endpoint.Address' \
  --output text \
  --region ap-southeast-2

# Check RDS status
aws rds describe-db-instances \
  --db-instance-identifier iso-standards-dev \
  --query 'DBInstances[0].DBInstanceStatus' \
  --region ap-southeast-2

# Create snapshot
aws rds create-db-snapshot \
  --db-instance-identifier iso-standards-dev \
  --db-snapshot-identifier iso-standards-dev-$(date +%Y%m%d) \
  --region ap-southeast-2

# Delete RDS (with final snapshot)
aws rds delete-db-instance \
  --db-instance-identifier iso-standards-dev \
  --final-db-snapshot-identifier iso-standards-dev-final \
  --region ap-southeast-2
```

## Cost Management

- **Free Tier**: 750 hours/month for 12 months
- **Monthly Cost** (after free tier): ~$14.50
  - Instance (db.t3.micro): $12/month
  - Storage (20GB): $2/month
  - Backup: $0.50/month

**Cost Saving**: Stop RDS when not developing (saves ~$12/month during stopped periods)

## Rollback to SQLite

If you need to revert:

1. Comment out RDS variables in `.env`:

   ```bash
   # DB_NAME=iso_standards
   # DB_USER=postgres
   # DB_PASSWORD=DevPassword123!
   # DB_HOST=...
   ```

2. Update `development.py`:

   ```python
   DATABASES = {
       "default": {
           "ENGINE": "django.db.backends.sqlite3",
           "NAME": BASE_DIR / "db.sqlite3",
       }
   }
   ```

3. Restore backup: `cp db.sqlite3.backup db.sqlite3`
