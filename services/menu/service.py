from typing import Tuple
from django.db.models.manager import BaseManager
from core.service import BaseService
from core.models import Menu, MenuItem


class MenuService(BaseService):
    """Service class for managing menu items."""

    def create_menu(self, data: dict) -> Tuple[Menu, Exception | None]:
        """Create a new menu."""
        try:
            menu = Menu.objects.create(**data)
            return menu, None
        except Exception as e:
            return Menu(), e

    def get_menus(self) -> BaseManager[Menu]:
        """Retrieve all menus."""
        return Menu.objects.all()

    def get_specific_menu(self, id: int) -> Tuple[Menu, Exception | None]:
        """Retrieve a specific menu by its ID."""
        try:
            menu = Menu.objects.get(id=id)
            return menu, None
        except Menu.DoesNotExist:
            return Menu(), Exception(f"Menu with id '{id}' does not exist.")
        except Exception as e:
            return Menu(), e

    def update_specific_menu(
        self, id: int, data: dict
    ) -> Tuple[Menu, Exception | None]:
        """Update a specific menu by its ID."""
        try:
            menu = Menu.objects.get(id=id)
            for key, value in data.items():
                setattr(menu, key, value)
            menu.save()
            return menu, None
        except Menu.DoesNotExist:
            return Menu(), Exception(f"Menu with id '{id}' does not exist.")
        except Exception as e:
            return Menu(), e

    def delete_specific_menu(self, id: int) -> Exception | None:
        """Delete a specific menu by its ID."""
        try:
            menu = Menu.objects.get(id=id)
            menu.delete()
            return None
        except Menu.DoesNotExist:
            return Exception(f"Menu with id '{id}' does not exist.")
        except Exception as e:
            return e

    def get_menu_items(
        self, menu_id: int
    ) -> Tuple[BaseManager[MenuItem], Exception | None]:
        """Retrieve all items for a specific menu."""
        try:
            menu = Menu.objects.get(id=menu_id)
            return MenuItem.objects.filter(menu=menu), None
        except Menu.DoesNotExist:
            return MenuItem.objects.none(), Exception(
                f"Menu with id '{menu_id}' does not exist."
            )
        except Exception as e:
            return MenuItem.objects.none(), e
