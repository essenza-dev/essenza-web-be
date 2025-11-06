from django.db import models


class UserRole(models.TextChoices):
    SUPERADMIN = "superadmin", "Super Admin"
    ADMIN = "admin", "Admin"
    EDITOR = "editor", "Editor"
