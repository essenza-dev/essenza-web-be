from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from utils import api_response
from docs.api.general import GeneralApi


@GeneralApi.health_check
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
