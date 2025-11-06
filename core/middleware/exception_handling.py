"""
Django Middleware for Exception Handling
Integrates the custom exception handler with Django's request/response cycle
"""

from typing import Optional, Callable, Any
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import APIException
from core.handlers.exception import exception_handler
import uuid
import logging

logger = logging.getLogger(__name__)


class ExceptionHandlingMiddleware(MiddlewareMixin):
    """
    Middleware to handle exceptions with consistent API responses and detailed logging.

    This middleware:
    1. Adds correlation IDs to requests for tracing
    2. Catches and handles DRF API exceptions
    3. Provides consistent error responses for API endpoints
    4. Logs detailed exception information
    """

    def process_request(self, request: HttpRequest) -> Optional[HttpResponse]:
        """
        Add correlation ID to request for exception tracking.

        Args:
            request: The incoming HTTP request

        Returns:
            None to continue processing
        """
        # Add correlation ID for exception tracking
        if not hasattr(request, 'correlation_id'):
            setattr(request, 'correlation_id', str(uuid.uuid4()))

        return None

    def process_exception(
        self,
        request: HttpRequest,
        exception: Exception
    ) -> Optional[HttpResponse]:
        """
        Handle exceptions with detailed logging and consistent API responses.

        Args:
            request: The HTTP request that caused the exception
            exception: The exception that was raised

        Returns:
            JsonResponse for API exceptions, None for default Django handling
        """
        try:
            # Handle the exception using our custom handler
            context = exception_handler.handle_exception(request, exception)

            # Create appropriate response
            return exception_handler.create_error_response(request, exception)

        except Exception as handler_exception:
            # If our exception handler fails, log it and fall back to Django's default
            logger.error(
                f"Exception handler failed: {handler_exception}",
                exc_info=True,
                extra={
                    'original_exception': str(exception),
                    'original_exception_type': type(exception).__name__,
                    'correlation_id': getattr(request, 'correlation_id', 'unknown'),
                }
            )

            # Return None to let Django handle the exception normally
            return None

    def process_response(
        self,
        request: HttpRequest,
        response: HttpResponse
    ) -> HttpResponse:
        """
        Add correlation ID to response headers for tracing.

        Args:
            request: The HTTP request
            response: The HTTP response

        Returns:
            The response with added headers
        """
        # Add correlation ID to response headers for debugging
        if hasattr(request, 'correlation_id'):
            response['X-Correlation-ID'] = getattr(request, 'correlation_id')

        return response