# AWS RDS Quick Reference

## Connection Details

- **Instance ID**: iso-standards-dev
- **Database**: iso_standards
- **User**: postgres
- **Password**: DevPassword123!
- **Port**: 5432
- **Region**: ap-southeast-2 (Sydney)
- **Endpoint**: iso-standards-dev.c70q6k8gwnr0.ap-southeast-2.rds.amazonaws.com
- **SSL/TLS**: Required (TLSv1.3, AES-256-GCM encryption)

## Quick Commands

### Get RDS Endpoint

```bash
export AWS_PROFILE=ben-sso
aws rds describe-db-instances \
  --db-instance-identifier iso-standards-dev \
  --query 'DBInstances[0].Endpoint.Address' \
  --output text \
  --region ap-southeast-2
```

### Check RDS Status

```bash
export AWS_PROFILE=ben-sso
aws rds describe-db-instances \
  --db-instance-identifier iso-standards-dev \
  --query 'DBInstances[0].DBInstanceStatus' \
  --region ap-southeast-2
```

### Stop RDS Instance (Save Costs)

```bash
export AWS_PROFILE=ben-sso
aws rds stop-db-instance \
  --db-instance-identifier iso-standards-dev \
  --region ap-southeast-2
```

**Note**: Stopped instances auto-start after 7 days.

### Start RDS Instance

```bash
export AWS_PROFILE=ben-sso
aws rds start-db-instance \
  --db-instance-identifier iso-standards-dev \
  --region ap-southeast-2

# Wait for it to be available
aws rds wait db-instance-available \
  --db-instance-identifier iso-standards-dev \
  --region ap-southeast-2
```

### Connect with psql (SSL Required)

```bash
export RDS_ENDPOINT=iso-standards-dev.c70q6k8gwnr0.ap-southeast-2.rds.amazonaws.com
PGPASSWORD='DevPassword123!' psql "sslmode=require host=$RDS_ENDPOINT user=postgres dbname=iso_standards"
```

### Create Database Snapshot

```bash
export AWS_PROFILE=ben-sso
aws rds create-db-snapshot \
  --db-instance-identifier iso-standards-dev \
  --db-snapshot-identifier iso-standards-dev-$(date +%Y%m%d) \
  --region ap-southeast-2
```

## Daily Development Workflow

### 1. Login to AWS (if session expired)

```bash
aws sso login --profile ben-sso
```

### 2. Start Development

```bash
cd Backend
source .venv/bin/activate  # If not using direnv
python manage.py runserver
```

### 3. When Done (Optional - Save Costs)

```bash
# Stop RDS to save money when not developing
export AWS_PROFILE=ben-sso
aws rds stop-db-instance \
  --db-instance-identifier iso-standards-dev \
  --region ap-southeast-2
```

## Troubleshooting

### Cannot Connect to RDS

**1. Check RDS is running:**

```bash
export AWS_PROFILE=ben-sso
aws rds describe-db-instances \
  --db-instance-identifier iso-standards-dev \
  --query 'DBInstances[0].DBInstanceStatus' \
  --region ap-southeast-2
```

**2. Check your current IP:**

```bash
curl -s https://checkip.amazonaws.com
```

**3. Update security group if IP changed:**

```bash
export AWS_PROFILE=ben-sso
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

- Verify password in `.env` matches: `DevPassword123!`
- Check `DB_HOST` is correct endpoint

### Django Connection Errors

- Ensure `psycopg2-binary` is installed
- Check `.env` file is loaded (direnv should auto-load)
- Verify `DJANGO_ENV=development` in `.env`

## Cost Information

- **Free Tier**: 750 hours/month for 12 months (db.t3.micro)
- **After Free Tier**: ~$14.50/month
  - Instance: $12/month
  - Storage (20GB): $2/month
  - Backup: $0.50/month

**Cost Saving Tip**: Stop RDS when not actively developing to save ~$12/month.

## Security Features

### Encryption

- **At Rest**: AWS KMS encryption enabled
- **In Transit**: SSL/TLS required (TLSv1.3)
- **Cipher**: TLS_AES_256_GCM_SHA384

### Network Security

- **Security Group**: sg-09a3593b4d4e6cc10
- **Allowed IP**: 115.130.93.84/32 (your computer only)
- **Port**: 5432 (PostgreSQL)

### Verify SSL Connection

```bash
cd Backend
python manage.py shell -c "from django.db import connection; connection.ensure_connection(); cursor = connection.cursor(); cursor.execute('SELECT * FROM pg_stat_ssl WHERE pid = pg_backend_pid();'); result = cursor.fetchone(); print(f'SSL Active: {result[1]}'); print(f'Version: {result[2]}'); print(f'Cipher: {result[3]}')"
```

## VS Code Database Plugin Configuration

### SSL Connection Error

If you get this error when connecting via VS Code database plugins:

```text
no pg_hba.conf entry for host "115.130.93.84", user "postgres", database "iso_standards", no encryption
```

**Cause**: RDS requires SSL/TLS encryption, but the plugin is attempting an unencrypted connection.

### Solution: Configure SSL in Database Plugin

**For Database Client/PostgreSQL extensions:**

1. **In connection settings, enable SSL mode:**

   - Set `SSL Mode` to: `require` (or `verify-ca` or `verify-full`)
   - Some plugins have an "SSL" checkbox - enable it
   - Add SSL parameter to connection string

2. **Connection String Format with SSL:**

   ```text
   postgresql://postgres:DevPassword123!@iso-standards-dev.c70q6k8gwnr0.ap-southeast-2.rds.amazonaws.com:5432/iso_standards?sslmode=require
   ```

3. **Individual Connection Parameters:**
   - **Host**: `iso-standards-dev.c70q6k8gwnr0.ap-southeast-2.rds.amazonaws.com`
   - **Port**: `5432`
   - **Database**: `iso_standards`
   - **User**: `postgres`
   - **Password**: `DevPassword123!`
   - **SSL Mode**: `require` ⚠️ **IMPORTANT**
   - **SSL**: Enabled/True

### Recommended VS Code Extensions

- **PostgreSQL** by Chris Kolkman - Has SSL support
- **SQLTools PostgreSQL** - Configure SSL in driver options

### Alternative: Use psql for Quick Queries

```bash
export RDS_ENDPOINT=iso-standards-dev.c70q6k8gwnr0.ap-southeast-2.rds.amazonaws.com
PGPASSWORD='DevPassword123!' psql "sslmode=require host=$RDS_ENDPOINT user=postgres dbname=iso_standards"
```

## Installed Extensions

- `uuid-ossp` - UUID generation
- `pg_trgm` - Text similarity and full-text search
- `vector` - For RAG features (can be added later if needed)

## Security Group

- **ID**: sg-09a3593b4d4e6cc10
- **Allowed IP**: 115.130.93.84/32 (your current IP)
- **Port**: 5432 (PostgreSQL)

## Rollback to Local PostgreSQL

If you need to revert to local development:

1. Comment out RDS settings in `.env`
2. Update to use local PostgreSQL or SQLite
3. Restore from backup if needed

## Delete RDS Instance (If Needed)

```bash
export AWS_PROFILE=ben-sso

# With final snapshot (recommended)
aws rds delete-db-instance \
  --db-instance-identifier iso-standards-dev \
  --final-db-snapshot-identifier iso-standards-dev-final \
  --region ap-southeast-2

# Without snapshot (permanent deletion)
# aws rds delete-db-instance \
#   --db-instance-identifier iso-standards-dev \
#   --skip-final-snapshot \
#   --region ap-southeast-2
```
