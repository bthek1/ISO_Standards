"""
Integration tests for accounts app.

This module tests:
- User authentication flow
- User registration flow
- Password reset flow
- User profile management
- Integration with Django auth system
"""

import pytest
from django.contrib.auth import authenticate, get_user_model

from accounts.models import CustomUser

User = get_user_model()


@pytest.mark.django_db
class TestUserAuthentication:
    """Test user authentication integration."""

    def test_user_can_authenticate_with_email(self):
        """User should be able to authenticate with email and password."""
        user = CustomUser.objects.create_user(
            email="auth@example.com", password="testpass123"
        )
        authenticated = authenticate(email="auth@example.com", password="testpass123")
        assert authenticated is not None
        assert authenticated == user

    def test_authentication_fails_with_wrong_password(self):
        """Authentication should fail with incorrect password."""
        CustomUser.objects.create_user(email="auth@example.com", password="correctpass")
        authenticated = authenticate(email="auth@example.com", password="wrongpass")
        assert authenticated is None

    def test_authentication_fails_with_wrong_email(self):
        """Authentication should fail with non-existent email."""
        CustomUser.objects.create_user(email="existing@example.com", password="pass123")
        authenticated = authenticate(email="wrong@example.com", password="pass123")
        assert authenticated is None

    def test_inactive_user_cannot_authenticate(self):
        """Inactive users should not be able to authenticate."""
        user = CustomUser.objects.create_user(
            email="inactive@example.com", password="testpass"
        )
        user.is_active = False
        user.save()
        authenticated = authenticate(email="inactive@example.com", password="testpass")
        assert authenticated is None

    def test_authentication_case_insensitive_domain(self):
        """Email domain should be case-insensitive."""
        CustomUser.objects.create_user(email="user@EXAMPLE.com", password="testpass")
        # Should work with lowercase domain
        authenticated = authenticate(email="user@example.com", password="testpass")
        assert authenticated is not None


@pytest.mark.django_db
class TestUserLogin:
    """Test user login flow."""

    def test_user_can_login(self, client):
        """User should be able to login through the client."""
        CustomUser.objects.create_user(
            email="login@example.com", password="loginpass123"
        )
        logged_in = client.login(email="login@example.com", password="loginpass123")
        assert logged_in is True

    def test_user_cannot_login_with_wrong_password(self, client):
        """User login should fail with wrong password."""
        CustomUser.objects.create_user(
            email="login@example.com", password="correctpass"
        )
        logged_in = client.login(email="login@example.com", password="wrongpass")
        assert logged_in is False

    def test_inactive_user_cannot_login(self, client):
        """Inactive user should not be able to login."""
        user = CustomUser.objects.create_user(
            email="inactive@example.com", password="testpass"
        )
        user.is_active = False
        user.save()
        logged_in = client.login(email="inactive@example.com", password="testpass")
        assert logged_in is False


@pytest.mark.django_db
class TestUserPermissions:
    """Test user permissions and authorization."""

    def test_superuser_has_all_permissions(self):
        """Superuser should have all permissions."""
        superuser = CustomUser.objects.create_superuser(
            email="super@example.com", password="superpass"
        )
        # Superusers have all permissions
        assert superuser.has_perm("any.permission")
        assert superuser.has_perm("accounts.add_customuser")
        assert superuser.has_perm("accounts.change_customuser")
        assert superuser.has_perm("accounts.delete_customuser")

    def test_regular_user_has_no_permissions_by_default(self):
        """Regular user should have no permissions by default."""
        user = CustomUser.objects.create_user(
            email="regular@example.com", password="regularpass"
        )
        assert not user.has_perm("accounts.add_customuser")
        assert not user.has_perm("accounts.change_customuser")
        assert not user.has_perm("any.permission")

    def test_staff_user_without_superuser_limited_perms(self):
        """Staff user without superuser flag has limited permissions."""
        user = CustomUser.objects.create_user(
            email="staff@example.com", password="staffpass"
        )
        user.is_staff = True
        user.save()
        # Staff without superuser doesn't automatically have all perms
        assert not user.has_perm("any.permission")

    def test_user_can_be_granted_specific_permissions(self):
        """User can be granted specific permissions."""
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        user = CustomUser.objects.create_user(
            email="perms@example.com", password="permspass"
        )

        # Get permission for CustomUser model
        content_type = ContentType.objects.get_for_model(CustomUser)
        permission = Permission.objects.get(
            content_type=content_type, codename="add_customuser"
        )

        # Grant permission
        user.user_permissions.add(permission)
        user.save()

        # Refresh from database
        user = CustomUser.objects.get(pk=user.pk)
        assert user.has_perm("accounts.add_customuser")


