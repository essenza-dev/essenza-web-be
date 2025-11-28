from functools import wraps
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from apps.internal.project import serializers
from docs.api.constants import DEFAULT_PAGINATION_PARAMS

TAGS = ["Internal / Project"]


class ProjectAPI:
    """API schema definitions for Project endpoints."""

    @staticmethod
    def create_project_schema(func):
        """Schema for creating a new project."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_project_create_project",
            summary="Create Project",
            description="Create a new project with file upload support.",
            request={"multipart/form-data": serializers.PostCreateProjectRequest},
            responses={
                200: {
                    "description": "Project created successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Project created successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "title": {
                                    "type": "string",
                                    "example": "Modern Office Building",
                                },
                                "slug": {
                                    "type": "string",
                                    "example": "modern-office-building",
                                },
                                "location": {
                                    "type": "string",
                                    "example": "Jakarta, Indonesia",
                                },
                                "description": {
                                    "type": "string",
                                    "example": "A comprehensive description of the project",
                                },
                                "image": {
                                    "type": "string",
                                    "format": "uri",
                                    "example": "/media/uploads/projects/modern-office-building.jpg",
                                },
                                "gallery": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "example": [
                                        "/media/uploads/projects/gallery/modern-office-building_gallery_0.jpg"
                                    ],
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "Modern Office Building Project",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "SEO description for the project",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "office, building, modern, architecture",
                                },
                                "is_active": {"type": "boolean", "example": True},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:00:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:00:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:00:00.000000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Bad Request - Validation error",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Project with this slug already exists.",
                        },
                        "meta": {
                            "type": "object",
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
    def get_projects_schema(func):
        """Schema for retrieving all projects."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_project_get_projects",
            summary="Retrieve all projects",
            description="Retrieve all projects with optional filtering and pagination.",
            parameters=[
                *DEFAULT_PAGINATION_PARAMS,
                OpenApiParameter(
                    name="search",
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                    description="Search in title, description, or location",
                    required=False,
                ),
                OpenApiParameter(
                    name="is_active",
                    type=OpenApiTypes.BOOL,
                    location=OpenApiParameter.QUERY,
                    description="Filter by active status",
                    required=False,
                ),
            ],
            responses={
                200: {
                    "description": "Projects retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Projects retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "example": 1},
                                    "title": {
                                        "type": "string",
                                        "example": "Modern Office Building",
                                    },
                                    "slug": {
                                        "type": "string",
                                        "example": "modern-office-building",
                                    },
                                    "location": {
                                        "type": "string",
                                        "example": "Jakarta, Indonesia",
                                    },
                                    "description": {
                                        "type": "string",
                                        "example": "A comprehensive description of the project",
                                    },
                                    "image": {
                                        "type": "string",
                                        "example": "/media/uploads/projects/modern-office-building.jpg",
                                    },
                                    "gallery": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "example": [
                                            "/media/uploads/projects/gallery/modern-office-building_gallery_0.jpg"
                                        ],
                                    },
                                    "meta_title": {
                                        "type": "string",
                                        "example": "Modern Office Building Project",
                                    },
                                    "meta_description": {
                                        "type": "string",
                                        "example": "SEO description for the project",
                                    },
                                    "meta_keywords": {
                                        "type": "string",
                                        "example": "office, building, modern, architecture",
                                    },
                                    "is_active": {"type": "boolean", "example": True},
                                    "created_at": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2025-11-28T10:00:00.000000+07:00",
                                    },
                                    "updated_at": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2025-11-28T10:00:00.000000+07:00",
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
                                    "example": "2025-11-28T10:00:00.000000",
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
    def get_specific_project_schema(func):
        """Schema for retrieving a specific project by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_project_get_specific_project",
            summary="Retrieve a specific project by ID",
            description="Retrieve a specific project by its ID.",
            responses={
                200: {
                    "description": "Project retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Project retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "title": {
                                    "type": "string",
                                    "example": "Modern Office Building",
                                },
                                "slug": {
                                    "type": "string",
                                    "example": "modern-office-building",
                                },
                                "location": {
                                    "type": "string",
                                    "example": "Jakarta, Indonesia",
                                },
                                "description": {
                                    "type": "string",
                                    "example": "A comprehensive description of the project",
                                },
                                "image": {
                                    "type": "string",
                                    "example": "/media/uploads/projects/modern-office-building.jpg",
                                },
                                "gallery": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "example": [
                                        "/media/uploads/projects/gallery/modern-office-building_gallery_0.jpg"
                                    ],
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "Modern Office Building Project",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "SEO description for the project",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "office, building, modern, architecture",
                                },
                                "is_active": {"type": "boolean", "example": True},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:00:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:00:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:00:00.000000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Project not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Project with id '1' does not exist.",
                        },
                        "meta": {
                            "type": "object",
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
    def get_project_by_slug_schema(func):
        """Schema for retrieving a project by slug."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_project_get_project_by_slug",
            summary="Retrieve a project by slug",
            description="Retrieve a project by its slug.",
            responses={
                200: {
                    "description": "Project retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Project retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "title": {
                                    "type": "string",
                                    "example": "Modern Office Building",
                                },
                                "slug": {
                                    "type": "string",
                                    "example": "modern-office-building",
                                },
                                "location": {
                                    "type": "string",
                                    "example": "Jakarta, Indonesia",
                                },
                                "description": {
                                    "type": "string",
                                    "example": "A comprehensive description of the project",
                                },
                                "image": {
                                    "type": "string",
                                    "example": "/media/uploads/projects/modern-office-building.jpg",
                                },
                                "gallery": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "example": [
                                        "/media/uploads/projects/gallery/modern-office-building_gallery_0.jpg"
                                    ],
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "Modern Office Building Project",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "SEO description for the project",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "office, building, modern, architecture",
                                },
                                "is_active": {"type": "boolean", "example": True},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:00:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:00:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:00:00.000000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Project not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Project with slug 'modern-office-building' does not exist.",
                        },
                        "meta": {
                            "type": "object",
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
    def update_specific_project_schema(func):
        """Schema for updating a specific project by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_project_update_specific_project",
            summary="Update a specific project by ID",
            description="Update a specific project by its ID.",
            request={"multipart/form-data": serializers.PutUpdateProjectRequest},
            responses={
                200: {
                    "description": "Project updated successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Project updated successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "title": {
                                    "type": "string",
                                    "example": "Updated Modern Office Building",
                                },
                                "slug": {
                                    "type": "string",
                                    "example": "updated-modern-office-building",
                                },
                                "location": {
                                    "type": "string",
                                    "example": "Jakarta, Indonesia",
                                },
                                "description": {
                                    "type": "string",
                                    "example": "Updated description of the project",
                                },
                                "image": {
                                    "type": "string",
                                    "example": "/media/uploads/projects/updated-modern-office-building.jpg",
                                },
                                "gallery": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "example": [
                                        "/media/uploads/projects/gallery/updated-modern-office-building_gallery_0.jpg"
                                    ],
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "Updated Modern Office Building Project",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "Updated SEO description for the project",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "office, building, modern, architecture, updated",
                                },
                                "is_active": {"type": "boolean", "example": True},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:00:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T11:00:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T11:00:00.000000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Project not found or validation error",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Project with id '1' does not exist.",
                        },
                        "meta": {
                            "type": "object",
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
    def delete_specific_project_schema(func):
        """Schema for deleting a specific project by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_project_delete_specific_project",
            summary="Delete a specific project by ID",
            description="Delete a specific project by its ID.",
            responses={
                200: {
                    "description": "Project deleted successfully.",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Project deleted successfully.",
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
                    "description": "Project not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Project with id '1' does not exist.",
                        },
                        "meta": {
                            "type": "object",
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
    def toggle_project_status_schema(func):
        """Schema for toggling project active status."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_project_toggle_project_status",
            summary="Toggle project active status",
            description="Toggle the active status of a project.",
            request=serializers.PatchToggleProjectStatusRequest,
            responses={
                200: {
                    "description": "Project status toggled successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Project status updated successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "title": {
                                    "type": "string",
                                    "example": "Modern Office Building",
                                },
                                "slug": {
                                    "type": "string",
                                    "example": "modern-office-building",
                                },
                                "location": {
                                    "type": "string",
                                    "example": "Jakarta, Indonesia",
                                },
                                "description": {
                                    "type": "string",
                                    "example": "A comprehensive description of the project",
                                },
                                "image": {
                                    "type": "string",
                                    "example": "/media/uploads/projects/modern-office-building.jpg",
                                },
                                "gallery": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "example": [
                                        "/media/uploads/projects/gallery/modern-office-building_gallery_0.jpg"
                                    ],
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "Modern Office Building Project",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "SEO description for the project",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "office, building, modern, architecture",
                                },
                                "is_active": {"type": "boolean", "example": False},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:00:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T11:00:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T11:00:00.000000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Project not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Project with id '1' does not exist.",
                        },
                        "meta": {
                            "type": "object",
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
    def upload_project_image_schema(func):
        """Schema for uploading project main image."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_project_upload_project_image",
            summary="Upload project main image",
            description="Upload or update the main image for a project.",
            request={"multipart/form-data": serializers.PostUploadProjectImageRequest},
            responses={
                200: {
                    "description": "Project image uploaded successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Project image uploaded successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "title": {
                                    "type": "string",
                                    "example": "Modern Office Building",
                                },
                                "slug": {
                                    "type": "string",
                                    "example": "modern-office-building",
                                },
                                "location": {
                                    "type": "string",
                                    "example": "Jakarta, Indonesia",
                                },
                                "description": {
                                    "type": "string",
                                    "example": "A comprehensive description of the project",
                                },
                                "image": {
                                    "type": "string",
                                    "example": "/media/uploads/projects/new-modern-office-building.jpg",
                                },
                                "gallery": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "example": [
                                        "/media/uploads/projects/gallery/modern-office-building_gallery_0.jpg"
                                    ],
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "Modern Office Building Project",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "SEO description for the project",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "office, building, modern, architecture",
                                },
                                "is_active": {"type": "boolean", "example": True},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:00:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T11:00:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T11:00:00.000000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Project not found or invalid file",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Project with id '1' does not exist.",
                        },
                        "meta": {
                            "type": "object",
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
    def upload_project_gallery_schema(func):
        """Schema for uploading project gallery images."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_project_upload_project_gallery",
            summary="Upload project gallery images",
            description="Upload multiple images to the project gallery.",
            request={
                "multipart/form-data": serializers.PostUploadProjectGalleryRequest
            },
            responses={
                200: {
                    "description": "Project gallery uploaded successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Project gallery uploaded successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "title": {
                                    "type": "string",
                                    "example": "Modern Office Building",
                                },
                                "slug": {
                                    "type": "string",
                                    "example": "modern-office-building",
                                },
                                "location": {
                                    "type": "string",
                                    "example": "Jakarta, Indonesia",
                                },
                                "description": {
                                    "type": "string",
                                    "example": "A comprehensive description of the project",
                                },
                                "image": {
                                    "type": "string",
                                    "example": "/media/uploads/projects/modern-office-building.jpg",
                                },
                                "gallery": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "example": [
                                        "/media/uploads/projects/gallery/modern-office-building_gallery_0.jpg",
                                        "/media/uploads/projects/gallery/modern-office-building_gallery_1.jpg",
                                    ],
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "Modern Office Building Project",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "SEO description for the project",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "office, building, modern, architecture",
                                },
                                "is_active": {"type": "boolean", "example": True},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:00:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T11:00:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T11:00:00.000000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Project not found or invalid files",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Project with id '1' does not exist.",
                        },
                        "meta": {
                            "type": "object",
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
    def delete_project_gallery_image_schema(func):
        """Schema for deleting a specific gallery image by index."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_project_delete_project_gallery_image",
            summary="Delete gallery image by index",
            description="Delete a specific image from the project gallery by index.",
            responses={
                200: {
                    "description": "Gallery image deleted successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Gallery image deleted successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "title": {
                                    "type": "string",
                                    "example": "Modern Office Building",
                                },
                                "slug": {
                                    "type": "string",
                                    "example": "modern-office-building",
                                },
                                "location": {
                                    "type": "string",
                                    "example": "Jakarta, Indonesia",
                                },
                                "description": {
                                    "type": "string",
                                    "example": "A comprehensive description of the project",
                                },
                                "image": {
                                    "type": "string",
                                    "example": "/media/uploads/projects/modern-office-building.jpg",
                                },
                                "gallery": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "example": [],
                                },
                                "meta_title": {
                                    "type": "string",
                                    "example": "Modern Office Building Project",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "SEO description for the project",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "office, building, modern, architecture",
                                },
                                "is_active": {"type": "boolean", "example": True},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T10:00:00.000000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T11:00:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-28T11:00:00.000000",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Project not found or invalid index",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Gallery image at index 0 does not exist for project 1.",
                        },
                        "meta": {
                            "type": "object",
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
