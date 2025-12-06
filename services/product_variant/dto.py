from typing import Optional, List, Dict
from django.core.files.uploadedfile import InMemoryUploadedFile

from core.dto import BaseDTO, dataclass, field


@dataclass
class CreateProductVariantDTO(BaseDTO):
    """Data Transfer Object for creating new product variant records."""

    sku: Optional[str] = field(default=None)
    model: Optional[str] = field(default=None)
    size: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    image: Optional[InMemoryUploadedFile] = field(default=None)
    is_active: Optional[bool] = field(default=True)
    specifications: Optional[List[Dict[str, str]]] = field(default=None)


@dataclass
class UpdateProductVariantDTO(BaseDTO):
    """Data Transfer Object for updating existing product variant records with partial data support."""

    sku: Optional[str] = field(default=None)
    model: Optional[str] = field(default=None)
    size: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    image: Optional[InMemoryUploadedFile] = field(default=None)
    is_active: Optional[bool] = field(default=None)


@dataclass
class ToggleProductVariantStatusDTO(BaseDTO):
    """Data Transfer Object for toggling product variant active status."""

    is_active: bool


@dataclass
class SpecificationValueDTO(BaseDTO):
    """Data Transfer Object for single specification value."""

    specification_slug: str
    value: str


@dataclass
class UpdateProductVariantSpecificationsDTO(BaseDTO):
    """Data Transfer Object for updating variant specifications."""

    specifications: List[Dict[str, str]]