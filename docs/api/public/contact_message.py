from drf_spectacular.utils import extend_schema

from apps.public.contact_message import serializers

TAGS = ["Public / Contact Messages"]


class ContactMessagePublicAPI:
    """API documentation for Public Contact Message endpoints."""

    @staticmethod
    def create_contact_message_schema(func):
        """Schema for creating a new contact message."""

        @extend_schema(
            tags=TAGS,
            operation_id="pub_v1_create_contact_message",
            summary="Create Contact Message",
            description="Submit a new contact message by providing name, email, subject, and message.",
            auth=[],
            request=serializers.PostCreateContactMessageSerializer,
            responses={
                200: {
                    "description": "Contact message created successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Contact message submitted successfully.",
                        },
                        "data": {
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
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T20:42:05.321082+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T20:42:05.330336",
                                },
                            },
                        },
                    },
                },
                400: {
                    "description": "Validation error or CAPTCHA failed.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Validation failed. Please check your input.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T20:42:46.761968",
                                }
                            },
                        },
                    },
                },
                500: {
                    "description": "Internal server error.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 500},
                        "message": {
                            "type": "string",
                            "example": "An unexpected error occurred while submitting the contact message.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-29T20:42:46.761968",
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
