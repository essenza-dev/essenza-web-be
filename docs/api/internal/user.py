from functools import wraps
from drf_spectacular.utils import extend_schema

from apps.internal.user import serializers
from docs.api.constants import DEFAULT_PAGINATION_PARAMS

TAGS = ["Internal / Users"]


class UserAPI:
    """API schema definitions for User endpoints."""

    @staticmethod
    def create_user_schema(func):
        """Schema for creating a new user."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_user_create_user",
            summary="Create User",
            description="Create a new user with specified role and permissions.",
            request=serializers.PostCreateUserRequest,
            responses={
                200: {
                    "description": "User created successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "User created successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "username": {"type": "string", "example": "johndoe"},
                                "name": {"type": "string", "example": "John Doe"},
                                "email": {
                                    "type": "string",
                                    "example": "john.doe@example.com",
                                },
                                "role": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string", "example": "admin"},
                                        "label": {"type": "string", "example": "Admin"},
                                    },
                                },
                                "is_active": {"type": "boolean", "example": True},
                                "last_login": {
                                    "type": "string",
                                    "format": "date-time",
                                    "nullable": True,
                                    "example": None,
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.000000",
                                }
                            },
                        },
                    },
                },
                422: {
                    "description": "Data validation failed",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 422},
                        "message": {
                            "type": "string",
                            "example": "Data validation failed",
                        },
                        "errors": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "field": {"type": "string", "example": "email"},
                                    "message": {
                                        "type": "string",
                                        "example": "Enter a valid email address.",
                                    },
                                    "code": {"type": "string", "example": "invalid"},
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.000000",
                                }
                            },
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def get_users_schema(func):
        """Schema for retrieving all users."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_user_get_users",
            summary="Retrieve all users",
            description="Retrieve all users with pagination support.",
            parameters=DEFAULT_PAGINATION_PARAMS,
            responses={
                200: {
                    "description": "Users retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Users retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "example": 1},
                                    "username": {
                                        "type": "string",
                                        "example": "johndoe",
                                    },
                                    "name": {"type": "string", "example": "John Doe"},
                                    "email": {
                                        "type": "string",
                                        "example": "john.doe@example.com",
                                    },
                                    "role": {
                                        "type": "object",
                                        "properties": {
                                            "name": {
                                                "type": "string",
                                                "example": "admin",
                                            },
                                            "label": {
                                                "type": "string",
                                                "example": "Admin",
                                            },
                                        },
                                    },
                                    "is_active": {"type": "boolean", "example": True},
                                    "last_login": {
                                        "type": "string",
                                        "format": "date-time",
                                        "nullable": True,
                                        "example": "2025-12-05T15:30:00.000000+07:00",
                                    },
                                    "created_at": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2025-12-01T10:00:00.000000+07:00",
                                    },
                                    "updated_at": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2025-12-05T10:00:00.000000+07:00",
                                    },
                                },
                            },
                        },
                        "pagination": {
                            "type": "object",
                            "properties": {
                                "current_page": {"type": "integer", "example": 1},
                                "per_page": {"type": "integer", "example": 20},
                                "total_pages": {"type": "integer", "example": 1},
                                "total_items": {"type": "integer", "example": 5},
                                "has_next": {"type": "boolean", "example": False},
                                "has_previous": {"type": "boolean", "example": False},
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.000000",
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
    def get_specific_user_schema(func):
        """Schema for retrieving a specific user by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_user_get_specific_user",
            summary="Retrieve a specific user by ID",
            description="Retrieve a specific user by its ID.",
            responses={
                200: {
                    "description": "User retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "User retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "username": {"type": "string", "example": "johndoe"},
                                "name": {"type": "string", "example": "John Doe"},
                                "email": {
                                    "type": "string",
                                    "example": "john.doe@example.com",
                                },
                                "role": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string", "example": "admin"},
                                        "label": {"type": "string", "example": "Admin"},
                                    },
                                },
                                "is_active": {"type": "boolean", "example": True},
                                "last_login": {
                                    "type": "string",
                                    "format": "date-time",
                                    "nullable": True,
                                    "example": "2025-12-05T15:30:00.000000+07:00",
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-01T10:00:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-05T10:00:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.000000",
                                }
                            },
                        },
                    },
                },
                404: {
                    "description": "User not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 404},
                        "message": {
                            "type": "string",
                            "example": "User with id '999' does not exist.",
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def get_user_roles_schema(func):
        """Schema for retrieving all user roles."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_user_get_user_roles",
            summary="Retrieve all user roles",
            description="Retrieve all available user roles.",
            responses={
                200: {
                    "description": "User roles retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "User roles retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string", "example": "superadmin"},
                                    "label": {
                                        "type": "string",
                                        "example": "Super Admin",
                                    },
                                },
                            },
                            "example": [
                                {"name": "superadmin", "label": "Super Admin"},
                                {"name": "admin", "label": "Admin"},
                                {"name": "editor", "label": "Editor"},
                            ],
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.000000",
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
    def update_specific_user_schema(func):
        """Schema for updating a specific user by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_user_update_specific_user",
            summary="Update a specific user by ID",
            description="Update a specific user by its ID.",
            request=serializers.PutUpdateUserRequest,
            responses={
                200: {
                    "description": "User updated successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "User updated successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "username": {"type": "string", "example": "johndoe"},
                                "name": {
                                    "type": "string",
                                    "example": "John Doe Updated",
                                },
                                "email": {
                                    "type": "string",
                                    "example": "john.doe@example.com",
                                },
                                "role": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string", "example": "admin"},
                                        "label": {"type": "string", "example": "Admin"},
                                    },
                                },
                                "is_active": {"type": "boolean", "example": True},
                                "last_login": {
                                    "type": "string",
                                    "format": "date-time",
                                    "nullable": True,
                                    "example": "2025-12-05T15:30:00.000000+07:00",
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-01T10:00:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.000000",
                                }
                            },
                        },
                    },
                },
                404: {
                    "description": "User not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 404},
                        "message": {
                            "type": "string",
                            "example": "User with id '999' does not exist.",
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def delete_specific_user_schema(func):
        """Schema for deleting a specific user by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_user_delete_specific_user",
            summary="Delete a specific user by ID",
            description="Delete a specific user by its ID.",
            responses={
                200: {
                    "description": "User deleted successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "User deleted successfully.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.000000",
                                }
                            },
                        },
                    },
                },
                404: {
                    "description": "User not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 404},
                        "message": {
                            "type": "string",
                            "example": "User with id '999' does not exist.",
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def toggle_user_status_schema(func):
        """Schema for toggling user active status."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_user_toggle_user_status",
            summary="Toggle user active status",
            description="Toggle the active status of a user.",
            responses={
                200: {
                    "description": "User status toggled successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "User status toggled to inactive.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "username": {"type": "string", "example": "johndoe"},
                                "name": {"type": "string", "example": "John Doe"},
                                "email": {
                                    "type": "string",
                                    "example": "john.doe@example.com",
                                },
                                "role": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string", "example": "admin"},
                                        "label": {"type": "string", "example": "Admin"},
                                    },
                                },
                                "is_active": {"type": "boolean", "example": False},
                                "last_login": {
                                    "type": "string",
                                    "format": "date-time",
                                    "nullable": True,
                                    "example": "2025-12-05T15:30:00.000000+07:00",
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-01T10:00:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.000000",
                                }
                            },
                        },
                    },
                },
                404: {
                    "description": "User not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 404},
                        "message": {
                            "type": "string",
                            "example": "User with id '999' does not exist.",
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def change_user_password_schema(func):
        """Schema for changing user password by admin."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_user_change_user_password",
            summary="Change user password",
            description="Change user password by admin. Does not require current password.",
            request=serializers.PutChangeUserPasswordRequest,
            responses={
                200: {
                    "description": "User password changed successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "User password changed successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "username": {"type": "string", "example": "johndoe"},
                                "name": {"type": "string", "example": "John Doe"},
                                "email": {
                                    "type": "string",
                                    "example": "john.doe@example.com",
                                },
                                "role": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string", "example": "admin"},
                                        "label": {"type": "string", "example": "Admin"},
                                    },
                                },
                                "is_active": {"type": "boolean", "example": True},
                                "last_login": {
                                    "type": "string",
                                    "format": "date-time",
                                    "nullable": True,
                                    "example": "2025-12-05T15:30:00.000000+07:00",
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-01T10:00:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.000000",
                                }
                            },
                        },
                    },
                },
                404: {
                    "description": "User not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 404},
                        "message": {
                            "type": "string",
                            "example": "User with id '999' does not exist.",
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
