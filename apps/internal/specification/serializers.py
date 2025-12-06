from rest_framework import serializers

from core.models import Specification


class SpecificationModelSerializer(serializers.ModelSerializer):
    """Serializer for Specification model."""

    class Meta:
        model = Specification
        fields = [
            "id",
            "slug",
            "label",
            "icon",
            "is_active",
            "created_at",
        ]


class PutUpdateSpecificationRequest(serializers.Serializer):
    """Serializer for updating an existing specification."""

    is_active = serializers.BooleanField(
        required=False,
        help_text="Whether the specification is active and visible (optional, default: true)",
    )

    def validate(self, attrs):
        """Validate that at least one field is provided for update."""
        if not attrs:
            raise serializers.ValidationError(
                "At least one field must be provided for update."
            )
        return attrs
