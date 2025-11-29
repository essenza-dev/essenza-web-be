"""
Optimized Activity Log Utility - Leveraging BaseModel Properties

Enhanced version that fully utilizes BaseModel properties to eliminate
redundant parameters and improve logging efficiency with complete type safety.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from django.http import HttpRequest
from rest_framework.request import Request

from core.enums.action_type import ActionType
from core.enums.actor_type import ActorType

from core.models import ActivityLog, BaseModel, User

# Type aliases for better readability
RequestType = HttpRequest | Request
LogData = Dict[str, Any]
ActorInfo = Dict[str, Any]
BaseParams = Dict[str, Any]


def get_client_ip(request: RequestType) -> Optional[str]:
    """Extract client IP address from request with proxy support."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # Get first IP from comma-separated list (original client IP)
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def log_activity(
    request: RequestType,
    action: ActionType,
    *,
    entity: str = "-",
    computed_entity: Optional[str] = None,
    entity_id: Optional[int] = None,
    entity_name: Optional[str] = None,
    old_values: Optional[Dict[str, Any]] = None,
    new_values: Optional[Dict[str, Any]] = None,
    changed_fields: Optional[List[str]] = None,
    description: Optional[str] = None,
    guest_name: Optional[str] = None,
    guest_email: Optional[str] = None,
    guest_phone: Optional[str] = None,
    extra_data: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> ActivityLog:
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
    # Early validation for better performance
    if action not in ActionType.values:
        raise ValueError(
            f"Invalid action type: {action}. Must be one of {ActionType.values}"
        )

    # Pre-compute common values to avoid repeated calculations
    client_ip = get_client_ip(request)
    user_agent = request.META.get("HTTP_USER_AGENT", "")

    # Build optimized log data structure
    log_data: LogData = {
        "action": action,
        "entity": entity,
        "computed_entity": computed_entity or "-",
        "entity_id": entity_id,
        "entity_name": entity_name,
        "old_values": old_values,
        "new_values": new_values,
        "changed_fields": changed_fields,
        "description": description,
        "ip_address": client_ip,
        "user_agent": user_agent,
        "extra_data": extra_data or {},
    }

    if (
        hasattr(request, "user")
        and request.user is not None
        and request.user.is_authenticated
    ):
        # Optimized authenticated user handling
        user = request.user
        log_data.update(
            {
                "user": user,
                "actor_type": ActorType.USER,
                "actor_identifier": getattr(user, "email", user.username),
                "actor_name": (
                    getattr(user, "get_full_name", lambda: user.username)()
                    or user.username
                ),
                "actor_metadata": None,  # Not needed for authenticated users
            }
        )
    else:
        # Optimized guest user handling with priority-based identifier selection
        actor_identifier = (
            guest_email
            or guest_phone
            or getattr(request.session, "session_key", None)
            or client_ip  # Reuse pre-computed IP
        )

        # Build guest metadata efficiently, filtering None values during creation
        guest_metadata = {
            k: v
            for k, v in {
                "email": guest_email,
                "phone": guest_phone,
                "session_id": getattr(request.session, "session_key", None),
                "device": kwargs.get("device"),
                "browser": kwargs.get("browser"),
                "platform": kwargs.get("platform"),
                "source": kwargs.get("source"),
                "campaign": kwargs.get("campaign"),
                "referrer": request.META.get("HTTP_REFERER"),
                "locale": kwargs.get("locale"),
            }.items()
            if v is not None
        }

        log_data.update(
            {
                "user": None,
                "actor_type": ActorType.GUEST,
                "actor_identifier": actor_identifier,
                "actor_name": guest_name or "Anonymous Guest",
                "actor_metadata": guest_metadata or None,
            }
        )

    # Efficiently merge kwargs into extra_data
    if kwargs:
        log_data["extra_data"].update(kwargs)

    # Create and return activity log
    return ActivityLog.objects.create(**log_data)


def _get_actor_info(request: RequestType, **kwargs: Any) -> ActorInfo:
    """Extract and validate actor information from request and context."""
    is_authenticated = (
        hasattr(request, "user")
        and request.user is not None
        and request.user.is_authenticated
    )

    return {
        "actor_type": ActorType.USER if is_authenticated else ActorType.GUEST,
        "user": (
            request.user
            if is_authenticated and isinstance(request.user, User)
            else None
        ),
        "actor_identifier": kwargs.pop("guest_email", None)
        or kwargs.pop("guest_phone", None),
        "actor_name": kwargs.pop("guest_name", None),
    }


def _get_base_params(
    request: RequestType, extra_data: Optional[Dict[str, Any]]
) -> BaseParams:
    """Generate base parameters for activity logging with optimized data extraction."""
    return {
        "ip_address": get_client_ip(request),
        "user_agent": request.META.get("HTTP_USER_AGENT", ""),
        "extra_data": extra_data,
    }


def _generate_description(
    action: ActionType, instance: BaseModel, description: Optional[str] = None
) -> str:
    """Generate human-readable description for activity log with action context."""
    if description:
        return description

    # Optimized action verb mapping with better performance than .get()
    action_verbs = {
        ActionType.CREATE: "Created",
        ActionType.UPDATE: "Updated",
        ActionType.DELETE: "Deleted",
        ActionType.VIEW: "Viewed",
    }

    action_verb = action_verbs.get(action, action.title())
    return f"{action_verb} {instance._entity}: {instance}"


def _handle_create_action(
    instance: BaseModel,
    actor_info: ActorInfo,
    base_params: BaseParams,
    exclude_fields: Optional[List[str]],
    include_relations: bool,
    mask_sensitive: bool,
    description: str,
) -> ActivityLog:
    """Process CREATE action with optimized data serialization."""
    new_values = instance.to_dict(
        exclude_fields=exclude_fields,
        include_relations=include_relations,
        mask_sensitive=mask_sensitive,
    )

    return ActivityLog.create_for_instance(
        instance=instance,
        action=ActionType.CREATE,
        new_values=new_values,
        description=description,
        **actor_info,
        **base_params,
    )


def _handle_update_action(
    instance: BaseModel,
    old_instance: BaseModel,
    actor_info: ActorInfo,
    base_params: BaseParams,
    exclude_fields: Optional[List[str]],
    mask_sensitive: bool,
    description: str,
) -> ActivityLog:
    """Process UPDATE action with intelligent change detection and optimization."""
    old_values, new_values, changed_fields = BaseModel.get_changed_fields(
        old_instance=old_instance,
        new_instance=instance,
        exclude_fields=exclude_fields,
        mask_sensitive=mask_sensitive,
    )

    # Early return for no-change scenario - log as VIEW for audit trail
    if not changed_fields:
        return ActivityLog.create_for_instance(
            instance=instance,
            action=ActionType.VIEW,
            description=f"No changes detected for {old_instance._entity}: {old_instance}",
            **actor_info,
            **base_params,
        )

    # Generate enhanced description with change statistics
    enhanced_description = (
        f"Updated {old_instance._entity}: {old_instance} ({len(changed_fields)} fields changed)"
        if "Updated" not in description
        else description
    )

    return ActivityLog.create_for_instance(
        instance=instance,
        action=ActionType.UPDATE,
        old_values=old_values,
        new_values=new_values,
        changed_fields=changed_fields,
        description=enhanced_description,
        **actor_info,
        **base_params,
    )


def _handle_delete_action(
    instance: BaseModel,
    actor_info: ActorInfo,
    base_params: BaseParams,
    exclude_fields: Optional[List[str]],
    include_relations: bool,
    mask_sensitive: bool,
    description: str,
) -> ActivityLog:
    """Process DELETE action with complete state preservation."""
    old_values = instance.to_dict(
        exclude_fields=exclude_fields,
        include_relations=include_relations,
        mask_sensitive=mask_sensitive,
    )

    return ActivityLog.create_for_instance(
        instance=instance,
        action=ActionType.DELETE,
        old_values=old_values,
        description=description,
        **actor_info,
        **base_params,
    )


def _handle_other_action(
    instance: BaseModel,
    action: ActionType,
    actor_info: ActorInfo,
    base_params: BaseParams,
    description: str,
) -> ActivityLog:
    """Process miscellaneous actions with minimal overhead (VIEW, LOGIN, etc.)."""
    return ActivityLog.create_for_instance(
        instance=instance,
        action=action,
        description=description,
        **actor_info,
        **base_params,
    )


def log_entity_change(
    request: RequestType,
    instance: BaseModel,
    action: ActionType,
    *,
    old_instance: Optional[BaseModel] = None,
    exclude_fields: Optional[List[str]] = None,
    include_relations: bool = False,
    mask_sensitive: bool = True,
    extra_data: Optional[Dict[str, Any]] = None,
    description: Optional[str] = None,
    **kwargs: Any,
) -> ActivityLog:
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
    # Early validation with optimized error messages
    if action not in ActionType.values:
        raise ValueError(
            f"Invalid action type '{action}'. Must be one of {ActionType.values}"
        )

    if action == ActionType.UPDATE and old_instance is None:
        raise ValueError(
            "old_instance parameter is required for UPDATE actions to ensure accurate change tracking"
        )

    # Extract information using optimized helper functions
    actor_info = _get_actor_info(request, **kwargs)
    base_params = _get_base_params(request, extra_data)
    final_description = _generate_description(action, instance, description)

    # Efficient action routing with match-like behavior
    if action == ActionType.CREATE:
        return _handle_create_action(
            instance,
            actor_info,
            base_params,
            exclude_fields,
            include_relations,
            mask_sensitive,
            final_description,
        )
    elif action == ActionType.UPDATE:
        return _handle_update_action(
            instance, old_instance, actor_info, base_params, exclude_fields, mask_sensitive, final_description  # type: ignore
        )
    elif action == ActionType.DELETE:
        return _handle_delete_action(
            instance,
            actor_info,
            base_params,
            exclude_fields,
            include_relations,
            mask_sensitive,
            final_description,
        )
    else:
        return _handle_other_action(
            instance, action, actor_info, base_params, final_description
        )


def log_guest_activity(
    request: RequestType,
    action: ActionType,
    entity: str,
    *,
    guest_email: Optional[str] = None,
    guest_phone: Optional[str] = None,
    guest_name: Optional[str] = None,
    entity_id: Optional[int] = None,
    entity_name: Optional[str] = None,
    description: Optional[str] = None,
    extra_data: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> ActivityLog:
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
    return log_activity(
        request,
        action,
        entity=entity,
        computed_entity=None,
        entity_id=entity_id,
        entity_name=entity_name,
        description=description,
        guest_name=guest_name,
        guest_email=guest_email,
        guest_phone=guest_phone,
        extra_data=extra_data,
        **kwargs,
    )


def log_bulk_operation(
    request: RequestType,
    action: ActionType,
    instances: List[BaseModel],
    operation_name: str,
    success_count: int,
    *,
    error_count: int = 0,
    extra_data: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> ActivityLog:
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
    if not instances:
        raise ValueError("At least one instance is required for entity type detection")

    # Extract entity information from first instance (assumes homogeneous list)
    first_instance = instances[0]

    # Pre-compute total for better performance in large operations
    total_processed = success_count + error_count

    # Build optimized bulk operation metadata
    bulk_extra_data = {
        "bulk_operation": True,
        "operation_name": operation_name,
        "total_processed": total_processed,
        "success_count": success_count,
        "error_count": error_count,
        "success_rate": (
            round((success_count / total_processed) * 100, 2)
            if total_processed > 0
            else 0
        ),
        "entity_ids": [
            instance.pk for instance in instances if instance.pk is not None
        ],
        **(extra_data or {}),
    }

    # Generate comprehensive description with statistics
    description = (
        f"Bulk {action.lower()} operation: {operation_name} "
        f"({success_count} successful, {error_count} failed)"
    )

    return log_activity(
        request,
        action,
        entity=first_instance._entity,
        computed_entity=first_instance._computed_entity,
        entity_name=f"Bulk {first_instance._entity} operation",
        description=description,
        extra_data=bulk_extra_data,
        **kwargs,
    )
