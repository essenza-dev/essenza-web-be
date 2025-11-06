from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from core.enums.user_role import UserRole
from core.models._base import TimeStampedModel


class User(TimeStampedModel):
    id = models.AutoField(primary_key=True, editable=False)
    username: models.CharField = models.CharField(max_length=100, unique=True)
    name: models.CharField = models.CharField(max_length=255, blank=True)
    email: models.CharField = models.CharField(max_length=255, unique=True)
    password: models.CharField = models.CharField(max_length=255)
    role: models.CharField = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.EDITOR
    )
    is_active: models.BooleanField = models.BooleanField(default=True)
    last_login: models.DateTimeField = models.DateTimeField(null=True, blank=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: list[str] = ["-created_at"]
        db_table: str = "users"

    def __str__(self) -> str:
        return f"{self.id}: {self.email}"

    def __pepper_password(self, raw_password: str) -> str:
        """Apply peppering to the raw password."""
        if not self.username:
            raise ValueError("Username must be set before peppering a password.")

        return f"{self.username}.{raw_password}.{settings.SECRET_KEY}"

    def set_password(self, raw_password: str) -> None:
        """Hash and set the user's password."""
        password = self.__pepper_password(raw_password)
        self.password = make_password(password)

    def check_password(self, raw_password: str) -> bool:
        """Check if the provided password matches the user's password."""
        password = self.__pepper_password(raw_password)
        return check_password(password, self.password)