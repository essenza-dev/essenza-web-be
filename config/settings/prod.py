"""
Production Django settings for config project.

This module contains production-specific settings.
"""

from .base import *
import logging.handlers

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Production hosts - must be set via environment
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# CORS settings for production - more restrictive
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")
CORS_ALLOW_CREDENTIALS = True

# Security settings for production
SECURE_SSL_REDIRECT = False  # Disabled for local testing
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Additional security settings
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Strict"
SESSION_COOKIE_SAMESITE = "Strict"

# Cache configuration for production (Redis)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "essenza_cache",
        "TIMEOUT": 300,  # 5 minutes default
    }
}

# Email backend for production
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)
SERVER_EMAIL = os.environ.get("SERVER_EMAIL", EMAIL_HOST_USER)

# Logging configuration for production
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
        "console_warning": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "level": "WARNING",
        },
        "console_error": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "level": "ERROR",
        },
        "mail_admins": {
            "class": "django.utils.log.AdminEmailHandler",
            "level": "CRITICAL",
            "formatter": "detailed",
            "include_html": True,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "core.middleware.request_logging": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "exception_handler": {
            "handlers": ["console_error", "mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django": {
            "handlers": ["console_error"],
            "level": "ERROR",  # Only errors in production
            "propagate": False,
        },
        "django.security": {
            "handlers": ["console_warning", "mail_admins"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

# Override database configuration for production
DATABASES["default"].update({
    "NAME": os.environ.get("DB_NAME", "essenza_db_prod"),
    "OPTIONS": {
        **DATABASES["default"]["OPTIONS"],
        # "init_command": (
        #     "SET sql_mode='STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO';"
        #     "SET innodb_strict_mode=1;"
        #     "SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;"
        #     "SET SESSION time_zone = '+00:00';"
        # ),
    },
})

# Production static files settings
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Media files for production
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Session configuration for production
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_SAVE_EVERY_REQUEST = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Production JWT settings (shorter expiry)
JWT_EXPIRY_SECONDS = int(os.environ.get("JWT_EXPIRY_SECONDS", "3600"))  # 1 hour

# Admin email notifications
ADMINS = [
    ("Admin", os.environ.get("ADMIN_EMAIL", "admin@essenza.com")),
]

MANAGERS = ADMINS

# Performance settings
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB

# Database connection pooling (if using connection pooling)
DATABASES["default"]["CONN_MAX_AGE"] = 60

# Disable debug toolbar in production
if "debug_toolbar" in INSTALLED_APPS:
    INSTALLED_APPS.remove("debug_toolbar")

# Remove debug middleware in production
MIDDLEWARE = [middleware for middleware in MIDDLEWARE
              if "debug_toolbar" not in middleware]
