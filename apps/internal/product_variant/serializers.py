from typing import List
from rest_framework import serializers

from core.models import ProductVariant, ProductSpecification


class ProductSpecificationNestedSerializer(serializers.ModelSerializer):
    """Serializer for ProductSpecification model."""

    class SpecificationMasterSerializer(serializers.ModelSerializer):
        """Serializer for the Specification master data."""

        class Meta:
            model = ProductSpecification._meta.get_field("specification").related_model
            fields = ["slug", "label", "icon"]

    specification = SpecificationMasterSerializer(read_only=True)

    class Meta:
        model = ProductSpecification
        fields = [
            "id",
            "specification",
            "value",
            "is_active",
            "created_at",
            "updated_at",
        ]


class ProductVariantModelSerializer(serializers.ModelSerializer):
    """Serializer for ProductVariant model."""

    product_name = serializers.CharField(source="product.name", read_only=True)
    product_slug = serializers.CharField(source="product.slug", read_only=True)
    specifications = ProductSpecificationNestedSerializer(
        source="product_specifications", many=True, read_only=True
    )

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "product",
            "product_name",
            "product_slug",
            "sku",
            "model",
            "size",
            "description",
            "image",
            "is_active",
            "specifications",
            "created_at",
        ]


class SpecificationValueSerializer(serializers.Serializer):
    """Serializer for specification value input."""

    specification_slug = serializers.CharField(
        max_length=150,
        help_text="Slug of the specification (required, max 150 characters)",
    )
    value = serializers.CharField(
        help_text="Value for the specification (required)",
    )


class PostCreateProductVariantRequest(serializers.Serializer):
    """Serializer for creating a new product variant."""

    sku = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        help_text="Stock Keeping Unit - unique identifier (optional, max 100 characters)",
    )
    model = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        help_text="Model name or code (optional, max 100 characters)",
    )
    size = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        help_text="Size specification (optional, max 100 characters, e.g., '60x60 cm')",
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Detailed description of the variant (optional)",
    )
    image = serializers.ImageField(
        required=False,
        allow_null=True,
        help_text="Variant image (optional)",
    )
    is_active = serializers.BooleanField(
        required=False,
        help_text="Whether the variant is active and visible (optional, default: true)",
    )
    specifications = serializers.JSONField(
        required=False,
        help_text='JSON array of specifications with their values (optional). Example: [{"specification_slug": "color", "value": "red"}]',
    )

    def validate_specifications(self, value):
        """Validate and parse specifications data."""
        if not value:
            return []

        # If it's a string, parse it
        if isinstance(value, str):
            import json

            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError(
                    "Invalid JSON format for specifications"
                )

        # Ensure it's a list
        if not isinstance(value, list):
            value = [value]

        # Validate each specification
        validated_specs = []
        for spec in value:
            if not isinstance(spec, dict):
                raise serializers.ValidationError(
                    "Each specification must be an object"
                )
            if "specification_slug" not in spec or "value" not in spec:
                raise serializers.ValidationError(
                    "Each specification must have 'specification_slug' and 'value' fields"
                )
            validated_specs.append(spec)

        return validated_specs


class PutUpdateProductVariantRequest(serializers.Serializer):
    """Serializer for updating an existing product variant."""

    sku = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        help_text="Stock Keeping Unit - unique identifier (optional, max 100 characters)",
    )
    model = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        help_text="Model name or code (optional, max 100 characters)",
    )
    size = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        help_text="Size specification (optional, max 100 characters)",
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Detailed description of the variant (optional)",
    )
    image = serializers.ImageField(
        required=False,
        allow_null=True,
        help_text="Variant image (optional)",
    )
    is_active = serializers.BooleanField(
        required=False,
        help_text="Whether the variant is active and visible (optional)",
    )

    def validate(self, attrs):
        """Validate that at least one field is provided for update."""
        if not attrs:
            raise serializers.ValidationError(
                "At least one field must be provided for update."
            )
        return attrs


class PatchToggleProductVariantStatusRequest(serializers.Serializer):
    """Serializer for toggling product variant active status."""

    is_active = serializers.BooleanField(
        required=True,
        help_text="New active status for the variant (required)",
    )


class PostUpdateProductVariantSpecificationsRequest(serializers.Serializer):
    """Serializer for adding/updating variant specifications."""

    specifications = SpecificationValueSerializer(
        many=True,
        required=True,
        help_text="List of specifications with their values",
    )
