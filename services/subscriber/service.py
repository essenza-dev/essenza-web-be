from django.core.paginator import Page

from core.service import BaseService
from core.models import Subscriber


class SubscriberService(BaseService):
    """Service class for managing subscribers."""

    def create_subscriber(self, email: str) -> tuple[Subscriber, Exception | None]:
        """Create a new subscriber."""
        try:
            if Subscriber.objects.filter(email=email).exists():
                return Subscriber(), Exception(
                    "Subscriber with this email already exists."
                )

            subscriber = Subscriber.objects.create(email=email)
            return subscriber, None
        except Exception as e:
            return Subscriber(), e

    def get_paginated_subscribers(
        self, str_page_number: str = "1", str_page_size: str = "20"
    ) -> Page:
        """Retrieve paginated list of subscribers."""
        queryset = Subscriber.objects.order_by("-created_at")
        return self.get_paginated_data(queryset, str_page_number, str_page_size)

    def get_specific_subscriber(self, pk: int) -> tuple[Subscriber, Exception | None]:
        """Retrieve a specific subscriber by its ID."""
        try:
            subscriber = Subscriber.objects.get(pk=pk)
            return subscriber, None
        except Subscriber.DoesNotExist:
            return Subscriber(), Exception(f"Subscriber with id '{pk}' does not exist.")
        except Exception as e:
            return Subscriber(), e

    def delete_specific_subscriber(self, pk: int) -> Exception | None:
        """Delete a specific subscriber by its ID."""
        try:
            subscriber = Subscriber.objects.get(pk=pk)
            subscriber.delete()
            return None
        except Subscriber.DoesNotExist:
            return Exception(f"Subscriber with id '{pk}' does not exist.")
        except Exception as e:
            return e
