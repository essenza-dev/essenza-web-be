"""
Project Service Module
Handles all business logic for project management operations.
"""

import logging
import os
from typing import Tuple, List, Optional, Sequence
from django.db.models.query import QuerySet
from django.db.models import Q
from django.core.paginator import Page
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.exceptions import ValidationError

from core.service import BaseService
from core.models import Project
from . import dto

logger = logging.getLogger(__name__)


class ProjectService(BaseService):
    """Service class for managing project operations with comprehensive CRUD functionality."""

    def validate_slug_uniqueness(
        self, slug: str, exclude_id: Optional[int] = None
    ) -> bool:
        """
        Validate if slug is unique.

        Args:
            slug: The slug to validate
            exclude_id: Project ID to exclude from validation (for updates)

        Returns:
            True if slug is unique, False otherwise
        """
        queryset = Project.objects.filter(slug=slug)
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return not queryset.exists()

    def create_project(
        self, data: dto.CreateProjectDTO
    ) -> Tuple[Project, Optional[Exception]]:
        """
        Create a new project with image and gallery handling.

        Args:
            data: Project creation data transfer object

        Returns:
            Tuple containing the created project and any error that occurred
        """
        try:
            # Validate slug uniqueness
            if data.slug and not self.validate_slug_uniqueness(data.slug):
                return Project(), ValidationError(
                    "Project with this slug already exists."
                )

            project_data = data.to_dict()

            # Process main image upload
            if isinstance(data.image, InMemoryUploadedFile):
                project_data["image"] = data.image

            # Process gallery images upload
            if data.gallery:
                project_data["gallery"] = self._process_gallery_images(
                    data.gallery, data.slug
                )

            project = Project.objects.create(**project_data)
            logger.info(f"Project created successfully with id {project.id}")
            return project, None

        except Exception as e:
            logger.error(f"Error creating project: {str(e)}", exc_info=True)
            return Project(), e

    def get_projects(
        self, filters: Optional[dto.ProjectFilterDTO] = None
    ) -> QuerySet[Project]:
        """
        Retrieve all projects with optional filtering and optimized queries.

        Args:
            filters: Optional filter criteria for project search

        Returns:
            QuerySet of filtered and ordered projects
        """
        queryset = Project.objects.all()

        if filters:
            filter_conditions = Q()

            if filters.search:
                search_q = (
                    Q(title__icontains=filters.search)
                    | Q(description__icontains=filters.search)
                    | Q(location__icontains=filters.search)
                )
                filter_conditions &= search_q
            if filters.is_active is not None:
                filter_conditions &= Q(is_active=filters.is_active)

            queryset = queryset.filter(filter_conditions)

        return queryset.order_by("-created_at")

    def get_paginated_projects(
        self,
        str_page_number: str,
        str_page_size: str,
        filters: Optional[dto.ProjectFilterDTO] = None,
    ) -> Page:
        """
        Retrieve paginated projects with optional filtering.

        Args:
            str_page_number: Page number as string
            str_page_size: Page size as string
            filters: Optional filter criteria for project search

        Returns:
            Page object containing filtered and paginated projects
        """
        queryset = self.get_projects(filters)
        return self.get_paginated_data(queryset, str_page_number, str_page_size)

    def get_specific_project(self, pk: int) -> Tuple[Project, Optional[Exception]]:
        """
        Retrieve a specific project by its ID.

        Args:
            pk: Project ID to retrieve

        Returns:
            Tuple containing the project and any error that occurred
        """
        try:
            project = Project.objects.get(id=pk)
            return project, None
        except Project.DoesNotExist:
            return self._handle_project_not_found_by_id(pk)
        except Exception as e:
            logger.error(f"Error retrieving project {pk}: {str(e)}", exc_info=True)
            return Project(), e

    def get_project_by_slug(self, slug: str) -> Tuple[Project, Optional[Exception]]:
        """
        Retrieve a project by its unique slug identifier.

        Args:
            slug: Project slug to search for

        Returns:
            Tuple containing the project and any error that occurred
        """
        try:
            project = Project.objects.get(slug=slug)
            return project, None
        except Project.DoesNotExist:
            return self._handle_project_not_found_by_slug(slug)
        except Exception as e:
            logger.error(
                f"Error retrieving project by slug '{slug}': {str(e)}", exc_info=True
            )
            return Project(), e

    def update_specific_project(
        self, pk: int, data: dto.UpdateProjectDTO
    ) -> Tuple[Project, Optional[Exception]]:
        """
        Update a specific project with comprehensive data handling.

        Args:
            pk: Project ID to update
            data: Project update data transfer object

        Returns:
            Tuple containing the updated project and any error that occurred
        """
        try:
            return self._update_project_with_data_handling(pk, data)
        except Project.DoesNotExist:
            return self._handle_project_not_found_by_id(pk)
        except Exception as e:
            logger.error(f"Error updating project {pk}: {str(e)}", exc_info=True)
            return Project(), e

    def delete_specific_project(self, pk: int) -> Optional[Exception]:
        """
        Delete a specific project and its associated files.

        Args:
            pk: Project ID to delete

        Returns:
            Exception if error occurs, None if successful
        """
        try:
            return self._delete_project_with_cleanup(pk)
        except Project.DoesNotExist:
            error_msg = f"Project with id '{pk}' does not exist."
            logger.warning(error_msg)
            return ValidationError(error_msg)
        except Exception as e:
            logger.error(f"Error deleting project {pk}: {str(e)}", exc_info=True)
            return e

    def toggle_project_status(
        self, pk: int, data: dto.ToggleProjectStatusDTO
    ) -> Tuple[Project, Optional[Exception]]:
        """
        Toggle project active status efficiently.

        Args:
            pk: Project ID to update
            data: Status toggle data transfer object

        Returns:
            Tuple containing the updated project and any error that occurred
        """
        try:
            return self._toggle_project_status_with_logging(pk, data)
        except Project.DoesNotExist:
            return self._handle_project_not_found_by_id(pk)
        except Exception as e:
            logger.error(f"Error toggling project {pk} status: {str(e)}", exc_info=True)
            return Project(), e

    def update_project_image(
        self, pk: int, data: dto.UpdateProjectImageDTO
    ) -> Tuple[Project, Optional[Exception]]:
        """
        Update project main image with automatic cleanup.

        Args:
            pk: Project ID to update
            data: Image update data transfer object

        Returns:
            Tuple containing the updated project and any error that occurred
        """
        try:
            return self._update_project_image_with_cleanup(pk, data)
        except Project.DoesNotExist:
            return self._handle_project_not_found_by_id(pk)
        except Exception as e:
            logger.error(f"Error updating project {pk} image: {str(e)}", exc_info=True)
            return Project(), e

    def update_project_gallery(
        self, pk: int, data: dto.UpdateProjectGalleryDTO
    ) -> Tuple[Project, Optional[Exception]]:
        """
        Update project gallery images with automatic cleanup.

        Args:
            pk: Project ID to update
            data: Gallery update data transfer object

        Returns:
            Tuple containing the updated project and any error that occurred
        """
        try:
            return self._update_project_gallery_with_cleanup(pk, data)
        except Project.DoesNotExist:
            return self._handle_project_not_found_by_id(pk)
        except Exception as e:
            logger.error(
                f"Error updating project {pk} gallery: {str(e)}", exc_info=True
            )
            return Project(), e

    def delete_project_gallery_image(
        self, pk: int, index: int
    ) -> Tuple[Project, Optional[Exception]]:
        """
        Delete a specific image from project gallery by index.

        Args:
            pk: Project ID
            index: Index of the gallery image to delete

        Returns:
            Tuple containing the updated project and any error that occurred
        """
        try:
            return self._delete_gallery_image_by_index(pk, index)
        except Project.DoesNotExist:
            return self._handle_project_not_found_by_id(pk)
        except Exception as e:
            logger.error(
                f"Error deleting gallery image from project {pk}: {str(e)}",
                exc_info=True,
            )
            return Project(), e

    # Helper Methods for Internal Operations

    def _process_gallery_images(
        self, gallery_images: Sequence[InMemoryUploadedFile | str], slug: str
    ) -> List[str]:
        """
        Process gallery images and return list of saved paths.

        Args:
            gallery_images: List of image files or existing paths
            slug: Project slug for filename generation

        Returns:
            List of saved gallery image paths
        """
        gallery_paths = []
        for i, gallery_image in enumerate(gallery_images):
            if isinstance(gallery_image, InMemoryUploadedFile):
                gallery_path = self._save_project_gallery_image(gallery_image, slug, i)
                gallery_paths.append(gallery_path)
            elif isinstance(gallery_image, str):
                gallery_paths.append(gallery_image)
        return gallery_paths

    def _update_project_fields(self, project: Project, update_data: dict) -> None:
        """
        Update project fields with provided data.

        Args:
            project: Project instance to update
            update_data: Dictionary of fields to update
        """
        for key, value in update_data.items():
            if value is not None:
                setattr(project, key, value)

    def _cleanup_old_gallery_images(self, gallery_paths: List[str]) -> None:
        """
        Clean up old gallery image files from storage.

        Args:
            gallery_paths: List of gallery image paths to delete
        """
        if gallery_paths:
            for image_path in gallery_paths:
                self._delete_project_file(image_path)

    def _save_project_gallery_image(
        self, image: InMemoryUploadedFile, slug: str, index: int
    ) -> str:
        """
        Save project gallery image to storage with proper naming.

        Args:
            image: Uploaded image file
            slug: Project slug for filename generation
            index: Gallery image index for uniqueness

        Returns:
            Path to saved image file

        Raises:
            Exception: If image saving fails
        """
        try:
            file_extension = os.path.splitext(image.name)[1]
            filename = f"{slug}_gallery_{index}{file_extension}"
            file_path = (
                f"{settings.FILE_UPLOAD_BASE_DIR}uploads/projects/gallery/{filename}"
            )

            saved_path = default_storage.save(file_path, image)
            logger.info(f"Project gallery image saved to {saved_path}")
            return saved_path

        except Exception as e:
            logger.error(f"Error saving project gallery image: {str(e)}", exc_info=True)
            raise ValidationError(f"Failed to save gallery image: {str(e)}") from e

    def _delete_project_file(self, file_path: str) -> None:
        """
        Delete project file from storage with error handling.

        Args:
            file_path: Path to file to delete
        """
        try:
            if file_path and default_storage.exists(file_path):
                default_storage.delete(file_path)
                logger.info(f"Project file {file_path} deleted successfully")
        except Exception as e:
            logger.warning(f"Error deleting project file {file_path}: {str(e)}")

    def _handle_project_not_found_by_id(self, pk: int) -> Tuple[Project, Exception]:
        """
        Handle Project.DoesNotExist exception for ID-based lookups.

        Args:
            pk: Project ID that was not found

        Returns:
            Tuple containing empty Project and exception
        """
        return self._create_project_not_found_error("Project with id '", pk)

    def _handle_project_not_found_by_slug(self, slug: str) -> Tuple[Project, Exception]:
        """
        Handle Project.DoesNotExist exception for slug-based lookups.

        Args:
            slug: Project slug that was not found

        Returns:
            Tuple containing empty Project and exception
        """
        return self._create_project_not_found_error("Project with slug '", slug)

    def _save_and_log_success(
        self, project: Project, field_name: str, pk: int, success_message: str
    ) -> Tuple[Project, None]:
        """
        Save project with specific field update and log success message.

        Args:
            project: Project instance to save
            field_name: Field name to include in update_fields
            pk: Project ID for logging
            success_message: Success message to log

        Returns:
            Tuple containing saved project and None
        """
        project.save(update_fields=[field_name, "updated_at"])
        logger.info(f"Project {pk} {success_message}")
        return project, None

    def _delete_project_with_cleanup(self, pk: int) -> None:
        """
        Delete project and clean up associated files.

        Args:
            pk: Project ID to delete

        Returns:
            None if successful
        """
        project = Project.objects.get(id=pk)

        # Clean up associated files
        if project.image:
            project.image.delete(save=False)
        if project.gallery:
            self._cleanup_old_gallery_images(project.gallery)

        project.delete()
        logger.info(f"Project {pk} deleted successfully")
        return None

    def _update_project_with_data_handling(
        self, pk: int, data: dto.UpdateProjectDTO
    ) -> Tuple[Project, None]:
        """
        Update project with comprehensive data handling including images.

        Args:
            pk: Project ID to update
            data: Project update data transfer object

        Returns:
            Tuple containing the updated project and None
        """
        project = Project.objects.get(id=pk)

        # Validate slug uniqueness if slug is being updated
        if data.slug and not self.validate_slug_uniqueness(data.slug, exclude_id=pk):
            raise ValidationError("Project with this slug already exists.")

        update_data = data.to_dict()

        # Handle main image update
        if isinstance(data.image, InMemoryUploadedFile):
            if project.image:
                project.image.delete(save=False)
            update_data["image"] = data.image

        # Handle gallery update
        if data.gallery:
            self._cleanup_old_gallery_images(project.gallery)
            update_data["gallery"] = self._process_gallery_images(
                data.gallery, data.slug or project.slug
            )

        # Apply updates to project
        self._update_project_fields(project, update_data)
        project.save()

        logger.info(f"Project {pk} updated successfully")
        return project, None

    def _toggle_project_status_with_logging(
        self, pk: int, data: dto.ToggleProjectStatusDTO
    ) -> Tuple[Project, None]:
        """
        Toggle project status and log the action.

        Args:
            pk: Project ID to update
            data: Status toggle data transfer object

        Returns:
            Tuple containing the updated project and None
        """
        project = Project.objects.get(id=pk)
        project.is_active = data.is_active
        project.save(update_fields=["is_active", "updated_at"])

        status_text = "activated" if data.is_active else "deactivated"
        logger.info(f"Project {pk} {status_text} successfully")
        return project, None

    def _update_project_image_with_cleanup(
        self, pk: int, data: dto.UpdateProjectImageDTO
    ) -> Tuple[Project, None]:
        """
        Update project image with cleanup of old image.

        Args:
            pk: Project ID to update
            data: Image update data transfer object

        Returns:
            Tuple containing the updated project and None
        """
        project = Project.objects.get(id=pk)

        # Clean up old image
        if project.image:
            project.image.delete(save=False)

        # Save new image
        project.image.save(data.image.name, data.image, save=False)
        return self._save_and_log_success(
            project, "image", pk, "main image updated successfully"
        )

    def _update_project_gallery_with_cleanup(
        self, pk: int, data: dto.UpdateProjectGalleryDTO
    ) -> Tuple[Project, None]:
        """
        Update project gallery with cleanup of old images.

        Args:
            pk: Project ID to update
            data: Gallery update data transfer object

        Returns:
            Tuple containing the updated project and None
        """
        project = Project.objects.get(id=pk)

        # Clean up old gallery images
        if project.gallery:
            self._cleanup_old_gallery_images(project.gallery)

        # Save new gallery images
        project.gallery = self._process_gallery_images(data.gallery, project.slug)
        return self._save_and_log_success(
            project, "gallery", pk, "gallery updated successfully"
        )

    def _delete_gallery_image_by_index(
        self, pk: int, index: int
    ) -> Tuple[Project, None]:
        """
        Delete a specific gallery image by index with validation.

        Args:
            pk: Project ID
            index: Index of the gallery image to delete

        Returns:
            Tuple containing the updated project and None

        Raises:
            Exception: If gallery image at index does not exist
        """
        project = Project.objects.get(id=pk)

        if not project.gallery or index >= len(project.gallery) or index < 0:
            error_msg = (
                f"Gallery image at index {index} does not exist for project {pk}."
            )
            logger.warning(error_msg)
            raise ValidationError(error_msg)

        # Delete the specific image file
        self._delete_project_file(project.gallery[index])

        # Remove from gallery list
        project.gallery = [img for i, img in enumerate(project.gallery) if i != index]
        project.save(update_fields=["gallery", "updated_at"])

        logger.info(f"Gallery image at index {index} deleted from project {pk}")
        return project, None

    def _create_project_not_found_error(
        self, prefix: str, identifier: int | str
    ) -> Tuple[Project, Exception]:
        """
        Create a standardized project not found error with logging.

        Args:
            prefix: Error message prefix (e.g., "Project with id '", "Project with slug '")
            identifier: Project identifier (ID or slug)

        Returns:
            Tuple containing empty Project and exception
        """
        error_msg = f"{prefix}{identifier}' does not exist."
        logger.warning(error_msg)
        return Project(), ValidationError(error_msg)
