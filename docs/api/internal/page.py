from functools import wraps

from drf_spectacular.utils import extend_schema

from docs.api.constants import DEFAULT_PAGINATION_PARAMS
from apps.internal.page import serializers

TAGS = ["Internal / Page"]


class PageAPI:
    """API schema definitions for Page endpoints."""

    @staticmethod
    def create_page_schema(func):
        """Schema for creating a new page."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_page_create_page",
            summary="Create Page",
            description="Create a new page with content and SEO metadata.",
            request=serializers.PostCreatePageRequest,
            responses={
                200: {
                    "description": "Page created successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Page created successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "slug": {"type": "string", "example": "about-us"},
                                "title": {"type": "string", "example": "About Us"},
                                "content": {
                                    "type": "string",
                                    "example": "<p>Welcome to our company...</p>",
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "About Us - Company Name",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "Learn more about our company history and values.",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "about, company, history, values",
                                },
                                "template": {"type": "string", "example": "default"},
                                "is_active": {"type": "boolean", "example": True},
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
                                    "example": "2025-11-28T10:30:00.000000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Bad Request - Validation Error",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "A page with slug 'about-us' already exists.",
                        },
                        "errors": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "field": {
                                        "type": "string",
                                        "example": "slug",
                                    },
                                    "message": {
                                        "type": "string",
                                        "example": "A page with slug 'about-us' already exists.",
                                    },
                                    "code": {
                                        "type": "string",
                                        "example": "unique",
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
                                    "example": "2025-11-28T10:30:00.000000",
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
    def get_pages_schema(func):
        """Schema for retrieving all pages."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_page_get_pages",
            summary="Retrieve all pages",
            description="Retrieve all pages with pagination support.",
            parameters=DEFAULT_PAGINATION_PARAMS,
            responses={
                200: {
                    "description": "Pages retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Pages retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "example": 1},
                                    "slug": {"type": "string", "example": "about-us"},
                                    "title": {"type": "string", "example": "About Us"},
                                    "content": {
                                        "type": "string",
                                        "example": "<p>Welcome to our company...</p>",
                                    },
                                    "meta_title": {
                                        "type": "string",
                                        "example": "About Us - Company Name",
                                    },
                                    "meta_description": {
                                        "type": "string",
                                        "example": "Learn more about our company history and values.",
                                    },
                                    "meta_keywords": {
                                        "type": "string",
                                        "example": "about, company, history, values",
                                    },
                                    "template": {
                                        "type": "string",
                                        "example": "default",
                                    },
                                    "is_active": {"type": "boolean", "example": True},
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
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000",
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
                                            "example": 5,
                                        },
                                        "has_next": {
                                            "type": "boolean",
                                            "example": False,
                                        },
                                        "has_previous": {
                                            "type": "boolean",
                                            "example": False,
                                        },
                                        "next_page": {
                                            "type": "integer",
                                            "nullable": True,
                                            "example": None,
                                        },
                                        "previous_page": {
                                            "type": "integer",
                                            "nullable": True,
                                            "example": None,
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
    def get_specific_page_schema(func):
        """Schema for retrieving a specific page by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_page_get_specific_page",
            summary="Retrieve a specific page by ID",
            description="Retrieve a specific page by its ID.",
            responses={
                200: {
                    "description": "Page retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Page retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "slug": {"type": "string", "example": "about-us"},
                                "title": {"type": "string", "example": "About Us"},
                                "content": {
                                    "type": "string",
                                    "example": "<p>Welcome to our company...</p>",
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "About Us - Company Name",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "Learn more about our company history and values.",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "about, company, history, values",
                                },
                                "template": {"type": "string", "example": "default"},
                                "is_active": {"type": "boolean", "example": True},
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
                                    "example": "2025-11-28T10:30:00.000000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Page not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Page with id '99' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000",
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
    def get_page_by_slug_schema(func):
        """Schema for retrieving a page by slug."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_page_get_page_by_slug",
            summary="Retrieve a page by slug",
            description="Retrieve a page by its slug identifier.",
            responses={
                200: {
                    "description": "Page retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Page retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "slug": {"type": "string", "example": "about-us"},
                                "title": {"type": "string", "example": "About Us"},
                                "content": {
                                    "type": "string",
                                    "example": "<p>Welcome to our company...</p>",
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "About Us - Company Name",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "Learn more about our company history and values.",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "about, company, history, values",
                                },
                                "template": {"type": "string", "example": "default"},
                                "is_active": {"type": "boolean", "example": True},
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
                                    "example": "2025-11-28T10:30:00.000000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Page not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Page with slug 'non-existent' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000",
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
    def update_specific_page_schema(func):
        """Schema for updating a specific page by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_page_update_specific_page",
            summary="Update a specific page by ID",
            description="Update a specific page by its ID with new data.",
            request=serializers.PutUpdatePageRequest,
            responses={
                200: {
                    "description": "Page updated successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Page updated successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "slug": {"type": "string", "example": "about-us"},
                                "title": {
                                    "type": "string",
                                    "example": "About Us - Updated",
                                },
                                "content": {
                                    "type": "string",
                                    "example": "<p>Updated content...</p>",
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "About Us - Company Name",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "Updated description.",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "about, company, updated",
                                },
                                "template": {"type": "string", "example": "default"},
                                "is_active": {"type": "boolean", "example": True},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T11:30:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T11:30:00.000000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Bad Request - Page not found or validation error",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Page with id '99' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T11:30:00.000000",
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
    def delete_specific_page_schema(func):
        """Schema for deleting a specific page by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_page_delete_specific_page",
            summary="Delete a specific page by ID",
            description="Delete a specific page by its ID.",
            responses={
                200: {
                    "description": "Page deleted successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Page deleted successfully.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T12:00:00.000000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Page not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Page with id '99' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T12:00:00.000000",
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
    def toggle_page_status_schema(func):
        """Schema for toggling page active status."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_page_toggle_page_status",
            summary="Toggle page active status",
            description="Toggle the active status of a specific page.",
            request=serializers.PatchTogglePageStatusRequest,
            responses={
                200: {
                    "description": "Page status updated successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Page status updated successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "slug": {"type": "string", "example": "about-us"},
                                "title": {"type": "string", "example": "About Us"},
                                "content": {
                                    "type": "string",
                                    "example": "<p>Welcome to our company...</p>",
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "About Us - Company Name",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "Learn more about our company history and values.",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "about, company, history, values",
                                },
                                "template": {"type": "string", "example": "default"},
                                "is_active": {"type": "boolean", "example": False},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T12:30:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T12:30:00.000000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Page not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Page with id '99' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T12:30:00.000000",
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
