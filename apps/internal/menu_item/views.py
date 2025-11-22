from core.views import BaseViewSet
from rest_framework.request import Request
from rest_framework.response import Response

from utils import api_response
from core.decorators import jwt_required, validate_body
from docs.api.internal import MenuItemAPI
from services import MenuItemService, menu
from services.menu_item.dto import CreateMenuItemDTO, UpdateMenuItemDTO

from . import serializers


class MenuItemViewSet(BaseViewSet):
    """ViewSet for managing menu items."""

    _menu_item_service = MenuItemService()

    @MenuItemAPI.create_menu_item
    @jwt_required
    @validate_body(serializers.PostCreateMenuItemRequest)
    def create_menu_item(self, request: Request, validated_data) -> Response:
        """Create a new menu item."""
        result, error = self._menu_item_service.create_menu_item(
            CreateMenuItemDTO(**validated_data)
        )
        print("result, error", result.id, error)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).created(
            message="Menu item created successfully",
            data=serializers.MenuItemModelSerializer(result).data,
        )

    @MenuItemAPI.get_menu_items
    @jwt_required
    def get_menu_items(self, request: Request) -> Response:
        """Retrieve all menu items."""
        results = self._menu_item_service.get_menu_items()
        return api_response(request).success(
            message="Menu items retrieved successfully",
            data=serializers.MenuItemModelSerializer(results, many=True).data,
        )

    @MenuItemAPI.get_specific_menu_item
    @jwt_required
    def get_specific_menu_item(self, request: Request, pk: int) -> Response:
        """Retrieve a specific menu item by its ID."""
        menu_item, error = self._menu_item_service.get_specific_menu_item(pk)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Menu item retrieved successfully",
            data=serializers.MenuItemModelSerializer(menu_item).data,
        )

    @MenuItemAPI.update_specific_menu_item
    @jwt_required
    @validate_body(serializers.PatchUpdateMenuItemRequest)
    def update_specific_menu_item(
        self, request: Request, pk: int, validated_data
    ) -> Response:
        """Update a specific menu item by its ID."""
        menu_item, error = self._menu_item_service.update_specific_menu_item(
            pk, UpdateMenuItemDTO(**validated_data)
        )
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Menu item updated successfully",
            data=serializers.MenuItemModelSerializer(menu_item).data,
        )

    @MenuItemAPI.delete_specific_menu_item
    @jwt_required
    def delete_specific_menu_item(self, request: Request, pk: int) -> Response:
        """Delete a specific menu item by its ID."""
        error = self._menu_item_service.delete_specific_menu_item(pk)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(message="Menu item deleted successfully")
