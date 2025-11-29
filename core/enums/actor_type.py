from django.db import models


class ActorType(models.TextChoices):
    """Type-safe choices for actor classification."""

    USER = "user", "User"
    GUEST = "guest", "Guest"
