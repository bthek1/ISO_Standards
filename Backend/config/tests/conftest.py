"""
Pytest configuration for config tests.

This module provides:
- Fixtures for testing
- Test configuration
- Common test utilities
"""

import os

import pytest
from django.conf import settings


@pytest.fixture
def temp_env_var():
    """Fixture to temporarily set environment variables."""
    original_env = os.environ.copy()

    def _set_env(key, value):
        os.environ[key] = value

    yield _set_env

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def django_env():
    """Get the current Django environment."""
    return os.environ.get("DJANGO_ENV", "test")


@pytest.fixture
def is_development(django_env):
    """Check if running in development environment."""
    return django_env == "development"


@pytest.fixture
def is_production(django_env):
    """Check if running in production environment."""
    return django_env == "production"


@pytest.fixture
def is_test(django_env):
    """Check if running in test environment."""
    return django_env == "test"


@pytest.fixture
def settings_module():
    """Get the current settings module path."""
    return os.environ.get("DJANGO_SETTINGS_MODULE")


@pytest.fixture
def base_dir():
    """Get the BASE_DIR from settings."""
    return settings.BASE_DIR


@pytest.fixture
def installed_apps():
    """Get list of installed apps."""
    return settings.INSTALLED_APPS


@pytest.fixture
def middleware():
    """Get list of middleware."""
    return settings.MIDDLEWARE


# Markers for environment-specific tests
def pytest_configure(config):
    """Register custom pytest markers."""
    config.addinivalue_line(
        "markers", "development: mark test as development environment only"
    )
    config.addinivalue_line(
        "markers", "production: mark test as production environment only"
    )
    config.addinivalue_line("markers", "test_env: mark test as test environment only")
