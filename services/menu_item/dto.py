from dataclasses import dataclass, field


@dataclass
class CreateMenuItemDTO:
    menu_id: int
    label: str
    link: str
    parent_id: int | None = field(default=None)
    lang: str = "en"
    order_no: int = 0


@dataclass
class UpdateMenuItemDTO:
    menu_id: int | None = field(default=None)
    label: str | None = field(default=None)
    link: str | None = field(default=None)
    parent_id: int | None = field(default=None)
    lang: str | None = field(default=None)
    order_no: int | None = field(default=None)
