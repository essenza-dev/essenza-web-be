from django.urls import path

from .views import SubscriberViewSet

urlpatterns = [
    path("", SubscriberViewSet.as_view({"get": "get_all_subscribers"})),
    path(
        "/<int:pk>",
        SubscriberViewSet.as_view(
            {"get": "get_specific_subscriber", "delete": "delete_subscriber"}
        ),
    ),
]
