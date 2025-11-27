from django.urls import path, include

urlpatterns = [
    path("/v1/subscribers", include("apps.public.subscriber.urls")),
]
