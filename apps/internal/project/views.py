from typing import Dict, Any
from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from core.decorators import jwt_required, validate_body
from utils import api_response
from docs.api.internal import ProjectAPI
from services import ProjectService
from services.project import dto

from . import serializers


class ProjectViewSet(BaseViewSet):
    """ViewSet for managing projects."""

    _project_service = ProjectService()

    @ProjectAPI.create_project_schema
    @jwt_required
    @validate_body(serializers.PostCreateProjectRequest)
    def create_project(
        self, request: Request, validated_data: Dict[str, Any]
    ) -> Response:
        """Create a new project."""
        project, error = self._project_service.create_project(
            dto.CreateProjectDTO(**validated_data)
        )

        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Project created successfully.",
            data=serializers.ProjectModelSerializer(project).data,
        )

    @ProjectAPI.get_projects_schema
    @jwt_required
    def get_projects(self, request: Request) -> Response:
        """Retrieve all projects with optional filtering."""
        # Get query parameters for filtering
        search = request.query_params.get("search")
        is_active = request.query_params.get("is_active")

        # Convert is_active to boolean if provided
        is_active_bool = None
        if is_active is not None:
            is_active_bool = is_active.lower() in ["true", "1", "yes"]

        # Create filter DTO
        filters = dto.ProjectFilterDTO(
            search=search,
            is_active=is_active_bool,
        )

        # Get pagination parameters
        page = request.query_params.get("page", "1")
        page_size = request.query_params.get("page_size", "20")

        # Get paginated projects
        projects_page = self._project_service.get_paginated_projects(
            str_page_number=page,
            str_page_size=page_size,
            filters=filters,
        )

        # Serialize data
        serialized_data = serializers.ProjectModelSerializer(
            projects_page.object_list, many=True
        ).data

        return api_response(request).paginated(
            data=serialized_data,
            page=projects_page,
            message="Projects retrieved successfully.",
        )

    @ProjectAPI.get_specific_project_schema
    @jwt_required
    def get_specific_project(self, request: Request, pk: int) -> Response:
        """Retrieve a specific project by its ID."""
        project, error = self._project_service.get_specific_project(pk=pk)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Project retrieved successfully.",
            data=serializers.ProjectModelSerializer(project).data,
        )

    @ProjectAPI.get_project_by_slug_schema
    @jwt_required
    def get_project_by_slug(self, request: Request, slug: str) -> Response:
        """Retrieve a project by its slug."""
        project, error = self._project_service.get_project_by_slug(slug=slug)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Project retrieved successfully.",
            data=serializers.ProjectModelSerializer(project).data,
        )

    @ProjectAPI.update_specific_project_schema
    @jwt_required
    @validate_body(serializers.PutUpdateProjectRequest)
    def update_specific_project(
        self, request: Request, pk: int, validated_data: Dict[str, Any]
    ) -> Response:
        """Update a specific project by its ID."""
        project, error = self._project_service.update_specific_project(
            pk=pk, data=dto.UpdateProjectDTO(**validated_data)
        )
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Project updated successfully.",
            data=serializers.ProjectModelSerializer(project).data,
        )

    @ProjectAPI.delete_specific_project_schema
    @jwt_required
    def delete_specific_project(self, request: Request, pk: int) -> Response:
        """Delete a specific project by its ID."""
        error = self._project_service.delete_specific_project(pk=pk)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(message="Project deleted successfully.")

    @ProjectAPI.toggle_project_status_schema
    @jwt_required
    @validate_body(serializers.PatchToggleProjectStatusRequest)
    def toggle_project_status(
        self, request: Request, pk: int, validated_data: Dict[str, Any]
    ) -> Response:
        """Toggle project active status."""
        project, error = self._project_service.toggle_project_status(
            pk=pk, data=dto.ToggleProjectStatusDTO(**validated_data)
        )
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Project status updated successfully.",
            data=serializers.ProjectModelSerializer(project).data,
        )

    @ProjectAPI.upload_project_image_schema
    @jwt_required
    @validate_body(serializers.PostUploadProjectImageRequest)
    def upload_project_image(
        self, request: Request, pk: int, validated_data: Dict[str, Any]
    ) -> Response:
        """Upload or update project main image."""
        project, error = self._project_service.update_project_image(
            pk=pk, data=dto.UpdateProjectImageDTO(**validated_data)
        )
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Project image uploaded successfully.",
            data=serializers.ProjectModelSerializer(project).data,
        )

    @ProjectAPI.upload_project_gallery_schema
    @jwt_required
    @validate_body(serializers.PostUploadProjectGalleryRequest)
    def upload_project_gallery(
        self, request: Request, pk: int, validated_data: Dict[str, Any]
    ) -> Response:
        """Upload project gallery images."""
        project, error = self._project_service.update_project_gallery(
            pk=pk, data=dto.UpdateProjectGalleryDTO(**validated_data)
        )
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Project gallery uploaded successfully.",
            data=serializers.ProjectModelSerializer(project).data,
        )

    @ProjectAPI.delete_project_gallery_image_schema
    @jwt_required
    def delete_project_gallery_image(
        self, request: Request, pk: int, index: int
    ) -> Response:
        """Delete a specific image from project gallery by index."""
        project, error = self._project_service.delete_project_gallery_image(
            pk=pk, index=index
        )
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Gallery image deleted successfully.",
            data=serializers.ProjectModelSerializer(project).data,
        )
