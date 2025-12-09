import dj_database_url

from .base import *

# Development-specific settings
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "192.168.2.22"]

# Add development apps
INSTALLED_APPS += [
    "debug_toolbar",
    "django_extensions",
]

# Add debug toolbar middleware
MIDDLEWARE.insert(4, "debug_toolbar.middleware.DebugToolbarMiddleware")

# Database (PostgreSQL for development)
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

# Use DATABASE_URL environment variable with fallback to SQLite
# Default: postgresql://ben:secretpassword@localhost:5432/iso_standards
DATABASES = {
    "default": dj_database_url.config(
        default="sqlite:///db.sqlite3",
        conn_max_age=0,  # Don't persist connections in dev
        conn_health_checks=True,
    )
}

# Add connection timeout for PostgreSQL
if DATABASES["default"].get("ENGINE") == "django.db.backends.postgresql":
    if "OPTIONS" not in DATABASES["default"]:
        DATABASES["default"]["OPTIONS"] = {}
    DATABASES["default"]["OPTIONS"]["connect_timeout"] = 10

# Email (Console backend for development)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Debug toolbar
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
# https://docs.djangoproject.com/en/dev/ref/settings/#internal-ips
INTERNAL_IPS = ["127.0.0.1"]
