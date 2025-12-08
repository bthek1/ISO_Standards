# PostgreSQL with Docker Setup Guide

This guide explains how to set up and use PostgreSQL with Docker for the ISO Standards project.

## Overview

The project now uses PostgreSQL running in Docker for development instead of SQLite. This provides:

- Better match with production environment (AWS RDS uses PostgreSQL)
- Advanced features like full-text search and pgvector for RAG
- Better data integrity and performance
- Persistent data storage across container restarts

## Docker Compose Configuration

The PostgreSQL database is configured in `docker-compose.dev.yml`:

```yaml
version: "3.9"

services:
  db:
    image: postgres:16
    container_name: iso-standards-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: ben
      POSTGRES_PASSWORD: secretpassword
      POSTGRES_DB: iso_standards
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/postgres/init:/docker-entrypoint-initdb.d

volumes:
  postgres_data:
```

### Configuration Details

- **Image**: postgres:16 (latest PostgreSQL 16)
- **Container Name**: iso-standards-postgres
- **Port**: 5432 (standard PostgreSQL port)
- **Database Name**: iso_standards
- **User**: ben
- **Password**: secretpassword (change in production!)
- **Persistent Storage**: Named volume `postgres_data`

## Quick Start

### 1. Install Dependencies

First, ensure psycopg (PostgreSQL adapter) is installed:

```bash
cd Backend
uv pip install psycopg[binary]
# or if not using uv:
pip install psycopg[binary]
```

### 2. Start PostgreSQL Container

```bash
cd Backend
docker compose -f docker-compose.dev.yml up -d
```

This will:
- Download the PostgreSQL 16 image (if not already downloaded)
- Create the `iso-standards-postgres` container
- Create the `iso_standards` database
- Run initialization scripts from `docker/postgres/init/`
- Start the database in the background

### 3. Verify Database is Running

```bash
docker compose -f docker-compose.dev.yml ps
```

You should see the `iso-standards-postgres` container running.

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

Or use the automated setup with environment variables from `.env`.

## Managing the Database

### Start the Database

```bash
docker compose -f docker-compose.dev.yml up -d
```

### Stop the Database

```bash
docker compose -f docker-compose.dev.yml down
```

### Stop and Remove Data (⚠️ Destructive)

```bash
docker compose -f docker-compose.dev.yml down -v
```

**Warning**: This removes the volume and all data!

### View Logs

```bash
docker compose -f docker-compose.dev.yml logs -f db
```

### Access PostgreSQL CLI

```bash
docker exec -it iso-standards-postgres psql -U ben -d iso_standards
```

Common psql commands:
- `\dt` - List all tables
- `\d table_name` - Describe table structure
- `\l` - List all databases
- `\du` - List all users
- `\q` - Quit psql

## Environment Variables

Update your `.env` file with these PostgreSQL settings:

```env
# Database - PostgreSQL (Docker)
DATABASE_URL="postgresql://ben:secretpassword@localhost:5432/iso_standards"
DB_ENGINE="django.db.backends.postgresql"
DB_NAME="iso_standards"
DB_USER="ben"
DB_PASSWORD="secretpassword"
DB_HOST="localhost"
DB_PORT="5432"
```

## Initialization Scripts

Custom SQL scripts can be placed in `Backend/docker/postgres/init/`. These run automatically when the container is first created.

Example `init.sql`:

```sql
-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search
```

**Note**: These scripts only run on first container creation. To re-run:

```bash
docker compose -f docker-compose.dev.yml down -v
docker compose -f docker-compose.dev.yml up -d
```

## Fallback to SQLite

If you need to use SQLite (e.g., Docker issues), update `.env`:

```env
DB_ENGINE="django.db.backends.sqlite3"
```

The development settings automatically handle this fallback.

## Database Backup and Restore

### Backup

```bash
# Using docker exec
docker exec iso-standards-postgres pg_dump -U ben iso_standards > backup.sql

# Using docker compose
docker compose -f docker-compose.dev.yml exec db pg_dump -U ben iso_standards > backup.sql
```

### Restore

```bash
# Drop and recreate database first
docker exec -it iso-standards-postgres psql -U ben -c "DROP DATABASE iso_standards;"
docker exec -it iso-standards-postgres psql -U ben -c "CREATE DATABASE iso_standards;"

# Restore from backup
docker exec -i iso-standards-postgres psql -U ben iso_standards < backup.sql
```

## Connecting with External Tools

You can connect to the database with tools like pgAdmin, DBeaver, or TablePlus:

- **Host**: localhost
- **Port**: 5432
- **Database**: iso_standards
- **User**: ben
- **Password**: secretpassword

## Troubleshooting

### Container Won't Start

Check logs:
```bash
docker compose -f docker-compose.dev.yml logs db
```

### Connection Refused

Ensure the container is running:
```bash
docker compose -f docker-compose.dev.yml ps
```

Check if port 5432 is already in use:
```bash
sudo lsof -i :5432
```

### Permission Issues

If you see "runc permission denied" errors, this is a Docker runtime issue. Try:

1. Restart Docker service:
   ```bash
   sudo systemctl restart docker
   ```

2. Update Docker to latest version

3. Check Docker socket permissions:
   ```bash
   sudo chmod 666 /var/run/docker.sock
   ```

### Data Persistence Issues

The data is stored in a Docker named volume. To verify:

```bash
docker volume ls | grep postgres
docker volume inspect iso_standards_postgres_data
```

### Fresh Start

To completely reset the database:

```bash
# Stop and remove containers and volumes
docker compose -f docker-compose.dev.yml down -v

# Remove any orphaned volumes
docker volume prune

# Start fresh
docker compose -f docker-compose.dev.yml up -d

# Run migrations
python manage.py migrate
```

## Performance Tuning

For development, the default PostgreSQL settings are fine. For production or heavy development:

1. Create `docker/postgres/postgresql.conf`
2. Add custom settings
3. Uncomment the volume mount in `docker-compose.dev.yml`

Example custom settings:

```conf
# Memory
shared_buffers = 256MB
effective_cache_size = 1GB

# Query planning
random_page_cost = 1.1

# Logging
log_min_duration_statement = 1000  # Log slow queries (>1s)
```

## CI/CD Considerations

GitHub Actions already uses PostgreSQL service containers. No changes needed.

## Production Differences

In production (AWS RDS):
- Managed PostgreSQL service (no Docker)
- Different credentials (from AWS Secrets Manager)
- Automated backups
- High availability setup
- Different port mapping

See `config/settings/production.py` for production database settings.

## Next Steps

1. ✅ Install psycopg dependency
2. ✅ Start PostgreSQL container
3. ✅ Update `.env` file
4. ✅ Run migrations
5. ✅ Create superuser
6. Test your application

## Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/16/)
- [Docker PostgreSQL Image](https://hub.docker.com/_/postgres)
- [Django PostgreSQL Notes](https://docs.djangoproject.com/en/5.0/ref/databases/#postgresql-notes)
- [psycopg3 Documentation](https://www.psycopg.org/psycopg3/docs/)
