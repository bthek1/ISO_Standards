# Config and Settings Test Suite

This directory contains comprehensive tests for the Django configuration and settings across all environments.

## Test Structure

```
config/tests/
├── __init__.py
├── conftest.py              # Pytest configuration and fixtures
├── README.md                # This file
├── test_asgi.py             # ASGI configuration tests
├── test_environment.py      # Environment configuration tests
├── test_urls.py             # URL configuration tests
└── test_wsgi.py             # WSGI configuration tests

config/settings/tests/
└── test_settings.py         # Comprehensive settings tests
```

## Test Coverage

### Settings Tests (`config/settings/tests/test_settings.py`)

#### TestBaseSettings
- **BASE_DIR configuration**: Validates that BASE_DIR exists, is correctly set, and contains expected directories
- **Installed apps**: Verifies core Django apps, third-party apps, and custom apps are installed
- **Middleware stack**: Checks all required middleware is present and in correct order
- **Template configuration**: Validates template backend, directories, APP_DIRS, and context processors
- **Static files**: Verifies STATIC_URL, STATIC_ROOT, STATICFILES_DIRS, and storage configuration
- **Custom user model**: Confirms AUTH_USER_MODEL is set to accounts.CustomUser
- **Core Django settings**: Tests ROOT_URLCONF, WSGI_APPLICATION, password validators
- **Internationalization**: Validates LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_TZ, LOCALE_PATHS
- **Third-party configurations**: Tests Crispy Forms, django-allauth, REST Framework settings

#### TestDevelopmentSettings
- **Debug mode**: Ensures DEBUG is enabled in development
- **Allowed hosts**: Validates localhost and 127.0.0.1 are in ALLOWED_HOSTS
- **Database**: Confirms SQLite is used with correct path
- **Email backend**: Verifies console email backend for development
- **Development apps**: Checks debug_toolbar and django_extensions are installed
- **Debug toolbar**: Validates middleware and INTERNAL_IPS configuration

#### TestTestSettings
- **Debug disabled**: Ensures DEBUG is False in test environment
- **Testing flag**: Verifies TESTING flag is set
- **In-memory database**: Confirms :memory: SQLite database is used
- **Email backend**: Validates locmem email backend for faster tests
- **Password hashers**: Checks simplified MD5 hasher for speed

#### TestProductionSettings
- **Debug disabled**: Confirms DEBUG is False in production
- **Secret key**: Validates secret key comes from environment, not default
- **Allowed hosts**: Ensures proper hosts are configured (not just localhost)
- **Security settings**: Tests SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE, XSS filter, etc.
- **HSTS settings**: Validates HTTPS Strict Transport Security configuration
- **PostgreSQL**: Confirms PostgreSQL database is used
- **Database credentials**: Checks all credentials come from environment
- **SMTP email**: Verifies SMTP backend with proper configuration
- **Logging**: Validates comprehensive logging configuration

#### TestEnvironmentVariables
- **Secret key**: Tests secret key loading from environment
- **Allowed hosts**: Validates list parsing from environment
- **DEBUG handling**: Tests boolean conversion from string
- **Default from email**: Verifies email address format

#### TestDatabaseConfiguration
- **Database exists**: Confirms default database is configured
- **Valid engine**: Checks database engine is SQLite, PostgreSQL, or MySQL

#### TestStaticAndMediaFiles
- **Static URL**: Validates STATIC_URL is set correctly
- **Static root**: Confirms STATIC_ROOT path
- **Static dirs**: Checks STATICFILES_DIRS configuration
- **Storage backends**: Tests default and staticfiles storage (WhiteNoise)

#### TestSecuritySettings
- **Secret key length**: Ensures sufficient key length (50+ chars)
- **No default key in production**: Validates production doesn't use insecure fallback
- **ALLOWED_HOSTS**: Confirms not empty
- **CSRF protection**: Verifies middleware is enabled
- **X-Frame-Options**: Checks XSS protection headers

#### TestLoggingConfiguration
- **Logging structure**: Validates version, handlers, loggers, formatters
- **Console handler**: Confirms console logging is configured
- **Django logger**: Checks Django-specific logger settings

### URL Tests (`config/tests/test_urls.py`)

#### TestURLPatterns
- Admin URLs (existence, resolution)
- Home page URL (existence, resolution, view name)
- About page URL (existence, resolution, view name)
- Django-allauth URLs (login, logout, signup)

