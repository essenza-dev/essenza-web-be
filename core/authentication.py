from typing import Optional, Tuple, Any
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from core.models import User
from utils.jwt import JsonWebToken


class JWTAuthentication(BaseAuthentication):
    """
    Custom JWT Bearer token authentication handler.

    Expected header format: Authorization: Bearer <jwt_token>
    """

    keyword = "Bearer"

    def authenticate(self, request: Request) -> Optional[Tuple[User, str]]:
        """
        Authenticate the request and return a tuple of (user, token).

        Args:
            request: The HTTP request object

        Returns:
            Tuple of (User, token) if authentication succeeds, None otherwise

        Raises:
            AuthenticationFailed: If authentication fails with invalid credentials
        """
        auth_header = self._get_auth_header(request)
        if not auth_header:
            return None

        token = self._extract_token(auth_header)
        return self._authenticate_token(token) if token else None

    def _get_auth_header(self, request: Request) -> Optional[str]:
        """Extract authorization header from request."""
        return request.META.get("HTTP_AUTHORIZATION")

    def _extract_token(self, auth_header: str) -> Optional[str]:
        """
        Extract JWT token from authorization header.

        Args:
            auth_header: The authorization header value

        Returns:
            The JWT token if found, None otherwise

        Raises:
            AuthenticationFailed: If header format is invalid
        """
        if not auth_header.startswith(f"{self.keyword} "):
            return None

        try:
            _, token = auth_header.split(" ", 1)
            return token.strip() if token else None
        except ValueError as e:
            raise AuthenticationFailed(
                f"Invalid authorization header format. Expected: {self.keyword} <token>"
            ) from e

    def _authenticate_token(self, token: str) -> Tuple[User, str]:
        """
        Validate JWT token and return authenticated user.

        Args:
            token: The JWT token to validate

        Returns:
            Tuple of (User, token)

        Raises:
            AuthenticationFailed: If token validation or user lookup fails
        """
        try:
            jwt_handler = JsonWebToken()
            payload = jwt_handler.decode(token)

            print("payload:", payload)  # Debugging line

            if not payload:
                raise AuthenticationFailed("Invalid or expired token")

            username = payload.get("username")
            if not username:
                raise AuthenticationFailed(
                    "Token payload is invalid - missing username"
                )

            user = self._get_user(username)
            return (user, token)

        except AuthenticationFailed:
            raise
        except Exception as exc:
            raise AuthenticationFailed(f"Token validation failed: {exc}") from exc

    def _get_user(self, username: str) -> User:
        """
        Retrieve user by username.

        Args:
            username: The username to look up

        Returns:
            User instance

        Raises:
            AuthenticationFailed: If user is not found
        """
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist as exc:
            raise AuthenticationFailed("User not found") from exc

    def authenticate_header(self, request: Request) -> str:
        """
        Return the authentication scheme name for WWW-Authenticate header.

        Args:
            request: The HTTP request object

        Returns:
            The authentication scheme name
        """
        return self.keyword
