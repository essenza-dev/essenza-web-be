from copy import deepcopy
import logging
from typing import Tuple, Optional, Dict

from django.core.paginator import Page
from django.db.models import QuerySet, Q
from django.db import transaction

from core.enums.action_type import ActionType
from core.service import BaseService, required_context
from core.models import ContactMessage
from utils.log.activity_log import ActivityLogParams, GuestInfo

from . import dto

logger = logging.getLogger(__name__)


class ContactMessageService(BaseService):
    """Service class for managing contact messages."""

    @required_context
    def create_contact_message(
        self, data: dto.CreateContactMessageDTO
    ) -> Tuple[ContactMessage, Optional[Exception]]:
        """Create a new contact message with transaction safety.

        Args:
            data: Contact message creation data transfer object

        Returns:
            Tuple containing created ContactMessage instance and optional Exception
        """
        try:
            with transaction.atomic():
                return self._create_contact_message_with_data(data)
        except Exception as e:
            logger.error(f"Error creating contact message: {e}", exc_info=True)
            return ContactMessage(), e

    @required_context
    def _create_contact_message_with_data(
        self, data: dto.CreateContactMessageDTO
    ) -> Tuple[ContactMessage, None]:
        """Create contact message with processed data.

        Args:
            data: Contact message creation data transfer object

        Returns:
            Tuple containing created ContactMessage instance and None
        """
        # Prepare creation data
        create_data = data.to_dict()

        # Create contact message
        contact_message = ContactMessage.objects.create(**create_data)
        self.log_activity(
            ActionType.CREATE,
            params=ActivityLogParams(
                entity=contact_message._entity,
                computed_entity=contact_message._computed_entity,
                entity_id=contact_message.id,
                entity_name=contact_message.subject,
                description=f"Contact message '{contact_message.subject}' created.",
            ),
            guest_info=GuestInfo(name=data.name, email=data.email, phone=data.phone),
        )
        logger.info(
            f"Contact message created successfully with ID: {contact_message.id}"
        )
        return contact_message, None

    def get_contact_messages(
        self, filters: Optional[Dict[str, str | bool]] = None
    ) -> QuerySet[ContactMessage]:
        """Retrieve all contact messages with optional filters and optimized queryset.

        Args:
            filters: Optional dictionary of filter parameters

        Returns:
            QuerySet of filtered ContactMessage instances
        """
        queryset = ContactMessage.objects.order_by("-created_at")

        if not filters:
            return queryset

        # Apply filters efficiently using Q objects when needed
        q_filters = Q()

        if search := filters.get("search"):
            q_filters &= (
                Q(name__icontains=search)
                | Q(email__icontains=search)
                | Q(subject__icontains=search)
                | Q(message__icontains=search)
            )

        if "is_read" in filters:
            q_filters &= Q(is_read=filters["is_read"])

        if name := filters.get("name"):
            q_filters &= Q(name__icontains=name)

        if email := filters.get("email"):
            q_filters &= Q(email__icontains=email)

        if subject := filters.get("subject"):
            q_filters &= Q(subject__icontains=subject)

        return queryset.filter(q_filters) if q_filters else queryset

    def get_paginated_contact_messages(
        self,
        str_page_number: str,
        str_page_size: str,
        filters: Optional[Dict[str, str | bool]] = None,
    ) -> Page:
        """Retrieve paginated contact messages with optimized ordering and filters.

        Args:
            str_page_number: Page number as string
            str_page_size: Page size as string
            filters: Optional dictionary of filter parameters

        Returns:
            Paginated ContactMessage instances
        """
        queryset = self.get_contact_messages(filters)
        return self.get_paginated_data(queryset, str_page_number, str_page_size)

    def get_specific_contact_message(
        self, pk: int
    ) -> Tuple[ContactMessage, Optional[Exception]]:
        """Retrieve a specific contact message by its ID with optimized query.

        Args:
            pk: Contact message primary key

        Returns:
            Tuple containing ContactMessage instance and optional Exception
        """
        try:
            contact_message = ContactMessage.objects.get(id=pk)
            logger.info(f"Contact message retrieved successfully: {contact_message.id}")
            return contact_message, None
        except ContactMessage.DoesNotExist:
            return self._handle_not_found_error(
                f"Contact message with id '{pk}' does not exist."
            )
        except Exception as e:
            logger.error(f"Error retrieving contact message {pk}: {e}", exc_info=True)
            return ContactMessage(), e

    @required_context
    def mark_contact_message_as_read(
        self, pk: int, data: dto.MarkAsReadContactMessageDTO
    ) -> Tuple[ContactMessage, Optional[Exception]]:
        """Mark contact message as read/unread with optimized update.

        Args:
            pk: Contact message primary key
            data: Mark as read data transfer object

        Returns:
            Tuple containing updated ContactMessage instance and optional Exception
        """
        try:
            with transaction.atomic():
                return self._update_contact_message_read_status(pk, data)
        except ContactMessage.DoesNotExist:
            return self._handle_not_found_error(
                f"Contact message with id '{pk}' does not exist."
            )
        except Exception as e:
            logger.error(
                f"Error marking contact message as read {pk}: {e}", exc_info=True
            )
            return ContactMessage(), e

    @required_context
    def _update_contact_message_read_status(
        self, pk: int, data: dto.MarkAsReadContactMessageDTO
    ) -> Tuple[ContactMessage, None]:
        """Update contact message read status efficiently.

        Args:
            pk: Contact message primary key
            data: Mark as read data transfer object

        Returns:
            Tuple containing updated ContactMessage instance and None
        """
        contact_message = ContactMessage.objects.select_for_update().get(id=pk)
        old_instance = deepcopy(contact_message)

        # Update read status efficiently
        contact_message.is_read = data.is_read
        contact_message.save(update_fields=["is_read"])

        self.log_entity_change(
            self.ctx,
            instance=contact_message,
            old_instance=old_instance,
            action=ActionType.UPDATE,
        )
        status = "read" if data.is_read else "unread"
        logger.info(
            f"Contact message marked as {status} successfully: {contact_message.id}"
        )
        return contact_message, None

    @required_context
    def delete_specific_contact_message(self, pk: int) -> Optional[Exception]:
        """Delete a specific contact message by its ID with transaction safety.

        Args:
            pk: Contact message primary key

        Returns:
            Optional Exception if error occurs
        """
        try:
            with transaction.atomic():
                contact_message = ContactMessage.objects.select_for_update().get(id=pk)
                old_instance = deepcopy(contact_message)
                contact_message_id = contact_message.id
                contact_message.delete()
                self.log_entity_change(
                    self.ctx,
                    instance=old_instance,
                    action=ActionType.DELETE,
                )
                logger.info(
                    f"Contact message deleted successfully: {contact_message_id}"
                )
                return None
        except ContactMessage.DoesNotExist:
            error_msg = f"Contact message with id '{pk}' does not exist."
            logger.warning(error_msg)
            return Exception(error_msg)
        except Exception as e:
            logger.error(f"Error deleting contact message {pk}: {e}", exc_info=True)
            return e

    def _handle_not_found_error(self, message: str) -> Tuple[ContactMessage, Exception]:
        """Handle not found errors consistently.

        Args:
            message: Error message

        Returns:
            Tuple containing empty ContactMessage instance and Exception
        """
        logger.warning(message)
        return ContactMessage(), Exception(message)
