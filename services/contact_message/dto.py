from core.dto import BaseDTO, dataclass, field


@dataclass
class CreateContactMessageDTO(BaseDTO):
    """DTO for creating a new contact message."""

    name: str
    email: str
    subject: str
    message: str
    phone: str | None = field(default=None)


@dataclass
class MarkAsReadContactMessageDTO(BaseDTO):
    """DTO for marking contact message as read/unread."""

    is_read: bool