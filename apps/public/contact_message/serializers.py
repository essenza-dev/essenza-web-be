from rest_framework import serializers

from core.models import ContactMessage
from utils.captcha import UseCaptchaSerializer


class ContactMessageModelSerializer(serializers.ModelSerializer):
    """Serializer for ContactMessage model."""

    class Meta:
        model = ContactMessage
        fields = ["id", "name", "email", "phone", "subject", "message", "created_at"]


class PostCreateContactMessageSerializer(UseCaptchaSerializer):
    """Serializer for creating a new contact message with CAPTCHA validation."""

    name = serializers.CharField(
        max_length=255,
        required=True,
        help_text="Full name of the sender.",
    )
    email = serializers.EmailField(
        required=True,
        help_text="Email address of the sender.",
    )
    phone = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True,
        help_text="Phone number of the sender (optional).",
    )
    subject = serializers.CharField(
        max_length=255,
        required=True,
        help_text="Subject of the message.",
    )
    message = serializers.CharField(
        required=True,
        help_text="Content of the message.",
    )
