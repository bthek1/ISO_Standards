"""
Comprehensive tests for Django settings across all environments.

This module tests:
- Base settings common to all environments
- Environment-specific settings (development, test, production)
- Security settings
- Database configurations
- Email configurations
- Static/media file settings
- Third-party app configurations
- Middleware stack
- Template settings
"""

import os
from pathlib import Path

from django.conf import settings


class TestBaseSettings:
    """Test base settings that should be present in all environments."""

    def test_base_dir_exists(self):
        """Verify BASE_DIR is set correctly."""
        assert settings.BASE_DIR.exists()
        assert settings.BASE_DIR.name == "Backend"
        assert isinstance(settings.BASE_DIR, Path)

    def test_base_dir_structure(self):
        """Verify expected directories exist within BASE_DIR."""
        expected_dirs = ["templates", "static", "config", "accounts", "pages"]
        for dir_name in expected_dirs:
            dir_path = settings.BASE_DIR / dir_name
            assert dir_path.exists(), f"Expected directory {dir_name} not found"

    def test_installed_apps_core(self):
        """Verify core Django apps are installed."""
        core_apps = [
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
            "django.contrib.sites",
        ]
        for app in core_apps:
            assert app in settings.INSTALLED_APPS, f"{app} not in INSTALLED_APPS"

    def test_third_party_apps_installed(self):
        """Verify third-party apps are installed."""
        third_party_apps = [
            "allauth",
            "allauth.account",
            "crispy_forms",
            "crispy_bootstrap5",
            "rest_framework",
            "whitenoise.runserver_nostatic",
        ]
        for app in third_party_apps:
            assert app in settings.INSTALLED_APPS, f"{app} not in INSTALLED_APPS"

    def test_custom_apps_installed(self):
        """Verify custom apps are installed."""
        custom_apps = ["accounts", "pages"]
        for app in custom_apps:
            assert app in settings.INSTALLED_APPS, f"{app} not in INSTALLED_APPS"

    def test_middleware_configured(self):
        """Verify essential middleware is present."""
        required_middleware = [
            "django.middleware.security.SecurityMiddleware",
            "whitenoise.middleware.WhiteNoiseMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
            "allauth.account.middleware.AccountMiddleware",
        ]
        for middleware in required_middleware:
            assert middleware in settings.MIDDLEWARE, f"{middleware} not in MIDDLEWARE"

    def test_middleware_order(self):
        """Verify critical middleware ordering."""
        # Security middleware should be first
        assert settings.MIDDLEWARE[0] == "django.middleware.security.SecurityMiddleware"
        # WhiteNoise should be second (after security)
        assert settings.MIDDLEWARE[1] == "whitenoise.middleware.WhiteNoiseMiddleware"
        # Session middleware should come before auth middleware
        session_idx = settings.MIDDLEWARE.index(
            "django.contrib.sessions.middleware.SessionMiddleware"
        )
        auth_idx = settings.MIDDLEWARE.index(
            "django.contrib.auth.middleware.AuthenticationMiddleware"
        )
        assert session_idx < auth_idx

    def test_templates_configured(self):
        """Verify templates are configured."""
        assert len(settings.TEMPLATES) > 0
        assert (
            settings.TEMPLATES[0]["BACKEND"]
            == "django.template.backends.django.DjangoTemplates"
        )
        # Verify template directories
        assert settings.BASE_DIR / "templates" in settings.TEMPLATES[0]["DIRS"]
        # Verify APP_DIRS is enabled
        assert settings.TEMPLATES[0]["APP_DIRS"] is True

    def test_template_context_processors(self):
        """Verify template context processors are configured."""
        required_processors = [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ]
        context_processors = settings.TEMPLATES[0]["OPTIONS"]["context_processors"]
        for processor in required_processors:
            assert processor in context_processors

    def test_static_files_configured(self):
        """Verify static files settings."""
        assert settings.STATIC_URL == "/static/"
        assert settings.STATIC_ROOT == settings.BASE_DIR / "staticfiles"
        assert settings.BASE_DIR / "static" in settings.STATICFILES_DIRS

    def test_static_storage_configured(self):
        """Verify static file storage is configured for WhiteNoise."""
        assert "staticfiles" in settings.STORAGES
        assert (
            settings.STORAGES["staticfiles"]["BACKEND"]
            == "whitenoise.storage.CompressedManifestStaticFilesStorage"
        )

    def test_custom_user_model(self):
        """Verify custom user model is set."""
        assert settings.AUTH_USER_MODEL == "accounts.CustomUser"

    def test_root_urlconf(self):
        """Verify ROOT_URLCONF is set."""
        assert settings.ROOT_URLCONF == "config.urls"

    def test_wsgi_application(self):
        """Verify WSGI application is set."""
        assert settings.WSGI_APPLICATION == "config.wsgi.application"

    def test_password_validators_configured(self):
        """Verify password validators are configured."""
        assert len(settings.AUTH_PASSWORD_VALIDATORS) == 4
        validator_names = [
            "UserAttributeSimilarityValidator",
            "MinimumLengthValidator",
            "CommonPasswordValidator",
            "NumericPasswordValidator",
        ]
        configured_validators = [
            v["NAME"].split(".")[-1] for v in settings.AUTH_PASSWORD_VALIDATORS
        ]
        for validator in validator_names:
            assert validator in configured_validators

    def test_internationalization_settings(self):
        """Verify internationalization settings."""
        assert settings.LANGUAGE_CODE == "en-us"
        assert settings.TIME_ZONE == "UTC"
        assert settings.USE_I18N is True
        assert settings.USE_TZ is True
        assert settings.BASE_DIR / "locale" in settings.LOCALE_PATHS

    def test_default_auto_field(self):
        """Verify default auto field is configured."""
        assert settings.DEFAULT_AUTO_FIELD == "django.db.models.BigAutoField"

    def test_crispy_forms_configured(self):
        """Verify crispy forms configuration."""
        assert settings.CRISPY_TEMPLATE_PACK == "bootstrap5"
        assert "bootstrap5" in settings.CRISPY_ALLOWED_TEMPLATE_PACKS

    def test_allauth_configuration(self):
        """Verify django-allauth configuration."""
        assert settings.SITE_ID == 1
        assert settings.LOGIN_REDIRECT_URL == "home"
        assert settings.ACCOUNT_LOGOUT_REDIRECT_URL == "home"
        assert settings.ACCOUNT_SESSION_REMEMBER is True
        assert settings.ACCOUNT_UNIQUE_EMAIL is True
        assert settings.ACCOUNT_USER_MODEL_USERNAME_FIELD is None
        assert {"email"} == settings.ACCOUNT_LOGIN_METHODS
        expected_signup_fields = ["email*", "password1*"]
        assert expected_signup_fields == settings.ACCOUNT_SIGNUP_FIELDS

    def test_authentication_backends(self):
        """Verify authentication backends are configured."""
        required_backends = [
            "django.contrib.auth.backends.ModelBackend",
            "allauth.account.auth_backends.AuthenticationBackend",
        ]
        for backend in required_backends:
            assert backend in settings.AUTHENTICATION_BACKENDS

    def test_rest_framework_configured(self):
        """Verify REST framework configuration."""
        assert "DEFAULT_AUTHENTICATION_CLASSES" in settings.REST_FRAMEWORK
        assert "DEFAULT_PERMISSION_CLASSES" in settings.REST_FRAMEWORK
        auth_classes = settings.REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"]
        assert "rest_framework.authentication.SessionAuthentication" in auth_classes
        assert "rest_framework.authentication.TokenAuthentication" in auth_classes
        perm_classes = settings.REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"]
        assert "rest_framework.permissions.IsAuthenticated" in perm_classes

    def test_secret_key_configured(self):
        """Verify secret key is set."""
        assert hasattr(settings, "SECRET_KEY")
        assert settings.SECRET_KEY is not None
        assert len(settings.SECRET_KEY) > 10


