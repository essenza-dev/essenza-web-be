from django.urls import path

from .views import AuthTokenAPIView, AuthUserViewSet

urlpatterns = [
    path("token", AuthTokenAPIView.as_view(), name="auth_token"),
    path(
        "me",
        AuthUserViewSet.as_view({"get": "get_profile", "patch": "update_profile"}),
        name="auth_user_profile",
    ),
    path(
        "password",
        AuthUserViewSet.as_view({"put": "change_password"}),
        name="auth_user_change_password",
    ),
]
