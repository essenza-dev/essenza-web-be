from typing import Dict, Any
from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from core.decorators import jwt_required, validate_body
from utils import api_response
from docs.api.internal import StoreAPI
from services import StoreService
from services.store import dto

from . import serializers


class StoreViewSet(BaseViewSet):
    """ViewSet for comprehensive store management operations."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._store_service = StoreService()

    @StoreAPI.create_store_schema
    @jwt_required
    @validate_body(serializers.PostCreateStoreRequest)
    def create_store(
        self, request: Request, validated_data: Dict[str, Any]
    ) -> Response:
        """Create a new store with comprehensive validation."""
        store, error = self._store_service.create_store(
            dto.CreateStoreDTO(**validated_data)
        )

        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Store created successfully.",
            data=serializers.StoreModelSerializer(store).data,
        )

    @StoreAPI.get_stores_schema
    @jwt_required
    def get_stores(self, request: Request) -> Response:
        """Retrieve paginated list of all stores."""
        page_number = request.GET.get("page", "1")
        page_size = request.GET.get("page_size", "20")

        page = self._store_service.get_paginated_stores(
            str_page_number=page_number, str_page_size=page_size
        )
        return api_response(request).paginated(
            message="Stores retrieved successfully.",
            data=serializers.StoreModelSerializer(page, many=True).data,
            page=page,
        )

    @StoreAPI.get_specific_store_schema
    @jwt_required
    def get_specific_store(self, request: Request, pk: int) -> Response:
        """Retrieve a specific store by ID with error handling."""
        store, error = self._store_service.get_specific_store(pk=pk)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Store retrieved successfully.",
            data=serializers.StoreModelSerializer(store).data,
        )

    @StoreAPI.update_specific_store_schema
    @jwt_required
    @validate_body(serializers.PostUpdateStoreRequest)
    def update_specific_store(
        self, request: Request, pk: int, validated_data: Dict[str, Any]
    ) -> Response:
        """Update a specific store with partial data support."""
        store, error = self._store_service.update_specific_store(
            pk=pk, data=dto.UpdateStoreDTO(**validated_data)
        )
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Store updated successfully.",
            data=serializers.StoreModelSerializer(store).data,
        )

    @StoreAPI.delete_specific_store_schema
    @jwt_required
    def delete_specific_store(self, request: Request, pk: int) -> Response:
        """Delete a specific store by ID with comprehensive error handling."""
        error = self._store_service.delete_specific_store(pk=pk)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(message="Store deleted successfully.")
