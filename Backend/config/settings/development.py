from .base import *

# Development-specific settings
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Add development apps
INSTALLED_APPS += [
    "debug_toolbar",
    "django_extensions",
]

# Add debug toolbar middleware
MIDDLEWARE.insert(4, "debug_toolbar.middleware.DebugToolbarMiddleware")

# Database (PostgreSQL for development)
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
import os

# Default to PostgreSQL, fallback to SQLite if needed
# This allows development to continue even if Docker is not running
DB_ENGINE = os.environ.get("DB_ENGINE", "django.db.backends.postgresql")

if DB_ENGINE == "django.db.backends.postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DB_NAME", "iso_standards"),
            "USER": os.environ.get("DB_USER", "ben"),
            "PASSWORD": os.environ.get("DB_PASSWORD", "secretpassword"),
            "HOST": os.environ.get("DB_HOST", "localhost"),
            "PORT": os.environ.get("DB_PORT", "5432"),
            "CONN_MAX_AGE": 0,  # Don't persist connections in dev
            "OPTIONS": {
                "connect_timeout": 10,
            },
        }
    }
else:
    # Fallback to SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Email (Console backend for development)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Debug toolbar
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
# https://docs.djangoproject.com/en/dev/ref/settings/#internal-ips
INTERNAL_IPS = ["127.0.0.1"]
