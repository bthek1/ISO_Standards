"""
Pytest fixtures for accounts app tests.

This module provides:
- User fixtures (regular, staff, superuser)
- Factory fixtures for creating test users
- Common test data
"""

import pytest
from django.contrib.auth import get_user_model

from accounts.models import CustomUser

User = get_user_model()


@pytest.fixture
def user():
    """Create a regular test user."""
    return CustomUser.objects.create_user(
        email="testuser@example.com",
        password="password123",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def superuser():
    """Create a superuser for testing admin functionality."""
    return CustomUser.objects.create_superuser(
        email="admin@example.com",
        password="adminpass123",
        first_name="Admin",
        last_name="User",
    )


@pytest.fixture
def staff_user():
    """Create a staff user (non-superuser)."""
    user = CustomUser.objects.create_user(
        email="staff@example.com",
        password="staffpass123",
        first_name="Staff",
        last_name="User",
    )
    user.is_staff = True
    user.save()
    return user


@pytest.fixture
def inactive_user():
    """Create an inactive user."""
    user = CustomUser.objects.create_user(
        email="inactive@example.com",
        password="inactivepass123",
        first_name="Inactive",
        last_name="User",
    )
    user.is_active = False
    user.save()
    return user


@pytest.fixture
def user_factory():
    """Factory fixture for creating multiple users."""

    def make_user(
        email=None,
        password="defaultpass123",  # noqa: S107
        first_name="",
        last_name="",
        is_staff=False,
        is_superuser=False,
        is_active=True,
        **extra_fields,
    ):
        """Create a user with specified parameters."""
        if email is None:
            # Generate unique email
            import uuid

            email = f"user-{uuid.uuid4().hex[:8]}@example.com"

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.is_active = is_active
        user.save()
        return user

    return make_user


@pytest.fixture
def multiple_users(user_factory):
    """Create multiple users for testing lists and queries."""
    users = []
    for i in range(5):
        user = user_factory(
            email=f"user{i}@example.com",
            first_name=f"User{i}",
            last_name=f"Test{i}",
        )
        users.append(user)
    return users


@pytest.fixture
def authenticated_client(client, user):
    """Provide an authenticated Django test client."""
    client.force_login(user)
    return client


@pytest.fixture
def admin_client(client, superuser):
    """Provide an authenticated admin client."""
    client.force_login(superuser)
    return client
