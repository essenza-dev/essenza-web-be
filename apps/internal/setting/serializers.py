from rest_framework import serializers
from core.models import Setting


class SettingModelSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving application settings
    """

    class Meta:
        model = Setting
        fields = "__all__"


class PostCreateSettingRequest(serializers.Serializer):
    """
    Serializer for creating or updating application settings
    """

    slug = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    label = serializers.CharField(max_length=100, required=True)
    value = serializers.CharField()
    description = serializers.CharField(allow_blank=True, required=False)
    is_active = serializers.BooleanField(required=True)
