from typing import Dict, Tuple

from core.service import BaseService
from core.models import User

from . import dto


class UserService(BaseService):
    """Service class for user-related operations."""

    def update_user_profile(
        self, data: dto.UpdateProfileDTO
    ) -> Tuple[User, Exception | None]:
        """Update user profile information."""

        user = data.user
        fields_to_update: Dict[str, str] = {}

        # Validate and prepare username update
        if data.username and data.username != user.username:
            if not User.available_username(data.username):
                return user, Exception("Username is already taken")

            fields_to_update["username"] = data.username

        # Validate and prepare name update
        if data.name and data.name != user.name:
            fields_to_update["name"] = data.name

        # Validate and prepare email update
        if data.email and data.email != user.email:
            if not User.available_email(data.email):
                return user, Exception("Email address is already taken")

            fields_to_update["email"] = data.email

        # Bulk update fields if any changes exist
        if fields_to_update:
            User.objects.filter(id=user.id).update(**fields_to_update)
            user.refresh_from_db(fields=list(fields_to_update.keys()))

        return user, None

    def update_user_password(
        self, user: User, data: dto.UpdatePasswordDTO
    ) -> Exception | None:
        """Update user password."""

        # Verify current password
        if not user.check_password(data.current_password):
            return Exception("Current password is incorrect")

        # Set new password
        user.set_password(data.new_password)
        user.save(update_fields=["password"])

        return None
