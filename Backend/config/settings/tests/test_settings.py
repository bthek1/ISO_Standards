import os

from django.conf import settings


class TestBaseSettings:
    """Test base settings that should be present in all environments."""

    def test_base_dir_exists(self):
        """Verify BASE_DIR is set correctly."""
        assert settings.BASE_DIR.exists()
        assert settings.BASE_DIR.name == "Backend"

    def test_installed_apps_core(self):
        """Verify core Django apps are installed."""
        core_apps = [
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
        ]
        for app in core_apps:
            assert app in settings.INSTALLED_APPS

    def test_custom_apps_installed(self):
        """Verify custom apps are installed."""
        assert "accounts" in settings.INSTALLED_APPS
        assert "pages" in settings.INSTALLED_APPS

    def test_middleware_configured(self):
        """Verify essential middleware is present."""
        assert "django.middleware.security.SecurityMiddleware" in settings.MIDDLEWARE
        assert (
            "django.contrib.sessions.middleware.SessionMiddleware"
            in settings.MIDDLEWARE
        )
        assert "django.middleware.csrf.CsrfViewMiddleware" in settings.MIDDLEWARE

    def test_templates_configured(self):
        """Verify templates are configured."""
        assert len(settings.TEMPLATES) > 0
        assert (
            settings.TEMPLATES[0]["BACKEND"]
            == "django.template.backends.django.DjangoTemplates"
        )

    def test_static_files_configured(self):
        """Verify static files settings."""
        assert settings.STATIC_URL == "/static/"
        assert settings.STATIC_ROOT == settings.BASE_DIR / "staticfiles"

    def test_custom_user_model(self):
        """Verify custom user model is set."""
        assert settings.AUTH_USER_MODEL == "accounts.CustomUser"


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

    def test_email_backend_console(self):
        """Development should use console email backend."""
        if os.environ.get("DJANGO_ENV") == "development":
            assert (
                settings.EMAIL_BACKEND
                == "django.core.mail.backends.console.EmailBackend"
            )


class TestTestSettings:
    """Test test-environment-specific settings."""

    def test_debug_disabled(self):
        """Debug should be disabled in test environment."""
        if os.environ.get("DJANGO_ENV") == "test":
            assert settings.DEBUG is False

    def test_database_in_memory(self):
        """Test environment should use in-memory database."""
        if os.environ.get("DJANGO_ENV") == "test":
            assert settings.DATABASES["default"]["NAME"] == ":memory:"

    def test_email_backend_memory(self):
        """Test environment should use memory email backend."""
        if os.environ.get("DJANGO_ENV") == "test":
            assert (
                settings.EMAIL_BACKEND
                == "django.core.mail.backends.locmem.EmailBackend"
            )


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
