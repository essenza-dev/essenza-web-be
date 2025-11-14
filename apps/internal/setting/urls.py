from django.urls import path
from .views import SettingsViewSet

urlpatterns = [
    path(
        "",
        SettingsViewSet.as_view(
            {"post": "create_setting", "get": "get_complete_settings"}
        ),
        name="settings",
    ),
    path(
        "/<str:slug>",
        SettingsViewSet.as_view(
            {
                "get": "get_specific_setting",
                "patch": "update_specific_setting",
                "delete": "delete_specific_setting",
            }
        ),
        name="setting-detail",
    ),
]
