from typing import Optional

from core.dto import BaseDTO, dataclass, field


@dataclass
class UpdateSpecificationDTO(BaseDTO):
    """Data Transfer Object for updating existing specification records with partial data support."""

    label: Optional[str] = field(default=None)
    icon: Optional[str] = field(default=None)
    is_active: Optional[bool] = field(default=None)
