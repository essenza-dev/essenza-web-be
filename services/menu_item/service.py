from typing import Tuple

from django.db import transaction
from django.db.models.manager import BaseManager

from core.service import BaseService
from core.models import MenuItem, Menu

from . import dto


class MenuItemService(BaseService):
    """Service class for managing menu items."""

    def create_menu_item(
        self, data: dto.CreateMenuItemDTO
    ) -> Tuple[MenuItem, Exception | None]:
        """Create a new menu item."""
        try:
            menu = Menu.objects.get(id=data.menu_id)
            parent_item = None
            if data.parent_id:
                parent_item = MenuItem.objects.get(id=data.parent_id)

            menu_item = MenuItem.objects.create(
                menu=menu,
                lang=data.lang,
                label=data.label,
                link=data.link,
                parent=parent_item,
                order_no=data.order_no,
            )

            return menu_item, None
        except Menu.DoesNotExist:
            return MenuItem(), Exception(
                f"Menu with id '{data.menu_id}' does not exist."
            )
        except MenuItem.DoesNotExist:
            return MenuItem(), Exception(
                f"Parent MenuItem with id '{data.parent_id}' does not exist."
            )
        except Exception as e:
            return MenuItem(), e

    def get_menu_items(self) -> BaseManager[MenuItem]:
        """Retrieve all menu items."""
        return MenuItem.objects.all()

    def get_specific_menu_item(self, pk: int) -> Tuple[MenuItem, Exception | None]:
        """Retrieve a specific menu item by its ID."""
        try:
            menu_item = MenuItem.objects.get(id=pk)
            return menu_item, None
        except MenuItem.DoesNotExist:
            return MenuItem(), Exception(f"MenuItem with id '{pk}' does not exist.")
        except Exception as e:
            return MenuItem(), e

    @transaction.atomic
    def update_specific_menu_item(
        self, pk: int, data: dto.UpdateMenuItemDTO
    ) -> Tuple[MenuItem, Exception | None]:
        """Update a specific menu item by its ID."""
        try:
            menu_item = MenuItem.objects.get(id=pk)
            self._update_menu_item_fields(menu_item, data)
            menu_item.save()
            return menu_item, None
        except MenuItem.DoesNotExist:
            return MenuItem(), Exception(f"MenuItem with id '{pk}' does not exist.")
        except Menu.DoesNotExist:
            return MenuItem(), Exception(
                f"Menu with id '{data.menu_id}' does not exist."
            )
        except Exception as e:
            return MenuItem(), e

    def delete_specific_menu_item(self, pk: int) -> Exception | None:
        """Delete a specific menu item by its ID."""
        try:
            menu_item = MenuItem.objects.get(id=pk)
            menu_item.delete()
            return None
        except MenuItem.DoesNotExist:
            return Exception(f"MenuItem with id '{pk}' does not exist.")
        except Exception as e:
            return e

    def _update_menu_item_fields(
        self, menu_item: MenuItem, data: dto.UpdateMenuItemDTO
    ) -> None:
        """Update menu item fields based on provided data."""
        if data.menu_id is not None:
            menu = Menu.objects.get(id=data.menu_id)
            menu_item.menu = menu
        if data.lang is not None:
            menu_item.lang = data.lang
        if data.label is not None:
            menu_item.label = data.label
        if data.link is not None:
            menu_item.link = data.link
        if data.parent_id is not None:
            self._update_parent_item(menu_item, data.parent_id)
        if data.order_no is not None:
            menu_item.order_no = data.order_no

    def _update_parent_item(self, menu_item: MenuItem, parent_id: int) -> None:
        """Update the parent item for a menu item."""
        if parent_id == 0:
            menu_item.parent = None
        else:
            parent_item = MenuItem.objects.get(id=parent_id)
            menu_item.parent = parent_item
