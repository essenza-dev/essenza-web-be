from rest_framework import serializers

from core.models import Subscriber
from utils.captcha import UseCaptchaSerializer


class SubscriberModelSerializer(serializers.ModelSerializer):
    """Serializer for Subscriber model."""

    class Meta:
        model = Subscriber
        fields = ["email", "created_at"]


class PostCreateSubscriberSerializer(UseCaptchaSerializer):
    """Serializer for creating a new subscriber with CAPTCHA validation."""

    email = serializers.EmailField(
        required=True,
        help_text="Email address of the subscriber.",
    )