class TestDevelopmentSettings:
    """Test development-specific settings."""

    def test_debug_enabled(self):
        """Debug should be enabled in development."""
        # This test assumes DJANGO_ENV=development
        if os.environ.get("DJANGO_ENV") == "development":
            assert settings.DEBUG is True

    def test_allowed_hosts(self):
        """Allowed hosts should include localhost in development."""
        if os.environ.get("DJANGO_ENV") == "development":
            assert "localhost" in settings.ALLOWED_HOSTS
            assert "127.0.0.1" in settings.ALLOWED_HOSTS

    def test_database_is_sqlite(self):
        """Development should use SQLite."""
        if os.environ.get("DJANGO_ENV") == "development":
            assert (
                settings.DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3"
            )
            expected_db_path = settings.BASE_DIR / "db.sqlite3"
            assert settings.DATABASES["default"]["NAME"] == expected_db_path

    def test_email_backend_console(self):
        """Development should use console email backend."""
        if os.environ.get("DJANGO_ENV") == "development":
            assert (
                settings.EMAIL_BACKEND
                == "django.core.mail.backends.console.EmailBackend"
            )

    def test_development_apps_installed(self):
        """Development should have debug apps installed."""
        if os.environ.get("DJANGO_ENV") == "development":
            assert "debug_toolbar" in settings.INSTALLED_APPS
            assert "django_extensions" in settings.INSTALLED_APPS

    def test_debug_toolbar_middleware(self):
        """Debug toolbar middleware should be present in development."""
        if os.environ.get("DJANGO_ENV") == "development":
            debug_middleware = "debug_toolbar.middleware.DebugToolbarMiddleware"
            assert debug_middleware in settings.MIDDLEWARE

    def test_internal_ips_configured(self):
        """Internal IPs should be configured in development."""
        if os.environ.get("DJANGO_ENV") == "development":
            assert hasattr(settings, "INTERNAL_IPS")
            assert "127.0.0.1" in settings.INTERNAL_IPS


