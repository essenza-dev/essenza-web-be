from django.db import models
from core.models._base import TimeStampedModel


class Page(TimeStampedModel):
    id = models.AutoField(primary_key=True, editable=False)
    slug: models.CharField = models.CharField(max_length=255, unique=True)
    title: models.CharField = models.CharField(max_length=255)
    content: models.TextField = models.TextField()
    meta_title: models.TextField = models.TextField(blank=True)
    meta_description: models.TextField = models.TextField(blank=True)
    meta_keywords: models.TextField = models.TextField(blank=True)
    template: models.CharField = models.CharField(max_length=100, blank=True)
    is_active: models.BooleanField = models.BooleanField(default=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: list[str] = ["-created_at"]
        db_table: str = "pages"

    def __str__(self) -> str:
        return f"{self.id}: {self.title}"