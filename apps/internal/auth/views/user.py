from typing import Any, Dict

from rest_framework.request import Request
from rest_framework.response import Response

from apps.internal.auth.serializers import (
    GetAuthUserProfileResponse,
    PatchAuthUserProfileRequest,
    PostAuthTokenResponse,
    PutAuthUserPasswordRequest,
)
from core.views import BaseViewSet
from utils.response import api_response
from docs.api.internal import AuthenticationApi
from core.decorators import validate_body, jwt_required
from services import UserService, AuthService
from services.user.dto import UpdateProfileDTO, UpdatePasswordDTO


class AuthUserViewSet(BaseViewSet):
    """
    ViewSet for managing authenticated user operations
    """

    _user_service = UserService()
    _auth_service = AuthService()

    @AuthenticationApi.get_profile
    @jwt_required
    def get_profile(self, request: Request) -> Response:
        """
        Retrieve the authenticated user's profile information
        """
        return api_response(request).success(
            data=GetAuthUserProfileResponse(instance=request.user).data,
            message="User profile retrieved successfully",
        )

    @AuthenticationApi.update_profile
    @jwt_required
    @validate_body(PatchAuthUserProfileRequest)
    def update_profile(
        self, request: Request, validated_data: Dict[str, Any]
    ) -> Response:
        """
        Update the authenticated user's profile information
        """
        user, error = self._user_service.update_user_profile(
            data=UpdateProfileDTO(user=request.user, **validated_data)
        )
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            data=GetAuthUserProfileResponse(instance=user).data,
            message="User profile updated successfully",
        )

    @AuthenticationApi.change_password
    @jwt_required
    @validate_body(PutAuthUserPasswordRequest)
    def change_password(
        self, request: Request, validated_data: Dict[str, Any]
    ) -> Response:
        """
        Change the authenticated user's password and regenerate tokens
        """
        user = request.user
        if error := self._user_service.update_user_password(
            user=user,
            data=UpdatePasswordDTO(**validated_data),
        ):
            return api_response(request).error(message=str(error))

        auth_token, refresh_token = self._auth_service.create_auth_token(user)

        return api_response(request).success(
            data=PostAuthTokenResponse(
                instance={"token": auth_token, "refresh_token": refresh_token}
            ).data,
            message="Password changed successfully",
        )
