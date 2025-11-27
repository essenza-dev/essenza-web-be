from django.urls import path

from .views import SubscriberPublicViewSet

urlpatterns = [
    path("", SubscriberPublicViewSet.as_view({"post": "create_subscriber"})),
]