class TestTestSettings:
    """Test test-environment-specific settings."""

    def test_debug_disabled(self):
        """Debug should be disabled in test environment."""
        if os.environ.get("DJANGO_ENV") == "test":
            assert settings.DEBUG is False

    def test_testing_flag(self):
        """TESTING flag should be set in test environment."""
        if os.environ.get("DJANGO_ENV") == "test":
            assert hasattr(settings, "TESTING")
            assert settings.TESTING is True

    def test_database_in_memory(self):
        """Test environment should use in-memory database."""
        if os.environ.get("DJANGO_ENV") == "test":
            assert settings.DATABASES["default"]["NAME"] == ":memory:"
            assert (
                settings.DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3"
            )

    def test_email_backend_memory(self):
        """Test environment should use memory email backend."""
        if os.environ.get("DJANGO_ENV") == "test":
            assert (
                settings.EMAIL_BACKEND
                == "django.core.mail.backends.locmem.EmailBackend"
            )

    def test_password_hashers_simplified(self):
        """Test environment should use simplified password hashers."""
        if os.environ.get("DJANGO_ENV") == "test":
            md5_hasher = "django.contrib.auth.hashers.MD5PasswordHasher"
            assert md5_hasher in settings.PASSWORD_HASHERS


class TestProductionSettings:
    """Test production-specific settings."""

    def test_debug_disabled(self):
        """Debug must be disabled in production."""
        if os.environ.get("DJANGO_ENV") == "production":
            assert settings.DEBUG is False

    def test_secret_key_from_env(self):
        """Secret key must come from environment in production."""
        if os.environ.get("DJANGO_ENV") == "production":
            # Should raise error if SECRET_KEY not in environment
            fallback_key = "django-insecure-fallback-key-for-development-only"
            has_env_key = "SECRET_KEY" in os.environ
            not_fallback = fallback_key != settings.SECRET_KEY
            assert has_env_key or not_fallback

    def test_allowed_hosts_configured(self):
        """Allowed hosts must be configured in production."""
        if os.environ.get("DJANGO_ENV") == "production":
            assert len(settings.ALLOWED_HOSTS) > 0
            # Should not contain localhost only
            assert settings.ALLOWED_HOSTS != ["localhost"]

    def test_security_settings(self):
        """Verify security settings in production."""
        if os.environ.get("DJANGO_ENV") == "production":
            assert settings.SESSION_COOKIE_SECURE is True
            assert settings.CSRF_COOKIE_SECURE is True
            assert settings.SECURE_BROWSER_XSS_FILTER is True
            assert settings.SECURE_CONTENT_TYPE_NOSNIFF is True
            assert settings.X_FRAME_OPTIONS == "DENY"

    def test_hsts_settings(self):
        """Verify HSTS settings are available in production."""
        if os.environ.get("DJANGO_ENV") == "production":
            assert hasattr(settings, "SECURE_HSTS_SECONDS")
            assert hasattr(settings, "SECURE_HSTS_INCLUDE_SUBDOMAINS")
            assert hasattr(settings, "SECURE_HSTS_PRELOAD")

    def test_database_postgresql(self):
        """Production should use PostgreSQL."""
        if os.environ.get("DJANGO_ENV") == "production":
            db_engine = settings.DATABASES["default"]["ENGINE"]
            assert "postgresql" in db_engine or "postgres" in db_engine

    def test_database_credentials_from_env(self):
        """Database credentials should come from environment."""
        if os.environ.get("DJANGO_ENV") == "production":
            db_config = settings.DATABASES["default"]
            assert "NAME" in db_config
            assert "USER" in db_config
            assert "HOST" in db_config
            assert "PORT" in db_config

    def test_email_backend_smtp(self):
        """Production should use SMTP email backend."""
        if os.environ.get("DJANGO_ENV") == "production":
            assert (
                settings.EMAIL_BACKEND == "django.core.mail.backends.smtp.EmailBackend"
            )

    def test_email_configuration(self):
        """Verify email configuration in production."""
        if os.environ.get("DJANGO_ENV") == "production":
            assert hasattr(settings, "EMAIL_HOST")
            assert hasattr(settings, "EMAIL_PORT")
            assert hasattr(settings, "EMAIL_USE_TLS")

    def test_logging_configured(self):
        """Verify logging is configured in production."""
        if os.environ.get("DJANGO_ENV") == "production":
            assert hasattr(settings, "LOGGING")
            assert "version" in settings.LOGGING
            assert "handlers" in settings.LOGGING
            assert "loggers" in settings.LOGGING


