from typing import Optional
from rest_framework import serializers
from decimal import Decimal

from core.models import Store


class StoreModelSerializer(serializers.ModelSerializer):
    """Serializer for Store model."""

    class Meta:
        model = Store
        fields = [
            "id",
            "name",
            "address",
            "phone",
            "email",
            "latitude",
            "longitude",
            "created_at",
        ]


class PostCreateStoreRequest(serializers.Serializer):
    """Serializer for creating a new store with validation."""

    name = serializers.CharField(
        max_length=255,
        help_text="Full name of the store or showroom (required, max 255 characters)",
    )
    address = serializers.CharField(
        help_text="Complete address including street, city, and postal code (required)"
    )
    phone = serializers.CharField(
        max_length=50,
        allow_blank=True,
        required=False,
        help_text="Contact phone number (optional, max 50 characters, e.g., +62-21-1234567)",
    )
    email = serializers.EmailField(
        max_length=100,
        allow_blank=True,
        required=False,
        help_text="Contact email address (optional, max 100 characters, must be valid email format)",
    )
    latitude = serializers.DecimalField(
        max_digits=10,
        decimal_places=6,
        required=False,
        allow_null=True,
        help_text="Latitude coordinate for map display (optional, -90 to 90 degrees)",
    )
    longitude = serializers.DecimalField(
        max_digits=10,
        decimal_places=6,
        required=False,
        allow_null=True,
        help_text="Longitude coordinate for map display (optional, -180 to 180 degrees)",
    )

    def validate_latitude(self, value: Optional[Decimal]) -> Optional[Decimal]:
        """Validate latitude is within valid range."""
        if value is not None and (value < -90 or value > 90):
            raise serializers.ValidationError(
                "Latitude must be between -90 and 90 degrees."
            )
        return value

    def validate_longitude(self, value: Optional[Decimal]) -> Optional[Decimal]:
        """Validate longitude is within valid range."""
        if value is not None and (value < -180 or value > 180):
            raise serializers.ValidationError(
                "Longitude must be between -180 and 180 degrees."
            )
        return value


class PostUpdateStoreRequest(serializers.Serializer):
    """Serializer for partial updates to existing store records."""

    name = serializers.CharField(
        max_length=255,
        required=False,
        allow_null=True,
        help_text="Full name of the store or showroom (optional, max 255 characters)",
    )
    address = serializers.CharField(
        required=False,
        allow_null=True,
        help_text="Complete address including street, city, and postal code (optional)",
    )
    phone = serializers.CharField(
        max_length=50,
        allow_blank=True,
        allow_null=True,
        required=False,
        help_text="Contact phone number (optional, max 50 characters, e.g., +62-21-1234567)",
    )
    email = serializers.EmailField(
        max_length=100,
        allow_blank=True,
        allow_null=True,
        required=False,
        help_text="Contact email address (optional, max 100 characters, must be valid email format)",
    )
    latitude = serializers.DecimalField(
        max_digits=10,
        decimal_places=6,
        required=False,
        allow_null=True,
        help_text="Latitude coordinate for map display (optional, -90 to 90 degrees)",
    )
    longitude = serializers.DecimalField(
        max_digits=10,
        decimal_places=6,
        required=False,
        allow_null=True,
        help_text="Longitude coordinate for map display (optional, -180 to 180 degrees)",
    )

    def validate_latitude(self, value: Optional[Decimal]) -> Optional[Decimal]:
        """Validate latitude is within valid range."""
        if value is not None and (value < -90 or value > 90):
            raise serializers.ValidationError(
                "Latitude must be between -90 and 90 degrees."
            )
        return value

    def validate_longitude(self, value: Optional[Decimal]) -> Optional[Decimal]:
        """Validate longitude is within valid range."""
        if value is not None and (value < -180 or value > 180):
            raise serializers.ValidationError(
                "Longitude must be between -180 and 180 degrees."
            )
        return value