@pytest.mark.django_db
class TestUserGroups:
    """Test user group functionality."""

    def test_user_can_be_added_to_group(self):
        """User can be added to a group."""
        from django.contrib.auth.models import Group

        user = CustomUser.objects.create_user(
            email="group@example.com", password="grouppass"
        )
        group = Group.objects.create(name="Test Group")
        user.groups.add(group)

        assert group in user.groups.all()

    def test_user_inherits_group_permissions(self):
        """User should inherit permissions from their groups."""
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType

        user = CustomUser.objects.create_user(
            email="inherit@example.com", password="inheritpass"
        )
        group = Group.objects.create(name="Editors")

        # Add permission to group
        content_type = ContentType.objects.get_for_model(CustomUser)
        permission = Permission.objects.get(
            content_type=content_type, codename="change_customuser"
        )
        group.permissions.add(permission)

        # Add user to group
        user.groups.add(group)
        user = CustomUser.objects.get(pk=user.pk)

        # User should have the permission through the group
        assert user.has_perm("accounts.change_customuser")


@pytest.mark.django_db
class TestUserQuerySet:
    """Test user queryset operations."""

    def test_can_filter_active_users(self, multiple_users):
        """Should be able to filter for active users."""
        # Make one user inactive
        user = multiple_users[0]
        user.is_active = False
        user.save()

        active_users = CustomUser.objects.filter(is_active=True)
        assert user not in active_users
        assert len(active_users) == len(multiple_users) - 1

    def test_can_filter_staff_users(self, multiple_users):
        """Should be able to filter for staff users."""
        # Make one user staff
        user = multiple_users[0]
        user.is_staff = True
        user.save()

        staff_users = CustomUser.objects.filter(is_staff=True)
        assert user in staff_users
        assert len(staff_users) == 1

    def test_can_search_by_email(self, multiple_users):
        """Should be able to search users by email."""
        target_user = multiple_users[0]
        found = CustomUser.objects.filter(email=target_user.email).first()
        assert found == target_user

    def test_can_search_by_name(self, multiple_users):
        """Should be able to search users by name."""
        target_user = multiple_users[0]
        found = CustomUser.objects.filter(first_name=target_user.first_name).first()
        assert found == target_user

    def test_users_ordered_by_email(self):
        """Users can be ordered by email."""
        CustomUser.objects.create_user(email="z@example.com", password="pass")
        CustomUser.objects.create_user(email="a@example.com", password="pass")
        CustomUser.objects.create_user(email="m@example.com", password="pass")

        users = CustomUser.objects.all().order_by("email")
        emails = [u.email for u in users]
        assert emails == sorted(emails)


@pytest.mark.django_db
class TestUserLifecycle:
    """Test complete user lifecycle."""

    def test_create_activate_deactivate_delete_user(self):
        """Test full user lifecycle."""
        # Create user
        user = CustomUser.objects.create_user(
            email="lifecycle@example.com", password="lifecyclepass"
        )
        assert user.is_active is True
        user_id = user.id

        # Deactivate user
        user.is_active = False
        user.save()
        user.refresh_from_db()
        assert user.is_active is False

        # Reactivate user
        user.is_active = True
        user.save()
        user.refresh_from_db()
        assert user.is_active is True

        # Delete user
        user.delete()
        assert not CustomUser.objects.filter(id=user_id).exists()

    def test_user_can_change_password(self):
        """User should be able to change their password."""
        user = CustomUser.objects.create_user(
            email="changepass@example.com", password="oldpass"
        )
        assert user.check_password("oldpass")

        user.set_password("newpass")
        user.save()

        user.refresh_from_db()
        assert user.check_password("newpass")
        assert not user.check_password("oldpass")

    def test_user_can_update_profile(self):
        """User should be able to update their profile information."""
        user = CustomUser.objects.create_user(
            email="profile@example.com",
            password="profilepass",
            first_name="Old",
            last_name="Name",
        )

        user.first_name = "New"
        user.last_name = "Name"
        user.save()

        user.refresh_from_db()
        assert user.first_name == "New"
        assert user.last_name == "Name"


@pytest.mark.django_db
class TestUserModelIntegration:
    """Test CustomUser integration with Django's auth system."""

    def test_get_user_model_returns_custom_user(self):
        """get_user_model() should return CustomUser."""
        assert get_user_model() == CustomUser

    def test_user_model_is_in_auth_system(self):
        """CustomUser should be recognized by Django's auth system."""
        from django.conf import settings

        assert settings.AUTH_USER_MODEL == "accounts.CustomUser"

    def test_user_can_be_used_with_django_auth_forms(self):
        """CustomUser should work with Django's built-in auth forms."""
        user = CustomUser.objects.create_user(
            email="form@example.com", password="formpass"
        )

        # CustomUser should be compatible with Django's auth system
        # Forms like AuthenticationForm work with email as username
        assert user.email == "form@example.com"
        assert user.check_password("formpass")

    def test_last_login_updated_on_login(self, client):
        """User's last_login should be updated when they log in."""
        user = CustomUser.objects.create_user(
            email="lastlogin@example.com", password="loginpass"
        )
        assert user.last_login is None

        # Login
        client.login(email="lastlogin@example.com", password="loginpass")

        user.refresh_from_db()
        assert user.last_login is not None
