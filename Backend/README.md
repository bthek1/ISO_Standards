# ISO Standards Backend

A Django REST API for the ISO Standards platform - enabling intelligent search and access to global standards documentation powered by RAG (Retrieval Augmented Generation).

## 🎯 Project Purpose

This backend serves as the foundation for a comprehensive standards exploration platform that:

- Stores and manages ISO, IEEE, ASTM, and other global standards
- Implements RAG with PostgreSQL + pgvector for semantic search
- Provides REST API endpoints for the React frontend
- Handles user authentication and authorization
- Processes and indexes standards documents for AI-powered search

## 🚀 Features

- **Django 5.2 & Python 3.13**
- **Django REST Framework** for API endpoints
- **PostgreSQL with pgvector** for vector embeddings
- **Custom User Model** with email-based authentication
- **django-allauth** for user management
- **Type hints** throughout the codebase
- **Comprehensive test coverage** with pytest
- **ASGI support** for async operations
- **AWS RDS** ready for production

## 📖 Installation

(.venv) $ python manage.py migrate
(.venv) $ python manage.py createsuperuser
(.venv) $ python manage.py runserver

# Load the site at <http://127.0.0.1:8000>

```

### Docker

To use Docker with PostgreSQL as the database update the `DATABASES` section of `config/settings.py` to reflect the following:

```python
# config/settings.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",  # set in docker-compose.yml
        "PORT": 5432,  # default postgres port
    }
}
```

The `INTERNAL_IPS` configuration in `config/settings.py` must be also be updated:

```python
# config/settings.py
# django-debug-toolbar
import socket
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + "1" for ip in ips]
```

And then proceed to build the Docker image, run the container, and execute the standard commands within Docker.

```
$ docker compose up -d --build
$ docker compose exec web python manage.py migrate
$ docker compose exec web python manage.py createsuperuser
# Load the site at http://127.0.0.1:8000
```

## Next Steps

- Add environment variables. There are multiple packages but I personally prefer [environs](https://pypi.org/project/environs/).
- Add [gunicorn](https://pypi.org/project/gunicorn/) as the production web server.
- Update the [EMAIL_BACKEND](https://docs.djangoproject.com/en/4.0/topics/email/#module-django.core.mail) and connect with a mail provider.
- Make the [admin more secure](https://opensource.com/article/18/1/10-tips-making-django-admin-more-secure).
- `django-allauth` supports [social authentication](https://django-allauth.readthedocs.io/en/latest/providers.html) if you need that.

I cover all of these steps in tutorials and premium courses over at [LearnDjango.com](https://learndjango.com).

----

## 🤝 Contributing

Contributions, issues and feature requests are welcome! See [CONTRIBUTING.md](https://github.com/wsvincent/djangox/blob/master/CONTRIBUTING.md).

## ⭐️ Support

Give a ⭐️  if this project helped you!

## License

[The MIT License](LICENSE)
