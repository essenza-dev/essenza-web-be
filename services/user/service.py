import copy
from typing import Dict, Tuple

from django.core.paginator import Page
from django.db.models.manager import BaseManager

from core.enums import ActionType
from core.service import BaseService, required_context
from core.models import User
from utils.log.activity_log import ActivityLogParams

from . import dto


class UserService(BaseService):
    """Service class for user-related operations."""

    # Error message constants
    _ERROR_USERNAME_TAKEN = "Username is already taken"
    _ERROR_EMAIL_TAKEN = "Email address is already taken"
    _ERROR_USER_NOT_FOUND = "User with id '{pk}' does not exist."
    _ERROR_CURRENT_PASSWORD_INCORRECT = "Current password is incorrect"

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
                return user, Exception(self._ERROR_USERNAME_TAKEN)

            fields_to_update["username"] = data.username

        # Validate and prepare name update
        if data.name and data.name != user.name:
            fields_to_update["name"] = data.name

        # Validate and prepare email update
        if data.email and data.email != user.email:
            if not User.available_email(data.email):
                return user, Exception(self._ERROR_EMAIL_TAKEN)

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
            return Exception(self._ERROR_CURRENT_PASSWORD_INCORRECT)

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

    @required_context
    def create_user(self, data: dto.CreateUserDTO) -> Tuple[User, Exception | None]:
        """Create a new user."""
        try:
            # Validate username availability
            if not User.available_username(data.username):
                return User(), Exception(self._ERROR_USERNAME_TAKEN)

            # Validate email availability
            if not User.available_email(data.email):
                return User(), Exception(self._ERROR_EMAIL_TAKEN)

            # Create user with hashed password
            user_data = data.to_dict()
            password = user_data.pop("password")

            user = User.objects.create(**user_data)
            user.set_password(password)
            user.save(update_fields=["password"])

            self.log_entity_change(
                self.ctx,
                instance=user,
                old_instance=None,
                action=ActionType.CREATE,
                description=f"User {user.username} created",
            )
            return user, None
        except Exception as e:
            return User(), e

    def get_users(self) -> BaseManager[User]:
        """Retrieve all users."""
        return User.objects.all()

    def get_paginated_users(self, str_page_number: str, str_page_size: str) -> Page:
        """Retrieve paginated users."""
        queryset = User.objects.order_by("-created_at")
        return self.get_paginated_data(queryset, str_page_number, str_page_size)

    def get_specific_user(self, pk: int) -> Tuple[User, Exception | None]:
        """Retrieve a specific user by its ID."""
        try:
            user = User.objects.get(id=pk)
            return user, None
        except User.DoesNotExist:
            return User(), Exception(self._ERROR_USER_NOT_FOUND.format(pk=pk))
        except Exception as e:
            return User(), e

    @required_context
    def update_specific_user(
        self, pk: int, data: dto.UpdateUserDTO
    ) -> Tuple[User, Exception | None]:
        """Update a specific user by its ID."""
        try:
            user = User.objects.get(id=pk)
            old_instance = copy.deepcopy(user)

            # Validate username availability if username is being changed
            if (
                data.username
                and data.username != user.username
                and not User.available_username(data.username)
            ):
                return user, Exception(self._ERROR_USERNAME_TAKEN)

            # Validate email availability if email is being changed
            if (
                data.email
                and data.email != user.email
                and not User.available_email(data.email)
            ):
                return user, Exception(self._ERROR_EMAIL_TAKEN)

            for key, value in data.to_dict().items():
                if value is not None:
                    setattr(user, key, value)
            user.save()

            self.log_entity_change(
                self.ctx,
                instance=user,
                old_instance=old_instance,
                action=ActionType.UPDATE,
                description=f"User {user.username} updated",
            )
            return user, None
        except User.DoesNotExist:
            return User(), Exception(self._ERROR_USER_NOT_FOUND.format(pk=pk))
        except Exception as e:
            return User(), e

    @required_context
    def delete_specific_user(self, pk: int) -> Exception | None:
        """Delete a specific user by its ID."""
        try:
            user = User.objects.get(id=pk)
            old_instance = copy.deepcopy(user)
            user.delete()

            self.log_entity_change(
                self.ctx,
                instance=old_instance,
                action=ActionType.DELETE,
                description=f"User {old_instance.username} deleted",
            )
            return None
        except User.DoesNotExist:
            return Exception(self._ERROR_USER_NOT_FOUND.format(pk=pk))
        except Exception as e:
            return e

    @required_context
    def toggle_user_status(self, pk: int) -> Tuple[User, Exception | None]:
        """Toggle user active status."""
        try:
            user = User.objects.get(id=pk)
            old_instance = copy.deepcopy(user)

            user.is_active = not user.is_active
            user.save(update_fields=["is_active"])

            self.log_entity_change(
                self.ctx,
                instance=user,
                old_instance=old_instance,
                action=ActionType.UPDATE,
                description=f"User {user.username} status toggled to {'active' if user.is_active else 'inactive'}",
            )
            return user, None
        except User.DoesNotExist:
            return User(), Exception(self._ERROR_USER_NOT_FOUND.format(pk=pk))
        except Exception as e:
            return User(), e

    @required_context
    def change_user_password(
        self, pk: int, data: dto.ChangeUserPasswordDTO
    ) -> Tuple[User, Exception | None]:
        """Change user password by admin."""
        try:
            user = User.objects.get(id=pk)

            # Set new password
            user.set_password(data.new_password)
            user.save(update_fields=["password"])

            params = ActivityLogParams(
                entity=user._entity,
                computed_entity=user._computed_entity,
                entity_id=user.id,
                entity_name=user.username,
                description=f"Admin changed password for user {user.username}",
            )
            self.log_activity(ActionType.UPDATE, params)

            return user, None
        except User.DoesNotExist:
            return User(), Exception(f"User with id '{pk}' does not exist.")
        except Exception as e:
            return User(), e
