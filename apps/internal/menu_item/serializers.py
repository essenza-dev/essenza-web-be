from rest_framework import serializers

from core.models import MenuItem
from core.enums import Language


class MenuItemModelSerializer(serializers.ModelSerializer):
    """Serializer for MenuItem model."""

    menu = serializers.PrimaryKeyRelatedField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = MenuItem
        fields = "__all__"


class PostCreateMenuItemRequest(serializers.Serializer):
    """Serializer for creating a new MenuItem."""

    menu_id = serializers.IntegerField(required=True)
    lang = serializers.ChoiceField(
        choices=Language.choices, required=False, default=Language.EN
    )
    label = serializers.CharField(max_length=255, required=True)
    link = serializers.CharField(max_length=255, required=True)
    parent_id = serializers.IntegerField(required=False, allow_null=True)
    order_no = serializers.IntegerField(required=False, default=0)


class PatchUpdateMenuItemRequest(serializers.Serializer):
    """Serializer for updating an existing MenuItem."""

    menu_id = serializers.IntegerField(required=False, allow_null=True)
    lang = serializers.ChoiceField(
        choices=Language.choices, required=False, allow_null=True
    )
    label = serializers.CharField(max_length=255, required=False, allow_null=True)
    link = serializers.CharField(max_length=255, required=False, allow_null=True)
    parent_id = serializers.IntegerField(required=False, allow_null=True)
    order_no = serializers.IntegerField(required=False, allow_null=True)
