"""
Professional API Response Builder for Django REST Framework

This module provides a comprehensive, standardized way to handle API responses
following industry best practices and popular API design patterns.

Features:
- Consistent response format across all endpoints
- Support for pagination metadata
- Flexible error handling
- Proper HTTP status codes
- Pydantic models for type safety
- Optimized performance with minimal overhead
"""

from __future__ import annotations

import contextlib
from typing import Any, Dict, List, Optional, Union, TypeVar, Generic
from datetime import datetime
from functools import wraps, lru_cache
import logging

from pydantic import BaseModel, Field, validator
from rest_framework import status
from rest_framework.response import Response
from django.core.paginator import Page
from django.db.models import QuerySet

# Type variables for generic support
T = TypeVar("T")


class PaginationInfo(BaseModel):
    """Pydantic model for pagination metadata with validation."""

    current_page: int = Field(ge=1, description="Current page number")
    per_page: int = Field(ge=1, le=1000, description="Items per page")
    total_pages: int = Field(ge=0, description="Total number of pages")
    total_items: int = Field(ge=0, description="Total number of items")
    has_next: bool = Field(description="Whether there is a next page")
    has_previous: bool = Field(description="Whether there is a previous page")
    next_page: Optional[int] = Field(default=None, ge=1, description="Next page number")
    previous_page: Optional[int] = Field(
        default=None, ge=1, description="Previous page number"
    )

    @validator("next_page")
    def validate_next_page(cls, v: Optional[int], values: dict) -> Optional[int]:
        """Validate next page number consistency."""
        return None if v is not None and not values.get("has_next", False) else v

    @validator("previous_page")
    def validate_previous_page(cls, v: Optional[int], values: dict) -> Optional[int]:
        """Validate previous page number consistency."""
        return None if v is not None and not values.get("has_previous", False) else v


class ErrorDetail(BaseModel):
    """Pydantic model for error details with validation."""

    field: str = Field(description="Field name where error occurred")
    message: str = Field(min_length=1, description="Error message")
    code: str = Field(default="invalid", description="Error code")


class APIResponseMeta(BaseModel):
    """Pydantic model for response metadata."""

    timestamp: str = Field(description="ISO timestamp of response")
    request_id: Optional[str] = Field(
        default=None, description="Unique request identifier"
    )
    pagination: Optional[PaginationInfo] = Field(
        default=None, description="Pagination information"
    )


class APIResponseModel(BaseModel, Generic[T]):
    """Pydantic model for standardized API response format."""

    success: bool = Field(description="Whether the request was successful")
    status_code: int = Field(ge=100, le=599, description="HTTP status code")
    message: Optional[str] = Field(
        default=None, min_length=1, description="Response message"
    )
    data: Optional[T] = Field(default=None, description="Response data")
    errors: Optional[List[ErrorDetail]] = Field(
        default=None, description="List of errors"
    )
    meta: APIResponseMeta = Field(description="Response metadata")

    class Config:
        """Pydantic configuration."""

        json_encoders = {datetime: lambda v: v.isoformat()}


