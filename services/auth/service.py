from typing import Tuple, Dict, Any
from datetime import datetime, timezone

from django.db.models import Q
from django.utils import timezone as django_timezone

from core.service import BaseService
from core.models import User
from utils.jwt import JsonWebToken

from . import dto


class AuthService(BaseService):
    """Service class for authentication-related operations."""

    def create_auth_token(self, user: User) -> Tuple[str, str]:
        """Create authentication tokens for a user."""
        jwt_handler = JsonWebToken(user.token_signature)
        token, refresh_token = jwt_handler.encode(str(user.id))
        return token, refresh_token

    def authenticate(
        self, username: str, password: str
    ) -> Tuple[dto.AuthTokensDTO, Exception | None]:
        """Authenticate user credentials and return JWT tokens."""
        # Optimize query with specific field selection and single database hit
        user: User | None = (
            User.objects.filter(Q(username=username) | Q(email=username))
            .only("id", "username", "password")
            .first()
        )

        if user and user.check_password(password):
            # Update last_login with optimized query
            User.objects.filter(id=user.id).update(last_login=django_timezone.now())
            auth_token, refresh_token = self.create_auth_token(user)
            return (
                dto.AuthTokensDTO(access_token=auth_token, refresh_token=refresh_token),
                None,
            )

        return dto.AuthTokensDTO(), Exception("Invalid username or password")

    def refresh_auth_token(
        self, user: User, current_token: str, refresh_token: str
    ) -> Tuple[dto.AuthTokensDTO, Exception | None]:
        """Refresh authentication token for a user."""
        jwt_handler = JsonWebToken(user.token_signature)

        current_signature: str = jwt_handler.get_signature(current_token)

        if current_signature != refresh_token:
            return dto.AuthTokensDTO(), Exception("Invalid refresh token")

        now = datetime.now(timezone.utc)
        payload: Dict[str, Any] = jwt_handler.decode(current_token, expiration=False)
        remaining_time: int = payload["exp"] - int(now.timestamp())

        # Generate new tokens only if current token expires within 2 minutes
        if remaining_time < 120:
            current_token, current_signature = self.create_auth_token(user)

        return (
            dto.AuthTokensDTO(
                access_token=current_token, refresh_token=current_signature
            ),
            None,
        )
