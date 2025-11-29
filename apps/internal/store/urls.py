from django.urls import path

from .views import StoreViewSet


urlpatterns = [
    path(
        "",
        StoreViewSet.as_view({"post": "create_store", "get": "get_stores"}),
    ),
    path(
        "/<int:pk>",
        StoreViewSet.as_view(
            {
                "get": "get_specific_store",
                "put": "update_specific_store",
                "delete": "delete_specific_store",
            }
        ),
    ),
]
