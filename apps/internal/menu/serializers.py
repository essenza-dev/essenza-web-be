from rest_framework import serializers

from core.models import Menu, MenuItem
from core.enums import MenuPosition


class MenuItemModelSerializer(serializers.ModelSerializer):
    """Serializer for MenuItem model."""

    class Meta:
        model = MenuItem
        fields = "__all__"


class MenuModelSerializer(serializers.ModelSerializer):
    """Serializer for Menu model."""

    items = MenuItemModelSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = "__all__"


class PostCreateMenuRequest(serializers.Serializer):
    """Serializer for creating a new Menu."""

    name = serializers.CharField(max_length=100)
    position = serializers.ChoiceField(
        choices=[choice[0] for choice in MenuPosition.choices]
    )


class PatchUpdateMenuRequest(serializers.Serializer):
    """Serializer for updating an existing Menu."""

    name = serializers.CharField(max_length=100, required=False)
    position = serializers.ChoiceField(
        choices=[choice[0] for choice in MenuPosition.choices], required=False
    )
