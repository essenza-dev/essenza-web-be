from typing import Optional
from rest_framework import serializers

from core.models import Distributor


class DistributorModelSerializer(serializers.ModelSerializer):
    """Serializer for Distributor model."""

    class Meta:
        model = Distributor
        fields = "__all__"


class PostCreateDistributorRequest(serializers.Serializer):
    """Serializer for creating a new distributor with validation."""

    name = serializers.CharField(
        max_length=255,
        help_text="Full name of the distributor company or individual (required, max 255 characters)",
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
    website = serializers.URLField(
        max_length=255,
        allow_blank=True,
        required=False,
        help_text="Company website URL (optional, max 255 characters, e.g., https://example.com)",
    )
    latitude = serializers.DecimalField(
        max_digits=10,
        decimal_places=6,
        required=False,
        allow_null=True,
        help_text="Geographic latitude coordinate (optional, decimal format, e.g., -6.208763)",
    )
    longitude = serializers.DecimalField(
        max_digits=10,
        decimal_places=6,
        required=False,
        allow_null=True,
        help_text="Geographic longitude coordinate (optional, decimal format, e.g., 106.845599)",
    )

    def _normalize_optional_field(self, value: Optional[str]) -> Optional[str]:
        """Normalize optional string fields by converting empty strings to None."""
        return None if value == "" else value

    def validate_email(self, value: Optional[str]) -> Optional[str]:
        """Validate and normalize email field."""
        return self._normalize_optional_field(value)

    def validate_phone(self, value: Optional[str]) -> Optional[str]:
        """Validate and normalize phone field."""
        return self._normalize_optional_field(value)

    def validate_website(self, value: Optional[str]) -> Optional[str]:
        """Validate and normalize website field."""
        return self._normalize_optional_field(value)


class PostUpdateDistributorRequest(serializers.Serializer):
    """Serializer for partial updates to existing distributor records."""

    name = serializers.CharField(
        max_length=255,
        allow_blank=True,
        allow_null=True,
        required=False,
        help_text="Update distributor name (optional, max 255 characters, leave empty to keep current value)",
    )
    address = serializers.CharField(
        allow_blank=True,
        allow_null=True,
        required=False,
        help_text="Update complete address (optional, leave empty to keep current value)",
    )
    phone = serializers.CharField(
        max_length=50,
        allow_blank=True,
        allow_null=True,
        required=False,
        help_text="Update contact phone number (optional, max 50 characters, leave empty to keep current value)",
    )
    email = serializers.EmailField(
        max_length=100,
        allow_blank=True,
        allow_null=True,
        required=False,
        help_text="Update contact email address (optional, max 100 characters, must be valid email, leave empty to keep current value)",
    )
    website = serializers.URLField(
        max_length=255,
        allow_blank=True,
        allow_null=True,
        required=False,
        help_text="Update company website URL (optional, max 255 characters, must be valid URL, leave empty to keep current value)",
    )
    latitude = serializers.DecimalField(
        max_digits=10,
        decimal_places=6,
        required=False,
        allow_null=True,
        help_text="Update geographic latitude coordinate (optional, decimal format, leave null to keep current value)",
    )
    longitude = serializers.DecimalField(
        max_digits=10,
        decimal_places=6,
        required=False,
        allow_null=True,
        help_text="Update geographic longitude coordinate (optional, decimal format, leave null to keep current value)",
    )

    def _normalize_update_field(self, value: Optional[str]) -> Optional[str]:
        """Normalize update fields by converting None or empty strings to None."""
        return None if (value is None or value == "") else value

    def validate_name(self, value: Optional[str]) -> Optional[str]:
        """Validate and normalize name field for updates."""
        return self._normalize_update_field(value)

    def validate_address(self, value: Optional[str]) -> Optional[str]:
        """Validate and normalize address field for updates."""
        return self._normalize_update_field(value)

    def validate_email(self, value: Optional[str]) -> Optional[str]:
        """Validate and normalize email field for updates."""
        return self._normalize_update_field(value)

    def validate_phone(self, value: Optional[str]) -> Optional[str]:
        """Validate and normalize phone field for updates."""
        return self._normalize_update_field(value)

    def validate_website(self, value: Optional[str]) -> Optional[str]:
        """Validate and normalize website field for updates."""
        return self._normalize_update_field(value)
