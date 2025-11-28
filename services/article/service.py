import logging
from typing import Tuple, Optional, Dict

from django.core.files.uploadedfile import UploadedFile
from django.core.paginator import Page
from django.db.models import QuerySet, Q
from django.utils.text import slugify
from django.utils import timezone
from django.db import IntegrityError, transaction

from core.service import BaseService
from core.models import Article, User

from . import dto

logger = logging.getLogger(__name__)


class ArticleService(BaseService):
    """Service class for managing articles."""

    def create_article(
        self, data: dto.CreateArticleDTO, user: Optional[User] = None
    ) -> Tuple[Article, Optional[Exception]]:
        """Create a new article with optimized slug generation and transaction safety.

        Args:
            data: Article creation data transfer object
            user: User object for auto-setting author if not provided

        Returns:
            Tuple containing created Article instance and optional Exception
        """
        try:
            with transaction.atomic():
                return self._create_article_with_data(data, user)
        except IntegrityError as e:
            return self._handle_integrity_error(e, data.slug, Article())
        except Exception as e:
            logger.error(f"Error creating article: {e}")
            return Article(), e

    def _create_article_with_data(
        self, data: dto.CreateArticleDTO, user: Optional[User]
    ) -> Tuple[Article, None]:
        """Create article with processed data and handle thumbnail upload.

        Args:
            data: Article creation data transfer object
            user: User object for auto-setting author

        Returns:
            Tuple containing created Article instance and None
        """
        # Optimize slug generation
        data.slug = self._generate_slug(data.slug, data.title)

        # Auto-set author from user if not provided
        if not data.author and user:
            data.author = user.name

        # Prepare creation data
        thumbnail_file = data.thumbnail
        create_data = {
            k: v for k, v in data.to_dict().items() if k not in ["thumbnail", "user"]
        }

        # Set published_at based on active status
        create_data["published_at"] = timezone.now() if data.is_active else None

        # Create article
        article = Article.objects.create(**create_data)

        # Handle thumbnail upload efficiently
        if thumbnail_file:
            self._save_thumbnail(article, thumbnail_file)

        logger.info(f"Article created successfully with ID: {article.id}")
        return article, None

    def _save_thumbnail(self, article: Article, thumbnail_file: UploadedFile) -> None:
        """Efficiently save thumbnail to article.

        Args:
            article: Article instance to update
            thumbnail_file: Uploaded thumbnail file
        """
        article.thumbnail.save(thumbnail_file.name, thumbnail_file, save=False)
        article.save(update_fields=["thumbnail"])

    def get_articles(
        self, filters: Optional[Dict[str, str | bool]] = None
    ) -> QuerySet[Article]:
        """Retrieve all articles with optional filters and optimized queryset.

        Args:
            filters: Optional dictionary of filter parameters

        Returns:
            QuerySet of filtered Article instances
        """
        queryset = Article.objects.select_related().order_by("-created_at")

        if not filters:
            return queryset

        # Apply filters efficiently using Q objects when needed
        q_filters = Q()

        if tags := filters.get("tags"):
            q_filters &= Q(tags__icontains=tags)

        if author := filters.get("author"):
            q_filters &= Q(author__icontains=author)

        if search := filters.get("search"):
            q_filters &= Q(title__icontains=search) | Q(content__icontains=search)

        if "is_active" in filters:
            q_filters &= Q(is_active=filters["is_active"])

        return queryset.filter(q_filters) if q_filters else queryset

    def get_paginated_articles(
        self,
        str_page_number: str,
        str_page_size: str,
        filters: Optional[Dict[str, str | bool]] = None,
    ) -> Page:
        """Retrieve paginated articles with optimized ordering and filters.

        Args:
            str_page_number: Page number as string
            str_page_size: Page size as string
            filters: Optional dictionary of filter parameters

        Returns:
            Paginated Article instances
        """
        queryset = self.get_articles(filters)
        return self.get_paginated_data(queryset, str_page_number, str_page_size)

    def get_specific_article(self, pk: int) -> Tuple[Article, Optional[Exception]]:
        """Retrieve a specific article by its ID with optimized query."""
        try:
            article = Article.objects.select_related().get(id=pk)
            logger.info(f"Article retrieved successfully: {article.id}")
            return article, None
        except Article.DoesNotExist:
            return self._handle_not_found_error(
                f"Article with id '{pk}' does not exist."
            )
        except Exception as e:
            logger.error(f"Error retrieving article {pk}: {e}")
            return Article(), e

    def get_article_by_slug(self, slug: str) -> Tuple[Article, Optional[Exception]]:
        """Retrieve an article by its slug with optimized query."""
        try:
            article = Article.objects.select_related().get(slug=slug)
            logger.info(f"Article retrieved successfully by slug: {slug}")
            return article, None
        except Article.DoesNotExist:
            return self._handle_not_found_error(
                f"Article with slug '{slug}' does not exist."
            )
        except Exception as e:
            logger.error(f"Error retrieving article by slug {slug}: {e}")
            return Article(), e

    def update_specific_article(
        self, pk: int, data: dto.UpdateArticleDTO
    ) -> Tuple[Article, Optional[Exception]]:
        """Update a specific article by its ID with optimized transaction handling."""
        try:
            return self._update_article_data(pk, data)
        except Article.DoesNotExist:
            return self._handle_not_found_error(
                f"Article with id '{pk}' does not exist."
            )
        except IntegrityError as e:
            return self._handle_integrity_error(e, data.slug, Article())
        except Exception as e:
            logger.error(f"Error updating article {pk}: {e}")
            return Article(), e

    def delete_specific_article(self, pk: int) -> Optional[Exception]:
        """Delete a specific article by its ID with transaction safety."""
        try:
            with transaction.atomic():
                article = Article.objects.select_for_update().get(id=pk)
                article_id = article.id
                article.delete()
                logger.info(f"Article deleted successfully: {article_id}")
                return None
        except Article.DoesNotExist:
            error_msg = f"Article with id '{pk}' does not exist."
            logger.warning(error_msg)
            return Exception(error_msg)
        except Exception as e:
            logger.error(f"Error deleting article {pk}: {e}")
            return e

    def toggle_article_status(
        self, pk: int, data: dto.ToggleArticleStatusDTO
    ) -> Tuple[Article, Optional[Exception]]:
        """Toggle article active status with optimized update."""
        try:
            with transaction.atomic():
                return self._update_article_status(pk, data)
        except Article.DoesNotExist:
            return self._handle_not_found_error(
                f"Article with id '{pk}' does not exist."
            )
        except Exception as e:
            logger.error(f"Error toggling article status {pk}: {e}")
            return Article(), e

    def _update_article_status(
        self, pk: int, data: dto.ToggleArticleStatusDTO
    ) -> Tuple[Article, None]:
        """Update article active status and manage publication status accordingly.

        Args:
            pk: Article primary key
            data: Toggle status data transfer object

        Returns:
            Tuple containing updated Article instance and None
        """
        article = Article.objects.select_for_update().get(id=pk)

        # Update status and publication date efficiently
        article.is_active = data.is_active

        # Handle published_at based on active status
        if data.is_active and not article.published_at:
            article.published_at = timezone.now()
        elif not data.is_active:
            article.published_at = None
        # If data.is_active is True and article.published_at exists, keep current value

        article.save(update_fields=["is_active", "published_at"])
        logger.info(
            f"Article status toggled successfully: {article.id} -> {data.is_active}"
        )
        return article, None

    def publish_article(
        self, pk: int, data: dto.PublishArticleDTO
    ) -> Tuple[Article, Optional[Exception]]:
        """Publish or unpublish an article with optimized update."""
        try:
            with transaction.atomic():
                return self._update_article_publication(pk, data)
        except Article.DoesNotExist:
            return self._handle_not_found_error(
                f"Article with id '{pk}' does not exist."
            )
        except Exception as e:
            logger.error(f"Error publishing/unpublishing article {pk}: {e}")
            return Article(), e

    def _update_article_publication(
        self, pk: int, data: dto.PublishArticleDTO
    ) -> Tuple[Article, None]:
        """Update article publication status with provided datetime."""
        article = Article.objects.select_for_update().get(id=pk)

        # Set published_at - use provided datetime or None to unpublish
        article.published_at = data.published_at
        article.save(update_fields=["published_at"])
        status = "published" if article.published_at else "unpublished"
        logger.info(f"Article {status} successfully: {article.id}")
        return article, None

    def upload_thumbnail(
        self, pk: int, thumbnail_file
    ) -> Tuple[Article, Optional[Exception]]:
        """Upload thumbnail for a specific article."""
        try:
            with transaction.atomic():
                return self._update_article_thumbnail(pk, thumbnail_file)
        except Article.DoesNotExist:
            return self._handle_not_found_error(
                f"Article with id '{pk}' does not exist."
            )
        except Exception as e:
            logger.error(f"Error uploading thumbnail for article {pk}: {e}")
            return Article(), e

    def _update_article_thumbnail(
        self, pk: int, thumbnail_file: UploadedFile
    ) -> Tuple[Article, None]:
        """Update article thumbnail, replacing existing one if present.

        Args:
            pk: Article primary key
            thumbnail_file: New thumbnail file to upload

        Returns:
            Tuple containing updated Article instance and None
        """
        article = Article.objects.select_for_update().get(id=pk)

        # Clean up old thumbnail safely
        self._delete_old_thumbnail(article)

        # Set new thumbnail using proper FileField method
        article.thumbnail.save(thumbnail_file.name, thumbnail_file, save=True)
        logger.info(f"Thumbnail uploaded successfully for article: {article.id}")
        return article, None

    def _delete_old_thumbnail(self, article: Article) -> None:
        """Safely delete old thumbnail if it exists.

        Args:
            article: Article instance with potential existing thumbnail
        """
        if article.thumbnail:
            try:
                article.thumbnail.delete(save=False)
            except Exception as e:
                logger.warning(f"Could not delete old thumbnail: {e}")

    def _generate_slug(self, slug: Optional[str], title: str) -> str:
        """Generate optimized slug from input or title."""
        return slugify(title) if not slug or not slug.strip() else slugify(slug)

    def _handle_integrity_error(
        self, error: IntegrityError, slug: Optional[str], empty_model: Article
    ) -> Tuple[Article, Exception]:
        """Handle database integrity errors with appropriate messaging."""
        if "slug" in str(error):
            error_msg = f"An article with slug '{slug}' already exists."
            logger.warning(error_msg)
            return empty_model, Exception(error_msg)
        logger.error(f"Database integrity error: {error}")
        return empty_model, error

    def _handle_not_found_error(self, message: str) -> Tuple[Article, Exception]:
        """Handle not found errors consistently."""
        logger.warning(message)
        return Article(), Exception(message)

    def _handle_slug_update(self, data: dto.UpdateArticleDTO, article: Article) -> None:
        """Handle slug update with optimized auto-generation logic."""
        if data.slug is not None:
            if data.slug.strip() == "":
                # Generate from updated title or existing article title
                source_title = data.title if data.title is not None else article.title
                data.slug = slugify(source_title)
            else:
                data.slug = slugify(data.slug)

    def _update_article_data(
        self, pk: int, data: dto.UpdateArticleDTO
    ) -> Tuple[Article, None]:
        """Update article data with optimized field updates and transaction safety.

        Args:
            pk: Article primary key
            data: Update data transfer object

        Returns:
            Tuple containing updated Article instance and None
        """
        with transaction.atomic():
            article = Article.objects.select_for_update().get(id=pk)

            # Handle slug update with auto-generation
            self._handle_slug_update(data, article)

            # Handle published_at based on is_active status
            self._handle_publication_status_update(data, article)

            # Prepare update data efficiently
            thumbnail_file = data.thumbnail
            if update_data := {
                k: v
                for k, v in data.to_dict().items()
                if v is not None and k != "thumbnail"
            }:
                for key, value in update_data.items():
                    setattr(article, key, value)
                article.save(update_fields=list(update_data.keys()))

            # Handle thumbnail update efficiently
            if thumbnail_file:
                self._delete_old_thumbnail(article)
                self._save_thumbnail(article, thumbnail_file)

            logger.info(f"Article updated successfully: {article.id}")
            return article, None

    def _handle_publication_status_update(
        self, data: dto.UpdateArticleDTO, article: Article
    ) -> None:
        """Handle published_at field based on is_active status during update.

        Args:
            data: Update data transfer object
            article: Article instance being updated
        """
        if data.is_active is not None:
            if data.is_active and not article.published_at:
                data.published_at = timezone.now()
            elif not data.is_active:
                data.published_at = None
