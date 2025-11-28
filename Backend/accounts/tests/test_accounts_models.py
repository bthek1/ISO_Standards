"""
Comprehensive tests for CustomUser model and CustomUserManager.

This module tests:
- User creation (regular and superuser)
- Field validation and constraints
- Model methods and properties
- User manager functionality
- Edge cases and error conditions
"""

from datetime import UTC, datetime

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from accounts.models import CustomUser, CustomUserManager, get_utc_now

User = get_user_model()


@pytest.mark.django_db
class TestCustomUserModel:
    """Test CustomUser model functionality."""

    def test_create_user_with_email_and_password(self):
        """User should be created with email and password."""
        user = CustomUser.objects.create_user(
            email="testuser@example.com", password="password123"
        )
        assert user.email == "testuser@example.com"
        assert user.check_password("password123")
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_user_with_extra_fields(self):
        """User should be created with additional fields."""
        user = CustomUser.objects.create_user(
            email="john@example.com",
            password="pass123",
            first_name="John",
            last_name="Doe",
        )
        assert user.email == "john@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"

    def test_create_superuser(self):
        """Superuser should have staff and superuser permissions."""
        user = CustomUser.objects.create_superuser(
            email="admin@example.com", password="adminpass"
        )
        assert user.is_superuser is True
        assert user.is_staff is True
        assert user.is_active is True
        assert user.check_password("adminpass")

    def test_create_superuser_with_extra_fields(self):
        """Superuser should be created with additional fields."""
        user = CustomUser.objects.create_superuser(
            email="admin@example.com",
            password="adminpass",
            first_name="Admin",
            last_name="User",
        )
        assert user.first_name == "Admin"
        assert user.last_name == "User"
        assert user.is_superuser is True

    def test_email_is_unique(self):
        """Email addresses should be unique."""
        CustomUser.objects.create_user(email="unique@example.com", password="pass123")
        with pytest.raises(IntegrityError):
            CustomUser.objects.create_user(
                email="unique@example.com", password="pass456"
            )

    def test_email_normalization(self):
        """Email should be normalized (lowercase domain)."""
        user = CustomUser.objects.create_user(
            email="test@EXAMPLE.COM", password="pass123"
        )
        assert user.email == "test@example.com"

    def test_username_field_is_email(self):
        """USERNAME_FIELD should be email."""
        assert CustomUser.USERNAME_FIELD == "email"

    def test_required_fields(self):
        """REQUIRED_FIELDS should include first_name and last_name."""
        assert "first_name" in CustomUser.REQUIRED_FIELDS
        assert "last_name" in CustomUser.REQUIRED_FIELDS

    def test_str_representation(self):
        """String representation should be the email address."""
        user = CustomUser.objects.create_user(
            email="test@example.com", password="pass123"
        )
        assert str(user) == "test@example.com"

    def test_date_joined_auto_set(self):
        """date_joined should be automatically set on creation."""
        user = CustomUser.objects.create_user(
            email="test@example.com", password="pass123"
        )
        assert user.date_joined is not None
        assert isinstance(user.date_joined, datetime)

    def test_is_active_default_true(self):
        """is_active should default to True."""
        user = CustomUser.objects.create_user(
            email="test@example.com", password="pass123"
        )
        assert user.is_active is True

    def test_is_staff_default_false(self):
        """is_staff should default to False for regular users."""
        user = CustomUser.objects.create_user(
            email="test@example.com", password="pass123"
        )
        assert user.is_staff is False

    def test_first_name_optional(self):
        """first_name should be optional."""
        user = CustomUser.objects.create_user(
            email="test@example.com", password="pass123"
        )
        assert user.first_name is None or user.first_name == ""

    def test_last_name_optional(self):
        """last_name should be optional."""
        user = CustomUser.objects.create_user(
            email="test@example.com", password="pass123"
        )
        assert user.last_name is None or user.last_name == ""

    def test_password_is_hashed(self):
        """Password should be hashed, not stored in plain text."""
        user = CustomUser.objects.create_user(
            email="test@example.com", password="plainpassword"
        )
        assert user.password != "plainpassword"
        assert user.check_password("plainpassword")

    def test_user_can_be_deactivated(self):
        """User's is_active flag can be set to False."""
        user = CustomUser.objects.create_user(
            email="test@example.com", password="pass123"
        )
        user.is_active = False
        user.save()
        user.refresh_from_db()
        assert user.is_active is False

    def test_user_permissions_mixin(self):
        """User should have PermissionsMixin functionality."""
        user = CustomUser.objects.create_user(
            email="test@example.com", password="pass123"
        )
        # Test that PermissionsMixin fields exist
        assert hasattr(user, "is_superuser")
        assert hasattr(user, "groups")
        assert hasattr(user, "user_permissions")


