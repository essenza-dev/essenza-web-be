from django.urls import path

from .views import ProductVariantViewSet


urlpatterns = [
    # Create variant for a product
    path(
        "/products/<str:product_slug>/variants",
        ProductVariantViewSet.as_view({"post": "create_product_variant"}),
        name="create_product_variant",
    ),
    # Get all variants by product slug
    path(
        "/products/<str:product_slug>/variants",
        ProductVariantViewSet.as_view({"get": "get_product_variants_by_slug"}),
        name="get_product_variants_by_slug",
    ),
    # Get, Update, Delete specific variant
    path(
        "/<int:pk>",
        ProductVariantViewSet.as_view(
            {
                "get": "get_specific_product_variant",
                "put": "update_specific_product_variant",
                "delete": "delete_specific_product_variant",
            }
        ),
        name="specific_product_variant",
    ),
    # Toggle variant status
    path(
        "/<int:pk>/toggle",
        ProductVariantViewSet.as_view({"patch": "toggle_product_variant_status"}),
        name="toggle_product_variant_status",
    ),
    # Update variant specifications
    path(
        "/<int:pk>/specifications",
        ProductVariantViewSet.as_view(
            {"post": "update_product_variant_specifications"}
        ),
        name="update_product_variant_specifications",
    ),
    # Delete variant specification
    path(
        "/<int:pk>/specifications/<str:spec_slug>",
        ProductVariantViewSet.as_view(
            {"delete": "delete_product_variant_specification"}
        ),
        name="delete_product_variant_specification",
    ),
]
