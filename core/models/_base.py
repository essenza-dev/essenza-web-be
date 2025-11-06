"""
Base/Abstract models for inheritance
"""

from __future__ import annotations

from typing import Optional
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
        self.save(update_fields=['is_deleted', 'deleted_at'])

    def restore(self) -> None:
        """Restore the soft deleted object."""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=['is_deleted', 'deleted_at'])

    @property
    def is_active(self) -> bool:
        """Check if the object is active (not soft deleted)."""
        return not self.is_deleted
