from abc import ABC
from django.core.paginator import Page, Paginator
from django.db.models import QuerySet


class BaseService(ABC):
    """Base class for all services."""

    def get_paginated_data(
        self,
        queryset: QuerySet,
        str_page_number: str = "1",
        str_page_size: str = "20"
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