from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response

from apps.setting import serializers
from core.models import Setting
from core.views import BaseViewSet
from docs.api import SettingApi
from utils.response import api_response


class SettingsViewSet(BaseViewSet):
    """
    ViewSet for managing application settings with optimized database operations
    """

    @SettingApi.get_settings
    def get_settings(self, request: Request) -> Response:
        """
        Retrieve application settings with optimized database query
        """
        if settings := Setting.objects.first():
            serialized_data: Any = serializers.GetSettingsResponse(
                instance=settings
            ).data

            return api_response(request).success(
                data=serialized_data,
                message="Settings retrieved successfully",
            )

        return api_response(request).error(
            message="Settings not found",
        )
