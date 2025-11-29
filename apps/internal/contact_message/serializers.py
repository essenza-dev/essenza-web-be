from rest_framework import serializers

from core.models import ContactMessage


class ContactMessageModelSerializer(serializers.ModelSerializer):
    """Serializer for ContactMessage model."""

    class Meta:
        model = ContactMessage
        fields = "__all__"


class PostMarkAsReadContactMessageSerializer(serializers.Serializer):
    """Serializer for marking contact message as read/unread."""

    is_read = serializers.BooleanField(
        required=True,
        help_text="Mark message as read (true) or unread (false).",
    )
