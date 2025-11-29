"""
Contact Message ViewSet
Contains all view logic for contact message-related API endpoints
"""

import logging
from typing import Dict, Any
from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from core.decorators import jwt_required, validate_body
from utils import api_response
from services import ContactMessageService
from services.contact_message import dto
from docs.api.internal import ContactMessageAPI

from . import serializers

logger = logging.getLogger(__name__)


class ContactMessageViewSet(BaseViewSet):
    """ViewSet for managing contact messages."""

    _contact_message_service = ContactMessageService()

    @ContactMessageAPI.get_all_contact_messages_schema
    @jwt_required
    def get_all_contact_messages(self, request: Request) -> Response:
        """Retrieve all contact messages with optional filters and pagination."""
        try:
            page_number = request.GET.get("page", "1")
            page_size = request.GET.get("page_size", "20")

            # Build filters from query parameters
            filters: Dict[str, str | bool] = {}

            if search := request.GET.get("search"):
                filters["search"] = search

            if is_read := request.GET.get("is_read"):
                # Convert string to boolean
                filters["is_read"] = is_read.lower() in ("true", "1", "yes")

            if name := request.GET.get("name"):
                filters["name"] = name

            if email := request.GET.get("email"):
                filters["email"] = email

            if subject := request.GET.get("subject"):
                filters["subject"] = subject

            logger.info(f"Retrieving contact messages with filters: {filters}")

            page = self._contact_message_service.get_paginated_contact_messages(
                str_page_number=page_number,
                str_page_size=page_size,
                filters=filters or None,
            )

            return api_response(request).paginated(
                message="Contact messages retrieved successfully.",
                data=serializers.ContactMessageModelSerializer(page, many=True).data,
                page=page,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in get_all_contact_messages: {str(e)}", exc_info=True
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while retrieving contact messages."
            )

    @ContactMessageAPI.get_specific_contact_message_schema
    @jwt_required
    def get_specific_contact_message(self, request: Request, pk: int) -> Response:
        """Retrieve a specific contact message by its ID."""
        try:
            logger.info(f"Retrieving contact message with ID: {pk}")

            contact_message, error = (
                self._contact_message_service.get_specific_contact_message(pk=pk)
            )
            if error:
                logger.warning(f"Contact message not found: {str(error)}")
                return api_response(request).error(message=str(error))

            return api_response(request).success(
                message="Contact message retrieved successfully.",
                data=serializers.ContactMessageModelSerializer(contact_message).data,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in get_specific_contact_message: {str(e)}",
                exc_info=True,
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while retrieving the contact message."
            )

    @ContactMessageAPI.mark_contact_message_as_read_schema
    @jwt_required
    @validate_body(serializers.PostMarkAsReadContactMessageSerializer)
    def mark_contact_message_as_read(
        self, request: Request, pk: int, validated_data: Dict[str, Any]
    ) -> Response:
        """Mark contact message as read/unread."""
        try:
            logger.info(
                f"Marking contact message {pk} as read: {validated_data.get('is_read')}"
            )

            mark_as_read_dto = dto.MarkAsReadContactMessageDTO(
                is_read=validated_data.get("is_read", False)
            )

            contact_message, error = (
                self._contact_message_service.mark_contact_message_as_read(
                    pk=pk, data=mark_as_read_dto
                )
            )
            if error:
                logger.warning(f"Failed to mark contact message as read: {str(error)}")
                return api_response(request).error(message=str(error))

            status_text = "read" if mark_as_read_dto.is_read else "unread"
            return api_response(request).success(
                message=f"Contact message marked as {status_text} successfully.",
                data=serializers.ContactMessageModelSerializer(contact_message).data,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in mark_contact_message_as_read: {str(e)}",
                exc_info=True,
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while updating the contact message."
            )

    @ContactMessageAPI.delete_contact_message_schema
    @jwt_required
    def delete_contact_message(self, request: Request, pk: int) -> Response:
        """Delete a specific contact message by its ID."""
        try:
            logger.info(f"Deleting contact message with ID: {pk}")

            if error := self._contact_message_service.delete_specific_contact_message(
                pk=pk
            ):
                logger.warning(f"Failed to delete contact message: {str(error)}")
                return api_response(request).error(message=str(error))

            return api_response(request).success(
                message="Contact message deleted successfully."
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in delete_contact_message: {str(e)}", exc_info=True
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while deleting the contact message."
            )
