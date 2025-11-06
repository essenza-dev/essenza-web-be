from django.urls import path

from .views import (
    AuthTokenAPIView,
)

urlpatterns = [
    path("token", AuthTokenAPIView.as_view(), name="auth_token"),
]