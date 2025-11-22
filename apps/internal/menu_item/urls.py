from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.MenuItemViewSet.as_view(
            {"post": "create_menu_item", "get": "get_menu_items"}
        ),
        name="menu_items",
    ),
    path(
        "/<int:pk>",
        views.MenuItemViewSet.as_view(
            {
                "get": "get_specific_menu_item",
                "patch": "update_specific_menu_item",
                "delete": "delete_specific_menu_item",
            }
        ),
        name="specific_menu_item",
    ),
]
