from django.db import models
from core.models._base import TimeStampedModel, FileUploadModel, upload_to
from core.models.product import Product


class ProductVariant(TimeStampedModel, FileUploadModel):
    id = models.BigAutoField(primary_key=True, editable=False)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
    )
    sku: models.CharField = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    size = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    image: models.ImageField = models.ImageField(
        upload_to=upload_to("products/variants"), blank=True
    )
    is_active: models.BooleanField = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: list[str] = ["-created_at"]
        db_table: str = "product_variants"

    def __str__(self) -> str:
        if self.sku:
            return f"{self.id}: {self.sku} / {self.model} - {self.product.name}"
        else:
            return f"{self.id}: {self.model} - {self.product.name}"
