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
        return _extract_dict_error_message(error_data)
    elif isinstance(error_data, list) and error_data:
        return str(error_data[0])
    elif isinstance(error_data, str):
        return error_data
    return "An error occurred"


def _extract_dict_error_message(error_dict: Dict[str, Any]) -> str:
    """
    Extract error message from dictionary-type error data.

    Args:
        error_dict: Dictionary containing error information

    Returns:
        Formatted error message string
    """
    # Handle detail field
    if 'detail' in error_dict:
        return str(error_dict['detail'])

    # Handle non-field errors
    if 'non_field_errors' in error_dict:
        return _extract_non_field_errors(error_dict['non_field_errors'])

    # Handle first field error
    return _extract_first_field_error(error_dict)


def _extract_non_field_errors(errors: Any) -> str:
    """
    Extract message from non-field errors.

    Args:
        errors: Non-field error data (could be list or other type)

    Returns:
        Error message string
    """
    return str(errors[0]) if isinstance(errors, list) and errors else str(errors)


def _extract_first_field_error(error_dict: Dict[str, Any]) -> str:
    """
    Extract error message from the first field error in dictionary.

    Args:
        error_dict: Dictionary containing field errors

    Returns:
        Formatted field error message
    """
    for field, errors in error_dict.items():
        if isinstance(errors, list) and errors:
            return f"{field}: {errors[0]}"
        return f"{field}: {errors}"
    return "An error occurred"