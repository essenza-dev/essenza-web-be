from django.db import models
from core.models._base import TimeStampedModel


class Store(TimeStampedModel):
    id = models.AutoField(primary_key=True, editable=False)
    name: models.CharField = models.CharField(max_length=255)
    address: models.TextField = models.TextField()
    phone: models.CharField = models.CharField(max_length=50, blank=True)
    email: models.CharField = models.CharField(max_length=100, blank=True)
    latitude: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=True,
        blank=True
    )
    longitude: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=True,
        blank=True
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: list[str] = ["-created_at"]
        db_table: str = "stores"

    def __str__(self) -> str:
        return f"{self.id}: {self.name}"