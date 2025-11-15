from functools import wraps
from drf_spectacular.utils import extend_schema

from apps.internal.menu import serializers

TAGS = ["Internal / Menu"]


class MenuAPI:
    """API documentation for Menu related endpoints."""

    @staticmethod
    def get_menu(func):

        @extend_schema(
            operation_id="int_v1_get_menu",
            tags=TAGS,
            summary="Get Application Menu",
            description="Endpoint to retrieve the application menu structure.",
            responses={
                200: {
                    "description": "Menus retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Menus retrieved successfully",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "example": 5},
                                    "items": {
                                        "type": "array",
                                        "items": {},
                                        "example": [],
                                    },
                                    "name": {"type": "string", "example": "Contact"},
                                    "position": {"type": "string", "example": "header"},
                                    "created_at": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2025-11-16T03:09:27.416438+07:00",
                                    },
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-16T03:09:30.434680",
                                }
                            },
                        },
                    },
                },
            },
        )
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def create_menu(func):

        @extend_schema(
            operation_id="int_v1_create_menu",
            tags=TAGS,
            summary="Create Application Menu",
            description="Endpoint to create a new application menu.",
            request=serializers.PostCreateMenuRequest,
            responses={
                200: {
                    "description": "Menu created successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Menu created successfully",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 4},
                                "items": {
                                    "type": "array",
                                    "items": {},  # struktur kosong sesuai response
                                    "example": [],
                                },
                                "name": {"type": "string", "example": "About"},
                                "position": {"type": "string", "example": "header"},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-16T03:06:17.942393+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-16T03:06:17.958291",
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
                                    "field": {"type": "string", "example": "position"},
                                    "message": {
                                        "type": "string",
                                        "example": '"invalidpos" is not a valid choice.',
                                    },
                                    "code": {
                                        "type": "string",
                                        "example": "invalid_choice",
                                    },
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-16T03:08:02.321171",
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
    def get_specific_menu(func):

        @extend_schema(
            operation_id="int_v1_specific_menu_get",
            tags=TAGS,
            summary="Get Specific Application Menu",
            description="Endpoint to retrieve a specific application menu by its ID.",
            responses={
                200: {
                    "description": "Menu updated successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Menu updated successfully",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 4},
                                "items": {
                                    "type": "array",
                                    "items": {},
                                    "example": [],
                                },
                                "name": {"type": "string", "example": "About"},
                                "position": {"type": "string", "example": "header"},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-16T03:06:17.942393+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-16T03:10:14.853766",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Menu not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Menu with id '44' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-16T03:10:46.083547",
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
    def update_specific_menu(func):

        @extend_schema(
            operation_id="int_v1_specific_menu_update",
            tags=TAGS,
            summary="Update Specific Application Menu",
            description="Endpoint to update a specific application menu by its ID.",
            request=serializers.PatchUpdateMenuRequest,
            responses={
                200: {
                    "description": "Menu deleted successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Menu deleted successfully",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-16T03:11:44.940787",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Menu not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Menu with id '55' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-16T03:14:23.217170",
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
                                    "field": {"type": "string", "example": "name"},
                                    "message": {
                                        "type": "string",
                                        "example": "This field may not be null.",
                                    },
                                    "code": {"type": "string", "example": "null"},
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-16T03:15:29.496915",
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
    def delete_specific_menu(func):

        @extend_schema(
            operation_id="int_v1_specific_menu_delete",
            tags=TAGS,
            summary="Delete Specific Application Menu",
            description="Endpoint to delete a specific application menu by its ID.",
            responses={
                200: {
                    "description": "Menu deleted successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Menu deleted successfully",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-16T03:11:44.940787",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Menu not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Menu with id '44' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-16T03:10:46.083547",
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
    def get_menu_items(func):
        @extend_schema(
            operation_id="int_v1_menu_items_get",
            tags=TAGS,
            summary="Get Menu Items",
            description="Endpoint to retrieve all items for a specific menu.",
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
