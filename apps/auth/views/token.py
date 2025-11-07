from datetime import datetime, timezone
from typing import Any, Dict

from django.db.models import Q
from django.utils import timezone as django_timezone
from rest_framework.request import Request
from rest_framework.response import Response

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
from docs.api.authentication import AuthenticationApi


class AuthTokenAPIView(BaseApiView):
    """
    API View for user authentication and token management operations
    """

    @AuthenticationApi.create_auth_token
    @validate_body(PostAuthTokenRequest)
    def post(self, request: Request, validated_data: Dict[str, Any]) -> Response:
        """
        Authenticate user credentials and generate JWT tokens
        """
        username: str = validated_data["username"]
        password: str = validated_data["password"]

        # Optimize query with specific field selection and single database hit
        user: User | None = User.objects.filter(
            Q(username=username) | Q(email=username)
        ).only('id', 'username', 'password', 'token_signature').first()

        if user and user.check_password(password):
            jwt_handler = JsonWebToken(user.token_signature)
            token, refresh_token = jwt_handler.encode(str(user.id))

            # Update last_login with optimized query
            User.objects.filter(id=user.id).update(last_login=django_timezone.now())

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
    @AuthenticationApi.refresh_auth_token
    @validate_body(PutAuthTokenRequest)
    def put(self, request: Request, validated_data: Dict[str, Any]) -> Response:
        """
        Refresh JWT tokens when current token is near expiration
        """
        user = request.user
        jwt_handler = JsonWebToken(user.token_signature)
        current_token: str = request.auth
        current_signature: str = jwt_handler.get_signature(current_token)

        if current_signature != validated_data["refresh_token"]:
            return api_response(request).unauthorized(
                message="Invalid refresh token"
            )

        now = datetime.now(timezone.utc)
        payload: Dict[str, Any] = jwt_handler.decode(current_token, expiration=False)
        remaining_time: int = payload['exp'] - int(now.timestamp())

        # Generate new tokens only if current token expires within 2 minutes
        if remaining_time < 120:
            current_token, current_signature = jwt_handler.encode(str(user.id))

        return api_response(request).success(
            data=PostAuthTokenResponse(
                instance={"token": current_token, "refresh_token": current_signature}
            ).data,
            message="Token refreshed successfully",
        )
