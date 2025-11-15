from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from utils.response import api_response
from core.decorators import jwt_required, validate_body
from docs.api.internal import MenuAPI
from services import MenuService

from . import serializers


class MenuViewSet(BaseViewSet):
    """ViewSet for managing menu items."""

    _menu_service = MenuService()

    @MenuAPI.create_menu
    @jwt_required
    @validate_body(serializers.PostCreateMenuRequest)
    def create_menu(self, request: Request, validated_data) -> Response:
        """Create a new menu."""
        menu, error = self._menu_service.create_menu(validated_data)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            data=serializers.MenuModelSerializer(menu).data,
            message="Menu created successfully",
        )

    @MenuAPI.get_menu
    @jwt_required
    def get_menus(self, request: Request) -> Response:
        """Retrieve all menus."""
        menus = self._menu_service.get_menus()
        return api_response(request).success(
            data=serializers.MenuModelSerializer(menus, many=True).data,
            message="Menus retrieved successfully",
        )

    @MenuAPI.get_specific_menu
    @jwt_required
    def get_specific_menu(self, request: Request, pk: int) -> Response:
        """Retrieve a specific menu by its ID."""
        menu, error = self._menu_service.get_specific_menu(pk)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            data=serializers.MenuModelSerializer(menu).data,
            message="Menu retrieved successfully",
        )

    @MenuAPI.update_specific_menu
    @jwt_required
    @validate_body(serializers.PatchUpdateMenuRequest)
    def update_specific_menu(
        self, request: Request, pk: int, validated_data
    ) -> Response:
        """Update a specific menu by its ID."""
        menu, error = self._menu_service.update_specific_menu(pk, validated_data)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            data=serializers.MenuModelSerializer(menu).data,
            message="Menu updated successfully",
        )

    @MenuAPI.delete_specific_menu
    @jwt_required
    def delete_specific_menu(self, request: Request, pk: int) -> Response:
        """Delete a specific menu by its ID."""
        error = self._menu_service.delete_specific_menu(pk)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(message="Menu deleted successfully")

    @MenuAPI.get_menu_items
    @jwt_required
    def get_menu_items(self, request: Request, menu_id: int) -> Response:
        """Retrieve all items for a specific menu."""
        items, error = self._menu_service.get_menu_items(menu_id)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            data=serializers.MenuItemModelSerializer(items, many=True).data,
            message="Menu items retrieved successfully",
        )
