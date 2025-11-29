"""
Activity Log Model

Efficient model for tracking all user and guest activities within the application.
Supports comprehensive activity logging including create, update, delete, and view operations.

Schema designed according to activity-log.md documentation for optimal performance.
"""

from __future__ import annotations
from typing import Optional, Type
from django.db import models
from core.models._base import BaseModel
from core.enums import ActorType, ActionType
from .user import User


class ActivityLog(BaseModel):
    """
    Optimized model for comprehensive activity logging.

    Efficiently tracks both authenticated users and anonymous guests with:
    - Type-safe user relations with proper foreign key constraints
    - Standardized action types using ActionType enum for consistency
    - Automatic entity type detection via BaseModel._entity property
    - Direct model access via computed_entity field (app_label.ModelName)
    - Flexible guest identification supporting multiple identifier types
    - JSON-based change tracking for minimal storage overhead
    - Comprehensive metadata storage with structured data types
    - Helper methods for retrieving original target instances

    Key Features:
    - get_target_instance(): Direct access to original model instance
    - get_target_model_class(): Get model class for dynamic queries
    - create_for_instance(): Automated activity log creation
    """

    # Actor Information - Optimized for both authenticated users and guests
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activity_logs",
        db_index=False,
        help_text="Authenticated user who performed the activity (NULL for guests)",
    )
    actor_type = models.CharField(
        max_length=5,
        choices=ActorType.choices,
        default=ActorType.USER,
        db_index=True,
        help_text="Classification of actor: authenticated user or anonymous guest",
    )
    actor_identifier = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
        help_text="Unique identifier: email, phone, session_id, or IP address",
    )
    actor_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Human-readable actor name for UI display",
    )
    actor_metadata = models.JSONField(
        null=True,
        blank=True,
        help_text="Structured metadata: email, phone, device, browser, session info",
    )

    # Activity Information - Core operation details
    action = models.CharField(
        max_length=12,  # Optimized for enum values
        choices=ActionType.choices,
        db_index=True,
        help_text="Standardized operation type from ActionType enum",
    )
    entity = models.CharField(
        max_length=50,
        db_index=True,
        help_text="Target entity type: product, order, user, article, etc",
    )
    computed_entity = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Full importable model path (app_label.ModelName) for direct access",
    )
    entity_id = models.BigIntegerField(
        null=True,
        blank=True,
        db_index=True,
        help_text="Primary key of the target entity",
    )
    entity_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Human-readable entity identifier for UI display",
    )

    # Change Tracking - Efficient delta storage
    old_values = models.JSONField(
        null=True,
        blank=True,
        help_text="Compressed snapshot of data before modification",
    )
    new_values = models.JSONField(
        null=True,
        blank=True,
        help_text="Compressed snapshot of data after modification",
    )
    changed_fields = models.JSONField(
        null=True, blank=True, help_text="Array of field names that were modified"
    )

    # Context Metadata
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Human-readable activity description for audit trails",
    )
    ip_address = models.GenericIPAddressField(
        null=True, blank=True, help_text="Source IP address of the actor"
    )
    user_agent = models.TextField(
        null=True, blank=True, help_text="Browser and device information string"
    )
    extra_data = models.JSONField(
        null=True,
        blank=True,
        help_text="Flexible storage for additional context, metadata, or application-specific data",
    )

    # Temporal Information
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Timestamp when the activity occurred",
    )

    class Meta:
        db_table = "activity_logs"
        ordering = ["-created_at"]

        # Optimized indexes for common query patterns - MySQL safe
        indexes = [
            # Separate indexes to avoid FK constraint conflicts
            models.Index(fields=["-created_at"], name="idx_actlog_created_at"),
            models.Index(
                fields=["actor_type", "-created_at"], name="idx_actlog_type_time"
            ),
            models.Index(fields=["entity", "entity_id"], name="idx_actlog_entity"),
            models.Index(
                fields=["computed_entity", "entity_id"], name="idx_actlog_comp_ent"
            ),
            # Activity analysis patterns
            models.Index(
                fields=["action", "-created_at"], name="idx_actlog_action_time"
            ),
            models.Index(fields=["actor_identifier"], name="idx_actlog_actor_id"),
            # Audit and reporting patterns
            models.Index(fields=["entity", "-created_at"], name="idx_actlog_ent_time"),
        ]

    def __str__(self) -> str:
        """Efficient string representation for admin and debugging."""
        actor_name: str = self.get_actor_display_name()
        return f"{actor_name} {self.action} {self.entity}"

    def get_actor_display_name(self) -> str:
        """Retrieve optimized display name for the activity actor."""
        if self.actor_type == ActorType.USER and self.user:
            user = self.user
            return (
                getattr(user, "name", None) or user.username if user else "Deleted User"
            )
        return self.actor_name or "Anonymous"

    def get_actor_display_identifier(self) -> Optional[str]:
        """Retrieve primary identifier for the activity actor."""
        if self.actor_type == ActorType.USER and self.user:
            return self.user.email
        return self.actor_identifier

    @property
    def is_user_activity(self) -> bool:
        """Efficiently determine if this represents an authenticated user activity."""
        return self.actor_type == ActorType.USER and self.user is not None

    @property
    def is_guest_activity(self) -> bool:
        """Efficiently determine if this represents a guest activity."""
        return self.actor_type == ActorType.GUEST

    @property
    def has_changes(self) -> bool:
        """Efficiently check if activity contains data modification records."""
        return bool(self.old_values or self.new_values or self.changed_fields)

    def get_guest_email(self) -> Optional[str]:
        """Extract guest email from metadata or identifier with validation."""
        if not self.is_guest_activity:
            return None

        if self.actor_metadata and "email" in self.actor_metadata:
            return self.actor_metadata["email"]

        # Fallback: validate identifier as email
        identifier = self.actor_identifier
        return identifier if identifier and "@" in identifier else None

    def get_guest_phone(self) -> Optional[str]:
        """Extract guest phone number from structured metadata."""
        if self.is_guest_activity and self.actor_metadata:
            return self.actor_metadata.get("phone")
        return None

    def get_session_id(self) -> Optional[str]:
        """Extract session identifier from metadata with fallback validation."""
        if not self.is_guest_activity:
            return None

        if self.actor_metadata and "session_id" in self.actor_metadata:
            return self.actor_metadata["session_id"]

        # Fallback: validate identifier as session ID
        identifier = self.actor_identifier
        return identifier if identifier and identifier.startswith("sess_") else None

    def get_target_instance(self) -> Optional[models.Model]:
        """
        Retrieve the original target instance using computed_entity path.

        Returns:
            BaseModel: The original model instance if exists, None otherwise

        Example:
            activity_log = ActivityLog.objects.get(id=1)
            original_product = activity_log.get_target_instance()
        """
        if not self.computed_entity or not self.entity_id:
            return None

        try:
            from django.apps import apps

            app_label, model_name = self.computed_entity.split(".")
            model_class = apps.get_model(app_label, model_name)
            return model_class.objects.get(pk=self.entity_id)
        except (ValueError, LookupError, model_class.DoesNotExist):
            return None

    def get_target_model_class(self) -> Optional[Type[models.Model]]:
        """
        Get the model class for the target entity.

        Returns:
            Model class or None if not found

        Example:
            activity_log = ActivityLog.objects.get(id=1)
            ProductModel = activity_log.get_target_model_class()
            # Now you can use ProductModel.objects.filter(...)
        """
        if not self.computed_entity:
            return None

        try:
            from django.apps import apps

            app_label, model_name = self.computed_entity.split(".")
            return apps.get_model(app_label, model_name)
        except (ValueError, LookupError):
            return None

    def get_extra_value(self, key: str, default=None):
        """
        Safely retrieve value from extra_data JSON field.

        Args:
            key: The key to retrieve from extra_data
            default: Default value if key not found or extra_data is None

        Returns:
            The value associated with the key, or default if not found

        Example:
            log.get_extra_value('integration_id')
            log.get_extra_value('batch_size', 0)
        """
        if not self.extra_data or not isinstance(self.extra_data, dict):
            return default
        return self.extra_data.get(key, default)

    def set_extra_value(self, key: str, value) -> None:
        """
        Safely set value in extra_data JSON field.

        Args:
            key: The key to set in extra_data
            value: The value to store (must be JSON serializable)

        Example:
            log.set_extra_value('processing_time', 1.5)
            log.set_extra_value('error_code', 'TIMEOUT')
            log.save()
        """
        if not isinstance(self.extra_data, dict):
            self.extra_data = {}

        self.extra_data[key] = value

    @classmethod
    def create_for_instance(
        cls,
        instance: BaseModel,
        action: str,
        actor_type: str = ActorType.USER,
        user: Optional[User] = None,
        actor_identifier: Optional[str] = None,
        actor_name: Optional[str] = None,
        **kwargs,
    ) -> "ActivityLog":
        """Helper method to create activity log with automatic entity type detection.

        Args:
            instance: The model instance that was acted upon
            action: The action performed (should be from ActionType choices)
            actor_type: Type of actor (user or guest)
            user: User who performed the action (if authenticated)
            actor_identifier: Unique identifier for the actor
            actor_name: Display name for the actor
            **kwargs: Additional fields for the activity log (including extra_data)

        Returns:
            ActivityLog: Created activity log instance

        Example:
            ActivityLog.create_for_instance(
                instance=product,
                action=ActionType.UPDATE,
                user=request.user,
                extra_data={
                    'integration_source': 'shopify',
                    'batch_id': 'batch_123',
                    'processing_time': 2.5
                }
            )
        """
        return cls.objects.create(
            user=user,
            actor_type=actor_type,
            actor_identifier=actor_identifier,
            actor_name=actor_name,
            action=action,
            entity=instance._entity,
            computed_entity=instance._computed_entity,
            entity_id=instance.pk,
            entity_name=str(instance),
            **kwargs,
        )
