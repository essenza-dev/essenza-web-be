import mimetypes
from pathlib import Path

from django.conf import settings
from django.http import FileResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from docs.api.general import GeneralApi
from utils import api_response


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


@GeneralApi.retrieve_media
@api_view(["GET"])
@permission_classes([AllowAny])
def retrieve_media(request: Request, file_path: str) -> Response | FileResponse:
    """
    Retrieve and serve media files from the server.

    This endpoint handles media file requests, performing security checks
    and returning the requested file if found and accessible.

    Args:
        request (Request): The Django REST framework request object
        file_path (str): Relative path to the requested media file

    Returns:
        Union[Response, FileResponse]: FileResponse with the media file if successful,
                                     or Response with error details if failed

    Raises:
        Returns error responses for:
        - 404: File not found or is a directory
        - 403: Access denied (path traversal attempt)
        - 500: Internal server error
    """
    try:
        # Construct full file path efficiently
        base_media_path = Path(settings.BASE_DIR, settings.FILE_UPLOAD_BASE_DIR)
        file_location = Path.joinpath(base_media_path, file_path)

        # Early validation: check if path is a valid file
        if not file_location.is_file():
            return api_response(request).error(
                message=f"File not found: {file_path}", status_code=404
            )

        # Security validation: prevent directory traversal attacks
        try:
            file_location.resolve().relative_to(base_media_path.resolve())
        except ValueError:
            return api_response(request).error(message="Access denied", status_code=403)

        # Determine MIME type with fallback
        mime_type = (
            mimetypes.guess_type(str(file_location))[0] or "application/octet-stream"
        )

        # Extract filename once for reuse
        filename = file_location.name

        # Create optimized file response
        response = FileResponse(
            open(file_location, "rb"),
            content_type=mime_type,
            filename=filename,
        )

        # Set content disposition header for proper browser handling
        response["Content-Disposition"] = f'inline; filename="{filename}"'

        return response

    except (OSError, IOError) as e:
        # Handle file system related errors specifically
        return api_response(request).error(
            message=f"File access error: {str(e)}", status_code=500
        )
    except Exception as e:
        # Handle any other unexpected errors
        return api_response(request).error(
            message=f"Unexpected error retrieving file: {str(e)}", status_code=500
        )