#### TestDebugToolbarURLs
- Debug toolbar URL patterns in development

#### TestURLSecurity
- Trailing slash requirements
- No sensitive data in URL patterns

### WSGI Tests (`config/tests/test_wsgi.py`)

#### TestWSGIConfiguration
- WSGI application is importable
- Application is callable
- DJANGO_SETTINGS_MODULE is set
- Correct settings module is used

#### TestWSGIIntegration
- WSGI can handle requests
- Application responds to basic WSGI environ

### ASGI Tests (`config/tests/test_asgi.py`)

#### TestASGIConfiguration
- ASGI application is importable
- Application is callable
- DJANGO_SETTINGS_MODULE is set
- Correct settings module is used

#### TestASGIIntegration
- ASGI application structure validation

### Environment Tests (`config/tests/test_environment.py`)

#### TestEnvironmentConfiguration
- Settings module loaded correctly
- BASE_DIR accessible and valid
- Required directories exist

#### TestEnvironmentVariableHandling
- DEBUG environment variable parsing
- ALLOWED_HOSTS list handling
- SECRET_KEY validation
- DEFAULT_FROM_EMAIL format

#### TestSettingsInheritance
- Base settings availability
- Environment-specific override behavior
- No circular import issues

#### TestSettingsValidation
- Required Django apps present
- Database properly configured
- Static files configured
- Templates configured
- Complete middleware stack
- Authentication backends
- Custom user model

## Running Tests

### Run all config and settings tests
```bash
python manage.py test config
```

### Run specific test module
```bash
python manage.py test config.tests.test_urls
python manage.py test config.settings.tests.test_settings
```

### Run with pytest
```bash
pytest config/tests/
pytest config/settings/tests/
```

### Run specific test class
```bash
pytest config/settings/tests/test_settings.py::TestBaseSettings
pytest config/settings/tests/test_settings.py::TestProductionSettings
```

### Run specific test method
```bash
pytest config/settings/tests/test_settings.py::TestBaseSettings::test_installed_apps_core
```

### Run tests for specific environment
```bash
# Set environment before running
export DJANGO_ENV=development
python manage.py test config

export DJANGO_ENV=production
python manage.py test config

export DJANGO_ENV=test
python manage.py test config
```

### Run with coverage
```bash
coverage run -m pytest config/
coverage report
coverage html
```

## Environment-Specific Testing

Many tests are conditional based on the `DJANGO_ENV` environment variable:

- **development**: Tests for DEBUG=True, SQLite, console email, debug toolbar
- **test**: Tests for in-memory database, locmem email, simplified hashers
- **production**: Tests for security settings, PostgreSQL, SMTP email, HTTPS settings

Set `DJANGO_ENV` before running tests to activate environment-specific test assertions.

## Test Fixtures

The `conftest.py` file provides useful fixtures:

- `temp_env_var`: Temporarily set environment variables
- `django_env`: Get current Django environment
- `is_development`, `is_production`, `is_test`: Boolean environment checks
- `settings_module`: Get current settings module path
- `base_dir`: Get BASE_DIR from settings
- `installed_apps`: Get list of installed apps
- `middleware`: Get list of middleware

## Continuous Integration

These tests should be run in CI/CD pipelines for all environments:

```yaml
# Example GitHub Actions workflow
- name: Test Development Settings
  env:
    DJANGO_ENV: development
  run: pytest config/

- name: Test Production Settings
  env:
    DJANGO_ENV: production
    SECRET_KEY: test-secret-key-for-ci
    DB_PASSWORD: test-password
  run: pytest config/

- name: Test Test Settings
  env:
    DJANGO_ENV: test
  run: pytest config/
```

## Adding New Tests

When adding new settings or configuration:

1. Add corresponding test in appropriate test class
2. Consider environment-specific behavior
3. Test both positive cases (setting exists and is correct) and negative cases (setting isn't misconfigured)
4. Update this README with new test coverage

## Best Practices

1. **Test each environment**: Run tests with all three DJANGO_ENV values
2. **Use fixtures**: Leverage pytest fixtures for common setup
3. **Conditional tests**: Use `if os.environ.get("DJANGO_ENV") == ...` for environment-specific assertions
4. **Descriptive names**: Test method names should clearly describe what is being tested
5. **Comprehensive coverage**: Test not just that settings exist, but that they have correct values
6. **Security focus**: Pay special attention to security-related settings in production tests
