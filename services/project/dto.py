"""
Project Data Transfer Objects (DTOs)
Contains all DTOs for project-related operations
"""

from typing import List
from django.core.files.uploadedfile import InMemoryUploadedFile

from core.dto import BaseDTO, dataclass, field


@dataclass
class CreateProjectDTO(BaseDTO):
    """DTO for creating a new project."""

    title: str
    slug: str
    location: str | None = field(default=None)
    description: str | None = field(default=None)
    image: InMemoryUploadedFile | str | None = field(default=None)
    gallery: List[InMemoryUploadedFile] | List[str] | None = field(default=None)
    meta_title: str | None = field(default=None)
    meta_description: str | None = field(default=None)
    meta_keywords: str | None = field(default=None)
    is_active: bool = field(default=True)


@dataclass
class UpdateProjectDTO(BaseDTO):
    """DTO for updating an existing project."""

    title: str | None = field(default=None)
    slug: str | None = field(default=None)
    location: str | None = field(default=None)
    description: str | None = field(default=None)
    image: InMemoryUploadedFile | str | None = field(default=None)
    gallery: List[InMemoryUploadedFile] | List[str] | None = field(default=None)
    meta_title: str | None = field(default=None)
    meta_description: str | None = field(default=None)
    meta_keywords: str | None = field(default=None)
    is_active: bool | None = field(default=None)


@dataclass
class ToggleProjectStatusDTO(BaseDTO):
    """DTO for toggling project active status."""

    is_active: bool


@dataclass
class UpdateProjectImageDTO(BaseDTO):
    """DTO for updating project main image."""

    image: InMemoryUploadedFile


@dataclass
class UpdateProjectGalleryDTO(BaseDTO):
    """DTO for updating project gallery images."""

    gallery: List[InMemoryUploadedFile]


@dataclass
class ProjectFilterDTO(BaseDTO):
    """DTO for filtering projects."""

    search: str | None = field(default=None)
    is_active: bool | None = field(default=None)
