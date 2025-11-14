from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response

from apps.internal.setting import serializers
from core.decorators.authentication import jwt_required
from core.decorators.validation import validate_body
from core.models import Setting
from core.views import BaseViewSet
from services import SettingService
from docs.api.internal import SettingApi
from utils.response import api_response


class SettingsViewSet(BaseViewSet):
    """
    ViewSet for managing application settings with optimized database operations
    """

    _setting_service = SettingService()

    @SettingApi.create_setting
    @jwt_required
    @validate_body(serializers.PostCreateSettingRequest)
    def create_setting(self, request: Request, validated_data) -> Response:
        """
        Create new application settings
        """
        setting, error = self._setting_service.create_setting(**validated_data)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).created(
            data=serializers.SettingModelSerializer(setting).data,
            message="Setting created successfully",
        )

    @SettingApi.get_complete_settings
    @jwt_required
    def get_complete_settings(self, request: Request) -> Response:
        """
        Retrieve all application settings
        """
        settings = self._setting_service.get_all_settings()
        return api_response(request).success(
            data=serializers.SettingModelSerializer(settings, many=True).data,
            message="Settings retrieved successfully",
        )

    @SettingApi.get_specific_setting
    @jwt_required
    def get_specific_setting(self, request: Request, slug: str) -> Response:
        """
        Retrieve a specific setting by its slug
        """
        if setting := self._setting_service.get_setting_by_slug(slug=slug):
            return api_response(request).success(
                data=serializers.SettingModelSerializer(setting).data,
                message="Setting retrieved successfully",
            )
        else:
            return api_response(request).not_found(message="Setting not found")

    @jwt_required
    def update_specific_setting(self, request: Request, slug: str) -> Response:
        """
        Update a specific setting by its slug
        """
        return api_response(request).success(message="Not implemented yet")

    @jwt_required
    def delete_specific_setting(self, request: Request, slug: str) -> Response:
        """
        Delete a specific setting by its slug
        """
        return api_response(request).success(message="Not implemented yet")
