from django.urls import path

from .views import BannerViewSet


urlpatterns = [
    path("", BannerViewSet.as_view({"post": "create_banner", "get": "get_banners"})),
    path(
        "/<int:pk>",
        BannerViewSet.as_view(
            {
                "get": "get_specific_banner",
                "post": "update_specific_banner",
                "delete": "delete_specific_banner",
            }
        ),
    )
]
