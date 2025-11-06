import time
from typing import Any, Dict, Optional

from django.db.models import Q
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from core.constants.api_docs import ApiResponseDocs, ApiTags
from core.constants.api_docs import ApiResponseDocs
from core.models import User
from core.views import BaseApiView
from utils.jwt import JsonWebToken
from utils.response import api_response
from core.decorators import validate_body, jwt_refresh_token_required
from apps.auth.serializers import (
    PostAuthTokenRequest,
    PostAuthTokenResponse,
    PutAuthTokenRequest,
)


class AuthTokenAPIView(BaseApiView):
    """
    API View for user authentication and token management
    """

    _jwt: JsonWebToken = JsonWebToken()

    @extend_schema(
        summary="Create Auth Token",
        description="Endpoint for user login with username and password",
        request=PostAuthTokenRequest,
        tags=[ApiTags.API_AUTHENTICATION],
        auth=[],
        responses=ApiResponseDocs.CREATE_AUTH_TOKEN
    )
    @validate_body(PostAuthTokenRequest)
    def post(self, request: Request, validated_data: Dict[str, Any]) -> Response:
        """
        Authenticate user and generate JWT tokens
        """
        username: str = validated_data["username"]
        password: str = validated_data["password"]

        # Optimize query by using select_related if needed and only() for specific fields
        user: Optional[User] = User.objects.filter(
            Q(username=username) | Q(email=username)
        ).only('id', 'username', 'password').first()

        if user and user.check_password(password):
            token, refresh_token = self._jwt.encode(user.username)
            return api_response(request).success(
                data=PostAuthTokenResponse(
                    instance={"token": token, "refresh_token": refresh_token}
                ).data,
                message="Login successful",
            )

        return api_response(request).unauthorized(
            message="Invalid username or password"
        )

    @jwt_refresh_token_required
    @extend_schema(
        summary="Refresh Auth Token",
        description="Endpoint for user to refresh JWT token",
        request=PutAuthTokenRequest,
        tags=[ApiTags.API_AUTHENTICATION],
        responses=ApiResponseDocs.REFRESH_AUTH_TOKEN,
    )
    @validate_body(PutAuthTokenRequest)
    def put(self, request: Request, validated_data: Dict[str, Any]) -> Response:
        """
        Refresh JWT token if the refresh token is valid and token is near expiration
        """
        current_token: str = request.auth
        current_signature: str = self._jwt.get_signature(current_token)

        if current_signature != validated_data["refresh_token"]:
            return api_response(request).unauthorized(
                message="Invalid refresh token"
            )

        payload: Dict[str, Any] = self._jwt.decode(current_token, expiration=False)
        remaining_time: int = payload['exp'] - int(time.time())

        # Only generate new token if current one expires within 2 minutes
        if remaining_time < 120:
            current_token, current_signature = self._jwt.encode(request.user.username)

        return api_response(request).success(
            data=PostAuthTokenResponse(
                instance={"token": current_token, "refresh_token": current_signature}
            ).data,
            message="Token refreshed successfully",
        )
