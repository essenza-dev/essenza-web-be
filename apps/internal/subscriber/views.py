from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from core.decorators import jwt_required
from services import SubscriberService
from utils import api_response
from docs.api.internal import SubscriberAPI

from . import serializers


class SubscriberViewSet(BaseViewSet):
    """ViewSet for managing subscribers."""

    _subscriber_service = SubscriberService()

    @SubscriberAPI.get_all_subscribers_schema
    @jwt_required
    def get_all_subscribers(self, request: Request) -> Response:
        """Retrieve all subscribers."""
        page_number = request.GET.get("page", "1")
        page_size = request.GET.get("page_size", "20")

        page = self._subscriber_service.get_paginated_subscribers(
            str_page_number=page_number, str_page_size=page_size
        )
        return api_response(request).paginated(
            message="Subscribers retrieved successfully.",
            data=serializers.SubscriberModelSerializer(page, many=True).data,
            page=page,
        )

    @SubscriberAPI.get_specific_subscriber_schema
    @jwt_required
    def get_specific_subscriber(self, request: Request, pk: int) -> Response:
        """Retrieve a specific subscriber by its ID."""
        subscriber, error = self._subscriber_service.get_specific_subscriber(pk=pk)
        if error:
            return api_response(request).error(message=str(error))
        return api_response(request).success(
            message="Subscriber retrieved successfully.",
            data=serializers.SubscriberModelSerializer(subscriber).data,
        )

    @SubscriberAPI.delete_subscriber_schema
    @jwt_required
    def delete_subscriber(self, request: Request, pk: int) -> Response:
        """Delete a specific subscriber by its ID."""
        error = self._subscriber_service.delete_specific_subscriber(pk=pk)
        if error:
            return api_response(request).error(message=str(error))
        return api_response(request).success(message="Subscriber deleted successfully.")
