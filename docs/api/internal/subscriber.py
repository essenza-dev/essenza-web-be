from functools import wraps
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from docs.api.constants import DEFAULT_PAGINATION_PARAMS

TAGS = ["Internal / Subscriber"]


class SubscriberAPI:
    """API documentation for Subscriber endpoints."""

    @staticmethod
    def get_all_subscribers_schema(func):
        """Schema for retrieving all subscribers."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_get_all_subscribers",
            summary="Get All Subscribers",
            description="Retrieve all subscribers with pagination support.",
            parameters=DEFAULT_PAGINATION_PARAMS,
            responses={
                200: {
                    "description": "Subscribers retrieved successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Subscribers retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "example": 1},
                                    "email": {
                                        "type": "string",
                                        "example": "me@ruriazz.com",
                                    },
                                    "created_at": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2025-11-26T18:44:38.623000+07:00",
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
                                    "example": "2025-11-27T20:21:46.534872",
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
                                            "example": 1,
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
    def get_specific_subscriber_schema(func):
        """Schema for retrieving a specific subscriber."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_get_specific_subscriber",
            summary="Get Specific Subscriber",
            description="Retrieve a specific subscriber by its ID.",
            responses={
                200: {
                    "description": "Subscriber retrieved successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Subscriber retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 2},
                                "email": {
                                    "type": "string",
                                    "format": "email",
                                    "example": "dev@ruriazz.com",
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-26T18:44:38.623000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-27T20:25:27.623802",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Subscriber not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Subscriber with id '12' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-27T20:24:37.935078",
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
    def delete_subscriber_schema(func):
        """Schema for deleting a specific subscriber."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_delete_subscriber",
            summary="Delete Subscriber",
            description="Delete a specific subscriber by its ID.",
            responses={
                200: {
                    "description": "Subscriber deleted successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Subscriber deleted successfully.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-27T20:26:17.949363",
                                },
                            },
                        },
                    },
                },
                400: {
                    "description": "Subscriber not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Subscriber with id '12' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-27T20:24:37.935078",
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
