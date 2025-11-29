from __future__ import annotations

from abc import ABC
from copy import copy
from functools import wraps
from typing import Any, Callable, TypeVar, Union, cast

from django.core.paginator import Page, Paginator
from django.db.models import QuerySet
from rest_framework.request import Request

# TypeVar for proper return type annotation
T = TypeVar("T", bound="BaseService")

# Sentinel object to detect unset context state
_UNSET_CONTEXT: object = object()


def required_context(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to ensure that the service method has a valid context.

    This decorator checks if self.ctx is not None before executing the method.
    If ctx is None, it raises a ValueError with a descriptive message.

    Args:
        func: The method to be decorated

    Returns:
        The decorated method

    Raises:
        ValueError: If self.ctx is None when the method is called

    Example:
        class AuthService(BaseService):
            @required_context
            def get_current_user(self):
                # This method requires context to be set
                return self.ctx.user
    """

    @wraps(func)
    def wrapper(self: BaseService, *args: Any, **kwargs: Any) -> Any:
        if self._ctx is _UNSET_CONTEXT:
            raise ValueError(
                f"Context is required for {self.__class__.__name__}.{func.__name__}(). "
                f"Please call use_context(request) first."
            )
        return func(self, *args, **kwargs)

    return wrapper


class BaseService(ABC):
    """Base class for all services."""

    __slots__ = ("_ctx",)

    def __init__(self) -> None:
        """Initialize the service with unset context state."""
        self._ctx: Union[Request, object] = _UNSET_CONTEXT

    @property
    def ctx(self) -> Request:
        """Get the request context. Type-safe access that assumes context is set."""
        return cast(Request, self._ctx)

    def get_paginated_data(
        self, queryset: QuerySet, str_page_number: str = "1", str_page_size: str = "20"
    ) -> Page:
        """Retrieve paginated data from any queryset.

        Args:
            queryset: Django QuerySet to paginate
            str_page_number: Page number as string (default: "1")
            str_page_size: Page size as string (default: "20")

        Returns:
            Page: Django Paginator Page object
        """
        try:
            page_number = int(str_page_number)
            page_size = int(str_page_size)
        except ValueError:
            page_number = 1
            page_size = 20

        page_number = max(page_number, 1)
        page_size = max(page_size, 1)
        page_size = min(page_size, 100)  # Maximum page size limit

        paginator = Paginator(queryset, page_size)

        try:
            page = paginator.get_page(page_number)
        except Exception:
            page = paginator.get_page(1)

        return page

    def use_context(self: T, ctx: Request) -> T:
        """Create a copy of the service with the given context.

        This method creates a shallow copy of the current service instance
        and sets the context, allowing for method chaining while maintaining
        immutability of the original instance.

        Args:
            ctx: Django Request object to set as context

        Returns:
            A new instance of the same service class with context set

        Example:
            service = AuthService().use_context(request)
            # or with chaining:
            result = AuthService().use_context(request).some_method()
        """
        # Create a shallow copy of the current instance
        new_instance = copy(self)
        new_instance._ctx = ctx
        return new_instance
