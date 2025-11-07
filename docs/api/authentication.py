from functools import wraps
from drf_spectacular.utils import extend_schema

from apps.auth import serializers

TAGS = "[02] Authentication"


class AuthenticationApi:
    """
    Documentation configuration for Authentication API endpoints
    """

    @staticmethod
    def create_auth_token(func):
        """
        Decorator for create auth token endpoint documentation
        """

        @extend_schema(
            tags=[TAGS],
            summary="Create Auth Token",
            description="Endpoint for user login with username and password",
            request=serializers.PostAuthTokenRequest,
            auth=[],
            responses={
                200: {
                    "description": "Login successful",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {"type": "string", "example": "Login successful"},
                        "data": {
                            "type": "object",
                            "properties": {
                                "token": {
                                    "type": "string",
                                    "example": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                                },
                                "refresh_token": {
                                    "type": "string",
                                    "example": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4gZXhhbXBsZQ==",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-05T17:39:56.395438",
                                }
                            },
                        },
                    },
                }
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def refresh_auth_token(func):
        """
        Decorator for refresh auth token endpoint documentation
        """

        @extend_schema(
            tags=[TAGS],
            summary="Refresh Auth Token",
            description="Endpoint for user to refresh JWT token",
            request=serializers.PutAuthTokenRequest,
            responses={
                200: {
                    "description": "Token refreshed successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Token refreshed successfully",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "token": {
                                    "type": "string",
                                    "example": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                                },
                                "refresh_token": {
                                    "type": "string",
                                    "example": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4gZXhhbXBsZQ==",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-05T17:39:56.395438",
                                }
                            },
                        },
                    },
                }
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
