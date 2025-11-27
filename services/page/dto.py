from core.dto import BaseDTO, dataclass, field


@dataclass
class CreatePageDTO(BaseDTO):
    """DTO for creating a new page."""

    slug: str
    title: str
    content: str
    meta_title: str | None = field(default=None)
    meta_description: str | None = field(default=None)
    meta_keywords: str | None = field(default=None)
    template: str | None = field(default=None)
    is_active: bool = field(default=True)


@dataclass
class UpdatePageDTO(BaseDTO):
    """DTO for updating an existing page."""

    slug: str | None = field(default=None)
    title: str | None = field(default=None)
    content: str | None = field(default=None)
    meta_title: str | None = field(default=None)
    meta_description: str | None = field(default=None)
    meta_keywords: str | None = field(default=None)
    template: str | None = field(default=None)
    is_active: bool | None = field(default=None)


@dataclass
class TogglePageStatusDTO(BaseDTO):
    """DTO for toggling page active status."""

    is_active: bool
