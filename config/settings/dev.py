"""
Development Django settings for config project.

This module contains development-specific settings.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "*",  # Allow all hosts in development (use with caution)
]

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Security settings - relaxed for development
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_BROWSER_XSS_FILTER = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Cache configuration for development (using dummy cache)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Email backend for development (console backend)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Logging configuration for development
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "[{asctime}] {levelname:<8} {name:<30} | {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "{levelname} | {message}",
            "style": "{",
        },
        "request": {
            "format": "[{asctime}] {levelname:<8} REQUEST | {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "level": "INFO",
        },
        "request_console": {
            "class": "logging.StreamHandler",
            "formatter": "request",
            "level": "INFO",
        },
        "exception_file": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "exceptions_dev.log",
            "formatter": "detailed",
            "level": "ERROR",
        },
        "exception_console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "level": "ERROR",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
    "loggers": {
        "core.middleware.request_logging": {
            "handlers": ["request_console"],
            "level": "INFO",
            "propagate": False,
        },
        "exception_handler": {
            "handlers": ["exception_console", "exception_file"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.server": {
            "handlers": [],
            "level": "INFO",
            "propagate": False,
        },
        "django": {
            "handlers": ["console"],
            "level": "WARNING",  # Hanya WARNING ke atas
            "propagate": False,
        },
    },
}

# Development-specific settings
INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

# Django Debug Toolbar (if installed)
if "debug_toolbar" in INSTALLED_APPS:
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
    }

# Override database name for development
DATABASES["default"]["NAME"] = os.environ.get("DB_NAME", "essenza_db_dev")

# Development JWT expiry (longer for convenience)
JWT_EXPIRY_SECONDS = int(os.environ.get("JWT_EXPIRY_SECONDS", "86400"))  # 1 day
