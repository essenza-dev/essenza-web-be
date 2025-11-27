from functools import wraps
from drf_spectacular.utils import extend_schema

from apps.public.subscriber import serializers

TAGS = ["Public / Subscriber"]


class SubscriberPublicAPI:
    """API documentation for Public Subscriber endpoints."""

    @staticmethod
    def create_subscriber_schema(func):
        """Schema for creating a new subscriber."""

        @extend_schema(
            tags=TAGS,
            operation_id="pub_v1_create_subscriber",
            summary="Create Subscriber",
            description="Create a new subscriber by providing an email address.",
            auth=[],
            request=serializers.PostCreateSubscriberSerializer,
            responses={
                200: {
                    "description": "Subscriber created successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Subscriber created successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "email": {
                                    "type": "string",
                                    "example": "user@example.com",
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-27T20:42:05.321082+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-27T20:42:05.330336",
                                },
                            },
                        },
                    },
                },
                400: {
                    "description": "Subscriber email already exists.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Subscriber with this email already exists.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-27T20:42:46.761968",
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
