from django.urls import path

from .views import DistributorViewSet


urlpatterns = [
    path(
        "",
        DistributorViewSet.as_view(
            {"post": "create_distributor", "get": "get_distributors"}
        ),
    ),
    path(
        "/<int:pk>",
        DistributorViewSet.as_view(
            {
                "get": "get_specific_distributor",
                "put": "update_specific_distributor",
                "delete": "delete_specific_distributor",
            }
        ),
    ),
]
