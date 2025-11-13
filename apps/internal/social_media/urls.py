from django.urls import path

from .views import SocialMediaViewSet

urlpatterns = [
    path(
        "",
        SocialMediaViewSet.as_view(
            {"get": "fetch_social_media", "post": "create_social_media"}
        ),
        name="social_media",
    ),
    path(
        "/<int:pk>",
        SocialMediaViewSet.as_view(
            {
                "get": "specific_social_media",
                "patch": "update_social_media",
                "delete": "delete_social_media",
            }
        ),
        name="specific_social_media",
    ),
]
