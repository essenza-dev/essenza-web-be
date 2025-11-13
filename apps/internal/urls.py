from django.urls import path, include

urlpatterns = [
    # V1 API Routes
    path("/v1/auth", include("apps.internal.auth.urls")),
    path("/v1/settings", include("apps.internal.setting.urls")),
    path("/v1/social-media", include("apps.internal.social_media.urls")),
]
