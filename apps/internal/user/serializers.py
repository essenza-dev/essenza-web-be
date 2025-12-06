from rest_framework import serializers

from core.models import User
from core.enums import UserRole


class UserModelSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class RoleSerializer(serializers.Serializer):
        name = serializers.CharField(help_text="Name of the role")
        label = serializers.CharField(help_text="Label of the role")

    role = serializers.SerializerMethodField()

    def get_role(self, obj) -> dict:
        return {"name": obj.role, "label": obj.get_role_display()}

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "name",
            "email",
            "role",
            "is_active",
            "last_login",
            "created_at",
            "updated_at",
        ]


class PostCreateUserRequest(serializers.Serializer):
    """Serializer for creating a new user."""

    username = serializers.CharField(
        required=True,
        min_length=5,
        max_length=100,
        help_text="Unique username for the user",
    )
    name = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255,
        help_text="Full name of the user",
    )
    email = serializers.EmailField(required=True, help_text="Email address of the user")
    password = serializers.CharField(
        required=True, min_length=8, help_text="Password for the user"
    )
    role = serializers.ChoiceField(
        required=True, choices=UserRole.choices, help_text="Role assigned to the user"
    )
    is_active = serializers.BooleanField(
        required=False, help_text="Whether the user is active"
    )


class PutUpdateUserRequest(serializers.Serializer):
    """Serializer for updating an existing user."""

    username = serializers.CharField(
        required=False,
        min_length=5,
        max_length=100,
        help_text="Unique username for the user",
    )
    name = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255,
        help_text="Full name of the user",
    )
    email = serializers.EmailField(
        required=False, help_text="Email address of the user"
    )
    role = serializers.ChoiceField(
        required=False, choices=UserRole.choices, help_text="Role assigned to the user"
    )
    is_active = serializers.BooleanField(
        required=False, help_text="Whether the user is active"
    )


class PutChangeUserPasswordRequest(serializers.Serializer):
    """Serializer for changing user password by admin."""

    new_password = serializers.CharField(
        required=True, min_length=8, help_text="New password for the user"
    )


class GetUserRolesResponse(serializers.Serializer):
    """Serializer for user roles response."""

    name = serializers.CharField(help_text="Role name")
    label = serializers.CharField(help_text="Role label")
