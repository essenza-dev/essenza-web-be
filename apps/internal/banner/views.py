from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from core.decorators import jwt_required, validate_body
from utils import api_response
from docs.api.internal import BannerAPI
from services import BannerService
from services.banner import dto

from . import serializers


class BannerViewSet(BaseViewSet):
    """ViewSet for managing banners."""

    _banner_service = BannerService()

    @BannerAPI.create_banner_schema
    @jwt_required
    @validate_body(serializers.PostCreateBannerRequest)
    def create_banner(self, request: Request, validated_data) -> Response:
        """Create a new banner."""
        banner, error = self._banner_service.create_banner(
            dto.CreateBannerDTO(**validated_data)
        )

        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Banner created successfully.",
            data=serializers.BannerModelSerializer(banner).data,
        )

    @BannerAPI.get_banners_schema
    @jwt_required
    def get_banners(self, request: Request) -> Response:
        """Retrieve all banners."""
        page_number = request.GET.get("page", "1")
        page_size = request.GET.get("page_size", "20")

        page = self._banner_service.get_paginated_banners(
            str_page_number=page_number, str_page_size=page_size
        )

        return api_response(request).paginated(
            data=serializers.BannerModelSerializer(page.object_list, many=True).data,
            page=page,
            message="Banners retrieved successfully.",
        )

    @BannerAPI.get_specific_banner_schema
    @jwt_required
    def get_specific_banner(self, request: Request, pk: int) -> Response:
        """Retrieve a specific banner by its ID."""
        banner, error = self._banner_service.get_specific_banner(pk=pk)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Banner retrieved successfully.",
            data=serializers.BannerModelSerializer(banner).data,
        )

    @BannerAPI.update_specific_banner_schema
    @jwt_required
    @validate_body(serializers.PostUpdateBannerRequest)
    def update_specific_banner(
        self, request: Request, pk: int, validated_data
    ) -> Response:
        """Update a specific banner by its ID."""
        banner, error = self._banner_service.update_specific_banner(
            pk=pk, data=dto.UpdateBannerDTO(**validated_data)
        )
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Banner updated successfully.",
            data=serializers.BannerModelSerializer(banner).data,
        )

    @BannerAPI.delete_specific_banner_schema
    @jwt_required
    def delete_specific_banner(self, request: Request, pk: int) -> Response:
        """Delete a specific banner by its ID."""
        error = self._banner_service.delete_specific_banner(pk=pk)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(message="Banner deleted successfully.")
