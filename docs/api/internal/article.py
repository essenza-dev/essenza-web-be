from functools import wraps

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from docs.api.constants import DEFAULT_PAGINATION_PARAMS
from apps.internal.article import serializers

TAGS = ["Internal / Article"]

# Additional query parameters for article filtering
ARTICLE_FILTER_PARAMS = [
    OpenApiParameter(
        name="tags",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description="Filter articles by tags (case-insensitive partial match)",
        required=False,
    ),
    OpenApiParameter(
        name="author",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description="Filter articles by author (case-insensitive partial match)",
        required=False,
    ),
    OpenApiParameter(
        name="search",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        description="Search in article title and content (case-insensitive)",
        required=False,
    ),
    OpenApiParameter(
        name="is_active",
        type=OpenApiTypes.BOOL,
        location=OpenApiParameter.QUERY,
        description="Filter articles by active status",
        required=False,
    ),
]


class ArticleAPI:
    """API schema definitions for Article endpoints."""

    @staticmethod
    def create_article_schema(func):
        """Schema for creating a new article."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_article_create_article",
            summary="Create Article",
            description="Create a new article with content and SEO metadata. If is_active is true, published_at will be automatically set to current time. If is_active is false, published_at will be null. Use the publish endpoint to set a specific publication date. If author field is empty, it will be automatically set from current user's name.",
            request={"multipart/form-data": serializers.PostCreateArticleRequest},
            responses={
                200: {
                    "description": "Article created successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Article created successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "slug": {
                                    "type": "string",
                                    "example": "my-first-article",
                                },
                                "title": {
                                    "type": "string",
                                    "example": "My First Article",
                                },
                                "content": {
                                    "type": "string",
                                    "example": "<p>This is the content of my article...</p>",
                                },
                                "thumbnail": {
                                    "type": "string",
                                    "nullable": True,
                                    "example": "/media/articles/thumbnails/article1.jpg",
                                },
                                "author": {"type": "string", "example": "John Doe"},
                                "tags": {
                                    "type": "string",
                                    "example": "tech, programming, django",
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "My First Article - Tech Blog",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "Learn about the latest in technology and programming.",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "technology, programming, django, python",
                                },
                                "published_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "nullable": True,
                                    "example": None,
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
                            "example": "An article with slug 'my-first-article' already exists.",
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
                                        "example": "An article with slug 'my-first-article' already exists.",
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
    def get_articles_schema(func):
        """Schema for retrieving all articles with filters."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_article_get_articles",
            summary="Retrieve all articles",
            description="Retrieve all articles with pagination support and filtering options (tags, author, search, active status).",
            parameters=DEFAULT_PAGINATION_PARAMS + ARTICLE_FILTER_PARAMS,
            responses={
                200: {
                    "description": "Articles retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Articles retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "example": 1},
                                    "slug": {
                                        "type": "string",
                                        "example": "my-first-article",
                                    },
                                    "title": {
                                        "type": "string",
                                        "example": "My First Article",
                                    },
                                    "content": {
                                        "type": "string",
                                        "example": "<p>This is the content...</p>",
                                    },
                                    "thumbnail": {
                                        "type": "string",
                                        "nullable": True,
                                        "example": "/media/articles/thumbnails/article1.jpg",
                                    },
                                    "author": {"type": "string", "example": "John Doe"},
                                    "tags": {
                                        "type": "string",
                                        "example": "tech, programming, django",
                                    },
                                    "meta_title": {
                                        "type": "string",
                                        "example": "My First Article - Tech Blog",
                                    },
                                    "meta_description": {
                                        "type": "string",
                                        "example": "Learn about technology...",
                                    },
                                    "meta_keywords": {
                                        "type": "string",
                                        "example": "technology, programming",
                                    },
                                    "published_at": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2025-11-28T10:30:00.000000+07:00",
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
                                        "next_page": {"type": "integer", "example": 2},
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
    def get_specific_article_schema(func):
        """Schema for retrieving a specific article by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_article_get_specific_article",
            summary="Retrieve a specific article by ID",
            description="Retrieve a specific article by its ID.",
            responses={
                200: {
                    "description": "Article retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Article retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "slug": {
                                    "type": "string",
                                    "example": "my-first-article",
                                },
                                "title": {
                                    "type": "string",
                                    "example": "My First Article",
                                },
                                "content": {
                                    "type": "string",
                                    "example": "<p>This is the content of my article...</p>",
                                },
                                "thumbnail": {
                                    "type": "string",
                                    "nullable": True,
                                    "example": "/media/articles/thumbnails/article1.jpg",
                                },
                                "author": {"type": "string", "example": "John Doe"},
                                "tags": {
                                    "type": "string",
                                    "example": "tech, programming, django",
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "My First Article - Tech Blog",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "Learn about the latest in technology.",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "technology, programming, django",
                                },
                                "published_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000+07:00",
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
                    "description": "Article not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Article with id '99' does not exist.",
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
    def get_article_by_slug_schema(func):
        """Schema for retrieving an article by slug."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_article_get_article_by_slug",
            summary="Retrieve an article by slug",
            description="Retrieve an article by its slug identifier.",
            responses={
                200: {
                    "description": "Article retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Article retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "slug": {
                                    "type": "string",
                                    "example": "my-first-article",
                                },
                                "title": {
                                    "type": "string",
                                    "example": "My First Article",
                                },
                                "content": {
                                    "type": "string",
                                    "example": "<p>This is the content of my article...</p>",
                                },
                                "thumbnail": {
                                    "type": "string",
                                    "nullable": True,
                                    "example": "/media/articles/thumbnails/article1.jpg",
                                },
                                "author": {"type": "string", "example": "John Doe"},
                                "tags": {
                                    "type": "string",
                                    "example": "tech, programming, django",
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "My First Article - Tech Blog",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "Learn about the latest in technology.",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "technology, programming, django",
                                },
                                "published_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000+07:00",
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
                    "description": "Article not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Article with slug 'non-existent' does not exist.",
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
    def update_specific_article_schema(func):
        """Schema for updating a specific article by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_article_update_specific_article",
            summary="Update a specific article by ID",
            description="Update a specific article by its ID with new data.",
            request={"multipart/form-data": serializers.PutUpdateArticleRequest},
            responses={
                200: {
                    "description": "Article updated successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Article updated successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "slug": {
                                    "type": "string",
                                    "example": "my-updated-article",
                                },
                                "title": {
                                    "type": "string",
                                    "example": "My Updated Article",
                                },
                                "content": {
                                    "type": "string",
                                    "example": "<p>Updated content...</p>",
                                },
                                "thumbnail": {
                                    "type": "string",
                                    "nullable": True,
                                    "example": "/media/articles/thumbnails/article1.jpg",
                                },
                                "author": {"type": "string", "example": "Jane Smith"},
                                "tags": {"type": "string", "example": "updated, tech"},
                                "meta_title": {
                                    "type": "string",
                                    "example": "Updated Article - Tech Blog",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "Updated description.",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "updated, technology",
                                },
                                "published_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000+07:00",
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
                    "description": "Bad Request - Article not found or validation error",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Article with id '99' does not exist.",
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
    def delete_specific_article_schema(func):
        """Schema for deleting a specific article by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_article_delete_specific_article",
            summary="Delete a specific article by ID",
            description="Delete a specific article by its ID.",
            responses={
                200: {
                    "description": "Article deleted successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Article deleted successfully.",
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
                    "description": "Article not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Article with id '99' does not exist.",
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
    def toggle_article_status_schema(func):
        """Schema for toggling article active status."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_article_toggle_article_status",
            summary="Toggle article active status",
            description="Toggle the active status of a specific article.",
            request=serializers.PatchToggleArticleStatusRequest,
            responses={
                200: {
                    "description": "Article status updated successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Article status updated successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "slug": {
                                    "type": "string",
                                    "example": "my-first-article",
                                },
                                "title": {
                                    "type": "string",
                                    "example": "My First Article",
                                },
                                "content": {
                                    "type": "string",
                                    "example": "<p>This is the content...</p>",
                                },
                                "thumbnail": {
                                    "type": "string",
                                    "nullable": True,
                                    "example": "/media/articles/thumbnails/article1.jpg",
                                },
                                "author": {"type": "string", "example": "John Doe"},
                                "tags": {
                                    "type": "string",
                                    "example": "tech, programming",
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "My First Article - Tech Blog",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "Learn about technology...",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "technology, programming",
                                },
                                "published_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "nullable": True,
                                    "example": None,
                                },
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
                    "description": "Article not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Article with id '99' does not exist.",
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

    @staticmethod
    def publish_article_schema(func):
        """Schema for publishing/unpublishing an article."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_article_publish_article",
            summary="Publish/unpublish an article",
            description="Publish or unpublish an article by setting the published_at timestamp.",
            request=serializers.PatchPublishArticleRequest,
            responses={
                200: {
                    "description": "Article published/unpublished successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Article published successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "slug": {
                                    "type": "string",
                                    "example": "my-first-article",
                                },
                                "title": {
                                    "type": "string",
                                    "example": "My First Article",
                                },
                                "content": {
                                    "type": "string",
                                    "example": "<p>This is the content...</p>",
                                },
                                "thumbnail": {
                                    "type": "string",
                                    "nullable": True,
                                    "example": "/media/articles/thumbnails/article1.jpg",
                                },
                                "author": {"type": "string", "example": "John Doe"},
                                "tags": {
                                    "type": "string",
                                    "example": "tech, programming",
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "My First Article - Tech Blog",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "Learn about technology...",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "technology, programming",
                                },
                                "published_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T12:30:00.000000+07:00",
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
                    "description": "Article not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Article with id '99' does not exist.",
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

    @staticmethod
    def upload_thumbnail_schema(func):
        """Schema for uploading article thumbnail."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_article_upload_thumbnail",
            summary="Upload article thumbnail",
            description="Upload or update the thumbnail image for a specific article. Accepts JPEG, PNG, JPG, and WebP files up to 5MB.",
            request={
                "multipart/form-data": {
                    "type": "object",
                    "properties": {
                        "thumbnail": {
                            "type": "string",
                            "format": "binary",
                            "description": "Image file for article thumbnail",
                        }
                    },
                    "required": ["thumbnail"],
                }
            },
            responses={
                200: {
                    "description": "Thumbnail uploaded successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Thumbnail uploaded successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "slug": {
                                    "type": "string",
                                    "example": "my-first-article",
                                },
                                "title": {
                                    "type": "string",
                                    "example": "My First Article",
                                },
                                "content": {
                                    "type": "string",
                                    "example": "<p>This is the content...</p>",
                                },
                                "thumbnail": {
                                    "type": "string",
                                    "example": "/media/articles/thumbnails/article1_new.jpg",
                                },
                                "author": {"type": "string", "example": "John Doe"},
                                "tags": {
                                    "type": "string",
                                    "example": "tech, programming",
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "My First Article - Tech Blog",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "Learn about technology...",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "technology, programming",
                                },
                                "published_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:30:00.000000+07:00",
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
                                    "example": "2025-11-28T13:00:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T13:00:00.000000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Bad Request - Article not found or invalid file",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Invalid file type. Only JPEG, PNG, JPG, and WebP images are allowed.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T13:00:00.000000",
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
