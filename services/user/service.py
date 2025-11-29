from typing import Dict, Tuple

from core.enums import ActionType
from core.service import BaseService, required_context
from core.models import User
from utils.log.activity_log import ActivityLogParams

from . import dto


class UserService(BaseService):
    """Service class for user-related operations."""

    @required_context
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
            params = ActivityLogParams(
                entity=user._entity,
                computed_entity=user._computed_entity,
                entity_id=user.id,
                entity_name=user.username,
                description=f"User {user.username} updated their profile.",
            )
            self.log_activity(ActionType.UPDATE, params)

        return user, None

    @required_context
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
        params = ActivityLogParams(
            entity=user._entity,
            computed_entity=user._computed_entity,
            entity_id=user.id,
            entity_name=user.username,
            description=f"User {user.username} changed their password.",
        )
        self.log_activity(ActionType.UPDATE, params)

        return None
