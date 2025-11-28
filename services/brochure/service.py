"""
Brochure Service Module
Handles all business logic for brochure management operations.
"""

import logging
import os
from typing import Tuple, Optional
from django.db.models.query import QuerySet
from django.db.models import Q
from django.core.paginator import Page
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage

from core.service import BaseService
from core.models import Brochure
from . import dto

logger = logging.getLogger(__name__)

# Constants for error messages
PDF_FILE_ERROR = "Only PDF files are allowed."
FILE_SIZE_ERROR = "File size must be less than 50MB."
TITLE_EXISTS_ERROR = "Brochure with this title already exists."
BROCHURE_NOT_FOUND_ERROR = "Brochure with id '{pk}' does not exist."


class BrochureService(BaseService):
    """Service class for managing brochure operations with comprehensive CRUD functionality."""

    def validate_file_extension(self, file: InMemoryUploadedFile) -> bool:
        """
        Validate if the uploaded file has a valid PDF extension.

        Args:
            file: The uploaded file to validate

        Returns:
            True if file extension is valid, False otherwise
        """
        if not file or not hasattr(file, "name"):
            return False

        allowed_extensions = [".pdf"]
        file_ext = os.path.splitext(file.name)[1].lower()
        return file_ext in allowed_extensions

    def validate_file_size(
        self, file: InMemoryUploadedFile, max_size_mb: int = 50
    ) -> bool:
        """
        Validate if the uploaded file size is within the allowed limit.

        Args:
            file: The uploaded file to validate
            max_size_mb: Maximum file size in MB (default: 50MB)

        Returns:
            True if file size is valid, False otherwise
        """
        return file.size <= max_size_mb * 1024 * 1024 if file else False

    def validate_brochure_title_uniqueness(
        self, title: str, exclude_id: Optional[int] = None
    ) -> bool:
        """
        Validate if brochure title is unique.

        Args:
            title: The title to validate
            exclude_id: Brochure ID to exclude from validation (for updates)

        Returns:
            True if title is unique, False otherwise
        """
        queryset = Brochure.objects.filter(title=title)
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return not queryset.exists()

    def create_brochure(
        self, data: dto.CreateBrochureDTO
    ) -> Tuple[Brochure, Optional[Exception]]:
        """
        Create a new brochure with file handling.

        Args:
            data: Brochure creation data transfer object

        Returns:
            Tuple containing the created brochure and any error that occurred
        """
        try:
            # Validate title uniqueness
            if not self.validate_brochure_title_uniqueness(data.title):
                return Brochure(), Exception(TITLE_EXISTS_ERROR)

            # Validate file if provided
            if data.file:
                if not self.validate_file_extension(data.file):
                    return Brochure(), Exception(PDF_FILE_ERROR)

                if not self.validate_file_size(data.file):
                    return Brochure(), Exception(FILE_SIZE_ERROR)

            brochure_data = data.to_dict()
            brochure = Brochure.objects.create(**brochure_data)

            logger.info(f"Brochure created successfully with id {brochure.id}")
            return brochure, None

        except Exception as e:
            logger.error(f"Error creating brochure: {str(e)}", exc_info=True)
            return Brochure(), e

    def get_brochures(self) -> QuerySet[Brochure]:
        """Retrieve all brochures."""
        return Brochure.objects.all()

    def get_paginated_brochures(self, str_page_number: str, str_page_size: str) -> Page:
        """
        Retrieve paginated brochures.

        Args:
            str_page_number: Page number as string
            str_page_size: Page size as string

        Returns:
            Page object containing brochures
        """
        queryset = Brochure.objects.order_by("-created_at")
        return self.get_paginated_data(queryset, str_page_number, str_page_size)

    def get_brochures_with_filters(
        self,
        search: Optional[str] = None,
        str_page_number: str = "1",
        str_page_size: str = "20",
    ) -> Page:
        """
        Retrieve filtered and paginated brochures.

        Args:
            search: Search term for title filtering
            str_page_number: Page number as string
            str_page_size: Page size as string

        Returns:
            Page object containing filtered brochures
        """
        queryset = Brochure.objects.order_by("-created_at")

        # Apply search filter
        if search:
            queryset = queryset.filter(Q(title__icontains=search))

        return self.get_paginated_data(queryset, str_page_number, str_page_size)

    def get_specific_brochure(self, pk: int) -> Tuple[Brochure, Optional[Exception]]:
        """
        Retrieve a specific brochure by its ID.

        Args:
            pk: Primary key of the brochure

        Returns:
            Tuple containing the brochure and any error that occurred
        """
        try:
            brochure = Brochure.objects.get(id=pk)
            return brochure, None
        except Brochure.DoesNotExist:
            return Brochure(), Exception(BROCHURE_NOT_FOUND_ERROR.format(pk=pk))
        except Exception as e:
            logger.error(f"Error retrieving brochure {pk}: {str(e)}", exc_info=True)
            return Brochure(), e

    def update_specific_brochure(
        self, pk: int, data: dto.UpdateBrochureDTO
    ) -> Tuple[Brochure, Optional[Exception]]:
        """
        Update a specific brochure by its ID.

        Args:
            pk: Primary key of the brochure
            data: Brochure update data transfer object

        Returns:
            Tuple containing the updated brochure and any error that occurred
        """
        try:
            return self._update_brochure_data(pk, data)
        except Brochure.DoesNotExist:
            return Brochure(), Exception(BROCHURE_NOT_FOUND_ERROR.format(pk=pk))
        except Exception as e:
            logger.error(f"Error updating brochure {pk}: {str(e)}", exc_info=True)
            return Brochure(), e

    def _update_brochure_data(
        self, pk: int, data: dto.UpdateBrochureDTO
    ) -> Tuple[Brochure, Optional[Exception]]:
        """
        Internal method to handle brochure data update with validations.

        Args:
            pk: Primary key of the brochure
            data: Brochure update data transfer object

        Returns:
            Tuple containing the updated brochure and any error that occurred
        """
        brochure = Brochure.objects.get(id=pk)

        # Validate title uniqueness if title is being updated
        if data.title and not self.validate_brochure_title_uniqueness(
            data.title, exclude_id=pk
        ):
            return Brochure(), Exception(TITLE_EXISTS_ERROR)

        # Validate file if provided
        if data.file:
            if not self.validate_file_extension(data.file):
                return Brochure(), Exception(PDF_FILE_ERROR)

            if not self.validate_file_size(data.file):
                return Brochure(), Exception(FILE_SIZE_ERROR)

            # Delete old file if exists
            if brochure.file:
                self._delete_brochure_file(brochure.file.name)

        # Update fields
        update_data = data.to_dict()
        for key, value in update_data.items():
            if value is not None:
                setattr(brochure, key, value)

        brochure.save()
        logger.info(f"Brochure {pk} updated successfully")
        return brochure, None

    def delete_specific_brochure(self, pk: int) -> Optional[Exception]:
        """
        Delete a specific brochure by its ID.

        Args:
            pk: Primary key of the brochure

        Returns:
            Exception if error occurred, None if successful
        """
        try:
            brochure = Brochure.objects.get(id=pk)

            # Delete file first
            if brochure.file:
                self._delete_brochure_file(brochure.file.name)

            brochure.delete()
            logger.info(f"Brochure {pk} deleted successfully")
            return None

        except Brochure.DoesNotExist:
            return Exception(BROCHURE_NOT_FOUND_ERROR.format(pk=pk))
        except Exception as e:
            logger.error(f"Error deleting brochure {pk}: {str(e)}", exc_info=True)
            return e

    def upload_brochure_file(
        self, pk: int, data: dto.UploadBrochureFileDTO
    ) -> Tuple[Brochure, Optional[Exception]]:
        """
        Upload a file for a specific brochure.

        Args:
            pk: Primary key of the brochure
            data: File upload data transfer object

        Returns:
            Tuple containing the updated brochure and any error that occurred
        """
        try:
            return self._process_file_upload(pk, data)
        except Brochure.DoesNotExist:
            return Brochure(), Exception(BROCHURE_NOT_FOUND_ERROR.format(pk=pk))
        except Exception as e:
            logger.error(
                f"Error uploading file for brochure {pk}: {str(e)}", exc_info=True
            )
            return Brochure(), e

    def _process_file_upload(
        self, pk: int, data: dto.UploadBrochureFileDTO
    ) -> Tuple[Brochure, Optional[Exception]]:
        """
        Internal method to handle file upload processing with validations.

        Args:
            pk: Primary key of the brochure
            data: File upload data transfer object

        Returns:
            Tuple containing the updated brochure and any error that occurred
        """
        brochure = Brochure.objects.get(id=pk)

        # Validate file
        if not self.validate_file_extension(data.file):
            return Brochure(), Exception(PDF_FILE_ERROR)

        if not self.validate_file_size(data.file):
            return Brochure(), Exception(FILE_SIZE_ERROR)

        # Delete old file if exists
        if brochure.file:
            self._delete_brochure_file(brochure.file.name)

        # Save new file
        brochure.file.save(data.file.name, data.file, save=True)

        logger.info(f"File uploaded successfully for brochure {pk}")
        return brochure, None

    def _delete_brochure_file(self, file_path: str) -> None:
        """
        Delete a brochure file from storage.

        Args:
            file_path: Path to the file to delete
        """
        try:
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
                logger.debug(f"Brochure file deleted: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to delete brochure file {file_path}: {str(e)}")

    def _handle_brochure_not_found_by_id(self, pk: int) -> Tuple[Brochure, Exception]:
        """
        Handle brochure not found by ID scenario.

        Args:
            pk: Brochure ID that was not found

        Returns:
            Tuple containing empty brochure and not found exception
        """
        error_msg = BROCHURE_NOT_FOUND_ERROR.format(pk=pk)
        logger.warning(error_msg)
        return Brochure(), Exception(error_msg)

    def get_brochures_count(self) -> int:
        """
        Get total count of brochures.

        Returns:
            Total number of brochures
        """
        return Brochure.objects.count()

    def search_brochures(self, query: str) -> QuerySet[Brochure]:
        """
        Search brochures by title.

        Args:
            query: Search query string

        Returns:
            QuerySet of matching brochures
        """
        return Brochure.objects.filter(title__icontains=query).order_by("-created_at")
