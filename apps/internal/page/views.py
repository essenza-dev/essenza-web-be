from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from core.decorators import jwt_required, validate_body
from utils import api_response
from docs.api.internal import PageAPI
from services import PageService
from services.page import dto

from . import serializers


class PageViewSet(BaseViewSet):
    """ViewSet for managing pages."""

    _page_service = PageService()

    @PageAPI.create_page_schema
    @jwt_required
    @validate_body(serializers.PostCreatePageRequest)
    def create_page(self, request: Request, validated_data) -> Response:
        """Create a new page."""
        page, error = self._page_service.create_page(
            dto.CreatePageDTO(**validated_data)
        )

        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Page created successfully.",
            data=serializers.PageModelSerializer(page).data,
        )

    @PageAPI.get_pages_schema
    @jwt_required
    def get_pages(self, request: Request) -> Response:
        """Retrieve all pages."""
        page_number = request.GET.get("page", "1")
        page_size = request.GET.get("page_size", "20")

        page = self._page_service.get_paginated_pages(
            str_page_number=page_number, str_page_size=page_size
        )

        return api_response(request).paginated(
            data=serializers.PageModelSerializer(page.object_list, many=True).data,
            page=page,
            message="Pages retrieved successfully.",
        )

    @PageAPI.get_specific_page_schema
    @jwt_required
    def get_specific_page(self, request: Request, pk: int) -> Response:
        """Retrieve a specific page by its ID."""
        page, error = self._page_service.get_specific_page(pk=pk)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Page retrieved successfully.",
            data=serializers.PageModelSerializer(page).data,
        )

    @PageAPI.get_page_by_slug_schema
    @jwt_required
    def get_page_by_slug(self, request: Request, slug: str) -> Response:
        """Retrieve a page by its slug."""
        page, error = self._page_service.get_page_by_slug(slug=slug)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Page retrieved successfully.",
            data=serializers.PageModelSerializer(page).data,
        )

    @PageAPI.update_specific_page_schema
    @jwt_required
    @validate_body(serializers.PutUpdatePageRequest)
    def update_specific_page(
        self, request: Request, pk: int, validated_data
    ) -> Response:
        """Update a specific page by its ID."""
        page, error = self._page_service.update_specific_page(
            pk=pk, data=dto.UpdatePageDTO(**validated_data)
        )
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Page updated successfully.",
            data=serializers.PageModelSerializer(page).data,
        )

    @PageAPI.delete_specific_page_schema
    @jwt_required
    def delete_specific_page(self, request: Request, pk: int) -> Response:
        """Delete a specific page by its ID."""
        error = self._page_service.delete_specific_page(pk=pk)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(message="Page deleted successfully.")

    @PageAPI.toggle_page_status_schema
    @jwt_required
    @validate_body(serializers.PatchTogglePageStatusRequest)
    def toggle_page_status(self, request: Request, pk: int, validated_data) -> Response:
        """Toggle page active status."""
        page, error = self._page_service.toggle_page_status(
            pk=pk, data=dto.TogglePageStatusDTO(**validated_data)
        )
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Page status updated successfully.",
            data=serializers.PageModelSerializer(page).data,
        )
