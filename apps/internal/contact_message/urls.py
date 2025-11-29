from django.urls import path

from .views import ContactMessageViewSet

urlpatterns = [
    path("", ContactMessageViewSet.as_view({"get": "get_all_contact_messages"})),
    path(
        "/<int:pk>",
        ContactMessageViewSet.as_view(
            {
                "get": "get_specific_contact_message",
                "delete": "delete_contact_message",
            }
        ),
    ),
    path(
        "/<int:pk>/read",
        ContactMessageViewSet.as_view({"patch": "mark_contact_message_as_read"}),
    ),
]
