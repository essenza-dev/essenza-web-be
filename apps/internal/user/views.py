from typing import Any, Dict

from rest_framework.request import Request
from rest_framework.response import Response

from core.enums import UserRole
from core.views import BaseViewSet
from core.decorators import jwt_required, validate_body
from utils import api_response
from docs.api.internal import UserAPI
from services import UserService
from services.user import dto

from . import serializers


class UserViewSet(BaseViewSet):
    """ViewSet for managing users."""

    _user_service = UserService()

    @UserAPI.create_user_schema
    @jwt_required
    @validate_body(serializers.PostCreateUserRequest)
    def create_user(self, request: Request, validated_data: Dict[str, Any]) -> Response:
        """Create a new user."""
        user, error = self._user_service.use_context(request).create_user(
            dto.CreateUserDTO(**validated_data)
        )

        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="User created successfully.",
            data=serializers.UserModelSerializer(user).data,
        )

    @UserAPI.get_users_schema
    @jwt_required
    def get_users(self, request: Request) -> Response:
        """Retrieve all users."""
        page_number = request.GET.get("page", "1")
        page_size = request.GET.get("page_size", "20")

        page = self._user_service.get_paginated_users(
            str_page_number=page_number, str_page_size=page_size
        )

        return api_response(request).paginated(
            data=serializers.UserModelSerializer(page.object_list, many=True).data,
            page=page,
            message="Users retrieved successfully.",
        )

    @UserAPI.get_specific_user_schema
    @jwt_required
    def get_specific_user(self, request: Request, pk: int) -> Response:
        """Retrieve a specific user by its ID."""
        user, error = self._user_service.get_specific_user(pk=pk)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="User retrieved successfully.",
            data=serializers.UserModelSerializer(user).data,
        )

    @UserAPI.get_user_roles_schema
    @jwt_required
    def get_user_roles(self, request: Request) -> Response:
        """Get all available user roles."""
        roles = [{"name": role[0], "label": role[1]} for role in UserRole.choices]

        return api_response(request).success(
            message="User roles retrieved successfully.",
            data=roles,
        )

    @UserAPI.update_specific_user_schema
    @jwt_required
    @validate_body(serializers.PutUpdateUserRequest)
    def update_specific_user(
        self, request: Request, pk: int, validated_data: Dict[str, Any]
    ) -> Response:
        """Update a specific user by its ID."""
        user, error = self._user_service.use_context(request).update_specific_user(
            pk=pk, data=dto.UpdateUserDTO(**validated_data)
        )
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="User updated successfully.",
            data=serializers.UserModelSerializer(user).data,
        )

    @UserAPI.delete_specific_user_schema
    @jwt_required
    def delete_specific_user(self, request: Request, pk: int) -> Response:
        """Delete a specific user by its ID."""
        error = self._user_service.use_context(request).delete_specific_user(pk=pk)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="User deleted successfully.",
        )

    @UserAPI.toggle_user_status_schema
    @jwt_required
    def toggle_user_status(self, request: Request, pk: int) -> Response:
        """Toggle user active status."""
        user, error = self._user_service.use_context(request).toggle_user_status(pk=pk)
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message=f"User status toggled to {'active' if user.is_active else 'inactive'}.",
            data=serializers.UserModelSerializer(user).data,
        )

    @UserAPI.change_user_password_schema
    @jwt_required
    @validate_body(serializers.PutChangeUserPasswordRequest)
    def change_user_password(
        self, request: Request, pk: int, validated_data: Dict[str, Any]
    ) -> Response:
        """Change user password by admin."""
        user, error = self._user_service.use_context(request).change_user_password(
            pk=pk, data=dto.ChangeUserPasswordDTO(**validated_data)
        )
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="User password changed successfully.",
            data=serializers.UserModelSerializer(user).data,
        )
