"""
Custom decorators for request data validation.

This module provides decorators for automatic request data validation
using Django REST Framework serializers with consistent response format
using utils.response.
"""

import contextlib
from functools import wraps
from typing import Type, Callable, Any, Optional, List, Dict
from enum import Enum

from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from django.http import QueryDict

from utils.response import api_response


class DataSource(Enum):
    """Enum for request data sources."""

    BODY = "body"
    QUERY_PARAMS = "query_params"


def _extract_request_from_args(*args, **kwargs) -> Request:
    """
    Extract Request object from function arguments.

    Args:
        *args: Function arguments
        **kwargs: Function keyword arguments

    Returns:
        Request object

    Raises:
        ValueError: If Request object is not found
    """
    # Check class-based view: args[0] = self, args[1] = request
    if len(args) >= 2 and hasattr(args[1], "method"):
        return args[1]

    # Check function-based view: args[0] = request
    if args and hasattr(args[0], "method"):
        return args[0]

    # Fallback: check kwargs
    request = kwargs.get("request")
    if request and isinstance(request, Request):
        return request

    raise ValueError(
        "Request object not found. Make sure to use this decorator on view functions/methods."
    )


def _get_data_from_source(
    request: Request, data_source: DataSource | str
) -> Dict[str, Any] | QueryDict | Any:
    """
    Get data from specified source.

    Args:
        request: Django REST Framework Request object
        data_source: Source of data (body or query_params)

    Returns:
        Data from the specified source (could be dict, QueryDict, or other data types)

    Raises:
        ValueError: If data_source is invalid
    """
    source = (
        DataSource(data_source.lower()) if isinstance(data_source, str) else data_source
    )

    if source == DataSource.BODY:
        return request.data
    elif source == DataSource.QUERY_PARAMS:
        return request.query_params
    else:
        raise ValueError(f"Invalid data_source: {data_source}")


def _clean_captcha_fields(validated_data: Any, serializer: Any) -> Dict[str, Any]:
    """
    Remove CAPTCHA fields from validated data if serializer extends UseCaptchaSerializer.

    Args:
        validated_data: The validated data (can be dict, QueryDict, or other)
        serializer: The serializer instance

    Returns:
        Cleaned validated data without CAPTCHA fields
    """
    with contextlib.suppress(ImportError):
        # Check if serializer is instance of or inherits from UseCaptchaSerializer
        from utils.captcha.serializers import UseCaptchaSerializer

        if isinstance(serializer, UseCaptchaSerializer):
            # Convert to dict and create a copy to remove CAPTCHA fields
            if hasattr(validated_data, "dict"):
                # Handle QueryDict
                cleaned_data = validated_data.dict()
            else:
                # Handle regular dict or other dict-like objects
                cleaned_data = dict(validated_data) if validated_data else {}

            # Remove CAPTCHA fields
            cleaned_data.pop("captcha_token", None)
            cleaned_data.pop("captcha_version", None)
            return cleaned_data

    # Return original data as dict if not a CAPTCHA serializer
    if hasattr(validated_data, "dict"):
        return validated_data.dict()
    else:
        return dict(validated_data) if validated_data else {}


def validate_request(
    serializer_class: Type[serializers.Serializer],
    data_source: DataSource | str = DataSource.BODY,
) -> Callable[[Callable[..., Response]], Callable[..., Response]]:
    """
    Decorator for automatic request data validation using serializer.

    Args:
        serializer_class: Serializer class for data validation
        data_source: Data source - 'body' for request.data or 'query_params' for request.query_params

    Returns:
        Decorated function that performs automatic validation

    Usage:
        @validate_request(MySerializer, DataSource.BODY)
        def my_view(self, request, validated_data):
            # validated_data is already validated
            return api_response(request).success(data=validated_data)

        @validate_request(MyQuerySerializer, DataSource.QUERY_PARAMS)
        def my_search_view(self, request, validated_data):
            # query params are already validated
            return api_response(request).success(data=search_results)
    """

    def decorator(view_func: Callable[..., Response]) -> Callable[..., Response]:
        @wraps(view_func)
        def wrapper(*args, **kwargs) -> Response:
            request = _extract_request_from_args(*args, **kwargs)
            data = _get_data_from_source(request, data_source)

            # Initialize serializer with data
            serializer = serializer_class(data=data)

            # Validate data
            if not serializer.is_valid():
                return api_response(request).validation_error(
                    errors=serializer.errors, message="Data validation failed"
                )

            # Clean validated data for CAPTCHA serializers
            cleaned_data = _clean_captcha_fields(serializer.validated_data, serializer)

            # Add cleaned validated_data to kwargs
            kwargs["validated_data"] = cleaned_data

            # Call original function with validated_data
            return view_func(*args, **kwargs)

        return wrapper

    return decorator


def validate_body(
    serializer_class: Type[serializers.Serializer],
) -> Callable[[Callable[..., Response]], Callable[..., Response]]:
    """
    Shortcut decorator for request body validation.

    Args:
        serializer_class: Serializer class for data validation

    Returns:
        Decorated function

    Usage:
        @validate_body(MySerializer)
        def my_view(self, request, validated_data):
            return api_response(request).success(data=validated_data)
    """
    return validate_request(serializer_class, DataSource.BODY)


def validate_query_params(
    serializer_class: Type[serializers.Serializer],
) -> Callable[[Callable[..., Response]], Callable[..., Response]]:
    """
    Shortcut decorator for query parameters validation.

    Args:
        serializer_class: Serializer class for data validation

    Returns:
        Decorated function

    Usage:
        @validate_query_params(MyQuerySerializer)
        def my_search_view(self, request, validated_data):
            return api_response(request).success(data=search_results)
    """
    return validate_request(serializer_class, DataSource.QUERY_PARAMS)


def validate_request_with_context(
    serializer_class: Type[serializers.Serializer],
    data_source: DataSource | str = DataSource.BODY,
    context_keys: Optional[List[str]] = None,
) -> Callable[[Callable[..., Response]], Callable[..., Response]]:
    """
    Decorator for request data validation with additional context.

    Args:
        serializer_class: Serializer class for data validation
        data_source: Request data source
        context_keys: List of keys to be taken from kwargs and passed to serializer context

    Returns:
        Decorated function

    Usage:
        @validate_request_with_context(MySerializer, DataSource.BODY, ['user_id'])
        def my_view(self, request, validated_data, user_id=None):
            # validated_data is already validated with user_id context
            return api_response(request).success(data=validated_data)
    """

    def decorator(view_func: Callable[..., Response]) -> Callable[..., Response]:
        @wraps(view_func)
        def wrapper(*args, **kwargs) -> Response:
            request = _extract_request_from_args(*args, **kwargs)
            data = _get_data_from_source(request, data_source)

            # Build context for serializer
            context: Dict[str, Any] = {"request": request}

            # Add context keys if provided
            if context_keys:
                context.update(
                    {key: kwargs[key] for key in context_keys if key in kwargs}
                )

            # Initialize serializer with data and context
            serializer = serializer_class(data=data, context=context)

            # Validate data
            if not serializer.is_valid():
                return api_response(request).validation_error(
                    errors=serializer.errors, message="Data validation failed"
                )

            # Clean validated data for CAPTCHA serializers
            cleaned_data = _clean_captcha_fields(serializer.validated_data, serializer)

            # Add cleaned validated_data to kwargs
            kwargs["validated_data"] = cleaned_data

            return view_func(*args, **kwargs)

        return wrapper

    return decorator
