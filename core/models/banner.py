from django.db import models
from core.models._base import TimeStampedModel


class Banner(TimeStampedModel):
    id = models.AutoField(primary_key=True, editable=False)
    title: models.CharField = models.CharField(max_length=255)
    subtitle: models.CharField = models.CharField(max_length=255, blank=True)
    image: models.CharField = models.CharField(max_length=255)
    link_url: models.CharField = models.CharField(max_length=255, blank=True)
    order_no: models.IntegerField = models.IntegerField(default=0)
    is_active: models.BooleanField = models.BooleanField(default=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: list[str] = ["-created_at"]
        db_table: str = "banners"

    def __str__(self) -> str:
        return f"{self.id}: {self.title}"