from functools import wraps
from drf_spectacular.utils import extend_schema

TAGS = ["Internal / Settings"]


class SettingApi:
    @staticmethod
    def get_settings(func):

        @extend_schema(
            operation_id="int_v1_settings_retrieve",
            tags=TAGS,
            summary="Retrieve Application Settings",
            description="Endpoint to retrieve application settings.",
            auth=[],
            responses={
                200: {
                    "description": "Settings retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Settings retrieved successfully",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "site_name": {
                                    "type": "string",
                                    "example": "My Awesome Site",
                                },
                                "site_description": {
                                    "type": "string",
                                    "example": "A modern web platform for various online services.",
                                },
                                "site_logo": {
                                    "type": "string",
                                    "example": "/static/images/logo.png",
                                },
                                "favicon": {
                                    "type": "string",
                                    "example": "/static/images/favicon.ico",
                                },
                                "meta_keywords": {
                                    "type": "string",
                                    "example": "website, online, platform, services",
                                },
                                "meta_description": {
                                    "type": "string",
                                    "example": "My Awesome Site provides fast and reliable web solutions.",
                                },
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-08T01:15:25.397000+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-08T01:15:25.397000+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-08T01:55:16.063682",
                                }
                            },
                        },
                    },
                }
            },
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
