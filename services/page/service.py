import logging
from typing import Tuple, Optional

from django.core.paginator import Page
from django.db.models import QuerySet
from django.utils.text import slugify
from django.db import IntegrityError, transaction

from core.service import BaseService
from core.models import Page as PageModel

from . import dto

logger = logging.getLogger(__name__)


class PageService(BaseService):
    """Service class for managing pages."""

    def create_page(
        self, data: dto.CreatePageDTO
    ) -> Tuple[PageModel, Optional[Exception]]:
        """Create a new page with optimized slug generation and transaction safety."""
        try:
            with transaction.atomic():
                # Optimize slug generation - only slugify if needed
                data.slug = self._generate_slug(data.slug, data.title)

                page = PageModel.objects.create(**data.to_dict())
                logger.info(f"Page created successfully with ID: {page.id}")
                return page, None
        except IntegrityError as e:
            return self._handle_integrity_error(e, data.slug, PageModel())
        except Exception as e:
            logger.error(f"Error creating page: {e}")
            return PageModel(), e

    def get_pages(self) -> QuerySet[PageModel]:
        """Retrieve all pages with optimized queryset."""
        return PageModel.objects.select_related().all()

    def get_paginated_pages(self, str_page_number: str, str_page_size: str) -> Page:
        """Retrieve paginated pages with optimized ordering and select_related."""
        queryset = PageModel.objects.select_related().order_by("-created_at")
        return self.get_paginated_data(queryset, str_page_number, str_page_size)

    def get_specific_page(self, pk: int) -> Tuple[PageModel, Optional[Exception]]:
        """Retrieve a specific page by its ID with optimized query."""
        try:
            page = PageModel.objects.select_related().get(id=pk)
            logger.info(f"Page retrieved successfully: {page.id}")
            return page, None
        except PageModel.DoesNotExist:
            return self._handle_not_found_error(f"Page with id '{pk}' does not exist.")
        except Exception as e:
            logger.error(f"Error retrieving page {pk}: {e}")
            return PageModel(), e

    def get_page_by_slug(self, slug: str) -> Tuple[PageModel, Optional[Exception]]:
        """Retrieve a page by its slug with optimized query."""
        try:
            page = PageModel.objects.select_related().get(slug=slug)
            logger.info(f"Page retrieved successfully by slug: {slug}")
            return page, None
        except PageModel.DoesNotExist:
            return self._handle_not_found_error(
                f"Page with slug '{slug}' does not exist."
            )
        except Exception as e:
            logger.error(f"Error retrieving page by slug {slug}: {e}")
            return PageModel(), e

    def _generate_slug(self, slug: Optional[str], title: str) -> str:
        """Generate optimized slug from input or title."""
        return slugify(title) if not slug or not slug.strip() else slugify(slug)

    def _handle_integrity_error(
        self, error: IntegrityError, slug: Optional[str], empty_model: PageModel
    ) -> Tuple[PageModel, Exception]:
        """Handle database integrity errors with appropriate messaging."""
        if "slug" in str(error):
            error_msg = f"A page with slug '{slug}' already exists."
            logger.warning(error_msg)
            return empty_model, Exception(error_msg)
        logger.error(f"Database integrity error: {error}")
        return empty_model, error

    def _handle_not_found_error(self, message: str) -> Tuple[PageModel, Exception]:
        """Handle not found errors consistently."""
        logger.warning(message)
        return PageModel(), Exception(message)

    def _handle_slug_update(self, data: dto.UpdatePageDTO, page: PageModel) -> None:
        """Handle slug update with optimized auto-generation logic."""
        if data.slug is not None:
            if data.slug.strip() == "":
                # Generate from updated title or existing page title
                source_title = data.title if data.title is not None else page.title
                data.slug = slugify(source_title)
            else:
                data.slug = slugify(data.slug)

    def update_specific_page(
        self, pk: int, data: dto.UpdatePageDTO
    ) -> Tuple[PageModel, Optional[Exception]]:
        """Update a specific page by its ID with optimized transaction handling."""
        try:
            return self._update_page_data(pk, data)
        except PageModel.DoesNotExist:
            return self._handle_not_found_error(f"Page with id '{pk}' does not exist.")
        except IntegrityError as e:
            return self._handle_integrity_error(e, data.slug, PageModel())
        except Exception as e:
            logger.error(f"Error updating page {pk}: {e}")
            return PageModel(), e

    def _update_page_data(
        self, pk: int, data: dto.UpdatePageDTO
    ) -> Tuple[PageModel, None]:
        """Update page data with optimized field updates and transaction safety."""
        with transaction.atomic():
            page = PageModel.objects.select_for_update().get(id=pk)

            # Handle slug update with auto-generation
            self._handle_slug_update(data, page)

            # Optimized field updates - only update non-None values
            update_data = {k: v for k, v in data.to_dict().items() if v is not None}
            if update_data:
                for key, value in update_data.items():
                    setattr(page, key, value)

            page.save(update_fields=list(update_data.keys()) if update_data else None)
            logger.info(f"Page updated successfully: {page.id}")
            return page, None

    def delete_specific_page(self, pk: int) -> Optional[Exception]:
        """Delete a specific page by its ID with transaction safety."""
        try:
            with transaction.atomic():
                page = PageModel.objects.select_for_update().get(id=pk)
                page_id = page.id
                page.delete()
                logger.info(f"Page deleted successfully: {page_id}")
                return None
        except PageModel.DoesNotExist:
            error_msg = f"Page with id '{pk}' does not exist."
            logger.warning(error_msg)
            return Exception(error_msg)
        except Exception as e:
            logger.error(f"Error deleting page {pk}: {e}")
            return e

    def toggle_page_status(
        self, pk: int, data: dto.TogglePageStatusDTO
    ) -> Tuple[PageModel, Optional[Exception]]:
        """Toggle page active status with optimized update."""
        try:
            with transaction.atomic():
                page = PageModel.objects.select_for_update().get(id=pk)
                page.is_active = data.is_active
                page.save(update_fields=["is_active"])
                logger.info(
                    f"Page status toggled successfully: {page.id} -> {data.is_active}"
                )
                return page, None
        except PageModel.DoesNotExist:
            return self._handle_not_found_error(f"Page with id '{pk}' does not exist.")
        except Exception as e:
            logger.error(f"Error toggling page status {pk}: {e}")
            return PageModel(), e
