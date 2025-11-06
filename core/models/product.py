from django.db import models
from core.models._base import TimeStampedModel
from core.enums import ProductType
from core.models.brochure import Brochure


class Product(TimeStampedModel):
    id = models.BigAutoField(primary_key=True, editable=False)
    slug: models.CharField = models.CharField(max_length=255, unique=True)
    name: models.CharField = models.CharField(max_length=255)
    lang: models.CharField = models.CharField(max_length=10, default='en')
    model: models.CharField = models.CharField(max_length=100, blank=True)
    size: models.CharField = models.CharField(max_length=100, blank=True)
    description: models.TextField = models.TextField(blank=True)
    product_type: models.CharField = models.CharField(
        max_length=20,
        choices=ProductType.choices,
        blank=True
    )
    image: models.CharField = models.CharField(max_length=255, blank=True)
    gallery: models.JSONField = models.JSONField(blank=True)
    brochure: models.ForeignKey = models.ForeignKey(
        Brochure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    meta_title: models.CharField = models.CharField(max_length=255, blank=True)
    meta_description: models.TextField = models.TextField(blank=True)
    meta_keywords: models.TextField = models.TextField(blank=True)
    is_active: models.BooleanField = models.BooleanField(default=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: list[str] = ["-created_at"]
        db_table: str = "products"

    def __str__(self) -> str:
        return f"{self.id}: {self.name}"