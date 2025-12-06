from dataclasses import dataclass

from core.dto import BaseDTO, field
from core.models import User


@dataclass
class UpdateProfileDTO:
    user: User
    username: str
    name: str
    email: str


@dataclass
class UpdatePasswordDTO:
    current_password: str
    new_password: str


@dataclass
class CreateUserDTO(BaseDTO):
    """DTO for creating a new user."""

    username: str
    email: str
    password: str
    role: str
    name: str | None = field(default=None)
    is_active: bool = field(default=True)


@dataclass
class UpdateUserDTO(BaseDTO):
    """DTO for updating an existing user."""

    username: str | None = field(default=None)
    name: str | None = field(default=None)
    email: str | None = field(default=None)
    role: str | None = field(default=None)
    is_active: bool | None = field(default=None)


@dataclass
class ChangeUserPasswordDTO:
    """DTO for changing user password by admin."""

    new_password: str
