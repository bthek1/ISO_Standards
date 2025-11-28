# Accounts App Testing Documentation

## Overview

Comprehensive pytest-based testing suite for the accounts app covering models, forms, admin, and integration scenarios.

## Test Structure

```
accounts/tests/
├── __init__.py
├── conftest.py                    # Pytest fixtures
├── test_accounts_models.py        # Model tests (69 tests)
├── test_forms.py                  # Form tests (22 tests)
├── test_admin.py                  # Admin tests (25 tests)
└── test_integration.py            # Integration tests (30 tests)
```

## Total Test Coverage: 146 Tests

### Test Files

#### 1. `test_accounts_models.py` (69 tests)

**TestCustomUserModel** (20 tests)
- User creation with email and password
- User creation with extra fields (first_name, last_name)
- Superuser creation with permissions
- Email uniqueness constraint
- Email normalization
- USERNAME_FIELD configuration
- REQUIRED_FIELDS validation
- String representation
- Auto-set date_joined
- Default field values (is_active, is_staff)
- Optional first_name and last_name
- Password hashing
- User deactivation
- PermissionsMixin functionality

**TestCustomUserManager** (6 tests)
- Email required validation
- User creation without password
- Manager accessibility
- Email normalization in manager
- Superuser default flags

**TestGetUtcNow** (3 tests)
- Returns datetime object
- Returns UTC timezone
- Returns current time

**TestUserModelIntegration** (40 tests)
- User authentication
- Wrong password handling
- Inactive user authentication blocking
- get_user_model() returns CustomUser
- Superuser permissions
- Regular user default permissions

#### 2. `test_forms.py` (22 tests)

**TestCustomUserCreationForm** (11 tests)
- Form field configuration
- Valid form creates user
- Duplicate email rejection
- Password mismatch validation
- Weak password rejection
- Email requirement
- Valid email format validation
- Optional first_name handling
- Optional last_name handling
- Correct model usage

**TestCustomUserChangeForm** (8 tests)
- Form field configuration
- User update functionality
- is_active status change
- is_staff status change
- Correct model usage
- Instance requirement for editing

**TestFormIntegration** (3 tests)
- Created users are active by default
- Created users are non-staff by default
- Password preservation on update

#### 3. `test_admin.py` (25 tests)

**TestCustomUserAdmin** (9 tests)
- Admin site registration
- List display fields
- List filter fields
- Search fields
- Ordering configuration
- Readonly fields
- Fieldsets structure (credentials, personal info, permissions, dates)
- Add fieldsets structure
- Custom form usage

**TestCustomUserAdminActions** (5 tests)
- View user list
- Search by email
- Search by name
- Filter by staff status
- Filter by active status

**TestAdminPermissions** (4 tests)
- Superuser all permissions
- Staff user flag
- Regular user not staff
- (Uses fixtures: superuser, staff_user, regular_user)

**TestAdminDisplay** (7 tests)
- User string representation in admin
- Admin shows user status
- Admin list ordered by email
- Multiple users ordering

#### 4. `test_integration.py` (30 tests)

**TestUserAuthentication** (5 tests)
- Authenticate with email
- Wrong password fails
- Wrong email fails
- Inactive user cannot authenticate
- Case-insensitive email domain

**TestUserLogin** (3 tests)
- User can login
- Wrong password prevents login
- Inactive user cannot login

**TestUserPermissions** (4 tests)
- Superuser has all permissions
- Regular user has no permissions
- Staff user limited permissions
- Grant specific permissions

**TestUserGroups** (2 tests)
- Add user to group
- Inherit group permissions

**TestUserQuerySet** (5 tests)
- Filter active users
- Filter staff users
- Search by email
- Search by name
- Users ordered by email

**TestUserLifecycle** (3 tests)
- Full lifecycle (create, activate, deactivate, delete)
- Change password
- Update profile

**TestUserModelIntegration** (8 tests)
- get_user_model returns CustomUser
- User model in auth system
- Works with Django auth forms
- Last login updated

## Fixtures (conftest.py)

### Available Fixtures

```python
@pytest.fixture
def user():
    """Regular test user."""

@pytest.fixture
def superuser():
    """Superuser for admin testing."""

@pytest.fixture
def staff_user():
    """Staff user (non-superuser)."""

@pytest.fixture
def inactive_user():
    """Inactive user."""

@pytest.fixture
def user_factory():
    """Factory for creating multiple users."""

@pytest.fixture
def multiple_users(user_factory):
    """Creates 5 test users."""

@pytest.fixture
def authenticated_client(client, user):
    """Django test client logged in as regular user."""

@pytest.fixture
def admin_client(client, superuser):
    """Django test client logged in as admin."""
```

