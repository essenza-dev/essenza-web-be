from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes


DEFAULT_PAGINATION_PARAMS = [
    OpenApiParameter(
        name="page",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
        description="Page number (default: 1)",
        required=False,
        default=1,
    ),
    OpenApiParameter(
        name="page_size",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
        description="Number of items per page (default: 20, max: 100)",
        required=False,
        default=20,
    ),
]
