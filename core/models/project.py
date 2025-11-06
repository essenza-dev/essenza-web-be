from django.db import models
from core.models._base import TimeStampedModel


class Project(TimeStampedModel):
    id = models.AutoField(primary_key=True, editable=False)
    title: models.CharField = models.CharField(max_length=255)
    slug: models.CharField = models.CharField(max_length=255, unique=True)
    location: models.CharField = models.CharField(max_length=255, blank=True)
    description: models.TextField = models.TextField(blank=True)
    image: models.CharField = models.CharField(max_length=255, blank=True)
    gallery: models.JSONField = models.JSONField(blank=True, null=True)
    meta_title: models.CharField = models.CharField(max_length=255, blank=True)
    meta_description: models.TextField = models.TextField(blank=True)
    meta_keywords: models.TextField = models.TextField(blank=True)
    is_active: models.BooleanField = models.BooleanField(default=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: list[str] = ["-created_at"]
        db_table: str = "projects"

    def __str__(self) -> str:
        return f"{self.id}: {self.title}"