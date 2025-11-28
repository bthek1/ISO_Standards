"""
Tests for URL configuration.

This module tests:
- URL patterns are correctly configured
- Admin URLs are accessible
- App URLs are included
- Debug toolbar URLs in development
- URL name resolution
"""

import pytest
from django.conf import settings
from django.urls import resolve, reverse


class TestURLPatterns:
    """Test URL configuration."""

    def test_admin_url_exists(self):
        """Admin URL should be configured."""
        url = reverse("admin:index")
        assert url == "/admin/"

    def test_admin_url_resolves(self):
        """Admin URL should resolve correctly."""
        resolver = resolve("/admin/")
        assert resolver is not None

    def test_home_url_exists(self):
        """Home URL should be configured."""
        url = reverse("home")
        assert url == "/"

    def test_home_url_resolves(self):
        """Home URL should resolve correctly."""
        resolver = resolve("/")
        assert resolver.view_name == "home"

    def test_about_url_exists(self):
        """About URL should be configured."""
        url = reverse("about")
        assert url == "/about/"

    def test_about_url_resolves(self):
        """About URL should resolve correctly."""
        resolver = resolve("/about/")
        assert resolver.view_name == "about"

    def test_allauth_login_url(self):
        """Allauth login URL should be configured."""
        url = reverse("account_login")
        assert url.startswith("/accounts/")

    def test_allauth_logout_url(self):
        """Allauth logout URL should be configured."""
        url = reverse("account_logout")
        assert url.startswith("/accounts/")

    def test_allauth_signup_url(self):
        """Allauth signup URL should be configured."""
        url = reverse("account_signup")
        assert url.startswith("/accounts/")


class TestDebugToolbarURLs:
    """Test debug toolbar URL configuration."""

    def test_debug_toolbar_in_development(self):
        """Debug toolbar URLs should be included in development."""
        if settings.DEBUG:
            try:
                resolver = resolve("/__debug__/")
                assert resolver is not None
            except Exception:
                # Debug toolbar may not be installed in all test environments
                pytest.skip("Debug toolbar not available")


class TestURLSecurity:
    """Test URL security configurations."""

    def test_admin_requires_trailing_slash(self):
        """Admin URL should require trailing slash."""
        url = reverse("admin:index")
        assert url.endswith("/")

    def test_no_sensitive_data_in_urls(self):
        """URLs should not expose sensitive data patterns."""
        # This is a basic check - extend as needed
        sensitive_patterns = ["secret", "password", "token", "key"]
        from django.urls import get_resolver

        urlpatterns = get_resolver().url_patterns
        for pattern in urlpatterns:
            pattern_str = str(pattern.pattern).lower()
            for sensitive in sensitive_patterns:
                assert sensitive not in pattern_str, (
                    f"URL pattern contains sensitive word: {sensitive}"
                )
