from django.urls import path, include

urlpatterns = [
    # V1 API Routes
    path("/v1/auth", include("apps.internal.auth.urls")),
    path("/v1/settings", include("apps.internal.setting.urls")),
    path("/v1/social-media", include("apps.internal.social_media.urls")),
    path("/v1/menus", include("apps.internal.menu.urls")),
    path("/v1/menu-items", include("apps.internal.menu_item.urls")),
    path("/v1/banners", include("apps.internal.banner.urls")),
    path("/v1/subscribers", include("apps.internal.subscriber.urls")),
    path("/v1/pages", include("apps.internal.page.urls")),
    path("/v1/products", include("apps.internal.product.urls")),
    path("/v1/brochures", include("apps.internal.brochure.urls")),
    path("/v1/projects", include("apps.internal.project.urls")),
]
