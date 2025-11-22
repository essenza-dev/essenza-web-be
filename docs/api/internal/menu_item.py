from functools import wraps
from drf_spectacular.utils import extend_schema

from apps.internal.menu_item import serializers

TAGS = ["Internal / Menu Item"]


class MenuItemAPI:
    """API documentation for Menu Item endpoints."""

    @staticmethod
    def create_menu_item(func):
        """Decorator for documenting the create_menu_item endpoint."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_create_menu_item",
            summary="Create Menu Item",
            description="Create a new menu item.",
            request=serializers.PostCreateMenuItemRequest,
            responses={
                201: {
                    "description": "Menu item created successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 201},
                        "message": {
                            "type": "string",
                            "example": "Menu item created successfully",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 10},
                                "menu": {"type": "integer", "example": 5},
                                "parent": {
                                    "type": "integer",
                                    "nullable": True,
                                    "example": 7,
                                },
                                "lang": {"type": "string", "example": "en"},
                                "label": {
                                    "type": "string",
                                    "example": "first menu item",
                                },
                                "link": {"type": "string", "example": "linkasas"},
                                "order_no": {"type": "integer", "example": 0},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-22T23:28:54.731251+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-22T23:28:54.739308",
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
                            "example": "Menu with id '51' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-22T23:28:15.860902",
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
                                    "field": {"type": "string", "example": "menu_id"},
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
                                    "example": "2025-11-22T23:23:17.220288",
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
        """Decorator for documenting the get_menu_items endpoint."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_get_menu_items",
            summary="Get Menu Items",
            description="Retrieve all menu items.",
            responses={
                200: {
                    "description": "Menu items retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Menu items retrieved successfully",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "example": 10},
                                    "menu": {"type": "integer", "example": 5},
                                    "parent": {
                                        "type": ["integer", "null"],
                                        "example": 7,
                                    },
                                    "lang": {"type": "string", "example": "en"},
                                    "label": {
                                        "type": "string",
                                        "example": "first menu item",
                                    },
                                    "link": {"type": "string", "example": "linkasas"},
                                    "order_no": {"type": "integer", "example": 0},
                                    "created_at": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2025-11-22T23:28:54.731251+07:00",
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
                                    "example": "2025-11-22T23:31:07.208419",
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
    def get_specific_menu_item(func):
        """Decorator for documenting the get_specific_menu_item endpoint."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_get_specific_menu_item",
            summary="Get Specific Menu Item",
            description="Retrieve a specific menu item by its ID.",
            responses={
                200: {
                    "description": "Menu item retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Menu item retrieved successfully",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 2},
                                "menu": {"type": "integer", "example": 5},
                                "parent": {
                                    "type": ["integer", "null"],
                                    "example": None,
                                },
                                "lang": {"type": "string", "example": "en"},
                                "label": {
                                    "type": "string",
                                    "example": "first menu item",
                                },
                                "link": {"type": "string", "example": "linkasas"},
                                "order_no": {"type": "integer", "example": 0},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-22T23:19:06.970907+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-22T23:34:26.621686",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Menu item not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "MenuItem with id '112' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-22T23:35:01.660931",
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
    def update_specific_menu_item(func):
        """Decorator for documenting the update_specific_menu_item endpoint."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_update_specific_menu_item",
            summary="Update Specific Menu Item",
            description="Update a specific menu item by its ID.",
            request=serializers.PatchUpdateMenuItemRequest,
            responses={
                200: {
                    "description": "Menu item updated successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Menu item updated successfully",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 3},
                                "menu": {"type": "integer", "example": 5},
                                "parent": {
                                    "type": ["integer", "null"],
                                    "example": None,
                                },
                                "lang": {"type": "string", "example": "en"},
                                "label": {
                                    "type": "string",
                                    "example": "first menu item",
                                },
                                "link": {"type": "string", "example": "linkasas"},
                                "order_no": {"type": "integer", "example": 0},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-22T23:19:24.021994+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-22T23:50:32.768143",
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
                            "example": "Menu with id '171' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-22T23:52:37.374021",
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
    def delete_specific_menu_item(func):
        """Decorator for documenting the delete_specific_menu_item endpoint."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_delete_specific_menu_item",
            summary="Delete Specific Menu Item",
            description="Delete a specific menu item by its ID.",
            responses={
                200: {
                    "description": "Menu item deleted successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Menu item deleted successfully",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-22T23:54:17.921024",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "MenuItem not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "MenuItem with id '2' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-22T23:54:49.696625",
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
