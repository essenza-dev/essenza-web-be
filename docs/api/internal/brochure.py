"""
API Schema Definitions for Brochure Endpoints
Contains all API documentation schemas for brochure-related endpoints
"""

from functools import wraps
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from apps.internal.brochure import serializers
from docs.api.constants import DEFAULT_PAGINATION_PARAMS

TAGS = ["Internal / Brochure"]


class BrochureAPI:
    """API schema definitions for Brochure endpoints."""

    @staticmethod
    def create_brochure_schema(func):
        """Schema for creating a new brochure."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_brochure_create_brochure",
            summary="Create Brochure",
            description="Create a new brochure with file upload support.",
            request={"multipart/form-data": serializers.PostCreateBrochureRequest},
            responses={
                201: {
                    "description": "Brochure created successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 201},
                        "message": {
                            "type": "string",
                            "example": "Brochure created successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "title": {
                                    "type": "string",
                                    "example": "Premium Product Brochure",
                                },
                                "file_url": {
                                    "type": "string",
                                    "format": "uri",
                                    "example": "/media/uploads/brochure/premium-product-brochure.pdf",
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.123456",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Bad Request",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Brochure with this title already exists.",
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
    def get_brochures_schema(func):
        """Schema for retrieving all brochures with filtering."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_brochure_get_brochures",
            summary="Get Brochures",
            description="Retrieve all brochures with optional search filtering and pagination.",
            parameters=DEFAULT_PAGINATION_PARAMS
            + [
                OpenApiParameter(
                    name="search",
                    description="Search term for filtering brochures by title",
                    required=False,
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                ),
            ],
            responses={
                200: {
                    "description": "Brochures retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Brochures retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "example": 1},
                                    "title": {
                                        "type": "string",
                                        "example": "Premium Product Brochure",
                                    },
                                    "file_url": {
                                        "type": "string",
                                        "format": "uri",
                                        "example": "/media/uploads/brochure/premium-product-brochure.pdf",
                                    },
                                    "created_at": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2025-11-28T10:30:00.000000+07:00",
                                    },
                                    "updated_at": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2025-11-28T10:30:00.000000+07:00",
                                    },
                                },
                            },
                        },
                        "pagination": {
                            "type": "object",
                            "properties": {
                                "page": {"type": "integer", "example": 1},
                                "page_size": {"type": "integer", "example": 20},
                                "total_pages": {"type": "integer", "example": 5},
                                "total_items": {"type": "integer", "example": 89},
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
                                    "example": "2025-11-28T10:30:00.123456",
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
    def get_specific_brochure_schema(func):
        """Schema for retrieving a specific brochure by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_brochure_get_specific_brochure",
            summary="Get Specific Brochure",
            description="Retrieve a specific brochure by its ID.",
            responses={
                200: {
                    "description": "Brochure retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Brochure retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "title": {
                                    "type": "string",
                                    "example": "Premium Product Brochure",
                                },
                                "file_url": {
                                    "type": "string",
                                    "format": "uri",
                                    "example": "/media/uploads/brochure/premium-product-brochure.pdf",
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.123456",
                                }
                            },
                        },
                    },
                },
                404: {
                    "description": "Brochure not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 404},
                        "message": {
                            "type": "string",
                            "example": "Brochure with id '1' does not exist.",
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
    def update_specific_brochure_schema(func):
        """Schema for updating a specific brochure by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_brochure_update_specific_brochure",
            summary="Update Specific Brochure",
            description="Update a specific brochure by its ID with file upload support.",
            request={"multipart/form-data": serializers.PutUpdateBrochureRequest},
            responses={
                200: {
                    "description": "Brochure updated successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Brochure updated successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "title": {
                                    "type": "string",
                                    "example": "Updated Premium Product Brochure",
                                },
                                "file_url": {
                                    "type": "string",
                                    "format": "uri",
                                    "example": "/media/uploads/brochure/updated-premium-product-brochure.pdf",
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T11:45:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T11:45:00.123456",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Bad Request",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Brochure with this title already exists.",
                        },
                    },
                },
                404: {
                    "description": "Brochure not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 404},
                        "message": {
                            "type": "string",
                            "example": "Brochure with id '1' does not exist.",
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
    def delete_specific_brochure_schema(func):
        """Schema for deleting a specific brochure by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_brochure_delete_specific_brochure",
            summary="Delete Specific Brochure",
            description="Delete a specific brochure by its ID.",
            responses={
                200: {
                    "description": "Brochure deleted successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Brochure deleted successfully.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T11:45:00.123456",
                                }
                            },
                        },
                    },
                },
                404: {
                    "description": "Brochure not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 404},
                        "message": {
                            "type": "string",
                            "example": "Brochure with id '1' does not exist.",
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
    def upload_brochure_file_schema(func):
        """Schema for uploading a brochure file."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_brochure_upload_brochure_file",
            summary="Upload Brochure File",
            description="Upload a PDF file for a specific brochure.",
            request={"multipart/form-data": serializers.PostUploadBrochureFileRequest},
            responses={
                200: {
                    "description": "Brochure file uploaded successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Brochure file uploaded successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "title": {
                                    "type": "string",
                                    "example": "Premium Product Brochure",
                                },
                                "file_url": {
                                    "type": "string",
                                    "format": "uri",
                                    "example": "/media/uploads/brochure/new-premium-product-brochure.pdf",
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T12:15:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T12:15:00.123456",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Bad Request",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Only PDF files are allowed.",
                        },
                    },
                },
                404: {
                    "description": "Brochure not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 404},
                        "message": {
                            "type": "string",
                            "example": "Brochure with id '1' does not exist.",
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
