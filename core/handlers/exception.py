"""
Exception Handler
Comprehensive exception logging and error handling
"""

import logging
import traceback
import json
import sys
from datetime import datetime
from typing import Optional, Dict, Any
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from rest_framework.exceptions import (
    AuthenticationFailed,
    PermissionDenied,
    ValidationError,
    APIException
)


class ExceptionHandler:
    """
    Comprehensive exception handler for detailed logging and reporting

    Features:
    - Detailed context collection with correlation ID support
    - Safe data extraction with sensitive field hiding
    - JSON and structured logging for parsing tools
    - Configurable response formatting based on request type
    - External service integration ready (Sentry, Slack, etc.)
    """

    # Class constants for optimization
    _SENSITIVE_FIELDS: tuple[str, ...] = ('password', 'token', 'secret', 'key', 'csrf')
    _USER_AGENT_MAX_LENGTH: int = 100
    _JSON_INDENT: int = 2

    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger('exception_handler')
        self.debug_mode: bool = getattr(settings, 'DEBUG', False)

    def handle_exception(
        self,
        request: HttpRequest,
        exception: Exception,
        exc_info: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Handle exception with detailed logging and context collection

        Args:
            request: Django request object
            exception: Exception instance
            exc_info: Exception info from sys.exc_info()

        Returns:
            Dictionary containing comprehensive exception context
        """
        # Handle DRF exceptions specifically
        if isinstance(exception, APIException):
            return self._handle_drf_exception(request, exception)

        # Collect comprehensive context for other exceptions
        context: Dict[str, Any] = self._collect_context(request, exception)

        # Log detailed exception
        self._log_detailed_exception(context, exc_info)

        # Send to external services if configured
        self._send_to_external_services(context)

        return context

    def _handle_drf_exception(
        self,
        request: HttpRequest,
        exception: APIException
    ) -> Dict[str, Any]:
        """
        Handle Django REST Framework exceptions with consistent API responses

        Args:
            request: Django request object
            exception: DRF APIException instance

        Returns:
            Dictionary containing exception context for DRF exceptions
        """
        # Collect basic context for DRF exceptions
        context: Dict[str, Any] = {
            'correlation_id': getattr(request, 'correlation_id', 'unknown'),
            'timestamp': datetime.now().isoformat(),
            'exception_type': 'drf_api_exception',
            'exception': self._extract_drf_exception_info(exception),
            'request': self._extract_request_info(request),
            'user': self._extract_user_info(request),
        }

        # Log DRF exception with appropriate level
        self._log_drf_exception(context, exception)

        return context

    def _extract_drf_exception_info(self, exception: APIException) -> Dict[str, Any]:
        """Extract DRF exception information"""
        return {
            'type': type(exception).__name__,
            'message': str(exception),
            'detail': getattr(exception, 'detail', None),
            'status_code': getattr(exception, 'status_code', 500),
            'default_code': getattr(exception, 'default_code', 'error'),
        }

    def _log_drf_exception(self, context: Dict[str, Any], exception: APIException) -> None:
        """Log DRF exceptions with appropriate severity level"""
        exception_type = type(exception).__name__
        correlation_id = context['correlation_id']
        user_info = context['user']
        request_info = context['request']

        # Determine log level based on exception type
        if isinstance(exception, AuthenticationFailed):
            log_level = logging.WARNING
            log_message = (
                f"🔐 AUTHENTICATION FAILED - Correlation: {correlation_id} | "
                f"User: {user_info.get('username', 'Anonymous')} | "
                f"IP: {request_info.get('remote_addr', 'Unknown')} | "
                f"Path: {request_info.get('method', 'Unknown')} {request_info.get('path', 'Unknown')} | "
                f"Message: {exception}"
            )
        elif isinstance(exception, PermissionDenied):
            log_level = logging.WARNING
            log_message = (
                f"🚫 PERMISSION DENIED - Correlation: {correlation_id} | "
                f"User: {user_info.get('username', 'Anonymous')} (ID: {user_info.get('id', 'None')}) | "
                f"IP: {request_info.get('remote_addr', 'Unknown')} | "
                f"Path: {request_info.get('method', 'Unknown')} {request_info.get('path', 'Unknown')} | "
                f"Message: {exception}"
            )
        elif isinstance(exception, ValidationError):
            log_level = logging.INFO
            log_message = (
                f"📝 VALIDATION ERROR - Correlation: {correlation_id} | "
                f"Path: {request_info.get('method', 'Unknown')} {request_info.get('path', 'Unknown')} | "
                f"Message: {exception}"
            )
        else:
            log_level = logging.ERROR
            log_message = (
                f"⚠️ DRF API EXCEPTION - Type: {exception_type} | "
                f"Correlation: {correlation_id} | "
                f"Path: {request_info.get('method', 'Unknown')} {request_info.get('path', 'Unknown')} | "
                f"Message: {exception}"
            )

        # Log with appropriate level
        self.logger.log(
            log_level,
            log_message,
            extra={
                'correlation_id': correlation_id,
                'exception_type': exception_type,
                'exception_context': context,
                'user_info': user_info,
                'drf_exception': True,
            }
        )

    def _collect_context(self, request: HttpRequest, exception: Exception) -> Dict[str, Any]:
        """Collect comprehensive context information"""
        # Get correlation ID from request
        correlation_id: str = getattr(request, 'correlation_id', 'unknown')

        return {
            'correlation_id': correlation_id,
            'timestamp': datetime.now().isoformat(),
            'exception': self._extract_exception_info(exception),
            'request': self._extract_request_info(request),
            'user': self._extract_user_info(request),
            'session': self._extract_session_info(request),
            'data': self._extract_request_data(request),
            'server': self._extract_server_info(),
        }

    def _extract_exception_info(self, exception: Exception) -> Dict[str, Any]:
        """Extract exception information"""
        return {
            'type': type(exception).__name__,
            'message': str(exception),
            'args': exception.args,
        }

    def _extract_request_info(self, request: HttpRequest) -> Dict[str, Optional[str]]:
        """Extract request information"""
        return {
            'method': request.method,
            'path': request.path,
            'full_path': request.get_full_path(),
            'url': request.build_absolute_uri(),
            'remote_addr': self._get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'referer': request.META.get('HTTP_REFERER', ''),
            'content_type': request.META.get('CONTENT_TYPE', ''),
        }

    def _extract_user_info(self, request: HttpRequest) -> Dict[str, bool | int | str | None]:
        """Extract user information safely"""
        if not hasattr(request, 'user'):
            return {'is_authenticated': False, 'id': None, 'username': None}

        user = request.user
        is_authenticated: bool = False
        if hasattr(user, 'is_authenticated'):
            is_authenticated = user.is_authenticated

        return {
            'is_authenticated': is_authenticated,
            'id': getattr(user, 'id', None) if is_authenticated else None,
            'username': getattr(user, 'username', None) if is_authenticated else None,
        }

    def _extract_session_info(self, request: HttpRequest) -> Dict[str, str | Dict[str, Any] | None]:
        """Extract session information safely"""
        if not hasattr(request, 'session'):
            return {'session_key': None, 'session_data': {}}

        session = request.session
        return {
            'session_key': session.session_key,
            'session_data': dict(session),
        }

    def _extract_request_data(self, request: HttpRequest) -> Dict[str, Any]:
        """Extract request data (GET, POST, FILES)"""
        return {
            'GET': dict(request.GET),
            'POST': self._get_safe_post_data(request),
            'FILES': list(request.FILES.keys()) if hasattr(request, 'FILES') else [],
        }

    def _extract_server_info(self) -> Dict[str, str | bool]:
        """Extract server environment information"""
        return {
            'django_version': getattr(settings, 'DJANGO_VERSION', 'Unknown'),
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}",
            'debug_mode': self.debug_mode,
        }

    def _get_safe_post_data(self, request: HttpRequest) -> Dict[str, str]:
        """Safely extract POST data while hiding sensitive fields"""
        if request.method != 'POST' or not hasattr(request, 'POST'):
            return {}

        return {
            key: '[HIDDEN]' if any(field in key.lower() for field in self._SENSITIVE_FIELDS) else value
            for key, value in request.POST.items()
        }

    def _log_detailed_exception(self, context: Dict[str, Any], exc_info: Optional[Any] = None) -> None:
        """Log detailed exception with full context"""
        # Format structured log message
        message: str = self._format_exception_message(context)

        # Log with full context as extra data
        self.logger.error(
            message,
            exc_info=exc_info or True,
            extra={
                'correlation_id': context['correlation_id'],
                'exception_context': context,
                'request_data': context['data'],
                'user_info': context['user'],
            }
        )

        # Also log in JSON format for parsing tools
        self._log_json_context(context)

    def _format_exception_message(self, context: Dict[str, Any]) -> str:
        """Format human-readable exception message"""
        user_display: str = context['user']['username'] or 'Anonymous'
        user_id: int | str | None = context['user']['id']
        user_agent: str = context['request']['user_agent'][:self._USER_AGENT_MAX_LENGTH]

        return (
            f"🔥 EXCEPTION OCCURRED 🔥\n"
            f"{'='*60}\n"
            f"Correlation ID: {context['correlation_id']}\n"
            f"Exception: {context['exception']['type']}\n"
            f"Message: {context['exception']['message']}\n"
            f"URL: {context['request']['method']} {context['request']['full_path']}\n"
            f"User: {user_display} (ID: {user_id})\n"
            f"IP: {context['request']['remote_addr']}\n"
            f"User-Agent: {user_agent}\n"
            f"Timestamp: {context['timestamp']}\n"
            f"{'='*60}\n"
        )

    def _log_json_context(self, context: Dict[str, Any]) -> None:
        """Log context in JSON format for parsing tools"""
        try:
            json_context: str = json.dumps(context, indent=self._JSON_INDENT)
            self.logger.error(f"EXCEPTION_JSON: {json_context}", exc_info=False)
        except (TypeError, ValueError) as e:
            self.logger.warning(f"Failed to serialize exception context to JSON: {e}")

    def _send_to_external_services(self, context: Dict[str, Any]) -> None:
        """Send exception to external services (Sentry, Slack, etc.)"""
        # TODO: Implement integration with:
        # - Sentry for error tracking
        # - Slack for real-time notifications
        # - Email for critical errors
        # - Custom webhooks
        pass

    def _get_client_ip(self, request: HttpRequest) -> str:
        """Get real client IP address with X-Forwarded-For support"""
        x_forwarded_for: Optional[str] = request.META.get('HTTP_X_FORWARDED_FOR')
        return (
            x_forwarded_for.split(',')[0].strip()
            if x_forwarded_for
            else request.META.get('REMOTE_ADDR', 'Unknown')
        )

    def create_error_response(
        self,
        request: HttpRequest,
        exception: Exception,
        status_code: int = 500
    ) -> Optional[JsonResponse]:
        """
        Create appropriate error response based on request type

        Args:
            request: Django request object
            exception: Exception instance
            status_code: HTTP status code for response

        Returns:
            JsonResponse for API requests, None for default Django handling
        """
        # Handle DRF exceptions with their specific response format
        if isinstance(exception, APIException):
            return self._create_drf_error_response(request, exception)

        # Handle other exceptions for API requests
        if self._is_api_request(request):
            return self._create_json_error_response(exception, status_code)

        # Return None for default Django error handling
        return None

    def _create_drf_error_response(
        self,
        request: HttpRequest,
        exception: APIException
    ) -> JsonResponse:
        """
        Create consistent API response for DRF exceptions

        Args:
            request: Django request object
            exception: DRF APIException instance

        Returns:
            JsonResponse with consistent error format
        """
        # Import here to avoid circular imports
        try:
            from utils.response import api_response

            # Use your existing api_response utility for consistency
            if isinstance(exception, AuthenticationFailed):
                response = api_response(request).unauthorized(
                    message=str(exception)
                )
            elif isinstance(exception, PermissionDenied):
                response = api_response(request).forbidden(
                    message=str(exception)
                )
            elif isinstance(exception, ValidationError):
                # Handle validation errors by converting to proper format
                response = api_response(request).validation_error(
                    message="Validation failed",
                    errors={'validation_detail': str(exception.detail) if hasattr(exception, 'detail') else str(exception)}
                )
            else:
                # Generic API exception
                response = api_response(request).error(
                    message=str(exception),
                    status_code=getattr(exception, 'status_code', 500)
                )

            # Add additional context to the response data if it's a dict
            if hasattr(response, 'data') and isinstance(response.data, dict):
                response.data.update({
                    'error_code': type(exception).__name__.upper(),
                    'correlation_id': getattr(request, 'correlation_id', 'unknown'),
                    'timestamp': datetime.now().isoformat(),
                })

            # Convert DRF Response to JsonResponse for consistency
            return JsonResponse(
                response.data,
                status=response.status_code,
                json_dumps_params={'ensure_ascii': False}
            )

        except ImportError:
            # Fallback to basic JsonResponse if api_response is not available
            return self._create_fallback_drf_response(exception)

    def _create_fallback_drf_response(self, exception: APIException) -> JsonResponse:
        """
        Fallback response creation for DRF exceptions

        Args:
            exception: DRF APIException instance

        Returns:
            Basic JsonResponse with error information
        """
        error_data: Dict[str, Any] = {
            'error': True,
            'message': str(exception),
            'error_code': type(exception).__name__.upper(),
            'timestamp': datetime.now().isoformat(),
        }

        if hasattr(exception, 'detail'):
            error_data['detail'] = exception.detail

        status_code = getattr(exception, 'status_code', 500)
        return JsonResponse(error_data, status=status_code)

    def _is_api_request(self, request: HttpRequest) -> bool:
        """Determine if request expects JSON response"""
        content_type: str = request.content_type or ''
        accept_header: str = request.META.get('HTTP_ACCEPT', '')

        return (
            'application/json' in content_type or
            accept_header.startswith('application/json')
        )

    def _create_json_error_response(self, exception: Exception, status_code: int) -> JsonResponse:
        """Create JSON error response for API requests"""
        error_data: Dict[str, Any] = {
            'error': True,
            'message': str(exception) if self.debug_mode else 'Internal server error',
            'type': type(exception).__name__ if self.debug_mode else 'ServerError',
            'timestamp': datetime.now().isoformat(),
        }

        if self.debug_mode:
            error_data['traceback'] = traceback.format_exc()

        return JsonResponse(error_data, status=status_code)


# Global instance for easy import and usage
exception_handler: ExceptionHandler = ExceptionHandler()