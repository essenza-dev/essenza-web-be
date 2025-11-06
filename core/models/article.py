from django.db import models
from core.models._base import TimeStampedModel


class Article(TimeStampedModel):
    id = models.AutoField(primary_key=True, editable=False)
    title: models.CharField = models.CharField(max_length=255)
    slug: models.CharField = models.CharField(max_length=255, unique=True)
    content: models.TextField = models.TextField()
    thumbnail: models.CharField = models.CharField(max_length=255, blank=True)
    author: models.CharField = models.CharField(max_length=100, blank=True)
    tags: models.CharField = models.CharField(max_length=255, blank=True)
    meta_title: models.CharField = models.CharField(max_length=255, blank=True)
    meta_description: models.TextField = models.TextField(blank=True)
    meta_keywords: models.TextField = models.TextField(blank=True)
    published_at: models.DateTimeField = models.DateTimeField(null=True, blank=True)
    is_active: models.BooleanField = models.BooleanField(default=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: list[str] = ["-created_at"]
        db_table: str = "articles"

    def __str__(self) -> str:
        return f"{self.id}: {self.title}"