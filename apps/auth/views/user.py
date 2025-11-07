from typing import Any, Dict

from rest_framework.request import Request
from rest_framework.response import Response

from apps.auth.serializers import (
    GetAuthUserProfileResponse,
    PatchAuthUserProfileRequest,
    PostAuthTokenResponse,
    PutAuthUserPasswordRequest,
)
from core.models.user import User
from core.views import BaseViewSet
from utils.jwt import JsonWebToken
from utils.response import api_response
from docs.api.authentication import AuthenticationApi
from core.decorators import validate_body, jwt_required


class AuthUserViewSet(BaseViewSet):
    """
    ViewSet for managing authenticated user operations
    """

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
    def update_profile(self, request: Request, validated_data: Dict[str, Any]) -> Response:
        """
        Update the authenticated user's profile information
        """
        user = request.user
        username: str | None = validated_data.get("username")
        name: str | None = validated_data.get("name")
        email: str | None = validated_data.get("email")

        fields_to_update: Dict[str, str] = {}

        # Validate and prepare username update
        if username and username != user.username:
            if not User.available_username(username):
                return api_response(request).error(message="Username is already taken")
            fields_to_update["username"] = username

        # Validate and prepare name update
        if name and name != user.name:
            fields_to_update["name"] = name

        # Validate and prepare email update
        if email and email != user.email:
            if not User.available_email(email):
                return api_response(request).error(
                    message="Email address is already taken"
                )
            fields_to_update["email"] = email

        # Bulk update fields if any changes exist
        if fields_to_update:
            User.objects.filter(id=user.id).update(**fields_to_update)
            user.refresh_from_db(fields=list(fields_to_update.keys()))

        return api_response(request).success(
            data=GetAuthUserProfileResponse(instance=user).data,
            message="User profile updated successfully",
        )

    @AuthenticationApi.change_password
    @jwt_required
    @validate_body(PutAuthUserPasswordRequest)
    def change_password(self, request: Request, validated_data: Dict[str, Any]) -> Response:
        """
        Change the authenticated user's password and regenerate tokens
        """
        user = request.user
        current_password: str = validated_data["current_password"]
        new_password: str = validated_data["new_password"]

        if not user.check_password(current_password):
            return api_response(request).error(message="Current password is incorrect")

        user.set_password(new_password)
        user.save(update_fields=["password"])

        jwt_handler = JsonWebToken(user.token_signature)
        auth_token, refresh_token = jwt_handler.encode(str(user.id))

        return api_response(request).success(
            data=PostAuthTokenResponse(
                instance={"token": auth_token, "refresh_token": refresh_token}
            ).data,
            message="Password changed successfully",
        )
