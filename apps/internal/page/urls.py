from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.PageViewSet.as_view({"post": "create_page", "get": "get_pages"}),
        name="pages",
    ),
    path(
        "/<int:pk>",
        views.PageViewSet.as_view(
            {
                "get": "get_specific_page",
                "put": "update_specific_page",
                "delete": "delete_specific_page",
            }
        ),
        name="specific_page",
    ),
    path(
        "/<int:pk>/toggle",
        views.PageViewSet.as_view({"patch": "toggle_page_status"}),
        name="toggle_page_status",
    ),
    path(
        "/slug/<str:slug>",
        views.PageViewSet.as_view({"get": "get_page_by_slug"}),
        name="page_by_slug",
    ),
]
