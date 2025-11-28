from django.urls import path

from .views import ArticleViewSet

urlpatterns = [
    path(
        "",
        ArticleViewSet.as_view({"get": "get_articles", "post": "create_article"}),
        name="articles",
    ),
    path(
        "/<int:pk>",
        ArticleViewSet.as_view(
            {
                "get": "get_specific_article",
                "put": "update_specific_article",
                "delete": "delete_specific_article",
            }
        ),
        name="specific_article",
    ),
    path(
        "/slug/<str:slug>",
        ArticleViewSet.as_view({"get": "get_article_by_slug"}),
        name="article_by_slug",
    ),
    path(
        "/<int:pk>/toggle",
        ArticleViewSet.as_view({"patch": "toggle_article_status"}),
        name="toggle_article_status",
    ),
    path(
        "/<int:pk>/publish",
        ArticleViewSet.as_view({"patch": "publish_article"}),
        name="publish_article",
    ),
    path(
        "/<int:pk>/thumbnail",
        ArticleViewSet.as_view({"post": "upload_thumbnail"}),
        name="upload_article_thumbnail",
    ),
]
