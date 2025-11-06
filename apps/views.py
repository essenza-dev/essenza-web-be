from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from utils import api_response
from core.constants.api_docs import ApiResponseDocs, ApiTags


@extend_schema(
    summary="Health Check",
    description="Simple health check endpoint to verify API is running",
    responses=ApiResponseDocs.HEALTH_CHECK,
    tags=[ApiTags.API_GENERAL],
    auth=[],
)
@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request: Request) -> Response:
    """
    Health check endpoint to ensure the API is running properly.

    Args:
        request: The HTTP request object

    Returns:
        Response: API health status response
    """
    return api_response(request).success(message="API is healthy")
