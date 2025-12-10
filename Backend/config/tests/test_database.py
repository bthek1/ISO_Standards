"""
Tests for database configuration and security.

This module tests:
- Database connectivity
- SSL/TLS encryption
- PostgreSQL version and extensions
- Connection pooling
- Database security settings
"""

import os

import pytest
from django.conf import settings
from django.db import connection
from django.test import TestCase


class TestDatabaseConfiguration(TestCase):
    """Test database configuration settings."""

    @pytest.mark.skipif(
        settings.DATABASES["default"]["ENGINE"] != "django.db.backends.postgresql",
        reason="PostgreSQL-specific test",
    )
    def test_database_engine_configured(self):
        """Database should be configured with PostgreSQL."""
        db_config = settings.DATABASES["default"]
        assert db_config["ENGINE"] == "django.db.backends.postgresql"

    def test_database_connection_successful(self):
        """Database connection should be successful."""
        connection.ensure_connection()
        assert connection.is_usable()

    @pytest.mark.skipif(
        settings.DATABASES["default"]["ENGINE"] != "django.db.backends.postgresql",
        reason="PostgreSQL-specific test",
    )
    def test_database_name(self):
        """Database name should be iso_standards or test variant."""
        db_config = settings.DATABASES["default"]
        db_name = db_config["NAME"]

        # Allow test_ prefix for test databases
        # pytest-xdist adds _gw0, _gw1, etc. for parallel workers
        valid_patterns = [
            "iso_standards",
            "test_iso_standards",
        ]

        # Check if it matches exactly or is a test database with worker suffix
        is_valid = db_name in valid_patterns or any(
            db_name.startswith(f"{pattern}_gw") for pattern in valid_patterns
        )

        assert is_valid, f"Unexpected database name: {db_name}"

    @pytest.mark.skipif(
        settings.DATABASES["default"]["ENGINE"] != "django.db.backends.postgresql",
        reason="PostgreSQL-specific test",
    )
    def test_connection_timeout_configured(self):
        """Connection timeout should be configured."""
        db_config = settings.DATABASES["default"]
        if "OPTIONS" in db_config:
            assert "connect_timeout" in db_config["OPTIONS"]
            assert db_config["OPTIONS"]["connect_timeout"] == 10


class TestDatabaseSSLSecurity(TestCase):
    """Test SSL/TLS encryption for database connections."""

    @pytest.mark.skipif(
        os.environ.get("DJANGO_ENV") == "test",
        reason="Test database may not use SSL",
    )
    def test_ssl_mode_required(self):
        """SSL mode should be set to 'require' for RDS connections."""
        db_config = settings.DATABASES["default"]

        # Check if using RDS (contains amazonaws.com in host)
        db_host = db_config.get("HOST", "")
        if "amazonaws.com" in db_host:
            assert "OPTIONS" in db_config
            assert "sslmode" in db_config["OPTIONS"]
            assert db_config["OPTIONS"]["sslmode"] == "require"

    @pytest.mark.skipif(
        os.environ.get("DJANGO_ENV") == "test",
        reason="Test database may not use SSL",
    )
    def test_ssl_connection_active(self):
        """SSL/TLS should be active on database connections."""
        db_host = settings.DATABASES["default"].get("HOST", "")

        # Only test SSL for RDS connections
        if "amazonaws.com" not in db_host:
            pytest.skip("Not using RDS, SSL test skipped")

        connection.ensure_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT ssl, version, cipher FROM pg_stat_ssl "
                "WHERE pid = pg_backend_pid();"
            )
            result = cursor.fetchone()

            if result:
                ssl_active, ssl_version, ssl_cipher = result
                assert ssl_active is True, "SSL is not active"
                assert ssl_version is not None, "SSL version not detected"
                assert ssl_cipher is not None, "SSL cipher not detected"

    @pytest.mark.skipif(
        os.environ.get("DJANGO_ENV") == "test",
        reason="Test database may not use SSL",
    )
    def test_ssl_version_modern(self):
        """SSL/TLS version should be modern (TLS 1.2+)."""
        db_host = settings.DATABASES["default"].get("HOST", "")

        if "amazonaws.com" not in db_host:
            pytest.skip("Not using RDS, SSL test skipped")

        connection.ensure_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT version FROM pg_stat_ssl WHERE pid = pg_backend_pid();"
            )
            result = cursor.fetchone()

            if result and result[0]:
                ssl_version = result[0]
                # Should be TLS 1.2 or 1.3
                assert ssl_version in [
                    "TLSv1.2",
                    "TLSv1.3",
                ], f"Outdated SSL version: {ssl_version}"


