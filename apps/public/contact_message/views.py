"""
Public Contact Message ViewSet
Contains view logic for public contact message submission
"""

import logging
from typing import Dict, Any
from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from core.decorators import validate_body
from utils import api_response
from services.contact_message import ContactMessageService
from services.contact_message import dto
from docs.api.public import ContactMessagePublicAPI

from . import serializers

logger = logging.getLogger(__name__)


class ContactMessagePublicViewSet(BaseViewSet):
    """Public ViewSet for managing contact message submissions."""

    _contact_message_service = ContactMessageService()

    @ContactMessagePublicAPI.create_contact_message_schema
    @validate_body(serializers.PostCreateContactMessageSerializer)
    def create_contact_message(
        self, request: Request, validated_data: Dict[str, Any]
    ) -> Response:
        """Create a new contact message from public form submission."""
        try:
            logger.info(
                f"Creating contact message from: {validated_data.get('email', 'Unknown')}"
            )

            create_contact_message_dto = dto.CreateContactMessageDTO(
                name=validated_data.get("name", ""),
                email=validated_data.get("email", ""),
                subject=validated_data.get("subject", ""),
                message=validated_data.get("message", ""),
                phone=validated_data.get("phone", "") or None,
            )

            contact_message, error = self._contact_message_service.use_context(
                request
            ).create_contact_message(data=create_contact_message_dto)
            if error:
                logger.warning(f"Failed to create contact message: {str(error)}")
                return api_response(request).error(message=str(error))

            return api_response(request).success(
                message="Contact message submitted successfully.",
                data=serializers.ContactMessageModelSerializer(contact_message).data,
            )
        except Exception as e:
            logger.error(
                f"Unexpected error in create_contact_message: {str(e)}", exc_info=True
            )
            return api_response(request).server_error(
                message="An unexpected error occurred while submitting the contact message."
            )
