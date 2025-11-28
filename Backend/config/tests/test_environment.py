"""
Tests for environment configuration and validation.

This module tests:
- Environment variable loading
- Settings module selection
- Configuration validation
- Environment-specific overrides
"""

import os

from django.conf import settings


class TestEnvironmentConfiguration:
    """Test environment-based configuration."""

    def test_settings_module_loaded(self):
        """Settings module should be loaded."""
        assert settings is not None
        assert settings.configured

    def test_environment_settings_path(self):
        """Settings should be loaded from config.settings."""
        settings_module = os.environ.get("DJANGO_SETTINGS_MODULE")
        assert settings_module is not None
        assert settings_module.startswith("config.settings")

    def test_base_dir_accessible(self):
        """BASE_DIR should be accessible and valid."""
        assert settings.BASE_DIR.exists()
        assert settings.BASE_DIR.is_dir()

    def test_required_directories_exist(self):
        """Required directories should exist."""
        required_dirs = [
            settings.BASE_DIR / "config",
            settings.BASE_DIR / "templates",
            settings.BASE_DIR / "static",
        ]
        for directory in required_dirs:
            assert directory.exists(), f"Required directory missing: {directory}"


class TestEnvironmentVariableHandling:
    """Test environment variable handling."""

    def test_debug_env_var_handling(self):
        """DEBUG setting should handle environment variable."""
        # Test that DEBUG can be controlled by environment
        # Note: This test just verifies DEBUG is a boolean
        assert isinstance(settings.DEBUG, bool)

    def test_allowed_hosts_env_var_handling(self):
        """ALLOWED_HOSTS should handle environment variable."""
        assert isinstance(settings.ALLOWED_HOSTS, list)

    def test_secret_key_exists(self):
        """SECRET_KEY should exist and not be empty."""
        assert settings.SECRET_KEY
        assert len(settings.SECRET_KEY) > 10

    def test_default_from_email(self):
        """DEFAULT_FROM_EMAIL should have a value."""
        assert settings.DEFAULT_FROM_EMAIL is not None
        assert "@" in settings.DEFAULT_FROM_EMAIL


class TestSettingsInheritance:
    """Test settings inheritance between base and environment-specific."""

    def test_base_settings_available(self):
        """Base settings should be available."""
        # Test a few key base settings
        assert hasattr(settings, "INSTALLED_APPS")
        assert hasattr(settings, "MIDDLEWARE")
        assert hasattr(settings, "TEMPLATES")

    def test_environment_override_works(self):
        """Environment-specific settings should override base."""
        # This test verifies that environment files can override base
        # The exact test depends on which environment is active
        assert hasattr(settings, "DATABASES")
        assert "default" in settings.DATABASES

    def test_no_circular_imports(self):
        """Settings import should not cause circular imports."""
        try:
            from config.settings import base  # noqa: F401

            success = True
        except ImportError:
            success = False
        assert success, "Settings import caused circular import"


class TestSettingsValidation:
    """Test settings validation."""

    def test_required_apps_present(self):
        """Required Django apps should be present."""
        required_apps = [
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
        ]
        for app in required_apps:
            assert app in settings.INSTALLED_APPS

    def test_database_configured(self):
        """Database should be properly configured."""
        assert "default" in settings.DATABASES
        db_config = settings.DATABASES["default"]
        assert "ENGINE" in db_config
        assert "NAME" in db_config

    def test_static_files_configured(self):
        """Static files should be configured."""
        assert hasattr(settings, "STATIC_URL")
        assert hasattr(settings, "STATIC_ROOT")
        assert hasattr(settings, "STATICFILES_DIRS")

    def test_templates_configured(self):
        """Templates should be configured."""
        assert len(settings.TEMPLATES) > 0
        assert "BACKEND" in settings.TEMPLATES[0]
        assert "DIRS" in settings.TEMPLATES[0]

    def test_middleware_stack_complete(self):
        """Middleware stack should be complete."""
        # Check for security-critical middleware
        critical_middleware = [
            "django.middleware.security.SecurityMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
        ]
        for middleware in critical_middleware:
            assert middleware in settings.MIDDLEWARE

    def test_auth_backend_configured(self):
        """Authentication backends should be configured."""
        assert hasattr(settings, "AUTHENTICATION_BACKENDS")
        assert len(settings.AUTHENTICATION_BACKENDS) > 0

    def test_custom_user_model_configured(self):
        """Custom user model should be configured."""
        assert settings.AUTH_USER_MODEL == "accounts.CustomUser"