@pytest.mark.django_db
class TestCustomUserManager:
    """Test CustomUserManager functionality."""

    def test_create_user_requires_email(self):
        """Creating user without email should raise ValueError."""
        with pytest.raises(ValueError, match="The Email field must be set"):
            CustomUser.objects.create_user(email="", password="pass123")

    def test_create_user_with_none_email(self):
        """Creating user with None email should raise ValueError."""
        with pytest.raises(ValueError, match="The Email field must be set"):
            CustomUser.objects.create_user(email=None, password="pass123")

    def test_create_user_without_password(self):
        """User can be created without password (for social auth)."""
        user = CustomUser.objects.create_user(email="test@example.com")
        assert user.email == "test@example.com"
        assert not user.has_usable_password()

    def test_manager_accessible_via_objects(self):
        """CustomUserManager should be accessible via objects."""
        assert isinstance(CustomUser.objects, CustomUserManager)

    def test_email_normalization_in_manager(self):
        """Manager should normalize email addresses."""
        user = CustomUser.objects.create_user(
            email="Test@EXAMPLE.com", password="pass123"
        )
        # Domain should be lowercase
        assert "@example.com" in user.email

    def test_superuser_defaults_set_correctly(self):
        """create_superuser should set is_staff and is_superuser to True."""
        user = CustomUser.objects.create_superuser(
            email="admin@example.com", password="adminpass"
        )
        assert user.is_staff is True
        assert user.is_superuser is True


@pytest.mark.django_db
class TestGetUtcNow:
    """Test the get_utc_now utility function."""

    def test_get_utc_now_returns_datetime(self):
        """get_utc_now should return a datetime object."""
        now = get_utc_now()
        assert isinstance(now, datetime)

    def test_get_utc_now_is_utc(self):
        """get_utc_now should return UTC time."""
        now = get_utc_now()
        assert now.tzinfo == UTC

    def test_get_utc_now_is_current(self):
        """get_utc_now should return current time (within 1 second)."""
        now = get_utc_now()
        current = datetime.now(UTC)
        diff = abs((current - now).total_seconds())
        assert diff < 1  # Should be within 1 second


@pytest.mark.django_db
class TestUserModelIntegration:
    """Integration tests for user model with Django auth system."""

    def test_user_can_authenticate(self):
        """User can be authenticated with email and password."""
        from django.contrib.auth import authenticate

        user = CustomUser.objects.create_user(
            email="auth@example.com", password="testpass123"
        )
        authenticated = authenticate(email="auth@example.com", password="testpass123")
        assert authenticated == user

    def test_wrong_password_returns_none(self):
        """Authentication with wrong password returns None."""
        from django.contrib.auth import authenticate

        CustomUser.objects.create_user(email="auth@example.com", password="correctpass")
        authenticated = authenticate(email="auth@example.com", password="wrongpass")
        assert authenticated is None

    def test_inactive_user_cannot_authenticate(self):
        """Inactive users cannot authenticate."""
        from django.contrib.auth import authenticate

        user = CustomUser.objects.create_user(
            email="inactive@example.com", password="testpass"
        )
        user.is_active = False
        user.save()
        authenticated = authenticate(email="inactive@example.com", password="testpass")
        assert authenticated is None

    def test_get_user_model_returns_custom_user(self):
        """get_user_model() should return CustomUser."""
        assert get_user_model() == CustomUser

    def test_user_has_perm_for_superuser(self):
        """Superuser should have all permissions."""
        superuser = CustomUser.objects.create_superuser(
            email="super@example.com", password="pass123"
        )
        assert superuser.has_perm("any.permission")

    def test_regular_user_has_no_perms_by_default(self):
        """Regular user should have no permissions by default."""
        user = CustomUser.objects.create_user(
            email="regular@example.com", password="pass123"
        )
        assert not user.has_perm("any.permission")
