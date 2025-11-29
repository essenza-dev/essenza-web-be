from copy import deepcopy
from typing import Optional, Tuple
import logging

from django.db.models import QuerySet
from django.core.paginator import Page
from django.db import transaction
from django.core.exceptions import ValidationError

from core.enums import ActionType
from core.service import BaseService, required_context
from core.models import Distributor

from . import dto


logger = logging.getLogger(__name__)


class DistributorService(BaseService):
    """Service class for managing distributors."""

    @required_context
    def create_distributor(
        self, data: dto.CreateDistributorDTO
    ) -> Tuple[Distributor, Optional[Exception]]:
        """Create a new distributor with validation."""
        try:
            with transaction.atomic():
                self._validate_email_uniqueness(data.email)
                distributor = Distributor.objects.create(**data.to_dict())
                self.log_entity_change(
                    self.ctx,
                    instance=distributor,
                    action=ActionType.CREATE,
                )
                logger.info(
                    f"Distributor created successfully with ID: {distributor.id}"
                )
                return distributor, None
        except (ValueError, ValidationError) as e:
            logger.warning(f"Validation error creating distributor: {e}")
            return Distributor(), e
        except Exception as e:
            logger.error(f"Error creating distributor: {e}")
            return Distributor(), e

    def get_distributors(self) -> QuerySet[Distributor]:
        """Retrieve all distributors ordered by creation date."""
        return Distributor.objects.order_by("-created_at")

    def get_paginated_distributors(
        self, str_page_number: str, str_page_size: str
    ) -> Page:
        """Retrieve paginated distributors with efficient ordering."""
        return self.get_paginated_data(
            self.get_distributors(), str_page_number, str_page_size
        )

    def get_specific_distributor(
        self, pk: int
    ) -> Tuple[Distributor, Optional[Exception]]:
        """Retrieve a specific distributor by ID with error handling."""
        try:
            distributor = self._get_distributor_by_id(pk)
            return distributor, None
        except Distributor.DoesNotExist:
            return self._handle_distributor_not_found_error(pk)
        except Exception as e:
            logger.error(f"Error retrieving distributor with id '{pk}': {e}")
            return Distributor(), e

    @required_context
    def update_specific_distributor(
        self, pk: int, data: dto.UpdateDistributorDTO
    ) -> Tuple[Distributor, Optional[Exception]]:
        """Update a specific distributor by ID with atomic transaction."""
        try:
            with transaction.atomic():
                distributor = self._prepare_distributor_for_update(pk, data)
                old_instance = deepcopy(distributor)
                self._apply_updates(distributor, data)
                distributor.save()
                self.log_entity_change(
                    self.ctx,
                    instance=distributor,
                    old_instance=old_instance,
                    action=ActionType.UPDATE,
                )
                logger.info(
                    f"Distributor with ID: {distributor.id} updated successfully"
                )
                return distributor, None
        except Distributor.DoesNotExist:
            return self._handle_distributor_not_found_error(pk)
        except (ValueError, ValidationError) as e:
            logger.warning(f"Validation error updating distributor: {e}")
            return Distributor(), e
        except Exception as e:
            logger.error(f"Error updating distributor with id '{pk}': {e}")
            return Distributor(), e

    @required_context
    def delete_specific_distributor(self, pk: int) -> Optional[Exception]:
        """Delete a specific distributor by ID with atomic transaction."""
        try:
            with transaction.atomic():
                distributor = self._get_distributor_by_id(pk)
                distributor.delete()
                self.log_entity_change(
                    self.ctx,
                    instance=distributor,
                    action=ActionType.DELETE,
                )
                logger.info(f"Distributor with ID: {pk} deleted successfully")
                return None
        except Distributor.DoesNotExist:
            return self._handle_distributor_not_found_error(pk)[1]
        except Exception as e:
            logger.error(f"Error deleting distributor with id '{pk}': {e}")
            return e

    def _get_distributor_by_id(self, pk: int) -> Distributor:
        """Retrieve distributor by ID, raises DoesNotExist if not found."""
        return Distributor.objects.get(id=pk)

    def _handle_distributor_not_found_error(
        self, pk: int
    ) -> Tuple[Distributor, Exception]:
        """Handle distributor not found error with consistent messaging."""
        error_msg = f"Distributor with id '{pk}' does not exist."
        logger.warning(error_msg)
        return Distributor(), Exception(error_msg)

    def _prepare_distributor_for_update(
        self, pk: int, data: dto.UpdateDistributorDTO
    ) -> Distributor:
        """Prepare distributor instance for update with validation."""
        distributor = self._get_distributor_by_id(pk)
        self._validate_email_for_update(data.email, distributor.email, pk)
        return distributor

    def _validate_email_uniqueness(self, email: Optional[str]) -> None:
        """Validate email uniqueness for creation operation."""
        if email and self._email_exists(email):
            raise ValueError(
                f"Email '{email}' is already in use by another distributor."
            )

    def _validate_email_for_update(
        self, new_email: Optional[str], current_email: Optional[str], pk: int
    ) -> None:
        """Validate email uniqueness for update operation."""
        if (
            new_email
            and new_email != current_email
            and self._email_exists(new_email, exclude_id=pk)
        ):
            raise ValueError(
                f"Email '{new_email}' is already in use by another distributor."
            )

    def _apply_updates(
        self, distributor: Distributor, data: dto.UpdateDistributorDTO
    ) -> None:
        """Apply non-null updates to distributor instance efficiently."""
        update_data = {k: v for k, v in data.to_dict().items() if v is not None}
        for key, value in update_data.items():
            setattr(distributor, key, value)

    def _email_exists(self, email: str, exclude_id: Optional[int] = None) -> bool:
        """Check if email exists in database with optional exclusion by ID."""
        queryset = Distributor.objects.filter(email__iexact=email)
        if exclude_id is not None:
            queryset = queryset.exclude(id=exclude_id)
        return queryset.exists()
