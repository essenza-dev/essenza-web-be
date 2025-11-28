"""
Product API ViewSet
Handles all product-related API endpoints with proper error handling and validation
"""

import logging
from typing import Dict, Any
from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from core.decorators import jwt_required, validate_body
from utils import api_response
from docs.api.internal import ProductAPI
from services import ProductService
from services.product import dto

from . import serializers

logger = logging.getLogger(__name__)


class ProductViewSet(BaseViewSet):
    """ViewSet for managing products."""

    _product_service = ProductService()

    @ProductAPI.create_product_schema
    @jwt_required
    @validate_body(serializers.PostCreateProductRequest)
    def create_product(
        self, request: Request, validated_data: Dict[str, Any]
    ) -> Response:
        """Create a new product."""
        try:
            logger.info(f"Creating new product with slug: {validated_data.get('slug')}")

            product, error = self._product_service.create_product(
                dto.CreateProductDTO(**validated_data)
            )

            if error:
                logger.error(f"Error creating product: {str(error)}")
                return api_response(request).error(message=str(error))

            logger.info(f"Product created successfully with ID: {product.id}")
            return api_response(request).success(
                message="Product created successfully.",
                data=serializers.ProductModelSerializer(product).data,
            )
        except Exception as e:
            logger.error(f"Unexpected error in create_product: {str(e)}", exc_info=True)
            return api_response(request).server_error(
                message="An unexpected error occurred while creating the product."
            )

    @ProductAPI.get_products_schema
    @jwt_required
    def get_products(self, request: Request) -> Response:
        """Retrieve all products with optional filtering."""
        try:
            # Extract pagination parameters
            page_number = request.GET.get("page", "1")
            page_size = request.GET.get("page_size", "20")

            # Extract filter parameters
            filter_data = {
                "product_type": request.GET.get("type"),
                "lang": request.GET.get("lang"),
                "search": request.GET.get("search"),
                "is_active": request.GET.get("is_active"),
            }

            # Convert is_active to boolean if provided
            if filter_data["is_active"] is not None:
                filter_data["is_active"] = filter_data["is_active"].lower() == "true"

            # Remove None values
            filter_data = {k: v for k, v in filter_data.items() if v is not None}

            filters = dto.ProductFilterDTO(**filter_data) if filter_data else None

            logger.info(f"Retrieving products with filters: {filter_data}")

            page = self._product_service.get_paginated_products(
                str_page_number=page_number, str_page_size=page_size, filters=filters
            )

            return api_response(request).paginated(
                data=serializers.ProductModelSerializer(
                    page.object_list, many=True
                ).data,
                page=page,
                message="Products retrieved successfully.",
            )
        except Exception as e:
            logger.error(f"Unexpected error in get_products: {str(e)}", exc_info=True)
            return api_response(request).server_error(
                message="An unexpected error occurred while retrieving products."
            )

    @ProductAPI.get_specific_product_schema
    @jwt_required
    def get_specific_product(self, request: Request, pk: int) -> Response:
        """Retrieve a specific product by its ID."""
        try:
            logger.info(f"Retrieving product with ID: {pk}")

            product, error = self._product_service.get_specific_product(pk=pk)
            if error:
                logger.warning(f"Product not found: {str(error)}")
                return api_response(request).error(message=str(error))

            return api_response(request).success(
                message="Product retrieved successfully.",
                data=serializers.ProductModelSerializer(product).data,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in get_specific_product: {str(e)}", exc_info=True
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while retrieving the product."
            )

    @ProductAPI.get_product_by_slug_schema
    @jwt_required
    def get_product_by_slug(self, request: Request, slug: str) -> Response:
        """Retrieve a product by its slug."""
        try:
            logger.info(f"Retrieving product with slug: {slug}")

            product, error = self._product_service.get_product_by_slug(slug=slug)
            if error:
                logger.warning(f"Product not found: {str(error)}")
                return api_response(request).error(message=str(error))

            return api_response(request).success(
                message="Product retrieved successfully.",
                data=serializers.ProductModelSerializer(product).data,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in get_product_by_slug: {str(e)}", exc_info=True
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while retrieving the product."
            )

    @ProductAPI.update_specific_product_schema
    @jwt_required
    @validate_body(serializers.PutUpdateProductRequest)
    def update_specific_product(
        self, request: Request, pk: int, validated_data: Dict[str, Any]
    ) -> Response:
        """Update a specific product by its ID."""
        try:
            logger.info(f"Updating product with ID: {pk}")

            product, error = self._product_service.update_specific_product(
                pk=pk, data=dto.UpdateProductDTO(**validated_data)
            )
            if error:
                logger.error(f"Error updating product: {str(error)}")
                return api_response(request).error(message=str(error))

            logger.info(f"Product {pk} updated successfully")
            return api_response(request).success(
                message="Product updated successfully.",
                data=serializers.ProductModelSerializer(product).data,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in update_specific_product: {str(e)}", exc_info=True
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while updating the product."
            )

    @ProductAPI.delete_specific_product_schema
    @jwt_required
    def delete_specific_product(self, request: Request, pk: int) -> Response:
        """Delete a specific product by its ID."""
        try:
            logger.info(f"Deleting product with ID: {pk}")

            if error := self._product_service.delete_specific_product(pk=pk):
                logger.error(f"Error deleting product: {str(error)}")
                return api_response(request).error(message=str(error))

            logger.info(f"Product {pk} deleted successfully")
            return api_response(request).success(
                message="Product deleted successfully."
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in delete_specific_product: {str(e)}", exc_info=True
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while deleting the product."
            )

    @ProductAPI.toggle_product_status_schema
    @jwt_required
    @validate_body(serializers.PatchToggleProductStatusRequest)
    def toggle_product_status(
        self, request: Request, pk: int, validated_data: Dict[str, Any]
    ) -> Response:
        """Toggle product active status."""
        try:
            logger.info(f"Toggling status for product with ID: {pk}")

            product, error = self._product_service.toggle_product_status(
                pk=pk, data=dto.ToggleProductStatusDTO(**validated_data)
            )
            if error:
                logger.error(f"Error toggling product status: {str(error)}")
                return api_response(request).error(message=str(error))

            status_text = "activated" if validated_data["is_active"] else "deactivated"
            logger.info(f"Product {pk} {status_text} successfully")
            return api_response(request).success(
                message="Product status updated successfully.",
                data=serializers.ProductModelSerializer(product).data,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in toggle_product_status: {str(e)}", exc_info=True
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while updating product status."
            )

    @ProductAPI.upload_product_image_schema
    @jwt_required
    @validate_body(serializers.PostUploadProductImageRequest)
    def upload_product_image(
        self, request: Request, pk: int, validated_data: Dict[str, Any]
    ) -> Response:
        """Upload product main image."""
        try:
            logger.info(f"Uploading main image for product with ID: {pk}")

            product, error = self._product_service.update_product_image(
                pk=pk, data=dto.UpdateProductImageDTO(**validated_data)
            )
            if error:
                logger.error(f"Error uploading product image: {str(error)}")
                return api_response(request).error(message=str(error))

            logger.info(f"Product {pk} main image uploaded successfully")
            return api_response(request).success(
                message="Product image uploaded successfully.",
                data=serializers.ProductModelSerializer(product).data,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in upload_product_image: {str(e)}", exc_info=True
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while uploading the product image."
            )

    @ProductAPI.upload_product_gallery_schema
    @jwt_required
    @validate_body(serializers.PostUploadProductGalleryRequest)
    def upload_product_gallery(
        self, request: Request, pk: int, validated_data: Dict[str, Any]
    ) -> Response:
        """Upload product gallery images."""
        try:
            logger.info(f"Uploading gallery images for product with ID: {pk}")

            product, error = self._product_service.update_product_gallery(
                pk=pk, data=dto.UpdateProductGalleryDTO(**validated_data)
            )
            if error:
                logger.error(f"Error uploading product gallery: {str(error)}")
                return api_response(request).error(message=str(error))

            logger.info(f"Product {pk} gallery images uploaded successfully")
            return api_response(request).success(
                message="Product gallery uploaded successfully.",
                data=serializers.ProductModelSerializer(product).data,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in upload_product_gallery: {str(e)}", exc_info=True
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while uploading the product gallery."
            )

    @ProductAPI.delete_product_gallery_image_schema
    @jwt_required
    def delete_product_gallery_image(
        self, request: Request, pk: int, index: int
    ) -> Response:
        """Delete a specific image from product gallery."""
        try:
            logger.info(
                f"Deleting gallery image at index {index} for product with ID: {pk}"
            )

            product, error = self._product_service.delete_product_gallery_image(
                pk=pk, index=index
            )
            if error:
                logger.error(f"Error deleting gallery image: {str(error)}")
                return api_response(request).error(message=str(error))

            logger.info(f"Gallery image at index {index} deleted from product {pk}")
            return api_response(request).success(
                message="Gallery image deleted successfully.",
                data=serializers.ProductModelSerializer(product).data,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in delete_product_gallery_image: {str(e)}",
                exc_info=True,
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while deleting the gallery image."
            )
