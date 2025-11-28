from datetime import UTC
from datetime import datetime as dt
from typing import Any

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


def get_utc_now():
    return dt.now(UTC)


class CustomUserManager(BaseUserManager["CustomUser"]):
    def create_user(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> "CustomUser":
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> "CustomUser":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id: int  # Django auto-generated primary key
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=get_utc_now)

    objects: CustomUserManager = CustomUserManager()  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    # TODO: Add required fields when ready
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email
