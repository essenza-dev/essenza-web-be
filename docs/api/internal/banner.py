from functools import wraps
from drf_spectacular.utils import extend_schema

from apps.internal.banner import serializers
from docs.api.constants import DEFAULT_PAGINATION_PARAMS

TAGS = ["Internal / Banner"]


class BannerAPI:
    """API schema definitions for Banner endpoints."""

    @staticmethod
    def create_banner_schema(func):
        """Schema for creating a new banner."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_banner_create_banner",
            description="Create a new banner with file upload support.",
            request={"multipart/form-data": serializers.PostCreateBannerRequest},
            responses={
                200: {
                    "description": "Banner created successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Banner created successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 6},
                                "image": {
                                    "type": "string",
                                    "format": "uri",
                                    "example": "/media/uploads/banners/lovepik-taobao-tmall-e-commerce-banner-background-image_500603827_Z4EGq4A.jpg",
                                },
                                "title": {"type": "string", "example": "string"},
                                "subtitle": {"type": "string", "example": "string"},
                                "link_url": {"type": "string", "example": "string"},
                                "order_no": {"type": "integer", "example": 0},
                                "is_active": {"type": "boolean", "example": True},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-26T19:06:14.763201+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-26T19:06:14.763222+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-26T19:06:14.770300",
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
                                        "example": "image",
                                    },
                                    "message": {
                                        "type": "string",
                                        "example": "Upload a valid image. The file you uploaded was either not an image or a corrupted image.",
                                    },
                                    "code": {
                                        "type": "string",
                                        "example": "invalid_image",
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
                                    "example": "2025-11-26T19:11:39.498145",
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
    def get_banners_schema(func):
        """Schema for retrieving all banners."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_banner_get_banners",
            description="Retrieve all banners.",
            parameters=DEFAULT_PAGINATION_PARAMS,
            responses={
                200: {
                    "description": "Banners retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Banners retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "example": 6},
                                    "title": {"type": "string", "example": "string"},
                                    "subtitle": {"type": "string", "example": "string"},
                                    "image": {
                                        "type": "string",
                                        "example": "/media/uploads/banners/lovepik-taobao-tmall-e-commerce-banner-background-image_500603827_Z4EGq4A.jpg",
                                    },
                                    "link_url": {"type": "string", "example": "string"},
                                    "order_no": {"type": "integer", "example": 0},
                                    "is_active": {"type": "boolean", "example": True},
                                    "created_at": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2025-11-26T19:06:14.763201+07:00",
                                    },
                                    "updated_at": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2025-11-26T19:06:14.763222+07:00",
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
                                    "example": "2025-11-26T19:37:20.085607",
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
    def get_specific_banner_schema(func):
        """Schema for retrieving a specific banner by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_banner_get_specific_banner",
            description="Retrieve a specific banner by its ID.",
            responses={
                200: {
                    "description": "Banner retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Banner retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 6},
                                "title": {"type": "string", "example": "string"},
                                "subtitle": {"type": "string", "example": "string"},
                                "image": {
                                    "type": "string",
                                    "example": "/media/uploads/banners/lovepik-taobao-tmall-e-commerce-banner-background-image_500603827_Z4EGq4A.jpg",
                                },
                                "link_url": {"type": "string", "example": "string"},
                                "order_no": {"type": "integer", "example": 0},
                                "is_active": {"type": "boolean", "example": True},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-26T19:06:14.763201+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-26T19:06:14.763222+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-26T19:48:32.052814",
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
    def update_specific_banner_schema(func):
        """Schema for updating a specific banner by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_banner_update_specific_banner",
            description="Update a specific banner by its ID.",
            request={"multipart/form-data": serializers.PostUpdateBannerRequest},
            responses={
                200: {
                    "description": "Banner updated successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Banner updated successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 6},
                                "title": {"type": "string", "example": "string"},
                                "subtitle": {
                                    "type": "string",
                                    "example": "new subtitle",
                                },
                                "image": {
                                    "type": "string",
                                    "example": "/media/uploads/banners/lovepik-taobao-tmall-e-commerce-banner-background-image_500603827_aexFCkx.jpg",
                                },
                                "link_url": {"type": "string", "example": ""},
                                "order_no": {"type": "integer", "example": 0},
                                "is_active": {"type": "boolean", "example": False},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-26T19:06:14.763201+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-26T20:01:22.298730+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-26T20:01:22.307124",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Banner not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Banner with id '221' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-26T20:04:41.117151",
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
                                    "field": {"type": "string", "example": "image"},
                                    "message": {
                                        "type": "string",
                                        "example": "Upload a valid image. The file you uploaded was either not an image or a corrupted image.",
                                    },
                                    "code": {
                                        "type": "string",
                                        "example": "invalid_image",
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
                                    "example": "2025-11-26T20:02:42.001064",
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
    def delete_specific_banner_schema(func):
        """Schema for deleting a specific banner by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_banner_delete_specific_banner",
            description="Delete a specific banner by its ID.",
            responses={
                200: {
                    "description": "Banner deleted successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Banner deleted successfully.",
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
                    "description": "Banner not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Banner with id '221' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-26T20:04:41.117151",
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
