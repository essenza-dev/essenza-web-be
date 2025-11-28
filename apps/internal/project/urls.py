"""
Project API URL Configuration
Maps URL patterns to ProjectViewSet actions
"""

from django.urls import path

from .views import ProjectViewSet


urlpatterns = [
    path(
        "",
        ProjectViewSet.as_view({"post": "create_project", "get": "get_projects"}),
        name="projects",
    ),
    path(
        "/<int:pk>",
        ProjectViewSet.as_view(
            {
                "get": "get_specific_project",
                "put": "update_specific_project",
                "delete": "delete_specific_project",
            }
        ),
        name="specific_project",
    ),
    path(
        "/<int:pk>/toggle",
        ProjectViewSet.as_view({"patch": "toggle_project_status"}),
        name="toggle_project_status",
    ),
    path(
        "/slug/<str:slug>",
        ProjectViewSet.as_view({"get": "get_project_by_slug"}),
        name="project_by_slug",
    ),
    path(
        "/<int:pk>/image",
        ProjectViewSet.as_view({"post": "upload_project_image"}),
        name="upload_project_image",
    ),
    path(
        "/<int:pk>/gallery",
        ProjectViewSet.as_view({"post": "upload_project_gallery"}),
        name="upload_project_gallery",
    ),
    path(
        "/<int:pk>/gallery/<int:index>",
        ProjectViewSet.as_view({"delete": "delete_project_gallery_image"}),
        name="delete_project_gallery_image",
    ),
]
