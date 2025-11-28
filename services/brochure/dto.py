"""
Brochure Data Transfer Objects (DTOs)
Contains all data transfer objects for brochure-related operations
"""

from django.core.files.uploadedfile import InMemoryUploadedFile

from core.dto import BaseDTO, dataclass, field


@dataclass
class CreateBrochureDTO(BaseDTO):
    """DTO for creating a new brochure."""

    title: str
    file: InMemoryUploadedFile | None = field(default=None)


@dataclass
class UpdateBrochureDTO(BaseDTO):
    """DTO for updating an existing brochure."""

    title: str | None = field(default=None)
    file: InMemoryUploadedFile | None = field(default=None)


@dataclass
class UploadBrochureFileDTO(BaseDTO):
    """DTO for uploading a brochure file."""

    file: InMemoryUploadedFile
