from typing import Dict, Any
from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from core.decorators import jwt_required, validate_body
from utils import api_response
from docs.api.internal import DistributorAPI
from services import DistributorService
from services.distributor import dto

from . import serializers


class DistributorViewSet(BaseViewSet):
    """ViewSet for comprehensive distributor management operations."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._distributor_service = DistributorService()

    @DistributorAPI.create_distributor_schema
    @jwt_required
    @validate_body(serializers.PostCreateDistributorRequest)
    def create_distributor(
        self, request: Request, validated_data: Dict[str, Any]
    ) -> Response:
        """Create a new distributor with comprehensive validation."""
        distributor, error = self._distributor_service.create_distributor(
            dto.CreateDistributorDTO(**validated_data)
        )

        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Distributor created successfully.",
            data=serializers.DistributorModelSerializer(distributor).data,
        )

    @DistributorAPI.get_distributors_schema
    @jwt_required
    def get_distributors(self, request: Request) -> Response:
        """Retrieve paginated list of all distributors."""
        page_number = request.GET.get("page", "1")
        page_size = request.GET.get("page_size", "20")

        page = self._distributor_service.get_paginated_distributors(
            str_page_number=page_number, str_page_size=page_size
        )

        return api_response(request).paginated(
            data=serializers.DistributorModelSerializer(
                page.object_list, many=True
            ).data,
            page=page,
            message="Distributors retrieved successfully.",
        )

    @DistributorAPI.get_specific_distributor_schema
    @jwt_required
    def get_specific_distributor(self, request: Request, pk: int) -> Response:
        """Retrieve a specific distributor by ID with error handling."""
        distributor, error = self._distributor_service.get_specific_distributor(pk=pk)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Distributor retrieved successfully.",
            data=serializers.DistributorModelSerializer(distributor).data,
        )

    @DistributorAPI.update_specific_distributor_schema
    @jwt_required
    @validate_body(serializers.PostUpdateDistributorRequest)
    def update_specific_distributor(
        self, request: Request, pk: int, validated_data: Dict[str, Any]
    ) -> Response:
        """Update a specific distributor with partial data support."""
        distributor, error = self._distributor_service.update_specific_distributor(
            pk=pk, data=dto.UpdateDistributorDTO(**validated_data)
        )
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Distributor updated successfully.",
            data=serializers.DistributorModelSerializer(distributor).data,
        )

    @DistributorAPI.delete_specific_distributor_schema
    @jwt_required
    def delete_specific_distributor(self, request: Request, pk: int) -> Response:
        """Delete a specific distributor with atomic transaction."""
        error = self._distributor_service.delete_specific_distributor(pk=pk)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Distributor deleted successfully."
        )
