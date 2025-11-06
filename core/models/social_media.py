from django.db import models
from core.models._base import TimeStampedModel


class SocialMedia(TimeStampedModel):
    id = models.AutoField(primary_key=True, editable=False)
    platform: models.CharField = models.CharField(max_length=100)
    icon: models.CharField = models.CharField(max_length=100, blank=True)
    url: models.CharField = models.CharField(max_length=255)
    order_no: models.IntegerField = models.IntegerField(default=0)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: list[str] = ["order_no", "-created_at"]
        db_table: str = "social_media"

    def __str__(self) -> str:
        return f"{self.id}: {self.platform}"