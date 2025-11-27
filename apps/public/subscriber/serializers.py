from rest_framework import serializers

from core.models import Subscriber

class SubscriberModelSerializer(serializers.ModelSerializer):
    """Serializer for Subscriber model."""

    class Meta:
        model = Subscriber
        fields = ['email', 'created_at']

class PostCreateSubscriberSerializer(serializers.Serializer):
    """Serializer for creating a new subscriber."""

    email = serializers.EmailField(
        required=True,
        help_text="Email address of the subscriber.",
    )
