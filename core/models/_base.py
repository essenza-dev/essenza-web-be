"""
Base/Abstract models for inheritance
"""

from __future__ import annotations
import logging
from typing import Optional, Tuple, Dict, Any

from django.conf import settings
from django.core.files.storage import default_storage
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """
    Abstract base model with common functionality for all models.

    Provides automatic entity type detection for activity logging.
    """

    @property
    def _entity(self) -> str:
        """
        Automatically determine entity type from model class name.

        Returns:
            str: Lowercase model name for consistent entity type identification
        """
        return self.__class__.__name__.lower()

    @property
    def _computed_entity(self) -> str:
        """
        Generate full importable model path for direct model access.

        Returns:
            str: Full model path in format 'app_label.ModelName' that can be used
                 with apps.get_model() for direct model access
        """
        return f"{self._meta.app_label}.{self.__class__.__name__}"

    def _get_default_exclude_fields(self) -> list[str]:
        """Get default fields to exclude for consistency and relevance."""
        return [
            "id",
            "created_at",
            "updated_at",
            "deleted_at",
        ]

    def _get_sensitive_fields(self) -> list[str]:
        """Get fields that should be masked for security."""
        return [
            "password",
            "token",
            "secret",
            "api_key",
            "private_key",
            "access_token",
            "refresh_token",
        ]

    def _mask_sensitive_value(self, field_name: str, value: Any) -> str:
        """Mask sensitive field values for security."""
        if not value:
            return value

        # Convert to string for masking
        str_value = str(value)

        # Show first 2 and last 2 characters for tokens/keys
        if any(keyword in field_name.lower() for keyword in ["token", "key", "secret"]):
            if len(str_value) > 8:
                return f"{str_value[:2]}{'*' * (len(str_value) - 4)}{str_value[-2:]}"
            else:
                return "*" * len(str_value)

        # Standard masking for passwords
        return "*" * min(len(str_value), 8)

    def _should_exclude_field(self, field_name: str, exclude_fields: list[str]) -> bool:
        """Check if field should be excluded from serialization."""
        return field_name in exclude_fields

    def _serialize_datetime_field(self, value: Any) -> Optional[str]:
        """Serialize datetime-related field values."""
        return value.isoformat() if value else None

    def _serialize_file_field(self, value: Any) -> Optional[str]:
        """Serialize file/image field values."""
        return value.url if value else None

    def _serialize_foreign_key_field(
        self, field_name: str, value: Any, include_relations: bool, data: Dict[str, Any]
    ) -> None:
        """Serialize foreign key field values."""
        data[field_name] = value.pk if value else None
        if include_relations:
            data[f"{field_name}_display"] = str(value) if value else None

    def _serialize_numeric_field(self, value: Any) -> Optional[float]:
        """Serialize decimal/float field values."""
        return float(value) if value is not None else None

    def _serialize_field_value(
        self,
        field: models.Field,
        value: Any,
        field_name: str,
        include_relations: bool,
        data: Dict[str, Any],
        mask_sensitive: bool = True,
    ) -> Any:
        """Serialize individual field value based on field type."""
        if value is None:
            return None

        # Check if field should be masked for security
        if mask_sensitive and field_name in self._get_sensitive_fields():
            return self._mask_sensitive_value(field_name, value)

        if isinstance(
            field, (models.DateTimeField, models.DateField, models.TimeField)
        ):
            return self._serialize_datetime_field(value)
        elif isinstance(field, (models.FileField, models.ImageField)):
            return self._serialize_file_field(value)
        elif isinstance(field, models.ForeignKey):
            self._serialize_foreign_key_field(
                field_name, value, include_relations, data
            )
            return None  # Already handled in the method above
        elif isinstance(field, models.JSONField):
            return value
        elif isinstance(field, (models.DecimalField, models.FloatField)):
            return self._serialize_numeric_field(value)
        elif isinstance(field, models.BooleanField):
            return bool(value)
        elif hasattr(value, "isoformat"):
            return value.isoformat()
        else:
            return value

    def to_dict(
        self,
        exclude_fields: Optional[list[str]] = None,
        include_relations: bool = False,
        mask_sensitive: bool = True,
    ) -> Dict[str, Any]:
        """
        Convert model instance to JSON-serializable dictionary for activity logging.

        Args:
            exclude_fields: List of field names to exclude from serialization
            include_relations: Whether to include foreign key relations (as IDs)
            mask_sensitive: Whether to mask sensitive fields like passwords

        Returns:
            Dict[str, Any]: JSON-serializable dictionary of model data

        Example:
            product = Product.objects.get(id=1)
            old_values = product.to_dict(exclude_fields=['created_at'])
            # For debugging (unmask sensitive data)
            debug_values = product.to_dict(mask_sensitive=False)
        """
        exclude_fields = (exclude_fields or []) + self._get_default_exclude_fields()
        data = {}

        for field in self._meta.fields:
            if self._should_exclude_field(field.name, exclude_fields):
                continue

            try:
                value = getattr(self, field.name)
                serialized_value = self._serialize_field_value(
                    field, value, field.name, include_relations, data, mask_sensitive
                )

                # Only set if not None (ForeignKey handling returns None)
                if serialized_value is not None or value is None:
                    data[field.name] = serialized_value

            except (AttributeError, ValueError) as e:
                logging.getLogger(__name__).debug(
                    f"Skipping field {field.name} in {self.__class__.__name__}.to_dict(): {e}"
                )

        return data

    @classmethod
    def get_changed_fields(
        cls,
        old_instance: "BaseModel",
        new_instance: "BaseModel",
        exclude_fields: Optional[list[str]] = None,
        mask_sensitive: bool = True,
    ) -> Tuple[Dict[str, Any], Dict[str, Any], list[str]]:
        """
        Compare two instances and return changed fields for activity logging.

        Args:
            old_instance: Previous state of the model
            new_instance: Current state of the model
            exclude_fields: Fields to exclude from comparison
            mask_sensitive: Whether to mask sensitive fields like passwords

        Returns:
            Tuple containing:
            - old_values: Dict of changed fields with old values
            - new_values: Dict of changed fields with new values
            - changed_fields: List of field names that changed

        Example:
            old_product = Product.objects.get(id=1)
            # ... modify product ...
            old_vals, new_vals, changed = Product.get_changed_fields(old_product, product)
        """
        exclude_fields = exclude_fields or []
        exclude_fields.extend(
            ["updated_at", "modified_at"]
        )  # Always exclude auto-update fields

        old_data = old_instance.to_dict(
            exclude_fields=exclude_fields, mask_sensitive=mask_sensitive
        )
        new_data = new_instance.to_dict(
            exclude_fields=exclude_fields, mask_sensitive=mask_sensitive
        )

        changed_fields = []
        old_values = {}
        new_values = {}

        # Compare all fields
        all_fields = set(old_data.keys()) | set(new_data.keys())

        for field_name in all_fields:
            old_val = old_data.get(field_name)
            new_val = new_data.get(field_name)

            if old_val != new_val:
                changed_fields.append(field_name)
                old_values[field_name] = old_val
                new_values[field_name] = new_val

        return old_values, new_values, changed_fields

    class Meta:
        abstract: bool = True


