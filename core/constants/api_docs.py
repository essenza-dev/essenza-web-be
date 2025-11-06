from dataclasses import dataclass

@dataclass
class ApiTags:
    API_GENERAL = "[01] General"
    API_AUTHENTICATION = "[02] Authentication"

@dataclass
class ApiResponseDocs:
    HEALTH_CHECK = {
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
    }

    CREATE_AUTH_TOKEN = {
        200: {
            "description": "Login successful",
            "type": "object",
            "properties": {
                "success": {"type": "boolean", "example": True},
                "status_code": {"type": "integer", "example": 200},
                "message": {"type": "string", "example": "Login successful"},
                "data": {
                    "type": "object",
                    "properties": {
                        "token": {
                            "type": "string",
                            "example": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        },
                        "refresh_token": {
                            "type": "string",
                            "example": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4gZXhhbXBsZQ==",
                        },
                    },
                },
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
        }
    }

    REFRESH_AUTH_TOKEN = {
        200: {
            "description": "Token refreshed successfully",
            "type": "object",
            "properties": {
                "success": {"type": "boolean", "example": True},
                "status_code": {"type": "integer", "example": 200},
                "message": {
                    "type": "string",
                    "example": "Token refreshed successfully",
                },
                "data": {
                    "type": "object",
                    "properties": {
                        "token": {
                            "type": "string",
                            "example": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        },
                        "refresh_token": {
                            "type": "string",
                            "example": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4gZXhhbXBsZQ==",
                        },
                    },
                },
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
        }
    }
