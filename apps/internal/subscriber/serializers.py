from rest_framework import serializers

from core.models import Subscriber


class SubscriberModelSerializer(serializers.ModelSerializer):
    """Serializer for Subscriber model."""

    class Meta:
        model = Subscriber
        fields = '__all__'