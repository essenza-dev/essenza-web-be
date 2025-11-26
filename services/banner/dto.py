from django.core.files.uploadedfile import InMemoryUploadedFile

from core.dto import BaseDTO, dataclass, field


@dataclass
class CreateBannerDTO(BaseDTO):
    title: str
    subtitle: str | None = field(default=None)
    image: InMemoryUploadedFile | None = field(default=None)
    link_url: str | None = field(default=None)
    order_no: int = field(default=0)
    is_active: bool = field(default=True)

@dataclass
class UpdateBannerDTO(BaseDTO):
    title: str | None = field(default=None)
    subtitle: str | None = field(default=None)
    image: InMemoryUploadedFile | None = field(default=None)
    link_url: str | None = field(default=None)
    order_no: int | None = field(default=None)
    is_active: bool | None = field(default=None)