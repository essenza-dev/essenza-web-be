from rest_framework import serializers
from core.models import Setting


class GetSettingsResponse(serializers.ModelSerializer):
    """
    Serializer for retrieving application settings
    """

    class Meta:
        model = Setting
        fields = "__all__"
