from django.urls import path

from .views import ContactMessagePublicViewSet

urlpatterns = [
    path("", ContactMessagePublicViewSet.as_view({"post": "create_contact_message"})),
]
