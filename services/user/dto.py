from dataclasses import dataclass
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