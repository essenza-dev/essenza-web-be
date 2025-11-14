from functools import wraps
from drf_spectacular.utils import extend_schema

from apps.internal.setting import serializers

TAGS = ["Internal / Settings"]


class SettingApi:
    @staticmethod
    def create_setting(func):

        @extend_schema(
            operation_id="int_v1_setting_create",
            tags=TAGS,
            summary="Create new Application Settings",
            description="Endpoint to create or update application settings.",
            request=serializers.PostCreateSettingRequest,
            responses={
                201: {
                    "description": "Setting created successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 201},
                        "message": {
                            "type": "string",
                            "example": "Setting created successfully",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 3},
                                "slug": {"type": "string", "example": "site-logo"},
                                "label": {"type": "string", "example": "Site Logo"},
                                "value": {
                                    "type": "string",
                                    "example": "https://mysite.com/assets/logo.png",
                                },
                                "description": {"type": "string", "example": ""},
                                "is_active": {"type": "boolean", "example": True},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-14T02:40:02.893665+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-14T02:40:02.893714+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-14T02:40:02.902052",
                                },
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
    def get_complete_settings(func):
        @extend_schema(
            operation_id="int_v1_complete_settings_retrieve",
            tags=TAGS,
            summary="Retrieve Application Settings",
            description="Endpoint to retrieve application settings.",
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
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "example": 3},
                                    "slug": {"type": "string", "example": "site-logo"},
                                    "label": {"type": "string", "example": "Site Logo"},
                                    "value": {
                                        "type": "string",
                                        "example": "https://mysite.com/assets/logo.png",
                                    },
                                    "description": {"type": "string", "example": ""},
                                    "is_active": {"type": "boolean", "example": True},
                                    "created_at": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2025-11-14T02:40:02.893665+07:00",
                                    },
                                    "updated_at": {
                                        "type": "string",
                                        "format": "date-time",
                                        "example": "2025-11-14T02:40:02.893714+07:00",
                                    },
                                },
                            },
                            "example": [
                                {
                                    "id": 3,
                                    "slug": "site-logo",
                                    "label": "Site Logo",
                                    "value": "https://mysite.com/assets/logo.png",
                                    "description": "",
                                    "is_active": True,
                                    "created_at": "2025-11-14T02:40:02.893665+07:00",
                                    "updated_at": "2025-11-14T02:40:02.893714+07:00",
                                },
                                {
                                    "id": 1,
                                    "slug": "meta-description",
                                    "label": "Meta Description",
                                    "value": "string",
                                    "description": "string",
                                    "is_active": True,
                                    "created_at": "2025-11-14T02:33:44.512794+07:00",
                                    "updated_at": "2025-11-14T02:33:44.512821+07:00",
                                },
                            ],
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-14T02:43:57.268135",
                                },
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
    def get_specific_setting(func):
        @extend_schema(
            operation_id="int_v1_specific_setting_retrieve",
            tags=TAGS,
            summary="Retrieve Specific Application Setting",
            description="Endpoint to retrieve a specific application setting by its slug.",
            responses={
                200: {
                    "description": "Setting retrieved successfully",
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "status_code": {"type": "integer", "example": 200},
                        "message": {
                            "type": "string",
                            "example": "Setting retrieved successfully",
                        },
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 3},
                                "slug": {"type": "string", "example": "site-logo"},
                                "label": {"type": "string", "example": "Site Logo"},
                                "value": {
                                    "type": "string",
                                    "format": "uri",
                                    "example": "https://mysite.com/assets/logo.png",
                                },
                                "description": {"type": "string", "example": ""},
                                "is_active": {"type": "boolean", "example": True},
                                "created_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-14T02:40:02.893665+07:00",
                                },
                                "updated_at": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-14T02:40:02.893714+07:00",
                                },
                            },
                        },
                        "meta": {
                            "type": "object",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "example": "2025-11-14T02:47:35.550732",
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
