from typing import Any, Dict
from rest_framework.request import Request
from rest_framework.response import Response

from core.decorators.authentication import jwt_required
from core.decorators.validation import validate_body
from core.views import BaseViewSet
from services import SocialMediaService
from utils.response import api_response
from docs.api.internal import SocialMediaAPI

from . import serializers


class SocialMediaViewSet(BaseViewSet):
    """
    ViewSet for managing social media integrations and settings
    """

    _social_media_service = SocialMediaService()

    @SocialMediaAPI.fetch_social_media
    @jwt_required
    def fetch_social_media(self, request: Request) -> Response:
        """
        Fetch social media data or settings with pagination
        """
        page_number = request.GET.get("page", "1")
        page_size = request.GET.get("page_size", "20")

        page = self._social_media_service.get_social_media_list(
            str_page_number=page_number, str_page_size=page_size
        )

        return api_response(request).paginated(
            data=serializers.SocialMediaModelSerializer(
                page.object_list, many=True
            ).data,
            page=page,
            message="Social media data fetched successfully",
        )

    @SocialMediaAPI.create_social_media
    @jwt_required
    @validate_body(serializers.PostCreateSocialMediaRequest)
    def create_social_media(
        self, request: Request, validated_data: Dict[str, Any]
    ) -> Response:
        """
        Create or update social media data or settings
        """
        socmed = self._social_media_service.create_social_media(**validated_data)

        return api_response(request).created(
            data=serializers.SocialMediaModelSerializer(socmed).data,
            message="Social media data created successfully",
        )

    @SocialMediaAPI.specific_social_media
    @jwt_required
    def specific_social_media(self, request: Request, pk: int) -> Response:
        """
        Retrieve a specific social media entry by its primary key
        """
        socmed, error = self._social_media_service.get_social_media_by_id(pk)

        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            data=serializers.SocialMediaModelSerializer(socmed).data,
            message="Social media data retrieved successfully",
        )

    @SocialMediaAPI.update_social_media
    @jwt_required
    @validate_body(serializers.PatchUpdateSocialMediaRequest)
    def update_social_media(
        self, request: Request, validated_data: Dict[str, Any], pk: int
    ) -> Response:
        """
        Update social media data or settings
        """
        socmed, error = self._social_media_service.update_social_media(
            pk, **validated_data
        )

        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            data=serializers.SocialMediaModelSerializer(socmed).data,
            message="Social media data updated successfully",
        )

    @SocialMediaAPI.delete_social_media
    @jwt_required
    def delete_social_media(self, request: Request, pk: int) -> Response:
        """
        Delete a specific social media entry by its primary key
        """
        error = self._social_media_service.delete_social_media(pk)

        if error:
            return api_response(request).error(message=str(error))

        return api_response(request).success(
            message="Social media data deleted successfully",
        )