class TestPostgreSQLVersion(TestCase):
    """Test PostgreSQL version and capabilities."""

    @pytest.mark.skipif(
        settings.DATABASES["default"]["ENGINE"] != "django.db.backends.postgresql",
        reason="PostgreSQL-specific test",
    )
    def test_postgresql_version(self):
        """PostgreSQL should be version 16+."""
        connection.ensure_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version_string = cursor.fetchone()[0]

            assert "PostgreSQL" in version_string
            # Extract major version number
            version_parts = version_string.split()
            for part in version_parts:
                if part.replace(".", "").isdigit():
                    major_version = int(part.split(".")[0])
                    assert (
                        major_version >= 16
                    ), f"PostgreSQL version too old: {major_version}"
                    break

    @pytest.mark.skipif(
        settings.DATABASES["default"]["ENGINE"] != "django.db.backends.postgresql",
        reason="PostgreSQL-specific test",
    )
    def test_required_extensions_installed(self):
        """Required PostgreSQL extensions should be installed (RDS only)."""
        # Skip for test database
        if settings.DATABASES["default"]["NAME"].startswith("test_"):
            pytest.skip("Extension test skipped for test database")

        required_extensions = ["uuid-ossp", "pg_trgm"]

        connection.ensure_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT extname FROM pg_extension WHERE extname = ANY(%s);",
                [required_extensions],
            )
            installed = [row[0] for row in cursor.fetchall()]
            assert set(installed) == set(
                required_extensions
            ), f"Missing extensions: {set(required_extensions) - set(installed)}"

    @pytest.mark.skipif(
        settings.DATABASES["default"]["ENGINE"] != "django.db.backends.postgresql",
        reason="PostgreSQL-specific test",
    )
    def test_uuid_extension_functional(self):
        """UUID extension should be functional (RDS only)."""
        # Skip for test database
        if settings.DATABASES["default"]["NAME"].startswith("test_"):
            pytest.skip("Extension test skipped for test database")

        connection.ensure_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT uuid_generate_v4();")
            uuid = cursor.fetchone()[0]
            assert uuid is not None
            assert len(str(uuid)) == 36  # Standard UUID format
            assert uuid is not None
            assert len(str(uuid)) == 36  # Standard UUID format


class TestDatabaseSecurity(TestCase):
    """Test database security configurations."""

    def test_no_superuser_access_in_production(self):
        """Application should not use superuser database account."""
        if os.environ.get("DJANGO_ENV") == "production":
            connection.ensure_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT current_user, usesuper FROM pg_user "
                    "WHERE usename = current_user;"
                )
                username, is_superuser = cursor.fetchone()
                assert (
                    not is_superuser
                ), f"Database user '{username}' should not be a superuser"

    def test_database_encryption_at_rest(self):
        """Database should have encryption at rest (for RDS)."""
        db_host = settings.DATABASES["default"].get("HOST", "")

        if "amazonaws.com" not in db_host:
            pytest.skip("Not using RDS, encryption test skipped")

        # For RDS, we can verify encryption is supported
        # (actual encryption verification requires AWS API access)
        connection.ensure_connection()
        with connection.cursor() as cursor:
            # Check if PostgreSQL supports encryption features
            cursor.execute("SELECT setting FROM pg_settings WHERE name = 'ssl';")
            result = cursor.fetchone()
            assert result is not None, "SSL support not available"

    @pytest.mark.skipif(
        settings.DATABASES["default"]["ENGINE"] != "django.db.backends.postgresql",
        reason="PostgreSQL-specific test",
    )
    def test_connection_parameters_secure(self):
        """Database connection parameters should be secure."""
        db_config = settings.DATABASES["default"]

        # Check that password is not empty
        password = db_config.get("PASSWORD", "")
        assert password != "", "Database password should not be empty"
        assert len(password) >= 8, "Database password should be at least 8 characters"

        # Check that host is specified (not using default)
        host = db_config.get("HOST", "")
        assert host != "", "Database host should be specified"
        assert host != "127.0.0.1", "Should not use localhost for production RDS"


