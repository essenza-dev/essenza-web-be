from django.urls import path

from .views import MenuViewSet

urlpatterns = [
    path(
        "",
        MenuViewSet.as_view({"post": "create_menu", "get": "get_menus"}),
        name="menus",
    ),
    path(
        "/<int:pk>",
        MenuViewSet.as_view(
            {
                "get": "get_specific_menu",
                "patch": "update_specific_menu",
                "delete": "delete_specific_menu",
            }
        ),
        name="menu-detail",
    ),
    path(
        "/<int:menu_id>/items",
        MenuViewSet.as_view({"get": "get_menu_items"}),
        name="menu-items",
    ),
]
