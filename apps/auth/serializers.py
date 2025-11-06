from rest_framework import serializers


class PostAuthTokenRequest(serializers.Serializer):
    """
    User login request schema.
    """
    username = serializers.CharField(
        trim_whitespace=True,
        required=True,
        min_length=5,
        help_text="Username or email address for login"
    )
    password = serializers.CharField(
        required=True,
        min_length=8,
        help_text="User password"
    )

class PostAuthTokenResponse(serializers.Serializer):
    """
    User login response schema.
    """
    token = serializers.CharField(
        help_text="JWT token for authenticated access"
    )
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