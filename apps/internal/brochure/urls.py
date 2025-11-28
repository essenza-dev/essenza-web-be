"""
Brochure URL Configuration
"""

from django.urls import path

from .views import BrochureViewSet


urlpatterns = [
    path(
        "", BrochureViewSet.as_view({"post": "create_brochure", "get": "get_brochures"})
    ),
    path(
        "/<int:pk>",
        BrochureViewSet.as_view(
            {
                "get": "get_specific_brochure",
                "put": "update_specific_brochure",
                "delete": "delete_specific_brochure",
            }
        ),
    ),
    path(
        "/<int:pk>/file",
        BrochureViewSet.as_view(
            {
                "post": "upload_brochure_file",
            }
        ),
    ),
]
