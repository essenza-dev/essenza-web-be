from django.urls import path

from .views import UserViewSet


urlpatterns = [
    path("", UserViewSet.as_view({"post": "create_user", "get": "get_users"})),
    path("/roles", UserViewSet.as_view({"get": "get_user_roles"})),
    path(
        "/<int:pk>",
        UserViewSet.as_view(
            {
                "get": "get_specific_user",
                "put": "update_specific_user",
                "delete": "delete_specific_user",
            }
        ),
    ),
    path(
        "/<int:pk>/toggle",
        UserViewSet.as_view({"patch": "toggle_user_status"}),
    ),
    path(
        "/<int:pk>/password",
        UserViewSet.as_view({"put": "change_user_password"}),
    ),
]