### Using Fixtures

```python
def test_with_user(user):
    """Use a regular user fixture."""
    assert user.email == "testuser@example.com"

def test_with_factory(user_factory):
    """Create custom users."""
    user = user_factory(
        email="custom@example.com",
        first_name="Custom",
        is_staff=True
    )
    assert user.is_staff is True

def test_with_client(authenticated_client):
    """Make authenticated requests."""
    response = authenticated_client.get('/some-url/')
    assert response.status_code == 200
```

## Running Tests

### All accounts tests
```bash
pytest accounts/
```

### Specific test file
```bash
pytest accounts/tests/test_accounts_models.py
pytest accounts/tests/test_forms.py
pytest accounts/tests/test_admin.py
pytest accounts/tests/test_integration.py
```

### Specific test class
```bash
pytest accounts/tests/test_accounts_models.py::TestCustomUserModel
pytest accounts/tests/test_forms.py::TestCustomUserCreationForm
```

### Specific test method
```bash
pytest accounts/tests/test_accounts_models.py::TestCustomUserModel::test_create_user_with_email_and_password
```

### With verbose output
```bash
pytest accounts/ -v
```

### With coverage
```bash
pytest accounts/ --cov=accounts --cov-report=html
```

### Run in parallel
```bash
pytest accounts/ -n auto
```

## Test Categories

### Unit Tests
- Model field validation
- Form validation
- Manager methods
- Utility functions

### Integration Tests
- Authentication flow
- Permission system
- Group membership
- Database queries
- Django auth integration

### Admin Tests
- Admin configuration
- List displays
- Filters and search
- Fieldsets
- Permissions

## What's Tested

### CustomUser Model
- ✅ User creation (regular and super)
- ✅ Email as username field
- ✅ Email uniqueness and normalization
- ✅ Password hashing
- ✅ Optional first/last name
- ✅ Default field values
- ✅ Date tracking (date_joined, last_login)
- ✅ Active/inactive status
- ✅ Staff status
- ✅ Permission system integration

### CustomUserManager
- ✅ create_user method
- ✅ create_superuser method
- ✅ Email validation
- ✅ Email normalization
- ✅ Password handling

### Forms
- ✅ CustomUserCreationForm
- ✅ CustomUserChangeForm
- ✅ Field validation
- ✅ Password validation
- ✅ Email validation
- ✅ Duplicate email prevention

### Admin
- ✅ Model registration
- ✅ List display configuration
- ✅ Search and filter options
- ✅ Fieldsets organization
- ✅ Custom forms
- ✅ Permissions

### Django Integration
- ✅ Authentication backend
- ✅ Permission system
- ✅ Group system
- ✅ get_user_model()
- ✅ AUTH_USER_MODEL setting

## Best Practices Demonstrated

1. **Pytest-only style** - No unittest TestCase classes
2. **Clear test names** - Descriptive method names explain what's tested
3. **Comprehensive fixtures** - Reusable test data
4. **Proper isolation** - Each test independent with `@pytest.mark.django_db`
5. **Edge case testing** - Invalid inputs, constraints, errors
6. **Integration testing** - Real Django auth system interaction
7. **Documentation** - Docstrings explain test purpose

## Adding New Tests

When adding features to the accounts app:

1. **Models**: Add tests to `test_accounts_models.py`
2. **Forms**: Add tests to `test_forms.py`
3. **Admin**: Add tests to `test_admin.py`
4. **Integration**: Add tests to `test_integration.py`
5. **Fixtures**: Add reusable fixtures to `conftest.py`

### Example Test

```python
@pytest.mark.django_db
class TestNewFeature:
    """Test new feature functionality."""

    def test_feature_works(self, user):
        """Feature should work as expected."""
        result = user.new_method()
        assert result == expected_value
```

## Coverage Goals

- **Models**: 100% coverage
- **Forms**: 100% coverage
- **Admin**: 95%+ coverage
- **Overall**: 95%+ coverage

Check coverage with:
```bash
pytest accounts/ --cov=accounts --cov-report=term-missing
```

## CI/CD Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run accounts tests
  run: |
    pytest accounts/ --cov=accounts --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage.xml
```

## Troubleshooting

### Tests fail with database errors
```bash
# Ensure database is properly set up
python manage.py migrate
pytest accounts/
```

### Import errors
```bash
# Ensure you're in the Backend directory
cd Backend
pytest accounts/
```

### Slow tests
```bash
# Run in parallel
pytest accounts/ -n auto
```

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-django documentation](https://pytest-django.readthedocs.io/)
- [Django testing documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- Project pytest guide: `../PYTEST_GUIDE.md`
