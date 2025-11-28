"""
Comprehensive tests for CustomUser admin interface.

This module tests:
- Admin site registration
- Admin list display
- Admin filters and search
- Admin fieldsets
- Admin permissions
- Admin actions
"""

import pytest
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory

from accounts.admin import CustomUserAdmin
from accounts.models import CustomUser


@pytest.mark.django_db
class TestCustomUserAdmin:
    """Test CustomUserAdmin configuration."""

    def test_custom_user_registered_in_admin(self):
        """CustomUser should be registered in admin site."""
        assert CustomUser in admin.site._registry
        assert isinstance(admin.site._registry[CustomUser], CustomUserAdmin)

    def test_list_display_fields(self):
        """Admin list should display correct fields."""
        admin_instance = CustomUserAdmin(CustomUser, AdminSite())
        expected_fields = (
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
        )
        assert admin_instance.list_display == expected_fields

    def test_list_filter_fields(self):
        """Admin should have correct filter options."""
        admin_instance = CustomUserAdmin(CustomUser, AdminSite())
        expected_filters = ("is_staff", "is_active")
        assert admin_instance.list_filter == expected_filters

    def test_search_fields(self):
        """Admin should be able to search by email and names."""
        admin_instance = CustomUserAdmin(CustomUser, AdminSite())
        expected_search = ("email", "first_name", "last_name")
        assert admin_instance.search_fields == expected_search

    def test_ordering(self):
        """Admin should order by email."""
        admin_instance = CustomUserAdmin(CustomUser, AdminSite())
        assert admin_instance.ordering == ("email",)

    def test_readonly_fields(self):
        """Admin should have correct readonly fields."""
        admin_instance = CustomUserAdmin(CustomUser, AdminSite())
        expected_readonly = ("last_login", "date_joined", "groups")
        assert admin_instance.readonly_fields == expected_readonly

    def test_fieldsets_structure(self):
        """Admin should have properly structured fieldsets."""
        admin_instance = CustomUserAdmin(CustomUser, AdminSite())
        fieldsets = admin_instance.fieldsets
        assert fieldsets is not None
        assert len(fieldsets) == 4  # None, Personal Info, Permissions, Important dates

        # Check first fieldset (None - credentials)
        assert fieldsets[0][0] is None
        assert "email" in fieldsets[0][1]["fields"]
        assert "password" in fieldsets[0][1]["fields"]

        # Check Personal Info fieldset
        assert fieldsets[1][0] == "Personal Info"
        assert "first_name" in fieldsets[1][1]["fields"]
        assert "last_name" in fieldsets[1][1]["fields"]

        # Check Permissions fieldset
        assert fieldsets[2][0] == "Permissions"
        assert "is_staff" in fieldsets[2][1]["fields"]
        assert "is_active" in fieldsets[2][1]["fields"]
        assert "is_superuser" in fieldsets[2][1]["fields"]

        # Check Important dates fieldset
        assert fieldsets[3][0] == "Important dates"
        assert "last_login" in fieldsets[3][1]["fields"]
        assert "date_joined" in fieldsets[3][1]["fields"]

    def test_add_fieldsets_structure(self):
        """Admin should have properly structured add_fieldsets."""
        admin_instance = CustomUserAdmin(CustomUser, AdminSite())
        add_fieldsets = admin_instance.add_fieldsets
        assert len(add_fieldsets) > 0

        # Check that add form includes necessary fields
        fields = add_fieldsets[0][1]["fields"]
        assert "email" in fields
        assert "first_name" in fields
        assert "last_name" in fields
        assert "password1" in fields
        assert "password2" in fields

    def test_uses_custom_forms(self):
        """Admin should use custom user forms."""
        from accounts.forms import CustomUserChangeForm, CustomUserCreationForm

        admin_instance = CustomUserAdmin(CustomUser, AdminSite())
        assert admin_instance.form == CustomUserChangeForm
        assert admin_instance.add_form == CustomUserCreationForm