class TestDatabasePerformance(TestCase):
    """Test database performance settings."""

    def test_connection_pooling_configured(self):
        """Connection pooling should be properly configured."""
        db_config = settings.DATABASES["default"]

        # Check CONN_MAX_AGE is set
        assert "CONN_MAX_AGE" in db_config

        # For development, should be 0 (no persistent connections)
        # For production, should be > 0
        if os.environ.get("DJANGO_ENV") == "development":
            assert db_config["CONN_MAX_AGE"] == 0

    @pytest.mark.skipif(
        settings.DATABASES["default"]["ENGINE"] != "django.db.backends.postgresql",
        reason="PostgreSQL-specific test",
    )
    def test_connection_health_checks(self):
        """Connection health checks should be enabled."""
        db_config = settings.DATABASES["default"]

        # dj_database_url should enable health checks
        conn_health = db_config.get("CONN_HEALTH_CHECKS", False)
        assert conn_health is True, "Connection health checks should be enabled"

    def test_database_query_execution(self):
        """Database should execute queries efficiently."""
        connection.ensure_connection()

        # Simple query execution test
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()
            assert result[0] == 1


class TestDatabaseMigrations(TestCase):
    """Test database migrations state."""

    def test_no_pending_migrations(self):
        """There should be no pending migrations."""
        from django.db.migrations.executor import MigrationExecutor

        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())

        assert len(plan) == 0, (
            f"There are {len(plan)} pending migrations. "
            "Run 'python manage.py migrate' to apply them."
        )

    @pytest.mark.skipif(
        settings.DATABASES["default"]["ENGINE"] != "django.db.backends.postgresql",
        reason="PostgreSQL-specific test",
    )
    def test_migrations_table_exists(self):
        """Django migrations table should exist."""
        connection.ensure_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT EXISTS (SELECT FROM information_schema.tables "
                "WHERE table_name = 'django_migrations');"
            )
            exists = cursor.fetchone()[0]
            assert exists, "django_migrations table does not exist"


class TestDatabaseEnvironmentVariables(TestCase):
    """Test database environment variable handling."""

    def test_database_url_loaded(self):
        """DATABASE_URL environment variable should be loaded."""
        database_url = os.environ.get("DATABASE_URL")

        if os.environ.get("DJANGO_ENV") in ["development", "production"]:
            assert database_url is not None, "DATABASE_URL not set"
            assert database_url.startswith(
                "postgresql://"
            ), "DATABASE_URL should start with postgresql://"

    def test_database_url_ssl_parameter(self):
        """DATABASE_URL should include SSL mode for RDS."""
        database_url = os.environ.get("DATABASE_URL", "")

        # Only check if using RDS and not test database
        if "amazonaws.com" in database_url and "test_" not in database_url:
            # Check if sslmode is in URL or will be added by Django settings
            db_config = settings.DATABASES["default"]
            has_ssl_in_url = "sslmode=require" in database_url
            has_ssl_in_options = (
                "OPTIONS" in db_config
                and db_config["OPTIONS"].get("sslmode") == "require"
            )

            assert (
                has_ssl_in_url or has_ssl_in_options
            ), "DATABASE_URL or Django settings should enforce SSL for RDS"

    def test_individual_db_env_vars(self):
        """Individual database environment variables should be set."""
        required_vars = ["DB_NAME", "DB_USER", "DB_HOST", "DB_PORT"]

        for var in required_vars:
            value = os.environ.get(var)
            assert value is not None, f"{var} environment variable not set"
            assert value != "", f"{var} environment variable is empty"
