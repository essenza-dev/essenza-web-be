from django.urls import path

from .views import SpecificationViewSet


urlpatterns = [
    path(
        "",
        SpecificationViewSet.as_view({"get": "get_specifications"}),
        name="specifications",
    ),
    path(
        "/<str:slug>",
        SpecificationViewSet.as_view(
            {
                "get": "get_specific_specification",
                "put": "update_specific_specification",
            }
        ),
        name="specific_specification",
    ),
]