@pytest.mark.django_db
class TestCustomUserAdminActions:
    """Test admin actions and functionality."""

    @pytest.fixture
    def admin_user(self):
        """Create an admin user for testing."""
        return CustomUser.objects.create_superuser(
            email="admin@example.com",
            password="adminpass123",
            first_name="Admin",
            last_name="User",
        )

    @pytest.fixture
    def regular_user(self):
        """Create a regular user for testing."""
        return CustomUser.objects.create_user(
            email="user@example.com",
            password="userpass123",
            first_name="Regular",
            last_name="User",
        )

    @pytest.fixture
    def request_factory(self):
        """Provide a request factory."""
        return RequestFactory()

    def test_admin_can_view_user_list(self, admin_user, regular_user, request_factory):
        """Admin should be able to view user list."""
        admin_instance = CustomUserAdmin(CustomUser, AdminSite())
        request = request_factory.get("/admin/accounts/customuser/")
        request.user = admin_user

        # Get queryset
        queryset = admin_instance.get_queryset(request)
        assert admin_user in queryset
        assert regular_user in queryset

    def test_admin_can_search_by_email(self, admin_user, regular_user):
        """Admin should be able to search users by email."""
        admin_instance = CustomUserAdmin(CustomUser, AdminSite())
        assert "email" in admin_instance.search_fields
        # Search functionality is tested through Django's admin interface

    def test_admin_can_search_by_name(self, admin_user, regular_user):
        """Admin should be able to search users by first and last name."""
        admin_instance = CustomUserAdmin(CustomUser, AdminSite())
        assert "first_name" in admin_instance.search_fields
        assert "last_name" in admin_instance.search_fields

    def test_admin_can_filter_by_staff_status(self, admin_user, regular_user):
        """Admin should be able to filter by is_staff."""
        admin_instance = CustomUserAdmin(CustomUser, AdminSite())
        assert "is_staff" in admin_instance.list_filter

    def test_admin_can_filter_by_active_status(self, admin_user, regular_user):
        """Admin should be able to filter by is_active."""
        admin_instance = CustomUserAdmin(CustomUser, AdminSite())
        assert "is_active" in admin_instance.list_filter


@pytest.mark.django_db
class TestAdminPermissions:
    """Test admin permissions and access control."""

    @pytest.fixture
    def superuser(self):
        """Create a superuser."""
        return CustomUser.objects.create_superuser(
            email="super@example.com", password="superpass"
        )

    @pytest.fixture
    def staff_user(self):
        """Create a staff user (non-superuser)."""
        user = CustomUser.objects.create_user(
            email="staff@example.com", password="staffpass"
        )
        user.is_staff = True
        user.save()
        return user

    @pytest.fixture
    def regular_user(self):
        """Create a regular user."""
        return CustomUser.objects.create_user(
            email="regular@example.com", password="regularpass"
        )

    def test_superuser_has_all_permissions(self, superuser):
        """Superuser should have all permissions."""
        assert superuser.is_superuser is True
        assert superuser.is_staff is True
        assert superuser.has_perm("accounts.add_customuser")
        assert superuser.has_perm("accounts.change_customuser")
        assert superuser.has_perm("accounts.delete_customuser")
        assert superuser.has_perm("accounts.view_customuser")

    def test_staff_user_is_staff(self, staff_user):
        """Staff user should have is_staff flag."""
        assert staff_user.is_staff is True
        assert staff_user.is_superuser is False

    def test_regular_user_not_staff(self, regular_user):
        """Regular user should not be staff."""
        assert regular_user.is_staff is False
        assert regular_user.is_superuser is False


@pytest.mark.django_db
class TestAdminDisplay:
    """Test admin display and representation."""

    def test_user_str_in_admin_list(self):
        """User's string representation should show email."""
        user = CustomUser.objects.create_user(
            email="display@example.com", password="pass123"
        )
        assert str(user) == "display@example.com"

    def test_admin_shows_user_status(self):
        """Admin list should show user active and staff status."""
        admin_instance = CustomUserAdmin(CustomUser, AdminSite())
        assert "is_active" in admin_instance.list_display
        assert "is_staff" in admin_instance.list_display

    def test_admin_list_ordered_by_email(self):
        """Admin list should be ordered by email."""
        CustomUser.objects.create_user(email="zuser@example.com", password="pass")
        CustomUser.objects.create_user(email="auser@example.com", password="pass")
        CustomUser.objects.create_user(email="muser@example.com", password="pass")

        admin_instance = CustomUserAdmin(CustomUser, AdminSite())
        ordering = admin_instance.ordering or []
        users = list(CustomUser.objects.all().order_by(*ordering))
        assert users[0].email == "auser@example.com"
        assert users[1].email == "muser@example.com"
        assert users[2].email == "zuser@example.com"
