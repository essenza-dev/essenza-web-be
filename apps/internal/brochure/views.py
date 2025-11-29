"""
Brochure ViewSet
Contains all view logic for brochure-related API endpoints
"""

from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from core.decorators import jwt_required, validate_body
from utils import api_response
from docs.api.internal import BrochureAPI
from services import BrochureService
from services.brochure import dto

from . import serializers


class BrochureViewSet(BaseViewSet):
    """ViewSet for managing brochures."""

    _brochure_service = BrochureService()

    @BrochureAPI.create_brochure_schema
    @jwt_required
    @validate_body(serializers.PostCreateBrochureRequest)
    def create_brochure(self, request: Request, validated_data) -> Response:
        """Create a new brochure."""
        brochure, error = self._brochure_service.use_context(request).create_brochure(
            dto.CreateBrochureDTO(**validated_data)
        )

        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Brochure created successfully.",
            data=serializers.BrochureModelSerializer(brochure).data,
        )

    @BrochureAPI.get_brochures_schema
    @jwt_required
    def get_brochures(self, request: Request) -> Response:
        """Retrieve all brochures with optional filtering."""
        search = request.GET.get("search", "").strip()
        page_number = request.GET.get("page", "1")
        page_size = request.GET.get("page_size", "20")

        # Get filtered and paginated brochures
        if search:
            page = self._brochure_service.get_brochures_with_filters(
                search=search, str_page_number=page_number, str_page_size=page_size
            )
        else:
            page = self._brochure_service.get_paginated_brochures(
                str_page_number=page_number, str_page_size=page_size
            )

        return api_response(request).paginated(
            data=serializers.BrochureModelSerializer(page.object_list, many=True).data,
            page=page,
            message="Brochures retrieved successfully.",
        )

    @BrochureAPI.get_specific_brochure_schema
    @jwt_required
    def get_specific_brochure(self, request: Request, pk: int) -> Response:
        """Retrieve a specific brochure by its ID."""
        brochure, error = self._brochure_service.get_specific_brochure(pk=pk)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Brochure retrieved successfully.",
            data=serializers.BrochureModelSerializer(brochure).data,
        )

    @BrochureAPI.update_specific_brochure_schema
    @jwt_required
    @validate_body(serializers.PutUpdateBrochureRequest)
    def update_specific_brochure(
        self, request: Request, pk: int, validated_data
    ) -> Response:
        """Update a specific brochure by its ID."""
        brochure, error = self._brochure_service.use_context(
            request
        ).update_specific_brochure(pk=pk, data=dto.UpdateBrochureDTO(**validated_data))
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Brochure updated successfully.",
            data=serializers.BrochureModelSerializer(brochure).data,
        )

    @BrochureAPI.delete_specific_brochure_schema
    @jwt_required
    def delete_specific_brochure(self, request: Request, pk: int) -> Response:
        """Delete a specific brochure by its ID."""
        error = self._brochure_service.use_context(request).delete_specific_brochure(
            pk=pk
        )
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Brochure deleted successfully.",
        )

    @BrochureAPI.upload_brochure_file_schema
    @jwt_required
    @validate_body(serializers.PostUploadBrochureFileRequest)
    def upload_brochure_file(
        self, request: Request, pk: int, validated_data
    ) -> Response:
        """Upload a file for a specific brochure."""
        brochure, error = self._brochure_service.use_context(
            request
        ).upload_brochure_file(pk=pk, data=dto.UploadBrochureFileDTO(**validated_data))
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Brochure file uploaded successfully.",
            data=serializers.BrochureModelSerializer(brochure).data,
        )
