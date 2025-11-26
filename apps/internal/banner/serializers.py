from rest_framework import serializers

from core.models import Banner


class BannerModelSerializer(serializers.ModelSerializer):
    """Serializer for Banner model."""

    class Meta:
        model = Banner
        fields = "__all__"


class PostCreateBannerRequest(serializers.Serializer):
    """Serializer for creating a new banner."""

    title = serializers.CharField(max_length=255)
    subtitle = serializers.CharField(max_length=255, allow_blank=True, required=False)
    image = serializers.ImageField(required=True, allow_empty_file=False, use_url=False)
    link_url = serializers.CharField(max_length=255, allow_blank=True, required=False)
    order_no = serializers.IntegerField(default=0)
    is_active = serializers.BooleanField()

class PostUpdateBannerRequest(serializers.Serializer):
    """Serializer for updating an existing banner."""

    title = serializers.CharField(max_length=255, required=False)
    subtitle = serializers.CharField(max_length=255, allow_blank=True, required=False)
    image = serializers.ImageField(required=False, allow_empty_file=True, use_url=False)
    link_url = serializers.CharField(max_length=255, allow_blank=True, required=False)
    order_no = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False)