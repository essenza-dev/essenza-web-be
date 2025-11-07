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

    @staticmethod
    def get_profile(func):
        """
        Decorator for get authenticated user profile endpoint documentation
        """

        @extend_schema(
            tags=[TAGS],
            summary="Get Authenticated User Profile",
            description="Endpoint to retrieve the profile of the authenticated user",
            responses={
                200: {
                    "description": "User profile retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "User profile retrieved successfully",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "username": {"type": "string", "example": "ruriazz"},
                                "name": {"type": "string", "example": "aziz ruri"},
                                "email": {
                                    "type": "string",
                                    "example": "me@ruriazz.com",
                                },
                                "role": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string", "example": "editor"},
                                        "label": {
                                            "type": "string",
                                            "example": "Editor",
                                        },
                                    },
                                },
                                "is_active": {"type": "boolean", "example": True},
                                "last_login": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-07T23:01:05.412277+07:00",
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-05T18:58:09.201000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-07T21:47:31.094337+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-07T23:20:19.170921",
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
    def update_profile(func):
        """
        Decorator for update authenticated user profile endpoint documentation
        """

        @extend_schema(
            tags=[TAGS],
            summary="Update Authenticated User Profile",
            description="Endpoint to update the profile of the authenticated user",
            request=serializers.PatchAuthUserProfileRequest,
            responses={
                200: {
                    "description": "User profile updated successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "User profile updated successfully",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "username": {"type": "string", "example": "ruriazz"},
                                "name": {"type": "string", "example": "aziz ruri"},
                                "email": {
                                    "type": "string",
                                    "example": "me@ruriazz.com",
                                },
                                "role": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string", "example": "editor"},
                                        "label": {
                                            "type": "string",
                                            "example": "Editor",
                                        },
                                    },
                                },
                                "is_active": {"type": "boolean", "example": True},
                                "last_login": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-07T23:01:05.412277+07:00",
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-05T18:58:09.201000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-07T21:47:31.094337+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-07T23:20:19.170921",
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
    def change_password(func):
        """
        Decorator for change authenticated user password endpoint documentation
        """

        @extend_schema(
            tags=[TAGS],
            summary="Change Authenticated User Password",
            description="Endpoint to change the password of the authenticated user",
            request=serializers.PutAuthUserPasswordRequest,
            responses={
                200: {
                    "description": "Password changed successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {"type": "string", "example": "Password changed successfully"},
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
