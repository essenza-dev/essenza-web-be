from __future__ import annotations

from abc import ABC
from copy import copy
from functools import wraps
from typing import Any, Callable, TypeVar, Union, cast, Dict, List, Optional

from django.core.paginator import Page, Paginator
from django.db.models import QuerySet
from rest_framework.request import Request

from utils.log.activity_log import (
    log_activity,
    log_entity_change,
    log_bulk_operation,
    log_guest_activity,
)
from core.enums.action_type import ActionType
from core.models import BaseModel

# TypeVar for proper return type annotation
T = TypeVar("T", bound="BaseService")

# Sentinel object to detect unset context state
_UNSET_CONTEXT: object = object()


def required_context(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to ensure that the service method has a valid context.

    This decorator checks if self.ctx is not None before executing the method.
    If ctx is None, it raises a ValueError with a descriptive message.

    Args:
        func: The method to be decorated

    Returns:
        The decorated method

    Raises:
        ValueError: If self.ctx is None when the method is called

    Example:
        class AuthService(BaseService):
            @required_context
            def get_current_user(self):
                # This method requires context to be set
                return self.ctx.user
    """

    @wraps(func)
    def wrapper(self: BaseService, *args: Any, **kwargs: Any) -> Any:
        if self._ctx is _UNSET_CONTEXT:
            raise ValueError(
                f"Context is required for {self.__class__.__name__}.{func.__name__}(). "
                f"Please call use_context(request) first."
            )
        return func(self, *args, **kwargs)

    return wrapper


class BaseService(ABC):
    """Base class for all services."""

    __slots__ = ("_ctx",)

    log_activity = staticmethod(log_activity)
    """
    Core activity logging function for non-model operations.

    This function serves as the foundation for log_guest_activity and log_bulk_operation
    where BaseModel instances are not available.

    Args:
        request: Django HTTP request or DRF request object
        action: Type of action being performed
        entity: Name of the entity type being acted upon
        computed_entity: Full model path for direct access (auto-generated if None)
        entity_id: Primary key of the target entity
        entity_name: Human-readable entity identifier
        old_values: Data state before modification
        new_values: Data state after modification
        changed_fields: List of modified field names
        description: Human-readable activity description
        guest_name: Display name for guest users
        guest_email: Email address for guest users
        guest_phone: Phone number for guest users
        extra_data: Additional structured context data
        **kwargs: Additional metadata for backward compatibility

    Returns:
        ActivityLog: Created activity log instance

    Example:
        log_activity(
            request=request,
            action=ActionType.CREATE,
            entity='product',
            computed_entity='core.Product',
            entity_id=product.pk,
            entity_name=str(product),
            new_values=product.to_dict(),
            extra_data={'source': 'admin_panel'}
        )

    Note:
        For model-based operations, prefer log_entity_change() for better efficiency
        and automatic entity detection.
    """

    log_entity_change = staticmethod(log_entity_change)
    """
    High-performance model change logging with automatic entity detection.

    Leverages BaseModel properties for zero-configuration entity information extraction:
    - entity: automatically from instance._entity
    - computed_entity: automatically from instance._computed_entity
    - entity_id: automatically from instance.pk
    - entity_name: automatically from str(instance)

    Args:
        request: Django HTTP request or DRF request object
        instance: Model instance with auto-extracted entity information
        action: Type of action being performed (CREATE, UPDATE, DELETE, etc.)
        old_instance: Previous instance state (required for UPDATE operations)
        exclude_fields: Field names to exclude from change detection
        include_relations: Whether to include foreign key relations in serialization
        mask_sensitive: Whether to mask sensitive fields (passwords, tokens, etc.)
        extra_data: Additional structured context data
        description: Custom description (auto-generated if not provided)
        **kwargs: Additional parameters for actor context

    Returns:
        ActivityLog: Created activity log instance with complete audit trail

    Raises:
        ValueError: If action type is invalid or required parameters are missing

    Examples:
        # CREATE - Minimal configuration with auto-detection
        log_entity_change(request, product, ActionType.CREATE)

        # UPDATE - With comprehensive change tracking
        old_product = Product.objects.get(id=product.id)
        # ... modify product ...
        log_entity_change(request, product, ActionType.UPDATE, old_instance=old_product)

        # DELETE - With additional context
        log_entity_change(
            request, product, ActionType.DELETE,
            extra_data={'reason': 'discontinued', 'batch_id': 'cleanup_2023'}
        )

    Performance Notes:
        - Uses optimized helper functions for reduced complexity
        - Implements early validation for improved error handling
        - Leverages BaseModel capabilities for consistent data handling
    """

    log_bulk_operation = staticmethod(log_bulk_operation)
    """
    High-performance bulk operation logging with automatic entity detection.

    Efficiently logs batch operations by extracting entity information from the first
    instance and creating comprehensive operation summaries with statistics.

    Args:
        request: Django HTTP request or DRF request object
        action: Type of bulk action performed (CREATE, UPDATE, DELETE, etc.)
        instances: List of model instances processed (entity info extracted from first)
        operation_name: Descriptive name of the bulk operation
        success_count: Number of successfully processed items
        error_count: Number of failed items (defaults to 0)
        extra_data: Additional structured context data
        **kwargs: Additional parameters for extended tracking

    Returns:
        ActivityLog: Created activity log with comprehensive bulk operation summary

    Raises:
        ValueError: If instances list is empty (required for entity type detection)

    Examples:
        # Bulk product creation from CSV import
        log_bulk_operation(
            request, ActionType.CREATE,
            instances=created_products,  # Entity info auto-detected from first product
            operation_name='CSV Product Import',
            success_count=45, error_count=5,
            extra_data={
                'source': 'csv_upload',
                'filename': 'products.csv',
                'import_batch_id': 'batch_2023_11_29'
            }
        )

        # Bulk user account activation
        log_bulk_operation(
            request, ActionType.UPDATE,
            instances=updated_users,
            operation_name='Account Activation Batch',
            success_count=120, error_count=3,
            extra_data={'trigger': 'admin_bulk_action', 'notification_sent': True}
        )

        # Bulk product deletion (cleanup operation)
        log_bulk_operation(
            request, ActionType.DELETE,
            instances=deleted_products,
            operation_name='Discontinued Products Cleanup',
            success_count=25,
            extra_data={'cleanup_reason': 'inventory_optimization'}
        )

    Performance Notes:
        - Uses first instance for efficient entity type detection
        - Optimized bulk metadata generation with pre-computed statistics
        - Minimal overhead for large batch operations
        - Comprehensive audit trail for compliance and monitoring
    """

    log_guest_activity = staticmethod(log_guest_activity)
    """
    Optimized guest activity logging for non-authenticated user interactions.

    Designed for scenarios where BaseModel instances are not available or applicable,
    such as form submissions, page views, and anonymous interactions.

    Args:
        request: Django HTTP request or DRF request object
        action: Type of action being performed (typically VIEW, SUBMIT, DOWNLOAD, etc.)
        entity: Entity type being accessed (manual specification required)
        guest_email: Email address of the guest user if available
        guest_phone: Phone number of the guest user if available
        guest_name: Display name for the guest user
        entity_id: Primary key of the entity being accessed
        entity_name: Human-readable name of the entity for display
        description: Human-readable description of the activity
        extra_data: Additional structured context data
        **kwargs: Additional metadata for extended tracking

    Returns:
        ActivityLog: Created activity log instance with guest context

    Examples:
        # Guest viewing product page
        log_guest_activity(
            request, ActionType.VIEW, 'product',
            entity_id=product.id, entity_name=product.name,
            extra_data={'referrer_source': 'google', 'campaign': 'summer_sale'}
        )

        # Guest form submission with contact details
        log_guest_activity(
            request, ActionType.SUBMIT, 'contact_message',
            guest_email=form.cleaned_data['email'],
            guest_name=form.cleaned_data['name'],
            description='Customer inquiry form submission'
        )

        # Anonymous file download
        log_guest_activity(
            request, ActionType.DOWNLOAD, 'document',
            entity_id=doc.id, entity_name=doc.title,
            extra_data={'file_type': 'pdf', 'file_size': doc.size}
        )

    Performance Notes:
        - Leverages core log_activity function for consistency
        - Optimized for scenarios without BaseModel auto-detection
        - Efficient guest metadata handling and validation
    """

    def __init__(self) -> None:
        """Initialize the service with unset context state."""
        self._ctx: Union[Request, object] = _UNSET_CONTEXT

    @property
    def ctx(self) -> Request:
        """Get the request context. Type-safe access that assumes context is set."""
        return cast(Request, self._ctx)

    def get_paginated_data(
        self, queryset: QuerySet, str_page_number: str = "1", str_page_size: str = "20"
    ) -> Page:
        """Retrieve paginated data from any queryset.

        Args:
            queryset: Django QuerySet to paginate
            str_page_number: Page number as string (default: "1")
            str_page_size: Page size as string (default: "20")

        Returns:
            Page: Django Paginator Page object
        """
        try:
            page_number = int(str_page_number)
            page_size = int(str_page_size)
        except ValueError:
            page_number = 1
            page_size = 20

        page_number = max(page_number, 1)
        page_size = max(page_size, 1)
        page_size = min(page_size, 100)  # Maximum page size limit

        paginator = Paginator(queryset, page_size)

        try:
            page = paginator.get_page(page_number)
        except Exception:
            page = paginator.get_page(1)

        return page

    def use_context(self: T, ctx: Request) -> T:
        """Create a copy of the service with the given context.

        This method creates a shallow copy of the current service instance
        and sets the context, allowing for method chaining while maintaining
        immutability of the original instance.

        Args:
            ctx: Django Request object to set as context

        Returns:
            A new instance of the same service class with context set

        Example:
            service = AuthService().use_context(request)
            # or with chaining:
            result = AuthService().use_context(request).some_method()
        """
        # Create a shallow copy of the current instance
        new_instance = copy(self)
        new_instance._ctx = ctx
        return new_instance
