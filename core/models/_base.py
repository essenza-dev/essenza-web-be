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
        self,
        using: Optional[str] = None,
        keep_parents: bool = False
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
        self,
        file_references: list[Tuple[str, Any]],
        logger: logging.Logger
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
