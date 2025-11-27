from .base import *

# Testing settings
DEBUG = False
TESTING = True

# In-memory database for faster tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Simplified password hashing for faster tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Email (Memory backend for testing)
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Note: To speed up tests, you can disable migrations by setting
# MIGRATION_MODULES to a custom class that returns None for all apps
