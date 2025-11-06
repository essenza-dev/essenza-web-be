"""
Request Logging Middleware
Log all requests for monitoring with correlation ID support
"""

import logging
import time
import uuid
from typing import Optional, Dict, Any, Union
from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from core.handlers.exception import exception_handler

logger = logging.getLogger(__name__)


class Colors:
    """ANSI color codes for terminal output"""
    BLUE: str = '\033[94m'      # Incoming request
    GREEN: str = '\033[92m'     # Success (2xx-3xx)
    YELLOW: str = '\033[93m'    # Client error (4xx)
    RED: str = '\033[91m'       # Server error (5xx)
    PURPLE: str = '\033[95m'    # Exception
    RESET: str = '\033[0m'      # Reset color
    BOLD: str = '\033[1m'       # Bold text


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log every request with correlation ID tracking

    Features:
    - Automatic correlation ID generation/extraction
    - Request/response logging with metrics
    - Query parameters and body logging
    - Exception handling with detailed context
    - Color-coded output for better readability

    Usage in settings.py:
        MIDDLEWARE = [
            ...
            'core.middleware.request_logging.RequestLoggingMiddleware',
        ]
    """

    # Class constants for optimization
    _SENSITIVE_FIELDS: tuple[str, ...] = ('password', 'token', 'secret', 'key', 'csrf')
    _BODY_METHODS: tuple[str, ...] = ('POST', 'PUT', 'PATCH', 'DELETE')
    _MAX_QUERY_LENGTH: int = 100
    _MAX_BODY_LENGTH: int = 150
    _MAX_ERROR_LENGTH: int = 50
    _CORRELATION_ID_LENGTH: int = 8

    def process_request(self, request: HttpRequest) -> None:
        """Log incoming request with correlation ID and request data"""
        # Set start time for duration calculation
        request.start_time = time.time()  # type: ignore

        # Handle correlation ID with fallback to UUID generation
        correlation_id: str = (
            request.META.get('HTTP_X_CORRELATION_ID') or
            str(uuid.uuid4())
        )
        request.correlation_id = correlation_id  # type: ignore

        # Extract and format user agent
        user_agent_short: str = self._extract_user_agent(request)
        client_ip: str = self._get_client_ip(request)

        # Main request log
        self._log_request_start(request, client_ip, user_agent_short, correlation_id)

        # Log additional request data if available
        self._log_query_params(request, correlation_id)
        self._log_request_body(request, correlation_id)

    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        """Log response with metrics and add correlation ID header"""
        if hasattr(request, 'start_time'):
            duration: float = time.time() - getattr(request, 'start_time')
            correlation_id: str = getattr(request, 'correlation_id', 'unknown')

            # Log response with metrics
            self._log_response(request, response, duration, correlation_id)

        # Add correlation ID to response header
        if hasattr(request, 'correlation_id'):
            response['X-Correlation-ID'] = getattr(request, 'correlation_id')

        return response

    def process_exception(self, request: HttpRequest, exception: Exception) -> None:
        """Log exception with dual approach: quick summary + detailed logging"""
        correlation_id: str = getattr(request, 'correlation_id', 'unknown')

        # Quick log for monitoring
        self._log_exception_summary(request, exception, correlation_id)

        # Detailed log using exception handler
        exception_handler.handle_exception(request, exception)

    def _extract_user_agent(self, request: HttpRequest) -> str:
        """Extract and format user agent for logging"""
        user_agent: str = request.META.get('HTTP_USER_AGENT', 'Unknown')
        return user_agent.split()[0] if user_agent else 'Unknown'

    def _get_client_ip(self, request: HttpRequest) -> str:
        """Get real client IP address with X-Forwarded-For support"""
        x_forwarded_for: Optional[str] = request.META.get('HTTP_X_FORWARDED_FOR')
        return (
            x_forwarded_for.split(',')[0].strip()
            if x_forwarded_for
            else request.META.get('REMOTE_ADDR', 'unknown')
        )

    def _log_request_start(
        self,
        request: HttpRequest,
        client_ip: str,
        user_agent: str,
        correlation_id: str
    ) -> None:
        """Log main request information"""
        logger.info(
            f"{Colors.BLUE}▶{Colors.RESET} {request.method:<4} {request.path:<30} │ "
            f"{client_ip:<15} │ "
            f"{user_agent:<12} │ "
            f"ID:{Colors.BOLD}{correlation_id[:self._CORRELATION_ID_LENGTH]}{Colors.RESET}"
        )

    def _log_query_params(self, request: HttpRequest, correlation_id: str) -> None:
        """Log query parameters if available"""
        if not request.GET:
            return

        query_params: Dict[str, Any] = dict(request.GET)
        query_str: str = str(query_params)[:self._MAX_QUERY_LENGTH]

        logger.info(
            f"  📋 Query: {Colors.BOLD}{query_str}{Colors.RESET} │ "
            f"ID:{Colors.BOLD}{correlation_id[:self._CORRELATION_ID_LENGTH]}{Colors.RESET}"
        )

    def _log_request_body(self, request: HttpRequest, correlation_id: str) -> None:
        """Log request body for methods that support body"""
        if request.method not in self._BODY_METHODS or not hasattr(request, 'body'):
            return

        try:
            if body_preview := self._extract_body_preview(request):
                logger.info(
                    f"  📝 Body: {Colors.BOLD}{body_preview}{Colors.RESET} │ "
                    f"ID:{Colors.BOLD}{correlation_id[:self._CORRELATION_ID_LENGTH]}{Colors.RESET}"
                )
        except Exception as e:
            logger.warning(
                f"  ⚠️  Body decode error: {str(e)[:self._MAX_ERROR_LENGTH]} │ "
                f"ID:{Colors.BOLD}{correlation_id[:self._CORRELATION_ID_LENGTH]}{Colors.RESET}"
            )

    def _extract_body_preview(self, request: HttpRequest) -> str:
        """Extract and format body preview based on content type"""
        content_type: str = request.content_type or ''

        if 'application/json' in content_type:
            return request.body.decode('utf-8')[:self._MAX_BODY_LENGTH] if request.body else ''
        elif 'form' in content_type:
            body_data: Dict[str, str] = self._get_safe_body_data(request)
            return str(body_data)[:self._MAX_BODY_LENGTH] if body_data else ''
        else:
            body_size: int = len(request.body) if request.body else 0
            return f"[{content_type or 'unknown'}, {body_size} bytes]"

    def _get_safe_body_data(self, request: HttpRequest) -> Dict[str, str]:
        """Extract body data while hiding sensitive fields"""
        if not hasattr(request, 'POST'):
            return {}

        return {
            key: '[HIDDEN]' if any(field in key.lower() for field in self._SENSITIVE_FIELDS) else value
            for key, value in request.POST.items()
        }

    def _log_response(
        self,
        request: HttpRequest,
        response: HttpResponse,
        duration: float,
        correlation_id: str
    ) -> None:
        """Log response with metrics and color coding"""
        color, icon = self._get_status_color_and_icon(response.status_code)
        size_str: str = self._format_response_size(response)

        logger.info(
            f"{color}{icon}{Colors.RESET} {request.method:<4} {request.path:<30} │ "
            f"{color}{response.status_code:<3}{Colors.RESET} │ "
            f"{Colors.BOLD}{duration*1000:.0f}ms{Colors.RESET:<6} │ "
            f"{size_str:<8} │ "
            f"ID:{Colors.BOLD}{correlation_id[:self._CORRELATION_ID_LENGTH]}{Colors.RESET}"
        )

    def _get_status_color_and_icon(self, status_code: int) -> tuple[str, str]:
        """Get color and icon based on status code"""
        if status_code < 400:
            return Colors.GREEN, "✓"
        elif status_code < 500:
            return Colors.YELLOW, "⚠"
        else:
            return Colors.RED, "✗"

    def _format_response_size(self, response: HttpResponse) -> str:
        """Format response size for readability"""
        if not hasattr(response, 'content'):
            return "0B"

        size: int = len(response.content)
        return f"{size/1024:.1f}KB" if size > 1024 else f"{size}B"

    def _log_exception_summary(
        self,
        request: HttpRequest,
        exception: Exception,
        correlation_id: str
    ) -> None:
        """Log quick exception summary for monitoring"""
        exception_name: str = type(exception).__name__
        exception_msg: str = str(exception)[:20]

        logger.error(
            f"{Colors.PURPLE}✗{Colors.RESET} {request.method:<4} {request.path:<30} │ "
            f"{Colors.RED}{exception_name:<12}{Colors.RESET} │ "
            f"{exception_msg:<20} │ "
            f"ID:{Colors.BOLD}{correlation_id[:self._CORRELATION_ID_LENGTH]}{Colors.RESET}"
        )
