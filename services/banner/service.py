from typing import Tuple

from django.db.models.manager import BaseManager
from core.service import BaseService
from core.models import Banner
from django.core.paginator import Page, Paginator

from . import dto


class BannerService(BaseService):
    """Service class for managing banners."""

    def create_banner(
        self, data: dto.CreateBannerDTO
    ) -> Tuple[Banner, Exception | None]:
        """Create a new banner."""
        try:
            banner = Banner.objects.create(**data.to_dict())
            return banner, None
        except Exception as e:
            return Banner(), e

    def get_banners(self) -> BaseManager[Banner]:
        """Retrieve all banners."""
        return Banner.objects.all()

    def get_paginated_banners(self, str_page_number: str, str_page_size: str) -> Page:
        """Retrieve paginated banners."""
        try:
            page_number = int(str_page_number)
            page_size = int(str_page_size)
        except ValueError:
            page_number = 1
            page_size = 20

        page_number = max(page_number, 1)
        page_size = max(page_size, 1)

        page_size = min(page_size, 100)

        socmeds = Banner.objects.order_by("order_no", "-created_at")

        paginator = Paginator(socmeds, page_size)

        try:
            page = paginator.get_page(page_number)
        except Exception:
            page = paginator.get_page(1)

        return page

    def get_specific_banner(self, pk: int) -> Tuple[Banner, Exception | None]:
        """Retrieve a specific banner by its ID."""
        try:
            banner = Banner.objects.get(id=pk)
            return banner, None
        except Banner.DoesNotExist:
            return Banner(), Exception(f"Banner with id '{pk}' does not exist.")
        except Exception as e:
            return Banner(), e

    def update_specific_banner(
        self, pk: int, data: dto.UpdateBannerDTO
    ) -> Tuple[Banner, Exception | None]:
        """Update a specific banner by its ID."""
        try:
            banner = Banner.objects.get(id=pk)
            for key, value in data.to_dict().items():
                if value is not None:
                    setattr(banner, key, value)
            banner.save()
            return banner, None
        except Banner.DoesNotExist:
            return Banner(), Exception(f"Banner with id '{pk}' does not exist.")
        except Exception as e:
            return Banner(), e

    def delete_specific_banner(self, pk: int):
        """Delete a specific banner by its ID."""
        try:
            banner = Banner.objects.get(id=pk)
            banner.delete()
            return None
        except Banner.DoesNotExist:
            return Exception(f"Banner with id '{pk}' does not exist.")
        except Exception as e:
            return e
