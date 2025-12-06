"""
Specification Service Module
Handles all business logic for specification management operations.
"""

import copy
import logging
from typing import Optional, Tuple

from django.db.models import QuerySet
from django.db import transaction
from django.core.exceptions import ValidationError

from core.enums import ActionType
from core.service import BaseService, required_context
from core.models import Specification

from . import dto

logger = logging.getLogger(__name__)


class SpecificationService(BaseService):
    """Service class for managing specification operations with comprehensive functionality."""

    def get_specifications(self) -> QuerySet[Specification]:
        """Retrieve all specifications with optimized queryset."""
        return Specification.objects.select_related().all()

    def get_specification_by_slug(
        self, slug: str
    ) -> Tuple[Specification, Optional[Exception]]:
        """Retrieve a specific specification by slug with error handling."""
        try:
            specification = self._get_specification_by_slug(slug)
            return specification, None
        except Specification.DoesNotExist:
            return self._handle_specification_not_found_error(slug)
        except Exception as e:
            logger.error(f"Error retrieving specification with slug '{slug}': {e}")
            return Specification(), e

    @required_context
    def update_specification_by_slug(
        self, slug: str, data: dto.UpdateSpecificationDTO
    ) -> Tuple[Specification, Optional[Exception]]:
        """Update a specific specification by slug with comprehensive validation and activity logging."""
        try:
            with transaction.atomic():
                specification = self._prepare_specification_for_update(slug, data)
                old_instance = copy.deepcopy(specification)

                self._apply_updates(specification, data)
                specification.save()

                # Log activity
                self.log_entity_change(
                    self.ctx,
                    instance=specification,
                    old_instance=old_instance,
                    action=ActionType.UPDATE,
                    description="Specification updated",
                )

                logger.info(f"Specification with slug '{slug}' updated successfully")
                return specification, None

        except Specification.DoesNotExist:
            return self._handle_specification_not_found_error(slug)
        except (ValueError, ValidationError) as e:
            logger.warning(f"Validation error updating specification: {e}")
            return Specification(), e
        except Exception as e:
            logger.error(f"Error updating specification with slug '{slug}': {e}")
            return Specification(), e

    def validate_slug_uniqueness(
        self, slug: str, exclude_slug: Optional[str] = None
    ) -> bool:
        """
        Validate that a slug is unique, optionally excluding a specific slug.

        Args:
            slug: The slug to validate
            exclude_slug: Optional slug to exclude from uniqueness check (for updates)

        Returns:
            True if slug is unique, False otherwise
        """
        queryset = Specification.objects.filter(slug=slug)
        if exclude_slug:
            queryset = queryset.exclude(slug=exclude_slug)
        return not queryset.exists()

    def _get_specification_by_slug(self, slug: str) -> Specification:
        """Retrieve specification by slug, raises DoesNotExist if not found."""
        return Specification.objects.get(slug=slug)

    def _handle_specification_not_found_error(
        self, slug: str
    ) -> Tuple[Specification, Exception]:
        """Handle specification not found error with consistent messaging."""
        error_msg = f"Specification with slug '{slug}' does not exist."
        logger.warning(error_msg)
        return Specification(), Exception(error_msg)

    def _prepare_specification_for_update(
        self, slug: str, data: dto.UpdateSpecificationDTO
    ) -> Specification:
        """Prepare specification for update with validation."""
        specification = self._get_specification_by_slug(slug)
        self._validate_update_data(data, specification.slug)
        return specification

    def _validate_update_data(
        self, data: dto.UpdateSpecificationDTO, current_slug: str
    ) -> None:
        """Validate update data with database checks."""
        # Since we're updating by slug and slug is not updateable in this API,
        # we don't need to validate slug uniqueness here
        pass

    def _apply_updates(
        self, specification: Specification, data: dto.UpdateSpecificationDTO
    ) -> None:
        """Apply validated updates to specification instance."""
        for key, value in data.to_dict().items():
            if value is not None:
                setattr(specification, key, value)
