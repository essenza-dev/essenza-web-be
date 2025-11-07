from django.urls import path
from .views import SettingsViewSet

urlpatterns = [
    path("", SettingsViewSet.as_view({"get": "get_settings"}), name="settings"),
]
