from functools import wraps
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from apps.internal.store import serializers

TAGS = ["Internal / Store"]


class StoreAPI:
    """API schema definitions for Store endpoints."""

    @staticmethod
    def create_store_schema(func):
        """Schema for creating a new store."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_store_create_store",
            summary="Create Store",
            description="Create a new store or showroom with contact information and location coordinates.",
            request=serializers.PostCreateStoreRequest,
            responses={
                200: {
                    "description": "Store created successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Store created successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "name": {
                                    "type": "string",
                                    "example": "Essenza Showroom Jakarta",
                                },
                                "address": {
                                    "type": "string",
                                    "example": "Jl. Sudirman No. 123, Jakarta Pusat",
                                },
                                "phone": {
                                    "type": "string",
                                    "example": "+62-21-1234567",
                                },
                                "email": {
                                    "type": "string",
                                    "example": "jakarta@essenza.com",
                                },
                                "latitude": {"type": "string", "example": "-6.208763"},
                                "longitude": {
                                    "type": "string",
                                    "example": "106.845599",
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T19:06:14.763201+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T19:06:14.770300",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Validation error",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Email 'jakarta@essenza.com' is already in use by another store.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T19:11:39.498145",
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
                                    "field": {
                                        "type": "string",
                                        "example": "email",
                                    },
                                    "message": {
                                        "type": "string",
                                        "example": "Enter a valid email address.",
                                    },
                                    "code": {
                                        "type": "string",
                                        "example": "invalid",
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
                                    "example": "2025-11-29T19:11:39.498145",
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
    def get_stores_schema(func):
        """Schema for retrieving all stores."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_store_get_stores",
            summary="Retrieve all stores",
            description="Retrieve a paginated list of all stores with optional pagination controls.",
            parameters=[
                OpenApiParameter(
                    name="page",
                    type=OpenApiTypes.INT,
                    location=OpenApiParameter.QUERY,
                    description="Page number for pagination (default: 1)",
                    required=False,
                ),
                OpenApiParameter(
                    name="page_size",
                    type=OpenApiTypes.INT,
                    location=OpenApiParameter.QUERY,
                    description="Number of items per page (default: 20, max: 100)",
                    required=False,
                ),
            ],
            responses={
                200: {
                    "description": "Stores retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Stores retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "example": 1},
                                    "name": {
                                        "type": "string",
                                        "example": "Essenza Showroom Jakarta",
                                    },
                                    "address": {
                                        "type": "string",
                                        "example": "Jl. Sudirman No. 123, Jakarta Pusat",
                                    },
                                    "phone": {
                                        "type": "string",
                                        "example": "+62-21-1234567",
                                    },
                                    "email": {
                                        "type": "string",
                                        "example": "jakarta@essenza.com",
                                    },
                                    "latitude": {
                                        "type": "string",
                                        "example": "-6.208763",
                                    },
                                    "longitude": {
                                        "type": "string",
                                        "example": "106.845599",
                                    },
                                    "created_at": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2025-11-29T19:06:14.763201+07:00",
                                    },
                                },
                            },
                        },
                        "pagination": {
                            "type": "object",
                            "properties": {
                                "current_page": {"type": "integer", "example": 1},
                                "page_size": {"type": "integer", "example": 20},
                                "total_pages": {"type": "integer", "example": 3},
                                "total_items": {"type": "integer", "example": 55},
                                "has_next": {"type": "boolean", "example": True},
                                "has_previous": {"type": "boolean", "example": False},
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T19:06:14.770300",
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
    def get_specific_store_schema(func):
        """Schema for retrieving a specific store by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_store_get_specific_store",
            summary="Retrieve a specific store by ID",
            description="Retrieve a specific store by its ID.",
            responses={
                200: {
                    "description": "Store retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Store retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "name": {
                                    "type": "string",
                                    "example": "Essenza Showroom Jakarta",
                                },
                                "address": {
                                    "type": "string",
                                    "example": "Jl. Sudirman No. 123, Jakarta Pusat",
                                },
                                "phone": {
                                    "type": "string",
                                    "example": "+62-21-1234567",
                                },
                                "email": {
                                    "type": "string",
                                    "example": "jakarta@essenza.com",
                                },
                                "latitude": {"type": "string", "example": "-6.208763"},
                                "longitude": {
                                    "type": "string",
                                    "example": "106.845599",
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T19:06:14.763201+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T20:01:22.307124",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Store not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Store with id '999' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T20:01:22.307124",
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
    def update_specific_store_schema(func):
        """Schema for updating a specific store by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_store_update_specific_store",
            summary="Update a specific store by ID",
            description="Update a specific store by its ID with partial data support.",
            request=serializers.PostUpdateStoreRequest,
            responses={
                200: {
                    "description": "Store updated successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Store updated successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "name": {
                                    "type": "string",
                                    "example": "Essenza Showroom Jakarta - Updated",
                                },
                                "address": {
                                    "type": "string",
                                    "example": "Jl. Sudirman No. 123, Jakarta Pusat",
                                },
                                "phone": {
                                    "type": "string",
                                    "example": "+62-21-1234567",
                                },
                                "email": {
                                    "type": "string",
                                    "example": "jakarta@essenza.com",
                                },
                                "latitude": {"type": "string", "example": "-6.208763"},
                                "longitude": {
                                    "type": "string",
                                    "example": "106.845599",
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T19:06:14.763201+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T20:01:22.307124",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Store not found or validation error",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Email 'jakarta@essenza.com' is already in use by another store.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T20:01:22.307124",
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
                                    "field": {
                                        "type": "string",
                                        "example": "latitude",
                                    },
                                    "message": {
                                        "type": "string",
                                        "example": "Latitude must be between -90 and 90 degrees.",
                                    },
                                    "code": {
                                        "type": "string",
                                        "example": "invalid",
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
                                    "example": "2025-11-29T20:01:22.307124",
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
    def delete_specific_store_schema(func):
        """Schema for deleting a specific store by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_store_delete_specific_store",
            summary="Delete a specific store by ID",
            description="Delete a specific store by its ID.",
            responses={
                200: {
                    "description": "Store deleted successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Store deleted successfully.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T20:01:22.307124",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Store not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Store with id '999' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T20:01:22.307124",
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
