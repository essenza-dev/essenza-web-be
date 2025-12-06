from functools import wraps
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from apps.internal.specification import serializers

TAGS = ["Internal / Specification"]


class SpecificationAPI:
    """API schema definitions for Specification endpoints."""

    @staticmethod
    def get_specifications_schema(func):
        """Schema for retrieving all specifications."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_specification_get_specifications",
            summary="Get All Specifications",
            description="Retrieve all specification master data for products.",
            responses={
                200: {
                    "description": "Specifications retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Specifications retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "example": 1},
                                    "slug": {"type": "string", "example": "size"},
                                    "label": {"type": "string", "example": "Size"},
                                    "icon": {"type": "string", "example": "ruler"},
                                    "is_active": {"type": "boolean", "example": True},
                                    "created_at": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2025-12-05T10:00:00.000000+07:00",
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
                                    "example": "2025-12-05T10:00:00.000000",
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
    def get_specific_specification_schema(func):
        """Schema for retrieving a specific specification by slug."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_specification_get_specific_specification",
            summary="Get Specification by Slug",
            description="Retrieve a specific specification master data by its slug identifier.",
            parameters=[
                OpenApiParameter(
                    name="slug",
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.PATH,
                    description="Unique slug identifier for the specification (e.g., size, material, color)",
                    required=True,
                ),
            ],
            responses={
                200: {
                    "description": "Specification retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Specification retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "slug": {"type": "string", "example": "size"},
                                "label": {"type": "string", "example": "Size"},
                                "icon": {"type": "string", "example": "ruler"},
                                "is_active": {"type": "boolean", "example": True},
                                "created_at": {
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
                                    "example": "2025-12-05T10:00:00.000000",
                                }
                            },
                        },
                    },
                },
                404: {
                    "description": "Specification not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 404},
                        "message": {
                            "type": "string",
                            "example": "Specification with slug 'invalid-slug' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-05T10:00:00.000000",
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
    def update_specific_specification_schema(func):
        """Schema for updating a specific specification by slug."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_specification_update_specific_specification",
            summary="Update Specification active status by Slug",
            description="Update a specific specification master data. Only provided fields will be updated.",
            parameters=[
                OpenApiParameter(
                    name="slug",
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.PATH,
                    description="Unique slug identifier for the specification (e.g., size, material, color)",
                    required=True,
                ),
            ],
            request=serializers.PutUpdateSpecificationRequest,
            responses={
                200: {
                    "description": "Specification updated successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Specification updated successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "slug": {"type": "string", "example": "size"},
                                "label": {"type": "string", "example": "Product Size"},
                                "icon": {"type": "string", "example": "ruler-alt"},
                                "is_active": {"type": "boolean", "example": True},
                                "created_at": {
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
                                    "example": "2025-12-05T10:00:00.000000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Business logic error",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Specification with slug 'invalid-slug' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-05T10:00:00.000000",
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
                                        "example": "label",
                                    },
                                    "message": {
                                        "type": "string",
                                        "example": "This field may not be blank.",
                                    },
                                    "code": {
                                        "type": "string",
                                        "example": "blank",
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
                                    "example": "2025-12-05T10:00:00.000000",
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
