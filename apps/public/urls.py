from django.urls import path, include

urlpatterns = [
    path("/v1/subscribers", include("apps.public.subscriber.urls")),
    path("/v1/contact-messages", include("apps.public.contact_message.urls")),
    path("/v1/contact-messages", include("apps.public.contact_message.urls")),
]
