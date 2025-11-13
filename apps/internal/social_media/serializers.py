from rest_framework import serializers

from core.models import SocialMedia


class SocialMediaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = "__all__"


class PostCreateSocialMediaRequest(serializers.Serializer):
    """
    Serializer for creating a new social media entry
    """

    platform = serializers.CharField(max_length=100, required=True)
    icon = serializers.CharField(max_length=100, allow_blank=True, required=False)
    url = serializers.CharField(max_length=255)
    order_no = serializers.IntegerField(default=0)


class PatchUpdateSocialMediaRequest(serializers.Serializer):
    """
    Serializer for updating an existing social media entry
    """

    platform = serializers.CharField(max_length=100, required=False)
    icon = serializers.CharField(max_length=100, allow_blank=True, required=False)
    url = serializers.CharField(max_length=255, required=False)
    order_no = serializers.IntegerField(required=False)
