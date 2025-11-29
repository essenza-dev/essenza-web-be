from functools import wraps
from drf_spectacular.utils import extend_schema

from apps.internal.distributor import serializers
from docs.api.constants import DEFAULT_PAGINATION_PARAMS

TAGS = ["Internal / Distributor"]


class DistributorAPI:
    """API schema definitions for Distributor endpoints."""

    @staticmethod
    def create_distributor_schema(func):
        """Schema for creating a new distributor."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_distributor_create_distributor",
            summary="Create Distributor",
            description="Create a new distributor with contact information and location coordinates.",
            request=serializers.PostCreateDistributorRequest,
            responses={
                200: {
                    "description": "Distributor created successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Distributor created successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "name": {
                                    "type": "string",
                                    "example": "PT. Toko Bangunan Jaya",
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
                                    "example": "info@tokojaya.com",
                                },
                                "website": {
                                    "type": "string",
                                    "example": "https://www.tokojaya.com",
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
                            "example": "Email 'info@tokojaya.com' is already in use by another distributor.",
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
    def get_distributors_schema(func):
        """Schema for retrieving all distributors."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_distributor_get_distributors",
            summary="Retrieve all distributors",
            description="Retrieve all distributors with pagination support.",
            parameters=DEFAULT_PAGINATION_PARAMS,
            responses={
                200: {
                    "description": "Distributors retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Distributors retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "example": 1},
                                    "name": {
                                        "type": "string",
                                        "example": "PT. Toko Bangunan Jaya",
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
                                        "example": "info@tokojaya.com",
                                    },
                                    "website": {
                                        "type": "string",
                                        "example": "https://www.tokojaya.com",
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
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T19:37:20.085607",
                                },
                                "pagination": {
                                    "type": "object",
                                    "properties": {
                                        "current_page": {
                                            "type": "integer",
                                            "example": 1,
                                        },
                                        "per_page": {"type": "integer", "example": 20},
                                        "total_pages": {
                                            "type": "integer",
                                            "example": 1,
                                        },
                                        "total_items": {
                                            "type": "integer",
                                            "example": 3,
                                        },
                                        "has_next": {
                                            "type": "boolean",
                                            "example": False,
                                        },
                                        "has_previous": {
                                            "type": "boolean",
                                            "example": False,
                                        },
                                    },
                                },
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
    def get_specific_distributor_schema(func):
        """Schema for retrieving a specific distributor by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_distributor_get_specific_distributor",
            summary="Retrieve a specific distributor by ID",
            description="Retrieve a specific distributor by its ID.",
            responses={
                200: {
                    "description": "Distributor retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Distributor retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "name": {
                                    "type": "string",
                                    "example": "PT. Toko Bangunan Jaya",
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
                                    "example": "info@tokojaya.com",
                                },
                                "website": {
                                    "type": "string",
                                    "example": "https://www.tokojaya.com",
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
                                    "example": "2025-11-29T19:48:32.052814",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Distributor not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Distributor with id '999' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T19:48:32.052814",
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
    def update_specific_distributor_schema(func):
        """Schema for updating a specific distributor by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_distributor_update_specific_distributor",
            summary="Update a specific distributor by ID",
            description="Update a specific distributor by its ID.",
            request=serializers.PostUpdateDistributorRequest,
            responses={
                200: {
                    "description": "Distributor updated successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Distributor updated successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "name": {
                                    "type": "string",
                                    "example": "PT. Toko Bangunan Jaya Updated",
                                },
                                "address": {
                                    "type": "string",
                                    "example": "Jl. Sudirman No. 456, Jakarta Selatan",
                                },
                                "phone": {
                                    "type": "string",
                                    "example": "+62-21-7654321",
                                },
                                "email": {
                                    "type": "string",
                                    "example": "info.updated@tokojaya.com",
                                },
                                "website": {
                                    "type": "string",
                                    "example": "https://www.tokojaya.co.id",
                                },
                                "latitude": {"type": "string", "example": "-6.240000"},
                                "longitude": {
                                    "type": "string",
                                    "example": "106.860000",
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
                    "description": "Distributor not found or validation error",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Email 'existing@email.com' is already in use by another distributor.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T20:04:41.117151",
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
                                    "example": "2025-11-29T20:02:42.001064",
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
    def delete_specific_distributor_schema(func):
        """Schema for deleting a specific distributor by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_distributor_delete_specific_distributor",
            summary="Delete a specific distributor by ID",
            description="Delete a specific distributor by its ID.",
            responses={
                200: {
                    "description": "Distributor deleted successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Distributor deleted successfully.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {"type": "string", "format": "date-time"},
                            },
                        },
                    },
                },
                400: {
                    "description": "Distributor not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Distributor with id '999' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T20:04:41.117151",
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
