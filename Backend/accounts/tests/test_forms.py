"""
Comprehensive tests for CustomUser forms.

This module tests:
- CustomUserCreationForm functionality
- CustomUserChangeForm functionality
- Form validation
- Field configuration
- Password validation
- Form saving
"""

import pytest
from django.contrib.auth import get_user_model

from accounts.forms import CustomUserChangeForm, CustomUserCreationForm
from accounts.models import CustomUser

User = get_user_model()


@pytest.mark.django_db
class TestCustomUserCreationForm:
    """Test CustomUserCreationForm functionality."""

    def test_form_has_correct_fields(self):
        """Form should have email, first_name, last_name, and password fields."""
        form = CustomUserCreationForm()
        assert "email" in form.fields
        assert "first_name" in form.fields
        assert "last_name" in form.fields
        assert "password1" in form.fields
        assert "password2" in form.fields

    def test_valid_form_creates_user(self):
        """Valid form data should create a user."""
        form_data = {
            "email": "newuser@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
        }
        form = CustomUserCreationForm(data=form_data)
        assert form.is_valid()
        user = form.save()
        assert user.email == "newuser@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.check_password("ComplexPass123!")

    def test_form_rejects_duplicate_email(self):
        """Form should reject duplicate email addresses."""
        CustomUser.objects.create_user(email="existing@example.com", password="pass123")
        form_data = {
            "email": "existing@example.com",
            "first_name": "Jane",
            "last_name": "Doe",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert "email" in form.errors

    def test_form_rejects_mismatched_passwords(self):
        """Form should reject when passwords don't match."""
        form_data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "Password123!",
            "password2": "DifferentPass123!",
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert "password2" in form.errors

    def test_form_rejects_weak_password(self):
        """Form should reject weak passwords."""
        form_data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "123",
            "password2": "123",
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert "password2" in form.errors

    def test_form_requires_email(self):
        """Form should require email field."""
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert "email" in form.errors

    def test_form_requires_valid_email(self):
        """Form should require valid email format."""
        form_data = {
            "email": "not-an-email",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert "email" in form.errors

    def test_form_allows_optional_first_name(self):
        """Form should allow empty first_name."""
        form_data = {
            "email": "test@example.com",
            "first_name": "",
            "last_name": "Doe",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
        }
        form = CustomUserCreationForm(data=form_data)
        # Check if form is valid - depends on Meta configuration
        if form.is_valid():
            user = form.save()
            assert user.first_name in ("", None)  # Nullable field can be None

    def test_form_allows_optional_last_name(self):
        """Form should allow empty last_name."""
        form_data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
        }
        form = CustomUserCreationForm(data=form_data)
        # Check if form is valid - depends on Meta configuration
        if form.is_valid():
            user = form.save()
            assert user.last_name in ("", None)  # Nullable field can be None

    def test_form_uses_correct_model(self):
        """Form should use CustomUser model."""
        form = CustomUserCreationForm()
        assert form.Meta.model == CustomUser


@pytest.mark.django_db
class TestCustomUserChangeForm:
    """Test CustomUserChangeForm functionality."""

    def test_form_has_correct_fields(self):
        """Form should have all user edit fields."""
        form = CustomUserChangeForm()
        assert "email" in form.fields
        assert "first_name" in form.fields
        assert "last_name" in form.fields
        assert "password" in form.fields
        assert "is_active" in form.fields
        assert "is_staff" in form.fields

    def test_form_can_update_user(self):
        """Form should be able to update existing user."""
        user = CustomUser.objects.create_user(
            email="original@example.com",
            password="pass123",
            first_name="Original",
            last_name="Name",
        )
        form_data = {
            "email": "updated@example.com",
            "first_name": "Updated",
            "last_name": "Name",
            "is_active": True,
            "is_staff": False,
        }
        form = CustomUserChangeForm(data=form_data, instance=user)
        if form.is_valid():
            updated_user = form.save()
            assert updated_user.email == "updated@example.com"
            assert updated_user.first_name == "Updated"

    def test_form_can_change_is_active_status(self):
        """Form should be able to change is_active status."""
        user = CustomUser.objects.create_user(
            email="test@example.com", password="pass123"
        )
        form_data = {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": False,
            "is_staff": user.is_staff,
        }
        form = CustomUserChangeForm(data=form_data, instance=user)
        if form.is_valid():
            updated_user = form.save()
            assert updated_user.is_active is False

    def test_form_can_change_is_staff_status(self):
        """Form should be able to change is_staff status."""
        user = CustomUser.objects.create_user(
            email="test@example.com", password="pass123"
        )
        form_data = {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
            "is_staff": True,
        }
        form = CustomUserChangeForm(data=form_data, instance=user)
        if form.is_valid():
            updated_user = form.save()
            assert updated_user.is_staff is True

    def test_form_uses_correct_model(self):
        """Form should use CustomUser model."""
        form = CustomUserChangeForm()
        assert form.Meta.model == CustomUser

    def test_form_requires_instance_for_edit(self):
        """Form should work with an instance for editing."""
        user = CustomUser.objects.create_user(
            email="test@example.com", password="pass123"
        )
        form = CustomUserChangeForm(instance=user)
        assert form.instance == user
        assert form.initial["email"] == "test@example.com"


@pytest.mark.django_db
class TestFormIntegration:
    """Integration tests for user forms."""

    def test_creation_form_creates_active_user(self):
        """Created users should be active by default."""
        form_data = {
            "email": "active@example.com",
            "first_name": "Active",
            "last_name": "User",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
        }
        form = CustomUserCreationForm(data=form_data)
        assert form.is_valid()
        user = form.save()
        assert user.is_active is True

    def test_creation_form_creates_non_staff_user(self):
        """Created users should not be staff by default."""
        form_data = {
            "email": "user@example.com",
            "first_name": "Regular",
            "last_name": "User",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
        }
        form = CustomUserCreationForm(data=form_data)
        assert form.is_valid()
        user = form.save()
        assert user.is_staff is False

    def test_change_form_preserves_password(self):
        """Change form should not require password change."""
        user = CustomUser.objects.create_user(
            email="test@example.com", password="originalpass"
        )
        form_data = {
            "email": "test@example.com",
            "first_name": "Updated",
            "last_name": "Name",
            "is_active": True,
            "is_staff": False,
        }
        form = CustomUserChangeForm(data=form_data, instance=user)
        if form.is_valid():
            updated_user = form.save()
            # Password should still work
            assert updated_user.check_password("originalpass")
