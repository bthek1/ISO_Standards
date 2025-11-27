from .base import *

# Development-specific settings
DEBUG = True
ALLOWED_HOSTS = ['localhost', '0.0.0.0', '127.0.0.1']

# Add development apps
INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]

# Add debug toolbar middleware
MIDDLEWARE.insert(4, 'debug_toolbar.middleware.DebugToolbarMiddleware')

# Database (SQLite for development)
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
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
