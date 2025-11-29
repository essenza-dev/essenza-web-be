from typing import Optional, Tuple
import logging

from django.db.models import QuerySet
from django.core.paginator import Page
from django.db import transaction
from django.core.exceptions import ValidationError

from core.service import BaseService
from core.models import Store

from . import dto


logger = logging.getLogger(__name__)


class StoreService(BaseService):
    """Service class for managing stores."""

    def create_store(
        self, data: dto.CreateStoreDTO
    ) -> Tuple[Store, Optional[Exception]]:
        """Create a new store with validation."""
        try:
            with transaction.atomic():
                self._validate_email_uniqueness(data.email)
                store = Store.objects.create(**data.to_dict())
                logger.info(f"Store created successfully with ID: {store.id}")
                return store, None
        except (ValueError, ValidationError) as e:
            logger.warning(f"Validation error creating store: {e}")
            return Store(), e
        except Exception as e:
            logger.error(f"Error creating store: {e}")
            return Store(), e

    def get_stores(self) -> QuerySet[Store]:
        """Retrieve all stores ordered by creation date."""
        return Store.objects.order_by("-created_at")

    def get_paginated_stores(self, str_page_number: str, str_page_size: str) -> Page:
        """Retrieve paginated stores with efficient ordering."""
        return self.get_paginated_data(
            self.get_stores(), str_page_number, str_page_size
        )

    def get_specific_store(self, pk: int) -> Tuple[Store, Optional[Exception]]:
        """Retrieve a specific store by ID with error handling."""
        try:
            store = self._get_store_by_id(pk)
            return store, None
        except Store.DoesNotExist:
            return self._handle_store_not_found_error(pk)
        except Exception as e:
            logger.error(f"Error retrieving store with id '{pk}': {e}")
            return Store(), e

    def update_specific_store(
        self, pk: int, data: dto.UpdateStoreDTO
    ) -> Tuple[Store, Optional[Exception]]:
        """Update a specific store by ID with atomic transaction."""
        try:
            with transaction.atomic():
                store = self._prepare_store_for_update(pk, data)
                self._apply_updates(store, data)
                store.save()
                logger.info(f"Store with ID: {store.id} updated successfully")
                return store, None
        except Store.DoesNotExist:
            return self._handle_store_not_found_error(pk)
        except (ValueError, ValidationError) as e:
            logger.warning(f"Validation error updating store: {e}")
            return Store(), e
        except Exception as e:
            logger.error(f"Error updating store with id '{pk}': {e}")
            return Store(), e

    def delete_specific_store(self, pk: int) -> Optional[Exception]:
        """Delete a specific store by ID with atomic transaction."""
        try:
            with transaction.atomic():
                store = self._get_store_by_id(pk)
                store.delete()
                logger.info(f"Store with ID: {pk} deleted successfully")
                return None
        except Store.DoesNotExist:
            return self._handle_store_not_found_error(pk)[1]
        except Exception as e:
            logger.error(f"Error deleting store with id '{pk}': {e}")
            return e

    def _get_store_by_id(self, pk: int) -> Store:
        """Retrieve store by ID, raises DoesNotExist if not found."""
        return Store.objects.get(id=pk)

    def _handle_store_not_found_error(self, pk: int) -> Tuple[Store, Exception]:
        """Handle store not found error with consistent messaging."""
        error_msg = f"Store with id '{pk}' does not exist."
        logger.warning(error_msg)
        return Store(), Exception(error_msg)

    def _prepare_store_for_update(self, pk: int, data: dto.UpdateStoreDTO) -> Store:
        """Prepare store instance for update with validation."""
        store = self._get_store_by_id(pk)
        self._validate_email_for_update(data.email, store.email, pk)
        return store

    def _validate_email_uniqueness(self, email: Optional[str]) -> None:
        """Validate email uniqueness for creation operation."""
        if email and self._email_exists(email):
            raise ValueError(f"Email '{email}' is already in use by another store.")

    def _validate_email_for_update(
        self, new_email: Optional[str], current_email: Optional[str], pk: int
    ) -> None:
        """Validate email uniqueness for update operation."""
        if (
            new_email
            and new_email != current_email
            and self._email_exists(new_email, exclude_id=pk)
        ):
            raise ValueError(f"Email '{new_email}' is already in use by another store.")

    def _apply_updates(self, store: Store, data: dto.UpdateStoreDTO) -> None:
        """Apply non-null updates to store instance efficiently."""
        update_data = {k: v for k, v in data.to_dict().items() if v is not None}
        for key, value in update_data.items():
            setattr(store, key, value)

    def _email_exists(self, email: str, exclude_id: Optional[int] = None) -> bool:
        """Check if email exists in database with optional exclusion by ID."""
        queryset = Store.objects.filter(email__iexact=email)
        if exclude_id is not None:
            queryset = queryset.exclude(id=exclude_id)
        return queryset.exists()