class TimeStampedModel(BaseModel):
    """
    Abstract model for timestamp functionality.
    Use this as a base class for other models.

    Usage:
        class MyModel(TimeStampedModel):
            name = models.CharField(max_length=100)
    """

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract: bool = True
        ordering: list[str] = ["-created_at"]


class SoftDeleteModel(BaseModel):
    """
    Abstract model for soft delete functionality.
    Provides methods to soft delete and restore objects.
    """

    is_deleted: models.BooleanField = models.BooleanField(default=False)
    deleted_at: models.DateTimeField = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract: bool = True

    def soft_delete(self) -> None:
        """Soft delete the object by marking it as deleted."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def restore(self) -> None:
        """Restore the soft deleted object."""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])

    @property
    def is_active(self) -> bool:
        """Check if the object is active (not soft deleted)."""
        return not self.is_deleted


class FileUploadModel(BaseModel):
    """
    Abstract model providing automatic file cleanup functionality.

    This mixin automatically detects and removes associated files from storage
    when model instances are deleted, preventing orphaned files in your storage backend.

    Features:
        - Automatic detection of FileField and ImageField instances
        - Storage backend agnostic (works with local, S3, GCS, etc.)
        - Graceful error handling that prioritizes database consistency
        - Comprehensive logging for monitoring and debugging

    Usage:
        class Document(TimeStampedModel, FileUploadModel):
            title = models.CharField(max_length=100)
            file = models.FileField(upload_to='documents/')
            thumbnail = models.ImageField(upload_to='thumbnails/')
    """

    class Meta:
        abstract: bool = True

    def delete(
        self, using: Optional[str] = None, keep_parents: bool = False
    ) -> Tuple[int, Dict[str, int]]:
        """
        Enhanced delete method with automatic file cleanup.

        Performs database deletion first, then removes associated files from storage.
        This approach ensures data consistency - database operations always succeed
        even if file cleanup encounters errors.

        Args:
            using (Optional[str]): Database alias to use for the deletion operation
            keep_parents (bool): Whether to preserve parent objects in cascade deletion

        Returns:
            Tuple[int, Dict[str, int]]: Number of deleted objects and deletion count
                                       breakdown by model type

        Raises:
            Does not raise exceptions from file operations to maintain transaction integrity.
            File deletion errors are logged but do not prevent database deletion.

        Note:
            Files are removed using Django's storage backend API, making this
            compatible with any configured storage system (filesystem, cloud, etc.).
        """
        logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

        # Efficiently collect file references using list comprehension
        file_references = [
            (field.name, file_instance)
            for field in self._meta.fields
            if isinstance(field, (models.FileField, models.ImageField))
            and (file_instance := getattr(self, field.name, None))
        ]

        # Execute database deletion with priority
        deletion_result = super().delete(using=using, keep_parents=keep_parents)

        # Perform file cleanup after successful database operation
        if file_references:
            self._cleanup_files(file_references, logger)

        return deletion_result

    def _cleanup_files(
        self, file_references: list[Tuple[str, Any]], logger: logging.Logger
    ) -> None:
        """
        Internal method to handle file cleanup operations.

        Args:
            file_references (list[Tuple[str, Any]]): List of (field_name, file_instance) tuples
            logger (logging.Logger): Logger instance for operation tracking
        """
        model_identifier = f"{self.__class__.__name__}({self.pk})"

        for field_name, file_instance in file_references:
            if not file_instance.name:
                continue

            try:
                if default_storage.exists(file_instance.name):
                    default_storage.delete(file_instance.name)
                    logger.debug(
                        f"File cleanup successful: '{file_instance.name}' "
                        f"from {model_identifier}.{field_name}"
                    )
                else:
                    logger.debug(
                        f"File already removed: '{file_instance.name}' "
                        f"from {model_identifier}.{field_name}"
                    )
            except Exception as exc:
                logger.warning(
                    f"File cleanup failed: '{file_instance.name}' "
                    f"from {model_identifier}.{field_name} - {exc.__class__.__name__}: {exc}"
                )


def upload_to(path: str) -> str:
    """
    Generate upload path for file fields.

    Args:
        instance (models.Model): The model instance.
        filename (str): The original filename.

    Returns:
        str: The upload path.
    """
    return f"{settings.FILE_UPLOAD_BASE_DIR}uploads/{path}"
