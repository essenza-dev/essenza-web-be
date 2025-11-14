from django.db import models
from core.models._base import TimeStampedModel


class Setting(TimeStampedModel):
    id = models.AutoField(primary_key=True, editable=False)
    slug = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=100)
    value = models.TextField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: list[str] = ["-created_at"]
        db_table: str = "settings"

    def __str__(self) -> str:
        return f"{self.id}: {self.label}"