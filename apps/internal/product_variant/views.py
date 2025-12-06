"""
Product Variant API ViewSet
Handles all product variant-related API endpoints with proper error handling and validation
"""

import logging
from typing import Dict, Any
from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from core.decorators import jwt_required, validate_body
from utils import api_response
from docs.api.internal import ProductVariantAPI
from services import ProductVariantService
from services.product_variant import dto

from . import serializers

logger = logging.getLogger(__name__)


class ProductVariantViewSet(BaseViewSet):
    """ViewSet for comprehensive product variant management operations."""

    _variant_service = ProductVariantService()

    @ProductVariantAPI.create_product_variant_schema
    @jwt_required
    @validate_body(serializers.PostCreateProductVariantRequest)
    def create_product_variant(
        self, request: Request, product_slug: str, validated_data: Dict[str, Any]
    ) -> Response:
        """Create a new variant for a specific product."""
        try:
            logger.info(f"Creating new variant for product {product_slug}")

            variant, error = self._variant_service.use_context(request).create_variant(
                product_slug=product_slug,
                data=dto.CreateProductVariantDTO(**validated_data),
            )

            if error:
                # Extract clean error message from ValidationError
                error_message = (
                    error.messages[0]
                    if hasattr(error, "messages") and error.messages
                    else str(error)
                )
                logger.error(f"Error creating variant: {error_message}")
                return api_response(request).error(message=error_message)

            logger.info(f"Variant created successfully with ID: {variant.id}")
            return api_response(request).success(
                message="Product variant created successfully.",
                data=serializers.ProductVariantModelSerializer(variant).data,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in create_product_variant: {str(e)}", exc_info=True
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while creating the variant."
            )

    @ProductVariantAPI.get_product_variants_by_slug_schema
    @jwt_required
    def get_product_variants_by_slug(
        self, request: Request, product_slug: str
    ) -> Response:
        """Retrieve all variants for a specific product by slug."""
        try:
            logger.info(f"Retrieving variants for product slug: {product_slug}")

            variants = self._variant_service.get_variants_by_product_slug(
                product_slug=product_slug
            )

            return api_response(request).success(
                message="Product variants retrieved successfully.",
                data=serializers.ProductVariantModelSerializer(
                    variants, many=True
                ).data,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in get_product_variants_by_slug: {str(e)}",
                exc_info=True,
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while retrieving variants."
            )

    @ProductVariantAPI.get_specific_product_variant_schema
    @jwt_required
    def get_specific_product_variant(self, request: Request, pk: int) -> Response:
        """Retrieve a specific product variant by ID."""
        try:
            logger.info(f"Retrieving variant with ID: {pk}")

            variant, error = self._variant_service.get_specific_variant(pk=pk)
            if error:
                return api_response(request).error(str(error))

            return api_response(request).success(
                message="Product variant retrieved successfully.",
                data=serializers.ProductVariantModelSerializer(variant).data,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in get_specific_product_variant: {str(e)}",
                exc_info=True,
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while retrieving the variant."
            )

    @ProductVariantAPI.update_specific_product_variant_schema
    @jwt_required
    @validate_body(serializers.PutUpdateProductVariantRequest)
    def update_specific_product_variant(
        self, request: Request, pk: int, validated_data: Dict[str, Any]
    ) -> Response:
        """Update a specific product variant."""
        try:
            logger.info(f"Updating variant with ID: {pk}")

            variant, error = self._variant_service.use_context(
                request
            ).update_specific_variant(
                pk=pk, data=dto.UpdateProductVariantDTO(**validated_data)
            )
            if error:
                error_message = (
                    error.messages[0]
                    if hasattr(error, "messages") and error.messages
                    else str(error)
                )
                logger.error(f"Error updating variant: {error_message}")
                return api_response(request).error(message=error_message)

            logger.info(f"Variant {pk} updated successfully")
            return api_response(request).success(
                message="Product variant updated successfully.",
                data=serializers.ProductVariantModelSerializer(variant).data,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in update_specific_product_variant: {str(e)}",
                exc_info=True,
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while updating the variant."
            )

    @ProductVariantAPI.delete_specific_product_variant_schema
    @jwt_required
    def delete_specific_product_variant(self, request: Request, pk: int) -> Response:
        """Delete a specific product variant."""
        try:
            logger.info(f"Deleting variant with ID: {pk}")

            if error := self._variant_service.use_context(
                request
            ).delete_specific_variant(pk=pk):
                error_message = (
                    error.messages[0]
                    if hasattr(error, "messages") and error.messages
                    else str(error)
                )
                logger.error(f"Error deleting variant: {error_message}")
                return api_response(request).error(message=error_message)

            logger.info(f"Variant {pk} deleted successfully")
            return api_response(request).success(
                message="Product variant deleted successfully."
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in delete_specific_product_variant: {str(e)}",
                exc_info=True,
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while deleting the variant."
            )

    @ProductVariantAPI.toggle_product_variant_status_schema
    @jwt_required
    @validate_body(serializers.PatchToggleProductVariantStatusRequest)
    def toggle_product_variant_status(
        self, request: Request, pk: int, validated_data: Dict[str, Any]
    ) -> Response:
        """Toggle product variant active status."""
        try:
            logger.info(f"Toggling status for variant with ID: {pk}")

            variant, error = self._variant_service.use_context(
                request
            ).toggle_variant_status(
                pk=pk, data=dto.ToggleProductVariantStatusDTO(**validated_data)
            )
            if error:
                error_message = (
                    error.messages[0]
                    if hasattr(error, "messages") and error.messages
                    else str(error)
                )
                logger.error(f"Error toggling variant status: {error_message}")
                return api_response(request).error(message=error_message)

            status_text = "activated" if validated_data["is_active"] else "deactivated"
            logger.info(f"Variant {pk} {status_text} successfully")
            return api_response(request).success(
                message="Product variant status updated successfully.",
                data=serializers.ProductVariantModelSerializer(variant).data,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in toggle_product_variant_status: {str(e)}",
                exc_info=True,
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while updating variant status."
            )

    @ProductVariantAPI.update_product_variant_specifications_schema
    @jwt_required
    @validate_body(serializers.PostUpdateProductVariantSpecificationsRequest)
    def update_product_variant_specifications(
        self, request: Request, pk: int, validated_data: Dict[str, Any]
    ) -> Response:
        """Add or update product variant specifications."""
        try:
            logger.info(f"Updating specifications for variant with ID: {pk}")

            variant, error = self._variant_service.use_context(
                request
            ).update_variant_specifications(
                pk=pk, data=dto.UpdateProductVariantSpecificationsDTO(**validated_data)
            )
            if error:
                error_message = (
                    error.messages[0]
                    if hasattr(error, "messages") and error.messages
                    else str(error)
                )
                logger.error(f"Error updating variant specifications: {error_message}")
                return api_response(request).error(message=error_message)

            logger.info(f"Variant {pk} specifications updated successfully")
            return api_response(request).success(
                message="Product variant specifications updated successfully.",
                data=serializers.ProductVariantModelSerializer(variant).data,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in update_product_variant_specifications: {str(e)}",
                exc_info=True,
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while updating variant specifications."
            )

    @ProductVariantAPI.delete_product_variant_specification_schema
    @jwt_required
    def delete_product_variant_specification(
        self, request: Request, pk: int, spec_slug: str
    ) -> Response:
        """Delete a specific product variant specification."""
        try:
            logger.info(f"Deleting specification {spec_slug} from variant {pk}")

            if error := self._variant_service.use_context(
                request
            ).delete_variant_specification(variant_id=pk, spec_slug=spec_slug):
                error_message = (
                    error.messages[0]
                    if hasattr(error, "messages") and error.messages
                    else str(error)
                )
                logger.error(f"Error deleting variant specification: {error_message}")
                return api_response(request).error(message=error_message)

            logger.info(
                f"Specification {spec_slug} deleted from variant {pk} successfully"
            )
            return api_response(request).success(
                message="Product variant specification deleted successfully."
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in delete_product_variant_specification: {str(e)}",
                exc_info=True,
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while deleting the variant specification."
            )
