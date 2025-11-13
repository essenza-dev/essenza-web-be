from typing import Any, Dict

from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseApiView
from utils.response import api_response
from core.decorators import validate_body, jwt_refresh_token_required
from apps.internal.auth.serializers import (
    PostAuthTokenRequest,
    PostAuthTokenResponse,
    PutAuthTokenRequest,
)
from docs.api.internal import AuthenticationApi
from services import AuthService


class AuthTokenAPIView(BaseApiView):
    """
    API View for user authentication and token management operations
    """

    _auth_service = AuthService()

    @AuthenticationApi.create_auth_token
    @validate_body(PostAuthTokenRequest)
    def post(self, request: Request, validated_data: Dict[str, Any]) -> Response:
        """
        Authenticate user credentials and generate JWT tokens
        """
        result, error = self._auth_service.authenticate(**validated_data)
        if error:
            return api_response(request).unauthorized(message=str(error))
        return api_response(request).success(
            data=PostAuthTokenResponse(
                instance={
                    "token": result.access_token,
                    "refresh_token": result.refresh_token,
                }
            ).data,
            message="Authentication successful",
        )

    @jwt_refresh_token_required
    @AuthenticationApi.refresh_auth_token
    @validate_body(PutAuthTokenRequest)
    def put(self, request: Request, validated_data: Dict[str, Any]) -> Response:
        """
        Refresh JWT tokens when current token is near expiration
        """
        result, error = self._auth_service.refresh_auth_token(
            user=request.user,
            current_token=request.auth,
            **validated_data,
        )

        if error:
            return api_response(request).unauthorized(message=str(error))

        current_token = result.access_token
        current_signature = result.refresh_token

        return api_response(request).success(
            data=PostAuthTokenResponse(
                instance={"token": current_token, "refresh_token": current_signature}
            ).data,
            message="Token refreshed successfully",
        )
