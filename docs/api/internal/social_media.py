from functools import wraps
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from apps.internal.social_media import serializers

TAGS = ["Internal / Social Media"]


class SocialMediaAPI:
    """
    API endpoints for managing social media links.
    """

    @staticmethod
    def fetch_social_media(func):
        """
        Retrieve all social media links with pagination support.
        """

        @extend_schema(
            operation_id="int_v1_social_media_list",
            tags=TAGS,
            summary="Fetch Social Media Settings",
            description="Endpoint for retrieving social media settings with pagination support. Use 'page' parameter to navigate through pages and 'page_size' to control items per page (max 100).",
            parameters=[
                OpenApiParameter(
                    name="page",
                    type=OpenApiTypes.INT,
                    location=OpenApiParameter.QUERY,
                    description="Page number (default: 1)",
                    required=False,
                    default=1,
                ),
                OpenApiParameter(
                    name="page_size",
                    type=OpenApiTypes.INT,
                    location=OpenApiParameter.QUERY,
                    description="Number of items per page (default: 20, max: 100)",
                    required=False,
                    default=20,
                ),
            ],
            responses={
                200: {
                    "description": "Social media data fetched successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Social media data fetched successfully",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "example": 1},
                                    "platform": {
                                        "type": "string",
                                        "example": "Instagram",
                                    },
                                    "icon": {"type": "string", "example": ""},
                                    "url": {
                                        "type": "string",
                                        "example": "https://instagram.com",
                                    },
                                    "order_no": {"type": "integer", "example": 0},
                                    "created_at": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2025-11-13T00:13:57.304284+07:00",
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
                                    "example": "2025-11-13T00:19:36.311755",
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
                                            "example": 3,
                                        },
                                        "total_items": {
                                            "type": "integer",
                                            "example": 45,
                                        },
                                        "has_next": {
                                            "type": "boolean",
                                            "example": True,
                                        },
                                        "has_previous": {
                                            "type": "boolean",
                                            "example": False,
                                        },
                                        "next_page": {
                                            "type": "integer",
                                            "example": 2,
                                            "nullable": True,
                                        },
                                        "previous_page": {
                                            "type": "integer",
                                            "example": None,
                                            "nullable": True,
                                        },
                                    },
                                },
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
    def create_social_media(func):
        """
        Decorator for create social media endpoint documentation
        """

        @extend_schema(
            operation_id="int_v1_social_media_create",
            tags=TAGS,
            summary="Create Social Media",
            description="Endpoint for creating a new social media setting",
            request=serializers.PostCreateSocialMediaRequest,
            responses={
                201: {
                    "description": "Social media data created successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 201},
                        "message": {
                            "type": "string",
                            "example": "Social media data created successfully",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 3},
                                "platform": {"type": "string", "example": "TikTok"},
                                "icon": {"type": "string", "example": ""},
                                "url": {
                                    "type": "string",
                                    "example": "https://tiktok.com",
                                },
                                "order_no": {"type": "integer", "example": 2},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-13T00:16:58.437634+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-13T00:16:58.443714",
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
    def specific_social_media(func):
        """
        Decorator for specific social media endpoint documentation
        """

        @extend_schema(
            operation_id="int_v1_social_media_retrieve",
            tags=TAGS,
            summary="Retrieve Specific Social Media",
            description="Endpoint for retrieving a specific social media setting by its primary key",
            responses={
                200: {
                    "description": "Social media data retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Social media data retrieved successfully",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "platform": {"type": "string", "example": "Instagram"},
                                "icon": {
                                    "type": "string",
                                    "example": "https://instagram/favicon.ico",
                                },
                                "url": {
                                    "type": "string",
                                    "example": "https://instagram.com",
                                },
                                "order_no": {"type": "integer", "example": 0},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-13T00:13:57.304284+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-14T01:32:04.715422",
                                },
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
    def update_social_media(func):
        """
        Decorator for update social media endpoint documentation
        """

        @extend_schema(
            operation_id="int_v1_social_media_update",
            tags=TAGS,
            summary="Update Social Media",
            description="Endpoint for updating an existing social media setting",
            request=serializers.PatchUpdateSocialMediaRequest,
            responses={
                200: {
                    "description": "Social media data updated successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Social media data updated successfully",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "platform": {"type": "string", "example": "Instagram"},
                                "icon": {
                                    "type": "string",
                                    "example": "https://instagram/favicon.ico",
                                },
                                "url": {
                                    "type": "string",
                                    "example": "https://instagram.com",
                                },
                                "order_no": {"type": "integer", "example": 0},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-13T00:13:57.304284+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-14T01:32:04.715422",
                                },
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
    def delete_social_media(func):
        """
        Decorator for delete social media endpoint documentation
        """

        @extend_schema(
            operation_id="int_v1_social_media_delete",
            tags=TAGS,
            summary="Delete Social Media",
            description="Endpoint for deleting a social media setting by its primary key",
            responses={
                200: {
                    "description": "Social media data deleted successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Social media data deleted successfully",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-14T01:45:12.345678",
                                },
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
