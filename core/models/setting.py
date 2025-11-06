from django.db import models
from core.models._base import TimeStampedModel


class Setting(TimeStampedModel):
    id = models.AutoField(primary_key=True, editable=False)
    site_name: models.CharField = models.CharField(max_length=255)
    site_description: models.TextField = models.TextField(blank=True)
    site_logo: models.CharField = models.CharField(max_length=255, blank=True)
    favicon: models.CharField = models.CharField(max_length=255, blank=True)
    meta_keywords: models.TextField = models.TextField(blank=True)
    meta_description: models.TextField = models.TextField(blank=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: list[str] = ["-created_at"]
        db_table: str = "settings"

    def __str__(self) -> str:
        return f"{self.id}: {self.site_name}"