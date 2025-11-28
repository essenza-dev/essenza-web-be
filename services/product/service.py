"""
Product Service Module
Handles all business logic for product management operations.
"""

import logging
import os
from typing import Tuple, List, Optional, Sequence
from django.db.models.query import QuerySet
from django.db.models import Q
from django.core.paginator import Page
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.exceptions import ValidationError

from core.service import BaseService
from core.models import Product, Brochure
from . import dto

logger = logging.getLogger(__name__)


class ProductService(BaseService):
    """Service class for managing product operations with comprehensive CRUD functionality."""

    def validate_slug_uniqueness(
        self, slug: str, exclude_id: Optional[int] = None
    ) -> bool:
        """
        Validate if slug is unique.

        Args:
            slug: The slug to validate
            exclude_id: Product ID to exclude from validation (for updates)

        Returns:
            True if slug is unique, False otherwise
        """
        queryset = Product.objects.filter(slug=slug)
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return not queryset.exists()

    def validate_brochure_exists(self, brochure_id: int) -> bool:
        """
        Validate if brochure exists.

        Args:
            brochure_id: The brochure ID to validate

        Returns:
            True if brochure exists, False otherwise
        """
        return Brochure.objects.filter(id=brochure_id).exists()

    def create_product(
        self, data: dto.CreateProductDTO
    ) -> Tuple[Product, Optional[Exception]]:
        """
        Create a new product with image and gallery handling.

        Args:
            data: Product creation data transfer object

        Returns:
            Tuple containing the created product and any error that occurred
        """
        try:
            # Validate slug uniqueness
            if data.slug and not self.validate_slug_uniqueness(data.slug):
                return Product(), ValidationError(
                    "Product with this slug already exists."
                )

            # Validate brochure exists if provided
            if data.brochure_id and not self.validate_brochure_exists(data.brochure_id):
                return Product(), ValidationError(
                    f"Brochure with id {data.brochure_id} does not exist."
                )

            product_data = data.to_dict()

            # Process main image upload
            if isinstance(data.image, InMemoryUploadedFile):
                product_data["image"] = data.image

            # Process gallery images upload
            if data.gallery:
                product_data["gallery"] = self._process_gallery_images(
                    data.gallery, data.slug
                )

            # Handle brochure relationship
            product_data["brochure"] = (
                self._get_brochure_by_id(data.brochure_id) if data.brochure_id else None
            )
            product_data.pop("brochure_id", None)

            product = Product.objects.create(**product_data)
            logger.info(f"Product created successfully with id {product.id}")
            return product, None

        except Exception as e:
            logger.error(f"Error creating product: {str(e)}", exc_info=True)
            return Product(), e

    def get_products(
        self, filters: Optional[dto.ProductFilterDTO] = None
    ) -> QuerySet[Product]:
        """
        Retrieve all products with optional filtering and optimized queries.

        Args:
            filters: Optional filter criteria for product search

        Returns:
            QuerySet of filtered and ordered products
        """
        queryset = Product.objects.select_related("brochure")

        if filters:
            filter_conditions = Q()

            if filters.product_type:
                filter_conditions &= Q(product_type=filters.product_type)
            if filters.lang:
                filter_conditions &= Q(lang=filters.lang)
            if filters.search:
                search_q = (
                    Q(name__icontains=filters.search)
                    | Q(description__icontains=filters.search)
                    | Q(model__icontains=filters.search)
                )
                filter_conditions &= search_q
            if filters.is_active is not None:
                filter_conditions &= Q(is_active=filters.is_active)

            queryset = queryset.filter(filter_conditions)

        return queryset.order_by("-created_at")

    def get_paginated_products(
        self,
        str_page_number: str,
        str_page_size: str,
        filters: Optional[dto.ProductFilterDTO] = None,
    ) -> Page:
        """
        Retrieve paginated products with optional filtering.

        Args:
            str_page_number: Page number as string
            str_page_size: Page size as string
            filters: Optional filter criteria for product search

        Returns:
            Page object containing filtered and paginated products
        """
        queryset = self.get_products(filters)
        return self.get_paginated_data(queryset, str_page_number, str_page_size)

    def get_specific_product(self, pk: int) -> Tuple[Product, Optional[Exception]]:
        """
        Retrieve a specific product by its ID with optimized query.

        Args:
            pk: Product ID to retrieve

        Returns:
            Tuple containing the product and any error that occurred
        """
        try:
            product = Product.objects.select_related("brochure").get(id=pk)
            return product, None
        except Product.DoesNotExist:
            return self._handle_product_not_found_by_id(pk)
        except Exception as e:
            logger.error(f"Error retrieving product {pk}: {str(e)}", exc_info=True)
            return Product(), e

    def get_product_by_slug(self, slug: str) -> Tuple[Product, Optional[Exception]]:
        """
        Retrieve a product by its unique slug identifier.

        Args:
            slug: Product slug to search for

        Returns:
            Tuple containing the product and any error that occurred
        """
        try:
            product = Product.objects.select_related("brochure").get(slug=slug)
            return product, None
        except Product.DoesNotExist:
            return self._handle_product_not_found_by_slug(slug)
        except Exception as e:
            logger.error(
                f"Error retrieving product by slug '{slug}': {str(e)}", exc_info=True
            )
            return Product(), e

    def update_specific_product(
        self, pk: int, data: dto.UpdateProductDTO
    ) -> Tuple[Product, Optional[Exception]]:
        """
        Update a specific product with comprehensive data handling.

        Args:
            pk: Product ID to update
            data: Product update data transfer object

        Returns:
            Tuple containing the updated product and any error that occurred
        """
        try:
            return self._update_product_with_data_handling(pk, data)
        except Product.DoesNotExist:
            return self._handle_product_not_found_by_id(pk)
        except Exception as e:
            logger.error(f"Error updating product {pk}: {str(e)}", exc_info=True)
            return Product(), e

    def delete_specific_product(self, pk: int) -> Optional[Exception]:
        """
        Delete a specific product and its associated files.

        Args:
            pk: Product ID to delete

        Returns:
            Exception if error occurs, None if successful
        """
        try:
            return self._delete_product_with_cleanup(pk)
        except Product.DoesNotExist:
            error_msg = f"Product with id '{pk}' does not exist."
            logger.warning(error_msg)
            return ValidationError(error_msg)
        except Exception as e:
            logger.error(f"Error deleting product {pk}: {str(e)}", exc_info=True)
            return e

    def toggle_product_status(
        self, pk: int, data: dto.ToggleProductStatusDTO
    ) -> Tuple[Product, Optional[Exception]]:
        """
        Toggle product active status efficiently.

        Args:
            pk: Product ID to update
            data: Status toggle data transfer object

        Returns:
            Tuple containing the updated product and any error that occurred
        """
        try:
            return self._toggle_product_status_with_logging(pk, data)
        except Product.DoesNotExist:
            return self._handle_product_not_found_by_id(pk)
        except Exception as e:
            logger.error(f"Error toggling product {pk} status: {str(e)}", exc_info=True)
            return Product(), e

    def update_product_image(
        self, pk: int, data: dto.UpdateProductImageDTO
    ) -> Tuple[Product, Optional[Exception]]:
        """
        Update product main image with automatic cleanup.

        Args:
            pk: Product ID to update
            data: Image update data transfer object

        Returns:
            Tuple containing the updated product and any error that occurred
        """
        try:
            return self._update_product_image_with_cleanup(pk, data)
        except Product.DoesNotExist:
            return self._handle_product_not_found_by_id(pk)
        except Exception as e:
            logger.error(f"Error updating product {pk} image: {str(e)}", exc_info=True)
            return Product(), e

    def update_product_gallery(
        self, pk: int, data: dto.UpdateProductGalleryDTO
    ) -> Tuple[Product, Optional[Exception]]:
        """
        Update product gallery images with automatic cleanup.

        Args:
            pk: Product ID to update
            data: Gallery update data transfer object

        Returns:
            Tuple containing the updated product and any error that occurred
        """
        try:
            return self._update_product_gallery_with_cleanup(pk, data)
        except Product.DoesNotExist:
            return self._handle_product_not_found_by_id(pk)
        except Exception as e:
            logger.error(
                f"Error updating product {pk} gallery: {str(e)}", exc_info=True
            )
            return Product(), e

    def delete_product_gallery_image(
        self, pk: int, index: int
    ) -> Tuple[Product, Optional[Exception]]:
        """
        Delete a specific image from product gallery by index.

        Args:
            pk: Product ID
            index: Index of the gallery image to delete

        Returns:
            Tuple containing the updated product and any error that occurred
        """
        try:
            return self._delete_gallery_image_by_index(pk, index)
        except Product.DoesNotExist:
            return self._handle_product_not_found_by_id(pk)
        except Exception as e:
            logger.error(
                f"Error deleting gallery image from product {pk}: {str(e)}",
                exc_info=True,
            )
            return Product(), e

    # Helper Methods for Internal Operations

    def _process_gallery_images(
        self, gallery_images: Sequence[InMemoryUploadedFile | str], slug: str
    ) -> List[str]:
        """
        Process gallery images and return list of saved paths.

        Args:
            gallery_images: List of image files or existing paths
            slug: Product slug for filename generation

        Returns:
            List of saved gallery image paths
        """
        gallery_paths = []
        for i, gallery_image in enumerate(gallery_images):
            if isinstance(gallery_image, InMemoryUploadedFile):
                gallery_path = self._save_product_gallery_image(gallery_image, slug, i)
                gallery_paths.append(gallery_path)
            elif isinstance(gallery_image, str):
                gallery_paths.append(gallery_image)
        return gallery_paths

    def _get_brochure_by_id(self, brochure_id: int) -> Optional[Brochure]:
        """
        Retrieve brochure by ID with error handling.

        Args:
            brochure_id: Brochure ID to retrieve

        Returns:
            Brochure instance or None if not found
        """
        try:
            return Brochure.objects.get(id=brochure_id)
        except Brochure.DoesNotExist:
            logger.warning(f"Brochure with id {brochure_id} not found")
            return None

    def _update_product_fields(self, product: Product, update_data: dict) -> None:
        """
        Update product fields with provided data.

        Args:
            product: Product instance to update
            update_data: Dictionary of fields to update
        """
        for key, value in update_data.items():
            if value is not None:
                setattr(product, key, value)

    def _cleanup_old_gallery_images(self, gallery_paths: List[str]) -> None:
        """
        Clean up old gallery image files from storage.

        Args:
            gallery_paths: List of gallery image paths to delete
        """
        if gallery_paths:
            for image_path in gallery_paths:
                self._delete_product_file(image_path)

    def _save_product_gallery_image(
        self, image: InMemoryUploadedFile, slug: str, index: int
    ) -> str:
        """
        Save product gallery image to storage with proper naming.

        Args:
            image: Uploaded image file
            slug: Product slug for filename generation
            index: Gallery image index for uniqueness

        Returns:
            Path to saved image file

        Raises:
            Exception: If image saving fails
        """
        try:
            file_extension = os.path.splitext(image.name)[1]
            filename = f"{slug}_gallery_{index}{file_extension}"
            file_path = (
                f"{settings.FILE_UPLOAD_BASE_DIR}uploads/products/gallery/{filename}"
            )

            saved_path = default_storage.save(file_path, image)
            logger.info(f"Product gallery image saved to {saved_path}")
            return saved_path

        except Exception as e:
            logger.error(f"Error saving product gallery image: {str(e)}", exc_info=True)
            raise ValidationError(f"Failed to save gallery image: {str(e)}") from e

    def _delete_product_file(self, file_path: str) -> None:
        """
        Delete product file from storage with error handling.

        Args:
            file_path: Path to file to delete
        """
        try:
            if file_path and default_storage.exists(file_path):
                default_storage.delete(file_path)
                logger.info(f"Product file {file_path} deleted successfully")
        except Exception as e:
            logger.warning(f"Error deleting product file {file_path}: {str(e)}")

    def _handle_product_not_found_by_id(self, pk: int) -> Tuple[Product, Exception]:
        """
        Handle Product.DoesNotExist exception for ID-based lookups.

        Args:
            pk: Product ID that was not found

        Returns:
            Tuple containing empty Product and exception
        """
        return self._create_product_not_found_error("Product with id '", pk)

    def _handle_product_not_found_by_slug(self, slug: str) -> Tuple[Product, Exception]:
        """
        Handle Product.DoesNotExist exception for slug-based lookups.

        Args:
            slug: Product slug that was not found

        Returns:
            Tuple containing empty Product and exception
        """
        return self._create_product_not_found_error("Product with slug '", slug)

    def _save_and_log_success(
        self, product: Product, field_name: str, pk: int, success_message: str
    ) -> Tuple[Product, None]:
        """
        Save product with specific field update and log success message.

        Args:
            product: Product instance to save
            field_name: Field name to include in update_fields
            pk: Product ID for logging
            success_message: Success message to log

        Returns:
            Tuple containing saved product and None
        """
        product.save(update_fields=[field_name, "updated_at"])
        logger.info(f"Product {pk} {success_message}")
        return product, None

    def _delete_product_with_cleanup(self, pk: int) -> None:
        """
        Delete product and clean up associated files.

        Args:
            pk: Product ID to delete

        Returns:
            None if successful
        """
        product = Product.objects.get(id=pk)

        # Clean up associated files
        if product.image:
            product.image.delete(save=False)
        if product.gallery:
            self._cleanup_old_gallery_images(product.gallery)

        product.delete()
        logger.info(f"Product {pk} deleted successfully")
        return None

    def _update_product_with_data_handling(
        self, pk: int, data: dto.UpdateProductDTO
    ) -> Tuple[Product, None]:
        """
        Update product with comprehensive data handling including images and relationships.

        Args:
            pk: Product ID to update
            data: Product update data transfer object

        Returns:
            Tuple containing the updated product and None
        """
        product = Product.objects.get(id=pk)

        # Validate slug uniqueness if slug is being updated
        if data.slug and not self.validate_slug_uniqueness(data.slug, exclude_id=pk):
            raise ValidationError("Product with this slug already exists.")

        # Validate brochure exists if provided
        if data.brochure_id and not self.validate_brochure_exists(data.brochure_id):
            raise ValidationError(
                f"Brochure with id {data.brochure_id} does not exist."
            )

        update_data = data.to_dict()

        # Handle main image update
        if isinstance(data.image, InMemoryUploadedFile):
            if product.image:
                product.image.delete(save=False)
            update_data["image"] = data.image

        # Handle gallery update
        if data.gallery:
            self._cleanup_old_gallery_images(product.gallery)
            update_data["gallery"] = self._process_gallery_images(
                data.gallery, data.slug or product.slug
            )

        # Handle brochure relationship update
        if data.brochure_id:
            update_data["brochure"] = self._get_brochure_by_id(data.brochure_id)

        update_data.pop("brochure_id", None)

        # Apply updates to product
        self._update_product_fields(product, update_data)
        product.save()

        logger.info(f"Product {pk} updated successfully")
        return product, None

    def _toggle_product_status_with_logging(
        self, pk: int, data: dto.ToggleProductStatusDTO
    ) -> Tuple[Product, None]:
        """
        Toggle product status and log the action.

        Args:
            pk: Product ID to update
            data: Status toggle data transfer object

        Returns:
            Tuple containing the updated product and None
        """
        product = Product.objects.get(id=pk)
        product.is_active = data.is_active
        product.save(update_fields=["is_active", "updated_at"])

        status_text = "activated" if data.is_active else "deactivated"
        logger.info(f"Product {pk} {status_text} successfully")
        return product, None

    def _update_product_image_with_cleanup(
        self, pk: int, data: dto.UpdateProductImageDTO
    ) -> Tuple[Product, None]:
        """
        Update product image with cleanup of old image.

        Args:
            pk: Product ID to update
            data: Image update data transfer object

        Returns:
            Tuple containing the updated product and None
        """
        product = Product.objects.get(id=pk)

        # Clean up old image
        if product.image:
            product.image.delete(save=False)

        # Save new image
        product.image.save(data.image.name, data.image, save=False)
        return self._save_and_log_success(
            product, "image", pk, "main image updated successfully"
        )

    def _update_product_gallery_with_cleanup(
        self, pk: int, data: dto.UpdateProductGalleryDTO
    ) -> Tuple[Product, None]:
        """
        Update product gallery with cleanup of old images.

        Args:
            pk: Product ID to update
            data: Gallery update data transfer object

        Returns:
            Tuple containing the updated product and None
        """
        product = Product.objects.get(id=pk)

        # Clean up old gallery images
        if product.gallery:
            self._cleanup_old_gallery_images(product.gallery)

        # Save new gallery images
        product.gallery = self._process_gallery_images(data.gallery, product.slug)
        return self._save_and_log_success(
            product, "gallery", pk, "gallery updated successfully"
        )

    def _delete_gallery_image_by_index(
        self, pk: int, index: int
    ) -> Tuple[Product, None]:
        """
        Delete a specific gallery image by index with validation.

        Args:
            pk: Product ID
            index: Index of the gallery image to delete

        Returns:
            Tuple containing the updated product and None

        Raises:
            Exception: If gallery image at index does not exist
        """
        product = Product.objects.get(id=pk)

        if not product.gallery or index >= len(product.gallery) or index < 0:
            error_msg = (
                f"Gallery image at index {index} does not exist for product {pk}."
            )
            logger.warning(error_msg)
            raise ValidationError(error_msg)

        # Delete the specific image file
        self._delete_product_file(product.gallery[index])

        # Remove from gallery list
        product.gallery = [img for i, img in enumerate(product.gallery) if i != index]
        product.save(update_fields=["gallery", "updated_at"])

        logger.info(f"Gallery image at index {index} deleted from product {pk}")
        return product, None

    def _create_product_not_found_error(
        self, prefix: str, identifier: int | str
    ) -> Tuple[Product, Exception]:
        """
        Create a standardized product not found error with logging.

        Args:
            prefix: Error message prefix (e.g., "Product with id '", "Product with slug '")
            identifier: Product identifier (ID or slug)

        Returns:
            Tuple containing empty Product and exception
        """
        error_msg = f"{prefix}{identifier}' does not exist."
        logger.warning(error_msg)
        return Product(), ValidationError(error_msg)
