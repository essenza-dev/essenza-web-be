from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from core.decorators import validate_body
from utils import api_response
from services import SubscriberService
from docs.api.public import SubscriberPublicAPI

from . import serializers


class SubscriberPublicViewSet(BaseViewSet):
    """Public ViewSet for managing subscribers."""

    _subscriber_service = SubscriberService()

    @SubscriberPublicAPI.create_subscriber_schema
    @validate_body(serializers.PostCreateSubscriberSerializer)
    def create_subscriber(self, request: Request, validated_data: dict) -> Response:
        """Create a new subscriber."""
        subscriber, error = self._subscriber_service.create_subscriber(
            email=validated_data.get("email", "")
        )
        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Subscriber created successfully.",
            data=serializers.SubscriberModelSerializer(subscriber).data,
        )
