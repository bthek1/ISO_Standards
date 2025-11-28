"""
Tests for ASGI configuration.

This module tests:
- ASGI application is correctly configured
- Environment variables are set
- Application is callable
"""

import os


class TestASGIConfiguration:
    """Test ASGI configuration."""

    def test_asgi_application_importable(self):
        """ASGI application should be importable."""
        from config.asgi import application

        assert application is not None

    def test_asgi_application_callable(self):
        """ASGI application should be callable."""
        from config.asgi import application

        assert callable(application)

    def test_django_settings_module_set(self):
        """DJANGO_SETTINGS_MODULE should be set in ASGI."""
        # Import the asgi module to trigger the os.environ.setdefault
        import config.asgi  # noqa: F401

        assert "DJANGO_SETTINGS_MODULE" in os.environ

    def test_asgi_uses_correct_settings(self):
        """ASGI should use the correct settings module."""
        from config.asgi import application  # noqa: F401

        settings_module = os.environ.get("DJANGO_SETTINGS_MODULE")
        assert settings_module is not None
        assert settings_module.startswith("config.settings")


class TestASGIIntegration:
    """Test ASGI integration with Django."""

    def test_asgi_application_structure(self):
        """ASGI application should have correct structure."""
        from config.asgi import application

        # ASGI3 applications should be coroutine functions
        # or have __call__ method
        assert callable(application), "ASGI application should be callable"
