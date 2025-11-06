from django.db import models
from core.models._base import TimeStampedModel


class Subscriber(TimeStampedModel):
    id = models.AutoField(primary_key=True, editable=False)
    email: models.CharField = models.CharField(max_length=255, unique=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: list[str] = ["-created_at"]
        db_table: str = "subscribers"

    def __str__(self) -> str:
        return f"{self.id}: {self.email}"


class ContactMessage(TimeStampedModel):
    id = models.AutoField(primary_key=True, editable=False)
    name: models.CharField = models.CharField(max_length=255)
    email: models.CharField = models.CharField(max_length=255)
    phone: models.CharField = models.CharField(max_length=50, blank=True)
    subject: models.CharField = models.CharField(max_length=255)
    message: models.TextField = models.TextField()
    is_read: models.BooleanField = models.BooleanField(default=False)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: list[str] = ["-created_at"]
        db_table: str = "contact_messages"

    def __str__(self) -> str:
        return f"{self.id}: {self.subject} - {self.name}"