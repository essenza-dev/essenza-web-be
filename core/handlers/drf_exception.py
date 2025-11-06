from typing import Optional, Dict, Any
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework.request import Request
from utils.response import api_response


def custom_exception_handler(exc: Exception, context: Dict[str, Any]) -> Optional[Response]:
    """
    Custom DRF exception handler that provides consistent API responses.

    This handler integrates with our custom exception handling system
    to provide consistent error responses across the entire API.

    Args:
        exc: The exception that was raised
        context: Context information about where the exception occurred

    Returns:
        Response with consistent error format, or None to use default handling
    """
    # Get the standard DRF response first
    response = drf_exception_handler(exc, context)

    if response is not None:
        # Get the request from context
        request: Optional[Request] = context.get('request')

        if request is not None:
            # Use our custom API response format
            api_resp = api_response(request)

            # Handle different types of exceptions
            if response.status_code == 401:
                # Authentication failed
                error_message = _extract_error_message(response.data)
                return api_resp.unauthorized(message=error_message)

            elif response.status_code == 403:
                # Permission denied
                error_message = _extract_error_message(response.data)
                return api_resp.forbidden(message=error_message)

            elif response.status_code == 400:
                # Validation error
                error_message = _extract_error_message(response.data)
                return api_resp.error(message=error_message, status_code=400)

            elif response.status_code == 404:
                # Not found
                error_message = _extract_error_message(response.data)
                return api_resp.not_found(message=error_message)

            elif response.status_code == 405:
                # Method not allowed
                error_message = _extract_error_message(response.data)
                return api_resp.error(message=error_message, status_code=405)

            elif response.status_code >= 500:
                # Server error
                error_message = _extract_error_message(response.data)
                return api_resp.server_error(message=error_message)

            else:
                # Other client errors
                error_message = _extract_error_message(response.data)
                return api_resp.error(message=error_message, status_code=response.status_code)

    # Return the original response if we can't handle it
    return response


def _extract_error_message(error_data: Any) -> str:
    """
    Extract a meaningful error message from DRF error data.

    Args:
        error_data: The error data from DRF response

    Returns:
        A clean error message string
    """
    if isinstance(error_data, dict):
        # Handle detail field
        if 'detail' in error_data:
            return str(error_data['detail'])

        # Handle field-specific errors
        if 'non_field_errors' in error_data:
            errors = error_data['non_field_errors']
            if isinstance(errors, list) and errors:
                return str(errors[0])
            return str(errors)

        # Handle first field error
        for field, errors in error_data.items():
            if isinstance(errors, list) and errors:
                return f"{field}: {errors[0]}"
            return f"{field}: {errors}"

    elif isinstance(error_data, list) and error_data:
        return str(error_data[0])

    elif isinstance(error_data, str):
        return error_data

    return "An error occurred"