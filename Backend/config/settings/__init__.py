import os

# Determine which settings to use based on DJANGO_ENV environment variable
environment = os.environ.get("DJANGO_ENV", "development")

if environment == "production":
    from .production import *
elif environment == "test":
    from .test import *
else:
    from .development import *
