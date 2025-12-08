-- PostgreSQL initialization script for ISO Standards database
-- This file runs automatically when the container is first created

-- Enable required extensions
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search optimization

-- You can add additional initialization SQL here
-- For example, creating additional databases, roles, or extensions

-- Note: The main database 'iso_standards' is already created by the
-- POSTGRES_DB environment variable in docker-compose.dev.yml
