"""
Specification API ViewSet
Handles all specification-related API endpoints with proper error handling and validation
"""

import logging
from typing import Dict, Any
from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from core.decorators import jwt_required, validate_body
from utils import api_response
from docs.api.internal import SpecificationAPI
from services import SpecificationService
from services.specification import dto

from . import serializers

logger = logging.getLogger(__name__)


class SpecificationViewSet(BaseViewSet):
    """ViewSet for comprehensive specification management operations."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._specification_service = SpecificationService()

    @SpecificationAPI.get_specifications_schema
    @jwt_required
    def get_specifications(self, request: Request) -> Response:
        """Retrieve all specifications with optimized queryset."""
        specifications = self._specification_service.get_specifications()
        return api_response(request).success(
            message="Specifications retrieved successfully.",
            data=serializers.SpecificationModelSerializer(
                specifications, many=True
            ).data,
        )

    @SpecificationAPI.get_specific_specification_schema
    @jwt_required
    def get_specific_specification(self, request: Request, slug: str) -> Response:
        """Retrieve a specific specification by slug with error handling."""
        specification, error = self._specification_service.get_specification_by_slug(
            slug=slug
        )
        if error:
            return api_response(request).not_found(message=str(error))

        return api_response(request).success(
            message="Specification retrieved successfully.",
            data=serializers.SpecificationModelSerializer(specification).data,
        )

    @SpecificationAPI.update_specific_specification_schema
    @jwt_required
    @validate_body(serializers.PutUpdateSpecificationRequest)
    def update_specific_specification(
        self, request: Request, slug: str, validated_data: Dict[str, Any]
    ) -> Response:
        """Update a specific specification with comprehensive validation."""
        specification, error = self._specification_service.use_context(
            request
        ).update_specification_by_slug(
            slug=slug, data=dto.UpdateSpecificationDTO(**validated_data)
        )
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Specification updated successfully.",
            data=serializers.SpecificationModelSerializer(specification).data,
        )
