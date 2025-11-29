from decimal import Decimal
from typing import Optional

from core.dto import BaseDTO, dataclass, field


@dataclass
class CreateDistributorDTO(BaseDTO):
    """Data Transfer Object for creating new distributor records."""

    name: str
    address: str
    phone: Optional[str] = field(default=None)
    email: Optional[str] = field(default=None)
    website: Optional[str] = field(default=None)
    latitude: Optional[Decimal] = field(default=None)
    longitude: Optional[Decimal] = field(default=None)


@dataclass
class UpdateDistributorDTO(BaseDTO):
    """Data Transfer Object for updating existing distributor records with partial data support."""

    name: Optional[str] = field(default=None)
    address: Optional[str] = field(default=None)
    phone: Optional[str] = field(default=None)
    email: Optional[str] = field(default=None)
    website: Optional[str] = field(default=None)
    latitude: Optional[Decimal] = field(default=None)
    longitude: Optional[Decimal] = field(default=None)
