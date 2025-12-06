from functools import wraps
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from apps.internal.product_variant import serializers

TAGS = ["Internal / Product Variant"]


class ProductVariantAPI:
    """API schema definitions for Product Variant endpoints."""

    @staticmethod
    def create_product_variant_schema(func):
        """Schema for creating a new product variant."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_product_variant_create",
            summary="Create Product Variant",
            description="Create a new variant for a specific product with SKU, model, size, description, optional image, and optional specifications. Use multipart/form-data for image upload. Specifications should be sent as JSON array in 'specifications' field.",
            request={
                "multipart/form-data": serializers.PostCreateProductVariantRequest
            },
            parameters=[
                OpenApiParameter(
                    name="product_slug",
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.PATH,
                    description="Product slug to create variant for",
                    required=True,
                )
            ],
            responses={
                200: {
                    "description": "Product variant created successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Product variant created successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "product": {"type": "integer", "example": 1},
                                "product_name": {"type": "string", "example": "Premium Ceramic Floor Tile"},
                                "product_slug": {"type": "string", "example": "premium-ceramic-floor-tile"},
                                "sku": {"type": "string", "example": "CT-FL-001-60X60"},
                                "model": {"type": "string", "example": "CT-FL-001"},
                                "size": {"type": "string", "example": "60x60 cm"},
                                "description": {"type": "string", "example": "Premium ceramic floor tile in 60x60cm size"},
                                "image": {"type": "string", "example": "/media/uploads/products/variants/variant-001.jpg"},
                                "is_active": {"type": "boolean", "example": True},
                                "specifications": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "integer", "example": 1},
                                            "specification": {"type": "integer", "example": 1},
                                            "specification_slug": {"type": "string", "example": "color"},
                                            "specification_label": {"type": "string", "example": "Color"},
                                            "specification_icon": {"type": "string", "example": "palette"},
                                            "value": {"type": "string", "example": "White"},
                                            "is_active": {"type": "boolean", "example": True},
                                        },
                                    },
                                    "example": [
                                        {
                                            "id": 1,
                                            "specification": 1,
                                            "specification_slug": "color",
                                            "specification_label": "Color",
                                            "specification_icon": "palette",
                                            "value": "White",
                                            "is_active": True,
                                        },
                                        {
                                            "id": 2,
                                            "specification": 2,
                                            "specification_slug": "thickness",
                                            "specification_label": "Thickness",
                                            "specification_icon": "layers",
                                            "value": "8mm",
                                            "is_active": True,
                                        },
                                    ],
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.000000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.770300",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Business validation error",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Product variant with SKU 'CT-FL-001-60X60' already exists.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.498145",
                                }
                            },
                        },
                    },
                },
                404: {
                    "description": "Product not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 404},
                        "message": {
                            "type": "string",
                            "example": "Product with slug 'premium-ceramic-floor-tile' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.498145",
                                }
                            },
                        },
                    },
                },
                422: {
                    "description": "Data validation failed",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 422},
                        "message": {
                            "type": "string",
                            "example": "Data validation failed",
                        },
                        "errors": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "field": {
                                        "type": "string",
                                        "example": "sku",
                                    },
                                    "message": {
                                        "type": "string",
                                        "example": "Ensure this field has no more than 100 characters.",
                                    },
                                    "code": {
                                        "type": "string",
                                        "example": "max_length",
                                    },
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.498145",
                                }
                            },
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def get_product_variants_by_slug_schema(func):
        """Schema for retrieving all variants for a specific product by slug."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_product_variant_get_by_slug",
            summary="Get Product Variants by Slug",
            description="Retrieve all variants for a specific product using product slug.",
            parameters=[
                OpenApiParameter(
                    name="product_slug",
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.PATH,
                    description="Product slug to get variants for",
                    required=True,
                )
            ],
            responses={
                200: {
                    "description": "Product variants retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Product variants retrieved successfully.",
                        },
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "example": 1},
                                    "product": {"type": "integer", "example": 1},
                                    "product_name": {"type": "string", "example": "Premium Ceramic Floor Tile"},
                                    "product_slug": {"type": "string", "example": "premium-ceramic-floor-tile"},
                                    "sku": {"type": "string", "example": "CT-FL-001-60X60"},
                                    "model": {"type": "string", "example": "CT-FL-001"},
                                    "size": {"type": "string", "example": "60x60 cm"},
                                    "description": {"type": "string", "example": "Premium ceramic floor tile"},
                                    "image": {"type": "string", "example": "/media/uploads/products/variants/variant-001.jpg"},
                                    "is_active": {"type": "boolean", "example": True},
                                    "specifications": {"type": "array", "items": {"type": "object"}},
                                    "created_at": {"type": "string", "format": "date-time", "example": "2025-12-06T10:00:00.000000+07:00"},
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.770300",
                                }
                            },
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def get_specific_product_variant_schema(func):
        """Schema for retrieving a specific product variant by ID."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_product_variant_get_specific",
            summary="Get Specific Product Variant",
            description="Retrieve a specific product variant by its ID with all specifications.",
            responses={
                200: {
                    "description": "Product variant retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Product variant retrieved successfully.",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "product": {"type": "integer", "example": 1},
                                "product_name": {"type": "string", "example": "Premium Ceramic Floor Tile"},
                                "product_slug": {"type": "string", "example": "premium-ceramic-floor-tile"},
                                "sku": {"type": "string", "example": "CT-FL-001-60X60"},
                                "model": {"type": "string", "example": "CT-FL-001"},
                                "size": {"type": "string", "example": "60x60 cm"},
                                "description": {"type": "string", "example": "Premium ceramic floor tile"},
                                "image": {"type": "string", "example": "/media/uploads/products/variants/variant-001.jpg"},
                                "is_active": {"type": "boolean", "example": True},
                                "specifications": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "integer", "example": 1},
                                            "specification": {"type": "integer", "example": 1},
                                            "specification_slug": {"type": "string", "example": "color"},
                                            "specification_label": {"type": "string", "example": "Color"},
                                            "specification_icon": {"type": "string", "example": "palette"},
                                            "value": {"type": "string", "example": "White"},
                                            "is_active": {"type": "boolean", "example": True},
                                            "created_at": {"type": "string", "format": "date-time"},
                                            "updated_at": {"type": "string", "format": "date-time"},
                                        },
                                    },
                                },
                                "created_at": {"type": "string", "format": "date-time", "example": "2025-12-06T10:00:00.000000+07:00"},
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.770300",
                                }
                            },
                        },
                    },
                },
                404: {
                    "description": "Product variant not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 404},
                        "message": {
                            "type": "string",
                            "example": "Product variant with id '99' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.498145",
                                }
                            },
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def update_specific_product_variant_schema(func):
        """Schema for updating a specific product variant."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_product_variant_update",
            summary="Update Product Variant",
            description="Update a specific product variant with partial data support. All fields are optional. Use multipart/form-data for image upload.",
            request={
                "multipart/form-data": serializers.PutUpdateProductVariantRequest
            },
            responses={
                200: {
                    "description": "Product variant updated successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Product variant updated successfully.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.770300",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Business validation error",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Product variant with SKU 'CT-FL-001-60X60' already exists.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.498145",
                                }
                            },
                        },
                    },
                },
                404: {
                    "description": "Product variant not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 404},
                        "message": {
                            "type": "string",
                            "example": "Product variant with id '99' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.498145",
                                }
                            },
                        },
                    },
                },
                422: {
                    "description": "Data validation failed",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 422},
                        "message": {
                            "type": "string",
                            "example": "Data validation failed",
                        },
                        "errors": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "field": {
                                        "type": "string",
                                        "example": "model",
                                    },
                                    "message": {
                                        "type": "string",
                                        "example": "Ensure this field has no more than 100 characters.",
                                    },
                                    "code": {
                                        "type": "string",
                                        "example": "max_length",
                                    },
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.498145",
                                }
                            },
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def delete_specific_product_variant_schema(func):
        """Schema for deleting a specific product variant."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_product_variant_delete",
            summary="Delete Product Variant",
            description="Delete a specific product variant and its associated specifications.",
            responses={
                200: {
                    "description": "Product variant deleted successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Product variant deleted successfully.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.770300",
                                }
                            },
                        },
                    },
                },
                404: {
                    "description": "Product variant not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 404},
                        "message": {
                            "type": "string",
                            "example": "Product variant with id '99' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.498145",
                                }
                            },
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def toggle_product_variant_status_schema(func):
        """Schema for toggling product variant active status."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_product_variant_toggle_status",
            summary="Toggle Product Variant Status",
            description="Toggle the active status of a product variant.",
            request=serializers.PatchToggleProductVariantStatusRequest,
            responses={
                200: {
                    "description": "Product variant status updated successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Product variant status updated successfully.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.770300",
                                }
                            },
                        },
                    },
                },
                404: {
                    "description": "Product variant not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 404},
                        "message": {
                            "type": "string",
                            "example": "Product variant with id '99' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.498145",
                                }
                            },
                        },
                    },
                },
                422: {
                    "description": "Data validation failed",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 422},
                        "message": {
                            "type": "string",
                            "example": "Data validation failed",
                        },
                        "errors": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "field": {
                                        "type": "string",
                                        "example": "is_active",
                                    },
                                    "message": {
                                        "type": "string",
                                        "example": "This field is required.",
                                    },
                                    "code": {
                                        "type": "string",
                                        "example": "required",
                                    },
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.498145",
                                }
                            },
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def update_product_variant_specifications_schema(func):
        """Schema for updating product variant specifications."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_product_variant_update_specifications",
            summary="Update Product Variant Specifications",
            description="Add or update specifications for a product variant.",
            request=serializers.PostUpdateProductVariantSpecificationsRequest,
            responses={
                200: {
                    "description": "Product variant specifications updated successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Product variant specifications updated successfully.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.770300",
                                }
                            },
                        },
                    },
                },
                400: {
                    "description": "Business validation error",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 400},
                        "message": {
                            "type": "string",
                            "example": "Specification with slug 'invalid-spec' does not exist or is inactive.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.498145",
                                }
                            },
                        },
                    },
                },
                404: {
                    "description": "Product variant not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 404},
                        "message": {
                            "type": "string",
                            "example": "Product variant with id '99' does not exist.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.498145",
                                }
                            },
                        },
                    },
                },
                422: {
                    "description": "Data validation failed",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 422},
                        "message": {
                            "type": "string",
                            "example": "Data validation failed",
                        },
                        "errors": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "field": {
                                        "type": "string",
                                        "example": "specifications",
                                    },
                                    "message": {
                                        "type": "string",
                                        "example": "This field is required.",
                                    },
                                    "code": {
                                        "type": "string",
                                        "example": "required",
                                    },
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.498145",
                                }
                            },
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def delete_product_variant_specification_schema(func):
        """Schema for deleting a product variant specification."""

        @extend_schema(
            tags=TAGS,
            operation_id="int_v1_product_variant_delete_specification",
            summary="Delete Product Variant Specification",
            description="Delete a specific specification from a product variant by specification slug.",
            parameters=[
                OpenApiParameter(
                    name="spec_slug",
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.PATH,
                    description="Specification slug to delete",
                    required=True,
                ),
            ],
            responses={
                200: {
                    "description": "Product variant specification deleted successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Product variant specification deleted successfully.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.770300",
                                }
                            },
                        },
                    },
                },
                404: {
                    "description": "Specification not found",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "status_code": {"type": "integer", "example": 404},
                        "message": {
                            "type": "string",
                            "example": "Product specification with slug 'color' does not exist for variant '1'.",
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-12-06T10:00:00.498145",
                                }
                            },
                        },
                    },
                },
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper