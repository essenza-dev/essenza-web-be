"""
Product Variant Service Module
Handles all business logic for product variant management operations.
"""

import copy
import logging
from typing import Optional, Tuple

from django.db.models import QuerySet
from django.db import transaction
from django.core.exceptions import ValidationError

from core.enums import ActionType
from core.service import BaseService, required_context
from core.models import ProductVariant, Product, ProductSpecification, Specification

from . import dto

logger = logging.getLogger(__name__)


class ProductVariantService(BaseService):
    """Service class for managing product variant operations with comprehensive functionality."""

    def validate_sku_uniqueness(
        self, sku: str, exclude_id: Optional[int] = None
    ) -> bool:
        """
        Validate if SKU is unique.

        Args:
            sku: The SKU to validate
            exclude_id: Variant ID to exclude from validation (for updates)

        Returns:
            True if SKU is unique, False otherwise
        """
        if not sku:
            return True
        queryset = ProductVariant.objects.filter(sku=sku)
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return not queryset.exists()

    def validate_product_exists(self, product_id: int) -> bool:
        """
        Validate if product exists.

        Args:
            product_id: The product ID to validate

        Returns:
            True if product exists, False otherwise
        """
        return Product.objects.filter(id=product_id).exists()

    def validate_product_exists_by_slug(self, product_slug: str) -> bool:
        """
        Validate if product exists by slug.

        Args:
            product_slug: The product slug to validate

        Returns:
            True if product exists, False otherwise
        """
        return Product.objects.filter(slug=product_slug).exists()

    def _get_active_specification(
        self, spec_slug: str
    ) -> Tuple[Optional[Specification], Optional[str]]:
        """
        Get active specification by slug with detailed error message.

        Args:
            spec_slug: The specification slug to retrieve

        Returns:
            Tuple containing the specification (or None) and error message (or None)
        """
        try:
            specification = Specification.objects.get(slug=spec_slug, is_active=True)
            logger.info(
                f"Found specification: {specification.label} (ID: {specification.id})"
            )
            return specification, None
        except Specification.DoesNotExist:
            if Specification.objects.filter(slug=spec_slug, is_active=False).exists():
                error_msg = f"Specification with slug '{spec_slug}' is not active."
            elif Specification.objects.filter(slug=spec_slug).exists():
                error_msg = f"Specification with slug '{spec_slug}' exists but has invalid status."
            else:
                error_msg = f"Specification with slug '{spec_slug}' does not exist."
            logger.error(error_msg)
            return None, error_msg

    def _create_product_specifications(
        self, variant: ProductVariant, specifications_data: list
    ) -> Optional[str]:
        """
        Create product specifications for a variant.

        Args:
            variant: The product variant to add specifications to
            specifications_data: List of specification data dictionaries

        Returns:
            Error message if error occurs, None if successful
        """
        logger.info(f"Processing {len(specifications_data)} specifications for variant")

        for spec_data in specifications_data:
            spec_slug = spec_data.get("specification_slug")
            spec_value = spec_data.get("value")
            logger.info(f"Looking for specification with slug: {spec_slug}")

            specification, error_msg = self._get_active_specification(spec_slug)
            if error_msg:
                return error_msg

            product_spec = ProductSpecification.objects.create(
                product_variant=variant,
                specification=specification,
                value=spec_value,
            )
            logger.info(
                f"Created ProductSpecification (ID: {product_spec.id}) with value: {spec_value}"
            )

        return None

    @required_context
    def create_variant(
        self, product_slug: str, data: dto.CreateProductVariantDTO
    ) -> Tuple[ProductVariant, Optional[Exception]]:
        """
        Create a new product variant with validation.

        Args:
            product_slug: Product slug to create variant for
            data: Variant creation data transfer object

        Returns:
            Tuple containing the created variant and any error that occurred
        """
        try:
            with transaction.atomic():
                # Validate product exists
                if not self.validate_product_exists_by_slug(product_slug):
                    return ProductVariant(), ValidationError(
                        f"Product with slug '{product_slug}' does not exist."
                    )

                # Validate SKU uniqueness if provided
                if data.sku and not self.validate_sku_uniqueness(data.sku):
                    return ProductVariant(), ValidationError(
                        f"Product variant with SKU '{data.sku}' already exists."
                    )

                # Get product instance
                product = Product.objects.get(slug=product_slug)

                # Extract specifications before creating variant
                specifications_data = data.specifications

                # Create variant (exclude specifications from dict)
                variant_data = data.to_dict()
                variant_data.pop("specifications", None)
                variant_data["product"] = product
                variant = ProductVariant.objects.create(**variant_data)

                # Add specifications if provided
                if specifications_data:
                    if error_msg := self._create_product_specifications(
                        variant, specifications_data
                    ):
                        variant.delete()  # Rollback: delete created variant
                        return ProductVariant(), ValidationError(error_msg)

                # Log activity
                self.log_entity_change(
                    self.ctx,
                    instance=variant,
                    action=ActionType.CREATE,
                    description=(
                        "Product variant created with specifications"
                        if specifications_data
                        else "Product variant created"
                    ),
                )

                logger.info(
                    f"Product variant created successfully with id {variant.id}"
                )
                return variant, None

        except Exception as e:
            logger.error(f"Error creating product variant: {str(e)}", exc_info=True)
            return ProductVariant(), e

    def get_variants_by_product(self, product_id: int) -> QuerySet[ProductVariant]:
        """
        Retrieve all variants for a specific product with optimized queries.

        Args:
            product_id: Product ID to get variants for

        Returns:
            QuerySet of variants for the product
        """
        return (
            ProductVariant.objects.filter(product_id=product_id)
            .select_related("product")
            .prefetch_related("product_specifications__specification")
            .order_by("-created_at")
        )

    def get_variants_by_product_slug(
        self, product_slug: str
    ) -> QuerySet[ProductVariant]:
        """
        Retrieve all variants for a specific product by slug with optimized queries.

        Args:
            product_slug: Product slug to get variants for

        Returns:
            QuerySet of variants for the product
        """
        return (
            ProductVariant.objects.filter(product__slug=product_slug)
            .select_related("product")
            .prefetch_related("product_specifications__specification")
            .order_by("-created_at")
        )

    def get_specific_variant(
        self, pk: int
    ) -> Tuple[ProductVariant, Optional[Exception]]:
        """
        Retrieve a specific product variant by ID with optimized query.

        Args:
            pk: Variant ID to retrieve

        Returns:
            Tuple containing the variant and any error that occurred
        """
        try:
            variant = (
                ProductVariant.objects.select_related("product")
                .prefetch_related("product_specifications__specification")
                .get(id=pk)
            )
            return variant, None
        except ProductVariant.DoesNotExist:
            return self._handle_variant_not_found_by_id(pk)
        except Exception as e:
            logger.error(f"Error retrieving variant {pk}: {str(e)}", exc_info=True)
            return ProductVariant(), e

    @required_context
    def update_specific_variant(
        self, pk: int, data: dto.UpdateProductVariantDTO
    ) -> Tuple[ProductVariant, Optional[Exception]]:
        """
        Update a specific product variant with comprehensive validation.

        Args:
            pk: Variant ID to update
            data: Variant update data transfer object

        Returns:
            Tuple containing the updated variant and any error that occurred
        """
        try:
            with transaction.atomic():
                variant = ProductVariant.objects.get(id=pk)
                old_instance = copy.deepcopy(variant)

                # Validate SKU uniqueness if being updated
                if data.sku and not self.validate_sku_uniqueness(
                    data.sku, exclude_id=pk
                ):
                    return ProductVariant(), ValidationError(
                        f"Product variant with SKU '{data.sku}' already exists."
                    )

                # Handle image update - cleanup old image if new one provided
                if data.image is not None and variant.image:
                    variant.image.delete(save=False)

                # Apply updates
                for key, value in data.to_dict().items():
                    if value is not None:
                        setattr(variant, key, value)

                variant.save()

                # Log activity
                self.log_entity_change(
                    self.ctx,
                    instance=variant,
                    old_instance=old_instance,
                    action=ActionType.UPDATE,
                    description="Product variant updated",
                )

                logger.info(f"Product variant {pk} updated successfully")
                return variant, None

        except ProductVariant.DoesNotExist:
            return self._handle_variant_not_found_by_id(pk)
        except Exception as e:
            logger.error(f"Error updating variant {pk}: {str(e)}", exc_info=True)
            return ProductVariant(), e

    @required_context
    def delete_specific_variant(self, pk: int) -> Optional[Exception]:
        """
        Delete a specific product variant and its associated files and specifications.

        Args:
            pk: Variant ID to delete

        Returns:
            Exception if error occurs, None if successful
        """
        try:
            with transaction.atomic():
                variant = ProductVariant.objects.get(id=pk)
                old_instance = copy.deepcopy(variant)

                # Clean up associated image
                if variant.image:
                    variant.image.delete(save=False)

                # Delete variant (specifications will be deleted via CASCADE)
                variant.delete()

                # Log activity
                self.log_entity_change(
                    self.ctx,
                    instance=old_instance,
                    action=ActionType.DELETE,
                    description="Product variant deleted",
                )

                logger.info(f"Product variant {pk} deleted successfully")
                return None

        except ProductVariant.DoesNotExist:
            error_msg = f"Product variant with id '{pk}' does not exist."
            logger.warning(error_msg)
            return ValidationError(error_msg)
        except Exception as e:
            logger.error(f"Error deleting variant {pk}: {str(e)}", exc_info=True)
            return e

    @required_context
    def toggle_variant_status(
        self, pk: int, data: dto.ToggleProductVariantStatusDTO
    ) -> Tuple[ProductVariant, Optional[Exception]]:
        """
        Toggle product variant active status.

        Args:
            pk: Variant ID to update
            data: Status toggle data transfer object

        Returns:
            Tuple containing the updated variant and any error that occurred
        """
        try:
            with transaction.atomic():
                variant = ProductVariant.objects.get(id=pk)
                old_instance = copy.deepcopy(variant)

                variant.is_active = data.is_active
                variant.save(update_fields=["is_active"])

                # Log activity
                self.log_entity_change(
                    self.ctx,
                    instance=variant,
                    old_instance=old_instance,
                    action=ActionType.UPDATE,
                    description="Product variant status updated",
                )

                status_text = "activated" if data.is_active else "deactivated"
                logger.info(f"Product variant {pk} {status_text} successfully")
                return variant, None

        except ProductVariant.DoesNotExist:
            return self._handle_variant_not_found_by_id(pk)
        except Exception as e:
            logger.error(f"Error toggling variant {pk} status: {str(e)}", exc_info=True)
            return ProductVariant(), e

    @required_context
    def update_variant_specifications(
        self, pk: int, data: dto.UpdateProductVariantSpecificationsDTO
    ) -> Tuple[ProductVariant, Optional[Exception]]:
        """
        Add or update product variant specifications.

        Args:
            pk: Variant ID to update
            data: Specifications update data transfer object

        Returns:
            Tuple containing the updated variant and any error that occurred
        """
        try:
            with transaction.atomic():
                variant = ProductVariant.objects.get(id=pk)

                # Process each specification
                for spec_data in data.specifications:
                    spec_slug = spec_data.get("specification_slug")
                    spec_value = spec_data.get("value")

                    # Get specification by slug
                    try:
                        specification = Specification.objects.get(
                            slug=spec_slug, is_active=True
                        )
                    except Specification.DoesNotExist:
                        return ProductVariant(), ValidationError(
                            f"Specification with slug '{spec_slug}' does not exist or is inactive."
                        )

                    # Update or create product specification
                    ProductSpecification.objects.update_or_create(
                        product_variant=variant,
                        specification=specification,
                        defaults={"value": spec_value, "is_active": True},
                    )

                # Log activity
                self.log_entity_change(
                    self.ctx,
                    instance=variant,
                    action=ActionType.UPDATE,
                    description="Product variant specifications updated",
                )

                logger.info(f"Product variant {pk} specifications updated successfully")

                # Reload variant with specifications
                variant = (
                    ProductVariant.objects.select_related("product")
                    .prefetch_related("product_specifications__specification")
                    .get(id=pk)
                )

                return variant, None

        except ProductVariant.DoesNotExist:
            return self._handle_variant_not_found_by_id(pk)
        except Exception as e:
            logger.error(
                f"Error updating variant {pk} specifications: {str(e)}", exc_info=True
            )
            return ProductVariant(), e

    @required_context
    def delete_variant_specification(
        self, variant_id: int, spec_slug: str
    ) -> Optional[Exception]:
        """
        Delete a specific product variant specification.

        Args:
            variant_id: Variant ID
            spec_slug: Specification slug to delete

        Returns:
            Exception if error occurs, None if successful
        """
        try:
            with transaction.atomic():
                # Verify variant exists
                variant = ProductVariant.objects.get(id=variant_id)

                # Get and delete the specification
                try:
                    product_spec = ProductSpecification.objects.get(
                        specification__slug=spec_slug, product_variant=variant
                    )
                    product_spec.delete()

                    # Log activity
                    self.log_entity_change(
                        self.ctx,
                        instance=variant,
                        action=ActionType.UPDATE,
                        description=f"Product variant specification '{product_spec.specification.label}' deleted",
                    )

                    logger.info(
                        f"Product specification with slug '{spec_slug}' deleted from variant {variant_id}"
                    )
                    return None

                except ProductSpecification.DoesNotExist:
                    error_msg = f"Product specification with slug '{spec_slug}' does not exist for variant '{variant_id}'."
                    logger.warning(error_msg)
                    return ValidationError(error_msg)

        except ProductVariant.DoesNotExist:
            error_msg = f"Product variant with id '{variant_id}' does not exist."
            logger.warning(error_msg)
            return ValidationError(error_msg)
        except Exception as e:
            logger.error(
                f"Error deleting specification with slug '{spec_slug}' from variant {variant_id}: {str(e)}",
                exc_info=True,
            )
            return e

    def _handle_variant_not_found_by_id(
        self, pk: int
    ) -> Tuple[ProductVariant, Exception]:
        """
        Handle ProductVariant.DoesNotExist exception.

        Args:
            pk: Variant ID that was not found

        Returns:
            Tuple containing empty ProductVariant and exception
        """
        error_msg = f"Product variant with id '{pk}' does not exist."
        logger.warning(error_msg)
        return ProductVariant(), ValidationError(error_msg)