class APIResponseBuilder:
    """
    Optimized API Response Builder with fluent interface and Pydantic validation.

    Provides methods to build standardized API responses for various scenarios
    with type safety and performance optimizations.
    """

    __slots__ = ("request", "request_id", "_base_meta")

    def __init__(self, request: Optional[Any] = None) -> None:
        """
        Initialize the response builder with request context.

        Args:
            request: Django request object for extracting metadata
        """
        self.request = request
        self.request_id = self._extract_request_id()
        self._base_meta = self._build_base_meta()

    def _extract_request_id(self) -> Optional[str]:
        """Extract request ID from request headers efficiently."""
        if self.request and hasattr(self.request, "META"):
            return self.request.META.get("HTTP_X_REQUEST_ID")
        return None

    @lru_cache(maxsize=1)
    def _build_base_meta(self) -> APIResponseMeta:
        """Build base metadata with caching for performance."""
        return APIResponseMeta(
            timestamp=datetime.now().isoformat(), request_id=self.request_id
        )

    def _create_response(
        self,
        success: bool,
        status_code: int,
        message: Optional[str] = None,
        data: Any = None,
        errors: Optional[List[ErrorDetail]] = None,
        pagination: Optional[PaginationInfo] = None,
    ) -> Response:
        """
        Internal method to create standardized response with validation.

        Args:
            success: Whether the request was successful
            status_code: HTTP status code
            message: Response message
            data: Response data
            errors: List of error details
            pagination: Pagination information

        Returns:
            DRF Response object
        """
        meta = APIResponseMeta(
            timestamp=datetime.now().isoformat(),
            request_id=self.request_id,
            pagination=pagination,
        )

        response_model = APIResponseModel[Any](
            success=success,
            status_code=status_code,
            message=message,
            data=data,
            meta=meta,
            errors=errors,
        )

        # Convert to dict and remove None values for cleaner output
        response_dict = response_model.dict(exclude_none=True)

        return Response(response_dict, status=status_code)

    def success(
        self,
        data: Any = None,
        message: str = "Operation completed successfully",
        status_code: int = status.HTTP_200_OK,
        pagination: Optional[PaginationInfo] = None,
    ) -> Response:
        """
        Create a successful response with optional data and pagination.

        Args:
            data: Response data
            message: Success message
            status_code: HTTP status code
            pagination: Pagination information

        Returns:
            DRF Response object
        """
        with contextlib.suppress(AttributeError):
            data = data.data
        return self._create_response(
            success=True,
            status_code=status_code,
            message=message,
            data=data,
            pagination=pagination,
        )

    def created(
        self, data: Any = None, message: str = "Resource created successfully"
    ) -> Response:
        """Create a 201 Created response."""
        return self.success(
            data=data, message=message, status_code=status.HTTP_201_CREATED
        )

    def updated(
        self, data: Any = None, message: str = "Resource updated successfully"
    ) -> Response:
        """Create a 200 OK response for updates."""
        return self.success(data=data, message=message)

    def deleted(self, message: str = "Resource deleted successfully") -> Response:
        """Create a 204 No Content response for deletions."""
        return self._create_response(
            success=True, status_code=status.HTTP_204_NO_CONTENT, message=message
        )

    def error(
        self,
        message: str = "An error occurred",
        errors: Optional[List[ErrorDetail]] = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        data: Any = None,
    ) -> Response:
        """
        Create an error response with optional error details.

        Args:
            message: Error message
            errors: List of detailed errors
            status_code: HTTP status code
            data: Additional error data

        Returns:
            DRF Response object
        """
        return self._create_response(
            success=False,
            status_code=status_code,
            message=message,
            data=data,
            errors=errors,
        )

    def validation_error(
        self,
        errors: Union[Dict[str, Any], List[str]],
        message: str = "Validation failed",
    ) -> Response:
        """
        Create a validation error response with formatted errors.

        Args:
            errors: Validation errors (from serializer.errors)
            message: Validation message

        Returns:
            DRF Response object
        """
        formatted_errors = self._format_validation_errors(errors)
        return self.error(
            message=message,
            errors=formatted_errors,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    def not_found(self, message: str = "Resource not found") -> Response:
        """Create a 404 Not Found response."""
        return self.error(message=message, status_code=status.HTTP_404_NOT_FOUND)

    def unauthorized(self, message: str = "Authentication required") -> Response:
        """Create a 401 Unauthorized response."""
        return self.error(message=message, status_code=status.HTTP_401_UNAUTHORIZED)

    def forbidden(self, message: str = "Access forbidden") -> Response:
        """Create a 403 Forbidden response."""
        return self.error(message=message, status_code=status.HTTP_403_FORBIDDEN)

    def server_error(self, message: str = "Internal server error") -> Response:
        """Create a 500 Internal Server Error response."""
        return self.error(
            message=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def paginated(
        self, data: Any, page: Page, message: str = "Data retrieved successfully"
    ) -> Response:
        """
        Create a paginated response from Django Page object.

        Args:
            data: Paginated data (usually serialized)
            page: Django Page object
            message: Response message

        Returns:
            DRF Response object
        """
        pagination_info = self._extract_pagination_info(page)
        return self.success(data=data, message=message, pagination=pagination_info)

    def _extract_pagination_info(self, page: Page) -> PaginationInfo:
        """
        Extract pagination metadata from Django Page object efficiently.

        Args:
            page: Django Page object

        Returns:
            PaginationInfo object
        """
        return PaginationInfo(
            current_page=page.number,
            per_page=page.paginator.per_page,
            total_pages=page.paginator.num_pages,
            total_items=page.paginator.count,
            has_next=page.has_next(),
            has_previous=page.has_previous(),
            next_page=page.next_page_number() if page.has_next() else None,
            previous_page=page.previous_page_number() if page.has_previous() else None,
        )

    def _format_validation_errors(
        self, errors: Union[Dict[str, Any], List[str]]
    ) -> List[ErrorDetail]:
        """
        Format validation errors into a consistent structure efficiently.

        Args:
            errors: Raw validation errors

        Returns:
            List of ErrorDetail objects
        """
        formatted_errors: List[ErrorDetail] = []

        if isinstance(errors, dict):
            for field, field_errors in errors.items():
                if isinstance(field_errors, list):
                    formatted_errors.extend(
                        [
                            ErrorDetail(
                                field=field,
                                message=str(error),
                                code=getattr(error, "code", "invalid"),
                            )
                            for error in field_errors
                        ]
                    )
                else:
                    formatted_errors.append(
                        ErrorDetail(
                            field=field, message=str(field_errors), code="invalid"
                        )
                    )
        elif isinstance(errors, list):
            formatted_errors.extend(
                [
                    ErrorDetail(
                        field="non_field_errors",
                        message=str(error),
                        code=getattr(error, "code", "invalid"),
                    )
                    for error in errors
                ]
            )

        return formatted_errors


# Factory function for convenience
def api_response(request: Optional[Any] = None) -> APIResponseBuilder:
    """
    Factory function to create an APIResponseBuilder instance.

    Args:
        request: Django request object

    Returns:
        APIResponseBuilder instance
    """
    return APIResponseBuilder(request)


# Decorator for automatic response wrapping
def api_response_wrapper(success_message: str = "Operation completed successfully"):
    """
    Decorator to automatically wrap view responses in standardized format.

    Args:
        success_message: Success message to use

    Returns:
        Decorated function
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            try:
                result = func(self, request, *args, **kwargs)

                # If it's already a Response object, return as is
                if isinstance(result, Response):
                    return result

                # Otherwise, wrap in success response
                builder = APIResponseBuilder(request)
                return builder.success(data=result, message=success_message)

            except Exception as e:
                builder = APIResponseBuilder(request)
                return builder.server_error(message="An unexpected error occurred")

        return wrapper

    return decorator


# Custom exception classes for better error handling
class APIException(Exception):
    """Base API exception class with status code and error details."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        errors: Optional[List[ErrorDetail]] = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.errors = errors or []
        super().__init__(self.message)


class ValidationException(APIException):
    """Exception for validation errors."""

    def __init__(
        self,
        message: str = "Validation failed",
        errors: Optional[List[ErrorDetail]] = None,
    ) -> None:
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY, errors)


class NotFoundException(APIException):
    """Exception for resource not found errors."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class UnauthorizedException(APIException):
    """Exception for unauthorized access."""

    def __init__(self, message: str = "Authentication required") -> None:
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class ForbiddenException(APIException):
    """Exception for forbidden access."""

    def __init__(self, message: str = "Access forbidden") -> None:
        super().__init__(message, status.HTTP_403_FORBIDDEN)
