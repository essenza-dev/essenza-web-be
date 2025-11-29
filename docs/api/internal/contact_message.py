from functools import wraps
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from docs.api.constants import DEFAULT_PAGINATION_PARAMS

TAGS = ["Internal / Contact Messages"]


class ContactMessageAPI:
    """API documentation for Contact Message endpoints."""

    @staticmethod
    def get_all_contact_messages_schema(func):
        """Schema for retrieving all contact messages."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_get_all_contact_messages",
            summary="Get All Contact Messages",
            description="Retrieve all contact messages with pagination support and optional filters.",
            parameters=DEFAULT_PAGINATION_PARAMS
            + [
                OpenApiParameter(
                    name="search",
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                    description="Search in name, email, subject, or message content",
                    required=False,
                ),
                OpenApiParameter(
                    name="is_read",
                    type=OpenApiTypes.BOOL,
                    location=OpenApiParameter.QUERY,
                    description="Filter by read status (true/false)",
                    required=False,
                ),
                OpenApiParameter(
                    name="name",
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                    description="Filter by sender name",
                    required=False,
                ),
                OpenApiParameter(
                    name="email",
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                    description="Filter by sender email",
                    required=False,
                ),
                OpenApiParameter(
                    name="subject",
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                    description="Filter by message subject",
                    required=False,
                ),
            ],
            responses={
                200: {
                    "description": "Contact messages retrieved successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Contact messages retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "example": 1},
                                    "name": {
                                        "type": "string",
                                        "example": "John Doe",
                                    },
                                    "email": {
                                        "type": "string",
                                        "format": "email",
                                        "example": "john.doe@example.com",
                                    },
                                    "phone": {
                                        "type": "string",
                                        "example": "+1234567890",
                                    },
                                    "subject": {
                                        "type": "string",
                                        "example": "Product Inquiry",
                                    },
                                    "message": {
                                        "type": "string",
                                        "example": "I would like to know more about your ceramic tiles.",
                                    },
                                    "is_read": {
                                        "type": "boolean",
                                        "example": False,
                                    },
                                    "created_at": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2025-11-29T18:44:38.623000+07:00",
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
                                    "example": "2025-11-29T20:21:46.534872",
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
    def get_specific_contact_message_schema(func):
        """Schema for retrieving a specific contact message."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_get_specific_contact_message",
            summary="Get Specific Contact Message",
            description="Retrieve a specific contact message by its ID.",
            responses={
                200: {
                    "description": "Contact message retrieved successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Contact message retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 2},
                                "name": {
                                    "type": "string",
                                    "example": "Jane Smith",
                                },
                                "email": {
                                    "type": "string",
                                    "format": "email",
                                    "example": "jane.smith@example.com",
                                },
                                "phone": {
                                    "type": "string",
                                    "example": "+9876543210",
                                },
                                "subject": {
                                    "type": "string",
                                    "example": "Partnership Inquiry",
                                },
                                "message": {
                                    "type": "string",
                                    "example": "We are interested in becoming a distributor for your products.",
                                },
                                "is_read": {
                                    "type": "boolean",
                                    "example": True,
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T18:44:38.623000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T20:24:37.935078",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Contact message not found.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Contact message with id '12' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T20:24:37.935078",
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
    def mark_contact_message_as_read_schema(func):
        """Schema for marking contact message as read/unread."""

        from apps.internal.contact_message import serializers

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_mark_contact_message_as_read",
            summary="Mark Contact Message as Read/Unread",
            description="Mark a specific contact message as read or unread.",
            request=serializers.PostMarkAsReadContactMessageSerializer,
            responses={
                200: {
                    "description": "Contact message read status updated successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Contact message marked as read successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 2},
                                "name": {
                                    "type": "string",
                                    "example": "Jane Smith",
                                },
                                "email": {
                                    "type": "string",
                                    "format": "email",
                                    "example": "jane.smith@example.com",
                                },
                                "phone": {
                                    "type": "string",
                                    "example": "+9876543210",
                                },
                                "subject": {
                                    "type": "string",
                                    "example": "Partnership Inquiry",
                                },
                                "message": {
                                    "type": "string",
                                    "example": "We are interested in becoming a distributor for your products.",
                                },
                                "is_read": {
                                    "type": "boolean",
                                    "example": True,
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T18:44:38.623000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T20:24:37.935078",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Contact message not found or validation error.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Contact message with id '12' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T20:24:37.935078",
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
    def delete_contact_message_schema(func):
        """Schema for deleting a specific contact message."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_delete_contact_message",
            summary="Delete Contact Message",
            description="Delete a specific contact message by its ID.",
            responses={
                200: {
                    "description": "Contact message deleted successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Contact message deleted successfully.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T20:24:37.935078",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Contact message not found.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Contact message with id '12' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T20:24:37.935078",
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
