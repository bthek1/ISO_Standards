from .base import *

# Testing settings
DEBUG = False
TESTING = True

# In-memory database for faster tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Simplified password hashing for faster tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Email (Memory backend for testing)
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Disable migrations for faster tests (optional)
# Uncomment the following to speed up tests
# class DisableMigrations:
#     def __contains__(self, item):
#         return True
#     def __getitem__(self, item):
#         return None
# MIGRATION_MODULES = DisableMigrations()
