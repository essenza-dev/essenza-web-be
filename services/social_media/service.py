from typing import Tuple
from django.core.paginator import Page, Paginator

from core.service import BaseService
from core.models import SocialMedia


class SocialMediaService(BaseService):
    """
    Service class for managing social media entities and operations
    """

    def get_social_media_list(
        self, str_page_number: str = "1", str_page_size: str = "20"
    ) -> Page:
        """
        Retrieve a paginated list of social media entries ordered by order_no and created_at
        """
        try:
            page_number = int(str_page_number)
            page_size = int(str_page_size)
        except ValueError:
            page_number = 1
            page_size = 20

        page_number = max(page_number, 1)
        page_size = max(page_size, 1)

        page_size = min(page_size, 100)

        socmeds = SocialMedia.objects.order_by("order_no", "-created_at")

        paginator = Paginator(socmeds, page_size)

        try:
            page = paginator.get_page(page_number)
        except Exception:
            page = paginator.get_page(1)

        return page

    def create_social_media(self, **data) -> SocialMedia:
        """
        Create a new social media entry with the provided data
        """
        return SocialMedia.objects.create(**data)

    def get_social_media_by_id(
        self, pk: int
    ) -> Tuple[SocialMedia | None, Exception | None]:
        """
        Retrieve a specific social media entry by its primary key
        """
        try:
            socmed = SocialMedia.objects.get(pk=pk)
            return socmed, None
        except SocialMedia.DoesNotExist:
            return None, Exception("Social media entry not found")
        except Exception as e:
            return None, e

    def update_social_media(
        self, pk: int, **data
    ) -> Tuple[SocialMedia | None, Exception | None]:
        """
        Update an existing social media entry identified by pk with the provided data
        """
        try:
            socmed = SocialMedia.objects.get(pk=pk)
            for key, value in data.items():
                setattr(socmed, key, value)
            socmed.save()
            return socmed, None
        except SocialMedia.DoesNotExist:
            return None, Exception("Social media entry not found")
        except Exception as e:
            return None, e

    def delete_social_media(self, pk: int) -> Exception | None:
        """
        Delete a specific social media entry by its primary key
        """
        try:
            socmed = SocialMedia.objects.get(pk=pk)
            socmed.delete()
            return None
        except SocialMedia.DoesNotExist:
            return Exception("Social media entry not found")
        except Exception as e:
            return e
