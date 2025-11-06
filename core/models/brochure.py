from django.db import models
from core.models._base import TimeStampedModel


class Brochure(TimeStampedModel):
    id = models.AutoField(primary_key=True, editable=False)
    title: models.CharField = models.CharField(max_length=255)
    file_url: models.CharField = models.CharField(max_length=255)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: list[str] = ["-created_at"]
        db_table: str = "brochures"

    def __str__(self) -> str:
        return f"{self.id}: {self.title}"