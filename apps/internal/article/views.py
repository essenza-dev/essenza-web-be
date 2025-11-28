"""
Article API ViewSet
Handles all article-related API endpoints with proper error handling and validation
"""

import logging
from typing import Dict, Any
from rest_framework.request import Request
from rest_framework.response import Response

from core.views import BaseViewSet
from core.decorators import jwt_required, validate_body
from utils import api_response
from services import ArticleService
from services.article import dto
from docs.api.internal import ArticleAPI

from . import serializers

logger = logging.getLogger(__name__)


class ArticleViewSet(BaseViewSet):
    """ViewSet for managing articles."""

    _article_service = ArticleService()

    @ArticleAPI.create_article_schema
    @jwt_required
    @validate_body(serializers.PostCreateArticleRequest)
    def create_article(
        self, request: Request, validated_data: Dict[str, Any]
    ) -> Response:
        """Create a new article."""
        try:
            article, error = self._article_service.create_article(
                data=dto.CreateArticleDTO(**validated_data), user=request.user
            )
            if error:
                return api_response(request).error(message=str(error))

            return api_response(request).success(
                data=serializers.ArticleModelSerializer(article).data,
                message="Article created successfully.",
            )
        except Exception as e:
            logger.error(f"Unexpected error creating article: {e}")
            return api_response(request).error(message="Failed to create article.")

    @ArticleAPI.get_articles_schema
    @jwt_required
    def get_articles(self, request: Request) -> Response:
        """Retrieve all articles with optional filters and pagination."""
        try:
            # Extract query parameters
            page_number = request.GET.get("page", "1")
            page_size = request.GET.get("page_size", "20")

            # Extract filters
            filters = {}
            if tags := request.GET.get("tags"):
                filters["tags"] = tags
            if author := request.GET.get("author"):
                filters["author"] = author
            if search := request.GET.get("search"):
                filters["search"] = search
            if is_active := request.GET.get("is_active"):
                filters["is_active"] = is_active.lower() == "true"

            page = self._article_service.get_paginated_articles(
                str_page_number=page_number,
                str_page_size=page_size,
                filters=filters or None,
            )

            return api_response(request).paginated(
                message="Articles retrieved successfully.",
                data=serializers.ArticleModelSerializer(page, many=True).data,
                page=page,
            )
        except Exception as e:
            logger.error(f"Unexpected error retrieving articles: {e}")
            return api_response(request).error(message="Failed to retrieve articles.")

    @ArticleAPI.get_specific_article_schema
    @jwt_required
    def get_specific_article(self, request: Request, pk: int) -> Response:
        """Retrieve a specific article by its ID."""
        try:
            article, error = self._article_service.get_specific_article(pk=pk)
            if error:
                return api_response(request).error(message=str(error))

            return api_response(request).success(
                message="Article retrieved successfully.",
                data=serializers.ArticleModelSerializer(article).data,
            )
        except Exception as e:
            logger.error(f"Unexpected error retrieving article {pk}: {e}")
            return api_response(request).error(message="Failed to retrieve article.")

    @ArticleAPI.get_article_by_slug_schema
    @jwt_required
    def get_article_by_slug(self, request: Request, slug: str) -> Response:
        """Retrieve an article by its slug."""
        try:
            article, error = self._article_service.get_article_by_slug(slug=slug)
            if error:
                return api_response(request).error(message=str(error))

            return api_response(request).success(
                message="Article retrieved successfully.",
                data=serializers.ArticleModelSerializer(article).data,
            )
        except Exception as e:
            logger.error(f"Unexpected error retrieving article by slug {slug}: {e}")
            return api_response(request).error(message="Failed to retrieve article.")

    @ArticleAPI.update_specific_article_schema
    @jwt_required
    @validate_body(serializers.PutUpdateArticleRequest)
    def update_specific_article(
        self, request: Request, pk: int, validated_data: Dict[str, Any]
    ) -> Response:
        """Update a specific article by its ID."""
        try:
            article, error = self._article_service.update_specific_article(
                pk=pk, data=dto.UpdateArticleDTO(**validated_data)
            )
            if error:
                return api_response(request).error(message=str(error))

            return api_response(request).success(
                message="Article updated successfully.",
                data=serializers.ArticleModelSerializer(article).data,
            )
        except Exception as e:
            logger.error(f"Unexpected error updating article {pk}: {e}")
            return api_response(request).error(message="Failed to update article.")

    @ArticleAPI.delete_specific_article_schema
    @jwt_required
    def delete_specific_article(self, request: Request, pk: int) -> Response:
        """Delete a specific article by its ID."""
        try:
            error = self._article_service.delete_specific_article(pk=pk)
            if error:
                return api_response(request).error(message=str(error))

            return api_response(request).success(
                message="Article deleted successfully."
            )
        except Exception as e:
            logger.error(f"Unexpected error deleting article {pk}: {e}")
            return api_response(request).error(message="Failed to delete article.")

    @ArticleAPI.toggle_article_status_schema
    @jwt_required
    @validate_body(serializers.PatchToggleArticleStatusRequest)
    def toggle_article_status(
        self, request: Request, pk: int, validated_data: Dict[str, Any]
    ) -> Response:
        """Toggle article active status."""
        try:
            article, error = self._article_service.toggle_article_status(
                pk=pk, data=dto.ToggleArticleStatusDTO(**validated_data)
            )
            if error:
                return api_response(request).error(message=str(error))

            return api_response(request).success(
                message="Article status updated successfully.",
                data=serializers.ArticleModelSerializer(article).data,
            )
        except Exception as e:
            logger.error(f"Unexpected error toggling article status {pk}: {e}")
            return api_response(request).error(
                message="Failed to update article status."
            )

    @ArticleAPI.publish_article_schema
    @jwt_required
    @validate_body(serializers.PatchPublishArticleRequest)
    def publish_article(
        self, request: Request, pk: int, validated_data: Dict[str, Any]
    ) -> Response:
        """Publish or unpublish an article."""
        try:
            # Handle default behavior - if no published_at provided, use current time
            if "published_at" not in validated_data:
                from django.utils import timezone

                validated_data["published_at"] = timezone.now()

            article, error = self._article_service.publish_article(
                pk=pk, data=dto.PublishArticleDTO(**validated_data)
            )
            if error:
                return api_response(request).error(message=str(error))

            status = "published" if article.published_at else "unpublished"
            return api_response(request).success(
                message=f"Article {status} successfully.",
                data=serializers.ArticleModelSerializer(article).data,
            )
        except Exception as e:
            logger.error(f"Unexpected error publishing/unpublishing article {pk}: {e}")
            return api_response(request).error(
                message="Failed to publish/unpublish article."
            )

    @ArticleAPI.upload_thumbnail_schema
    @jwt_required
    def upload_thumbnail(self, request: Request, pk: int) -> Response:
        """Upload thumbnail for a specific article."""
        try:
            files = getattr(request, "FILES", None)
            if not files or "thumbnail" not in files:
                return api_response(request).error(
                    message="No thumbnail file provided."
                )

            thumbnail_file = files["thumbnail"]

            # Validate file type
            allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
            content_type = getattr(thumbnail_file, "content_type", None)
            if content_type and content_type not in allowed_types:
                return api_response(request).error(
                    message="Invalid file type. Only JPEG, PNG, JPG, and WebP images are allowed."
                )

            # Validate file size (5MB limit)
            max_size = 5 * 1024 * 1024  # 5MB
            file_size = getattr(thumbnail_file, "size", 0)
            if file_size > max_size:
                return api_response(request).error(
                    message="File size too large. Maximum size is 5MB."
                )

            article, error = self._article_service.upload_thumbnail(
                pk=pk, thumbnail_file=thumbnail_file
            )
            if error:
                return api_response(request).error(message=str(error))

            return api_response(request).success(
                message="Thumbnail uploaded successfully.",
                data=serializers.ArticleModelSerializer(article).data,
            )
        except Exception as e:
            logger.error(f"Unexpected error uploading thumbnail for article {pk}: {e}")
            return api_response(request).error(message="Failed to upload thumbnail.")
