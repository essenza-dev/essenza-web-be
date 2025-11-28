"""
Product API Serializers
Contains all serializers for product-related API operations
"""

from rest_framework import serializers
from typing import List, Dict, Any
from django.conf import settings

from core.models import Product, Brochure
from core.enums import ProductType

# Constants
PRODUCT_ACTIVE_STATUS_HELP = "Product active status"


class ProductModelSerializer(serializers.ModelSerializer):
    """Serializer for Product model with brochure relationship."""

    brochure = serializers.SerializerMethodField()
    gallery = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_brochure(self, obj: Product) -> Dict[str, Any] | None:
        """Get brochure information if available."""
        if obj.brochure:
            return {
                "id": obj.brochure.id,
                "title": obj.brochure.title,
                "file_url": obj.brochure.file_url,
            }
        return None

    def get_gallery(self, obj: Product) -> List[str]:
        """Get gallery images with proper media URL prefix."""
        if obj.gallery and isinstance(obj.gallery, list):
            media_base = settings.FILE_UPLOAD_BASE_DIR.rstrip("/")
            return [
                f"/{path}" if path.startswith(media_base) else f"/{media_base}/{path}"
                for path in obj.gallery
            ]
        return []


class PostCreateProductRequest(serializers.Serializer):
    """Serializer for creating a new product."""

    slug = serializers.CharField(
        max_length=255, help_text="Unique URL slug for the product"
    )
    name = serializers.CharField(max_length=255, help_text="Product name")
    lang = serializers.CharField(
        max_length=10, default="en", help_text="Language code (e.g., 'en', 'id')"
    )
    model = serializers.CharField(
        max_length=100, allow_blank=True, required=False, help_text="Product model/code"
    )
    size = serializers.CharField(
        max_length=100,
        allow_blank=True,
        required=False,
        help_text="Product size specifications",
    )
    description = serializers.CharField(
        allow_blank=True, required=False, help_text="Product description"
    )
    product_type = serializers.ChoiceField(
        choices=ProductType.choices,
        allow_blank=True,
        required=False,
        help_text="Product type (lantai/dinding)",
    )
    image = serializers.ImageField(
        required=False,
        allow_empty_file=True,
        use_url=False,
        help_text="Product main image",
    )
    gallery = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=True, use_url=False),
        required=False,
        allow_empty=True,
        help_text="Product gallery images",
    )
    brochure_id = serializers.IntegerField(
        required=False, allow_null=True, help_text="ID of associated brochure"
    )
    meta_title = serializers.CharField(
        max_length=255, allow_blank=True, required=False, help_text="SEO meta title"
    )
    meta_description = serializers.CharField(
        allow_blank=True, required=False, help_text="SEO meta description"
    )
    meta_keywords = serializers.CharField(
        allow_blank=True, required=False, help_text="SEO meta keywords"
    )
    is_active = serializers.BooleanField(help_text=PRODUCT_ACTIVE_STATUS_HELP)

    def validate_slug(self, value: str) -> str:
        """Validate slug format and basic requirements."""
        # Basic slug validation - actual uniqueness will be validated in service layer
        if not value or not value.strip():
            raise serializers.ValidationError("Slug cannot be empty.")
        return value

    def validate_brochure_id(self, value: int | None) -> int | None:
        """Validate brochure ID format - existence will be validated in service layer."""
        if value is not None and value <= 0:
            raise serializers.ValidationError("Brochure ID must be a positive integer.")
        return value


class PutUpdateProductRequest(serializers.Serializer):
    """Serializer for updating an existing product."""

    slug = serializers.CharField(
        max_length=255, required=False, help_text="Unique URL slug for the product"
    )
    name = serializers.CharField(
        max_length=255, required=False, help_text="Product name"
    )
    lang = serializers.CharField(
        max_length=10, required=False, help_text="Language code (e.g., 'en', 'id')"
    )
    model = serializers.CharField(
        max_length=100, allow_blank=True, required=False, help_text="Product model/code"
    )
    size = serializers.CharField(
        max_length=100,
        allow_blank=True,
        required=False,
        help_text="Product size specifications",
    )
    description = serializers.CharField(
        allow_blank=True, required=False, help_text="Product description"
    )
    product_type = serializers.ChoiceField(
        choices=ProductType.choices,
        allow_blank=True,
        required=False,
        help_text="Product type (lantai/dinding)",
    )
    image = serializers.ImageField(
        required=False,
        allow_empty_file=True,
        use_url=False,
        help_text="Product main image",
    )
    gallery = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=True, use_url=False),
        required=False,
        allow_empty=True,
        help_text="Product gallery images",
    )
    brochure_id = serializers.IntegerField(
        required=False, allow_null=True, help_text="ID of associated brochure"
    )
    meta_title = serializers.CharField(
        max_length=255, allow_blank=True, required=False, help_text="SEO meta title"
    )
    meta_description = serializers.CharField(
        allow_blank=True, required=False, help_text="SEO meta description"
    )
    meta_keywords = serializers.CharField(
        allow_blank=True, required=False, help_text="SEO meta keywords"
    )
    is_active = serializers.BooleanField(
        required=False, help_text=PRODUCT_ACTIVE_STATUS_HELP
    )

    def validate_slug(self, value: str) -> str:
        """Validate slug format and basic requirements - uniqueness will be validated in service layer."""
        if not value or not value.strip():
            raise serializers.ValidationError("Slug cannot be empty.")
        return value

    def validate_brochure_id(self, value: int | None) -> int | None:
        """Validate brochure ID format - existence will be validated in service layer."""
        if value is not None and value <= 0:
            raise serializers.ValidationError("Brochure ID must be a positive integer.")
        return value


class PatchToggleProductStatusRequest(serializers.Serializer):
    """Serializer for toggling product active status."""

    is_active = serializers.BooleanField(help_text=PRODUCT_ACTIVE_STATUS_HELP)


class PostUploadProductImageRequest(serializers.Serializer):
    """Serializer for uploading product main image."""

    image = serializers.ImageField(
        required=True,
        allow_empty_file=False,
        use_url=False,
        help_text="Product main image to upload",
    )


class PostUploadProductGalleryRequest(serializers.Serializer):
    """Serializer for uploading product gallery images."""

    gallery = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        required=True,
        allow_empty=False,
        help_text="Product gallery images to upload",
    )


class ProductFilterSerializer(serializers.Serializer):
    """Serializer for product filtering query parameters."""

    product_type = serializers.ChoiceField(
        choices=ProductType.choices, required=False, help_text="Filter by product type"
    )
    lang = serializers.CharField(
        max_length=10, required=False, help_text="Filter by language code"
    )
    search = serializers.CharField(
        required=False, help_text="Search in name, description, and model"
    )
    is_active = serializers.BooleanField(
        required=False, help_text="Filter by active status"
    )
