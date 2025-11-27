from typing import Any
from rest_framework import serializers
from utils.captcha.serializers import UseCaptchaSerializer


class PostAuthTokenRequest(UseCaptchaSerializer):
    """
    User login request schema.
    """

    username = serializers.CharField(
        trim_whitespace=True,
        required=True,
        min_length=5,
        help_text="Username or email address for login",
    )
    password = serializers.CharField(
        required=True, min_length=8, help_text="User password"
    )


class PostAuthTokenResponse(serializers.Serializer):
    """
    User login response schema.
    """

    token = serializers.CharField(help_text="JWT token for authenticated access")
    refresh_token = serializers.CharField(
        help_text="JWT refresh token for obtaining new access tokens"
    )


class PutAuthTokenRequest(serializers.Serializer):
    """
    User token refresh request schema.
    """

    refresh_token = serializers.CharField(
        help_text="JWT refresh token for obtaining new access tokens"
    )


class GetAuthUserProfileResponse(serializers.ModelSerializer):
    """
    Authenticated user profile response schema.
    """

    class RoleSerializer(serializers.Serializer):
        name = serializers.CharField(help_text="Name of the role")
        label = serializers.CharField(help_text="Label of the role")

    role = serializers.SerializerMethodField()

    def get_role(self, obj) -> serializers.ReturnList | Any | serializers.ReturnDict:
        return self.RoleSerializer(
            instance={"name": obj.role, "label": obj.get_role_display()}
        ).data

    class Meta:
        from core.models import User

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

class PatchAuthUserProfileRequest(serializers.Serializer):
    """
    Authenticated user profile update request schema.
    """

    username = serializers.CharField(
        required=False, allow_null=True, min_length=5, max_length=100, help_text="Username of the user"
    )
    name = serializers.CharField(
        required=False, allow_null=True, allow_blank=True, max_length=255, help_text="Full name of the user"
    )
    email = serializers.EmailField(
        required=False, allow_null=True, help_text="Email address of the user"
    )

class PutAuthUserPasswordRequest(serializers.Serializer):
    """
    Authenticated user password change request schema.
    """

    current_password = serializers.CharField(
        required=True, min_length=8, help_text="Current password of the user"
    )
    new_password = serializers.CharField(
        required=True, min_length=8, help_text="New password for the user"
    )
