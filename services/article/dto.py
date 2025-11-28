from datetime import datetime
from django.core.files.uploadedfile import InMemoryUploadedFile
from core.dto import BaseDTO, dataclass, field


@dataclass
class CreateArticleDTO(BaseDTO):
    """DTO for creating a new article."""

    slug: str
    title: str
    content: str
    thumbnail: InMemoryUploadedFile | None = field(default=None)  # File field
    author: str | None = field(default=None)
    tags: str | None = field(default=None)
    meta_title: str | None = field(default=None)
    meta_description: str | None = field(default=None)
    meta_keywords: str | None = field(default=None)
    is_active: bool = field(default=True)


@dataclass
class UpdateArticleDTO(BaseDTO):
    """DTO for updating an existing article."""

    slug: str | None = field(default=None)
    title: str | None = field(default=None)
    content: str | None = field(default=None)
    thumbnail: InMemoryUploadedFile | None = field(default=None)  # File field
    author: str | None = field(default=None)
    tags: str | None = field(default=None)
    meta_title: str | None = field(default=None)
    meta_description: str | None = field(default=None)
    meta_keywords: str | None = field(default=None)
    published_at: datetime | None = field(default=None)
    is_active: bool | None = field(default=None)


@dataclass
class ToggleArticleStatusDTO(BaseDTO):
    """DTO for toggling article active status."""

    is_active: bool


@dataclass
class PublishArticleDTO(BaseDTO):
    """DTO for publishing/unpublishing an article."""

    published_at: datetime | None = field(default=None)