class TestEnvironmentVariables:
    """Test environment variable loading."""

    def test_secret_key_exists(self):
        """Secret key should always be set."""
        assert settings.SECRET_KEY is not None
        assert len(settings.SECRET_KEY) > 10

    def test_allowed_hosts_configured(self):
        """Allowed hosts should be configured."""
        assert isinstance(settings.ALLOWED_HOSTS, list)
        assert len(settings.ALLOWED_HOSTS) > 0

    def test_debug_from_env(self):
        """DEBUG setting should respect environment variable."""
        debug_env = os.environ.get("DEBUG", "False")
        expected_debug = debug_env == "True"
        # Only test if not overridden by environment-specific settings
        if os.environ.get("DJANGO_ENV") not in ["development", "test", "production"]:
            assert expected_debug == settings.DEBUG

    def test_default_from_email(self):
        """DEFAULT_FROM_EMAIL should be configured."""
        assert hasattr(settings, "DEFAULT_FROM_EMAIL")
        assert settings.DEFAULT_FROM_EMAIL is not None


class TestDatabaseConfiguration:
    """Test database configuration."""

    def test_database_exists(self):
        """Verify default database is configured."""
        assert "default" in settings.DATABASES
        assert "ENGINE" in settings.DATABASES["default"]

    def test_database_engine_valid(self):
        """Verify database engine is valid."""
        engine = settings.DATABASES["default"]["ENGINE"]
        valid_engines = [
            "django.db.backends.sqlite3",
            "django.db.backends.postgresql",
            "django.db.backends.mysql",
        ]
        assert any(valid_engine in engine for valid_engine in valid_engines)


