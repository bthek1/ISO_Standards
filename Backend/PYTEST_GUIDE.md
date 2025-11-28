# Pytest Quick Reference for ISO_Standards Project

## ✅ Project-Wide Testing Standard: PYTEST ONLY

**All tests in this project use pytest.** No unittest-style `TestCase` classes.

## Running Tests

```bash
# All tests
pytest

# Specific app
pytest config/
pytest accounts/

# Specific file
pytest config/tests/test_urls.py

# Specific class
pytest config/tests/test_urls.py::TestURLPatterns

# Specific test
pytest config/tests/test_urls.py::TestURLPatterns::test_admin_url_exists

# With verbose output
pytest -v

# With coverage
pytest --cov=config --cov-report=html

# Parallel execution (faster)
pytest -n auto

# Stop on first failure
pytest -x

# Show local variables on failure
pytest -l
```

## Writing Tests - Pytest Style

### Basic Test Class

```python
class TestMyFeature:
    """Test my feature."""

    def test_something(self):
        """Test description."""
        result = my_function()
        assert result == expected_value
```

### Common Assertions

```python
# Equality
assert a == b
assert a != b

# Boolean
assert value
assert not value
assert value is True
assert value is False

# None checks
assert value is None
assert value is not None

# Membership
assert item in collection
assert item not in collection

# Comparisons
assert a > b
assert a >= b
assert a < b
assert a <= b

# Type checking
assert isinstance(obj, MyClass)

# String matching
assert "substring" in string
assert string.startswith("prefix")
assert string.endswith("suffix")

# Collection length
assert len(items) == 5
assert len(items) > 0
```

### Testing Exceptions

```python
import pytest

def test_raises_exception():
    with pytest.raises(ValueError):
        my_function_that_raises()

def test_exception_message():
    with pytest.raises(ValueError, match="Invalid input"):
        my_function_that_raises()
```

### Using Fixtures

```python
import pytest

@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {"key": "value"}

def test_with_fixture(sample_data):
    """Test using fixture."""
    assert sample_data["key"] == "value"
```

### Django-Specific Testing

```python
from django.conf import settings
from django.urls import reverse

class TestDjangoFeature:
    """Test Django features."""

    def test_setting(self):
        """Test a Django setting."""
        assert settings.DEBUG is False

    def test_url(self):
        """Test URL reverse."""
        url = reverse("home")
        assert url == "/"
```

### Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_doubling(input, expected):
    """Test doubling function with multiple inputs."""
    assert double(input) == expected
```

### Skip and Conditional Tests

```python
import pytest
import os

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(
    os.environ.get("DJANGO_ENV") != "production",
    reason="Production only"
)
def test_production_feature():
    pass

def test_optional_feature():
    if not feature_available():
        pytest.skip("Feature not available")
    # test code here
```

## Project-Specific Fixtures

Available in `config/tests/conftest.py`:

```python
def test_with_fixtures(django_env, base_dir, installed_apps):
    """Use project fixtures."""
    assert django_env in ["development", "test", "production"]
    assert base_dir.exists()
    assert "django.contrib.admin" in installed_apps
```

## Environment-Specific Tests

```python
import os

class TestEnvironmentFeature:
    """Test environment-specific behavior."""

    def test_development_feature(self):
        """Test only runs in development."""
        if os.environ.get("DJANGO_ENV") == "development":
            assert settings.DEBUG is True
        # Test passes/skips in other environments
```

## What NOT to Do

### ❌ Don't use unittest-style assertions

```python
# WRONG - Don't do this
from django.test import TestCase

class MyTest(TestCase):
    def test_something(self):
        self.assertEqual(a, b)
        self.assertTrue(value)
```

### ❌ Don't use Django TestCase

```python
# WRONG - Don't do this
from django.test import TestCase

# RIGHT - Do this instead
class TestMyFeature:
    def test_something(self):
        assert a == b
```

### ❌ Don't suppress exceptions silently

```python
# WRONG - Don't do this
try:
    something()
except Exception:
    pass

# RIGHT - Do this instead
try:
    something()
except Exception:
    pytest.skip("Optional dependency not available")
```

## Configuration

Tests are configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.test"
python_files = ["*test*.py", "tests/*.py"]
addopts = "--tb=short --show-capture=no -ra"
```

## Coverage Reports

```bash
# Run with coverage
pytest --cov=config --cov=accounts --cov=pages

# Generate HTML report
pytest --cov=config --cov-report=html

# View report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## CI/CD Integration

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pytest --cov --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Tips

1. **Use descriptive test names**: `test_user_cannot_login_with_wrong_password`
2. **One assertion per test** (when possible)
3. **Use fixtures** for common setup
4. **Test edge cases** and error conditions
5. **Keep tests fast** - use mocks for external services
6. **Run tests frequently** during development
7. **Use markers** for slow or integration tests

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-django documentation](https://pytest-django.readthedocs.io/)
- Project tests: `config/tests/README.md`
