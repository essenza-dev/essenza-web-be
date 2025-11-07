from functools import wraps
from drf_spectacular.utils import extend_schema

TAGS = "[01] General"


class GeneralApi:
    """
    Documentation configuration for General API endpoints
    """

    @staticmethod
    def health_check(func):
        """
        Decorator for health check endpoint documentation
        """

        @extend_schema(
            tags=[TAGS],
            summary="Health Check",
            description="Simple health check endpoint to verify API is running",
            auth=[],
            responses={
                200: {
                    "description": "API is healthy",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {"type": "string", "example": "API is healthy"},
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-05T17:39:56.395438",
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