class TestStaticAndMediaFiles:
    """Test static and media file configuration."""

    def test_static_url_set(self):
        """Verify STATIC_URL is set."""
        assert settings.STATIC_URL == "/static/"

    def test_static_root_set(self):
        """Verify STATIC_ROOT is set."""
        assert settings.STATIC_ROOT == settings.BASE_DIR / "staticfiles"

    def test_staticfiles_dirs_configured(self):
        """Verify STATICFILES_DIRS is configured."""
        assert len(settings.STATICFILES_DIRS) > 0
        assert settings.BASE_DIR / "static" in settings.STATICFILES_DIRS

    def test_storages_configured(self):
        """Verify STORAGES setting is configured."""
        assert "default" in settings.STORAGES
        assert "staticfiles" in settings.STORAGES

    def test_whitenoise_storage(self):
        """Verify WhiteNoise storage backend."""
        staticfiles_storage = settings.STORAGES["staticfiles"]["BACKEND"]
        assert "whitenoise" in staticfiles_storage.lower()


class TestSecuritySettings:
    """Test security-related settings."""

    def test_secret_key_length(self):
        """Secret key should be sufficiently long."""
        # Django's default key length is 50, but fallback dev key is 49
        # In production, should be 50+, in dev/test 40+ is acceptable
        min_length = 50 if os.environ.get("DJANGO_ENV") == "production" else 40
        assert len(settings.SECRET_KEY) >= min_length

    def test_secret_key_not_default_in_prod(self):
        """Secret key should not be default in production."""
        if os.environ.get("DJANGO_ENV") == "production":
            assert "django-insecure" not in settings.SECRET_KEY

    def test_allowed_hosts_not_empty(self):
        """ALLOWED_HOSTS should not be empty."""
        assert len(settings.ALLOWED_HOSTS) > 0

    def test_csrf_protection_enabled(self):
        """CSRF middleware should be enabled."""
        assert "django.middleware.csrf.CsrfViewMiddleware" in settings.MIDDLEWARE

    def test_xframe_options(self):
        """X-Frame-Options should be set in production."""
        if os.environ.get("DJANGO_ENV") == "production":
            assert hasattr(settings, "X_FRAME_OPTIONS")
            assert settings.X_FRAME_OPTIONS in ["DENY", "SAMEORIGIN"]


class TestLoggingConfiguration:
    """Test logging configuration."""

    def test_logging_exists(self):
        """Verify logging configuration exists in production."""
        if os.environ.get("DJANGO_ENV") == "production":
            assert hasattr(settings, "LOGGING")

    def test_logging_structure(self):
        """Verify logging configuration structure."""
        if os.environ.get("DJANGO_ENV") == "production":
            assert "version" in settings.LOGGING
            assert settings.LOGGING["version"] == 1
            assert "handlers" in settings.LOGGING
            assert "loggers" in settings.LOGGING
            assert "formatters" in settings.LOGGING

    def test_console_handler(self):
        """Verify console handler is configured."""
        if os.environ.get("DJANGO_ENV") == "production":
            assert "console" in settings.LOGGING["handlers"]

    def test_django_logger(self):
        """Verify Django logger is configured."""
        if os.environ.get("DJANGO_ENV") == "production":
            assert "django" in settings.LOGGING["loggers"]
