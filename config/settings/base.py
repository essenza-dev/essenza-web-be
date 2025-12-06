"""
Base Django settings for config project.

This module contains settings shared across all environments.
"""

from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SILENCED_SYSTEM_CHECKS = ["urls.W002"]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# Application definition
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps
    "rest_framework",
    "drf_spectacular",
    # Local apps
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.request_logging.RequestLoggingMiddleware",
]

ROOT_URLCONF = "apps.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database configuration for MySQL/MariaDB 10.3+
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DB_NAME", "essenza_db_dev"),
        "USER": os.environ.get("DB_USER", "root"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "root"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "3306"),
        "OPTIONS": {
            "charset": "utf8mb4",
            "collation": "utf8mb4_unicode_ci",
            # MariaDB 10.3 compatibility settings
            "isolation_level": "read committed",
            "autocommit": True,
            "connect_timeout": 60,
            "read_timeout": 60,
            "write_timeout": 60,
        },
        "TEST": {
            "NAME": "test_essenza_dev",
            "CHARSET": "utf8mb4",
            "COLLATION": "utf8mb4_unicode_ci",
        },
    }
}

# Password hashers - untuk keamanan maksimal
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",  # Paling aman, pemenang PHC
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",  # Default Django
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Jakarta"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django REST Framework Configuration
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "core.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",  # Allow any access
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_SCHEMA_CLASS": "utils.schema.CustomAutoSchema",
    "UNAUTHENTICATED_USER": None,  # No default user object
    "UNAUTHENTICATED_TOKEN": None,  # No default token object
    "EXCEPTION_HANDLER": "core.handlers.drf_exception.custom_exception_handler",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

# drf-spectacular Configuration
SPECTACULAR_SETTINGS = {
    "TITLE": "Essenza Backend API",
    "DESCRIPTION": "API Documentation for Essenza Backend Application",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SORT_OPERATIONS": False,
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    "SERVE_AUTHENTICATION": [],
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": False,
        "defaultModelsExpandDepth": 1,
        "defaultModelExpandDepth": 1,
        "defaultModelRendering": "example",
        "displayRequestDuration": True,
        "docExpansion": "none",
        "filter": True,
        "showExtensions": True,
        "showCommonExtensions": True,
        "supportedSubmitMethods": ["get", "post", "put", "delete", "patch"],
        "oauth2RedirectUrl": None,
        "validatorUrl": None,  # Disable validator to avoid caching issues
    },
    "SECURITY": [{"BearerAuth": []}],
    "COMPONENTS": {
        "securitySchemes": {
            "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
        }
    },
    "REDOC_UI_SETTINGS": {
        "hideDownloadButton": False,
        "expandResponses": "all",
        "pathInMiddlePanel": True,
        "theme": {"colors": {"primary": {"main": "#2196F3"}}},
    },
    "PREPROCESSING_HOOKS": [],
    "POSTPROCESSING_HOOKS": [
        "utils.docs.add_security_schemes",
    ],
    "SCHEMA_PATH_PREFIX": "/api/",
    "DEFAULT_GENERATOR_CLASS": "drf_spectacular.generators.SchemaGenerator",
    "TAGS": [
        # General Tags
        {"name": "General", "description": "General purpose endpoints"},
        # Internal API Tags
        {
            "name": "Internal / Authentication",
            "description": "Authentication related endpoints",
        },
        {
            "name": "Internal / Settings",
            "description": "Application settings management",
        },
        {
            "name": "Internal / Social Media",
            "description": "Social media links management",
        },
        {
            "name": "Internal / Menu",
            "description": "Application menu management",
        },
        {
            "name": "Internal / Menu Item",
            "description": "Application menu item management",
        },
        {
            "name": "Internal / Banner",
            "description": "Application banner management",
        },
        {
            "name": "Internal / Subscriber",
            "description": "Application subscriber management",
        },
        {
            "name": "Internal / Page",
            "description": "Application page management",
        },
        {
            "name": "Internal / Specification",
            "description": "Application specification master data management",
        },
        {
            "name": "Internal / Product",
            "description": "Application product management",
        },
        {
            "name": "Internal / Product Variant",
            "description": "Application product variant management",
        },
        {
            "name": "Internal / Brochure",
            "description": "Application brochure management",
        },
        {
            "name": "Internal / Project",
            "description": "Application project management",
        },
        {
            "name": "Internal / Article",
            "description": "Application article management",
        },
        {
            "name": "Internal / Distributor",
            "description": "Application distributor management",
        },
        {
            "name": "Internal / Store",
            "description": "Application store management",
        },
        {
            "name": "Internal / Contact Messages",
            "description": "Application contact message management",
        },
        # Public API Tags
        {
            "name": "Public / Subscriber",
            "description": "Application subscriber management",
        },
        {
            "name": "Public / Contact Messages",
            "description": "Application contact message management",
        },
    ],
}

# Migration modules - Skip unwanted migrations
MIGRATION_MODULES = {
    "auth": None,  # Skip auth app migrations to avoid groups, permissions tables
}

# Database router to exclude certain tables
DATABASE_ROUTERS = []

# File upload settings
FILE_UPLOAD_BASE_DIR = "media/"
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# Session settings
SESSION_COOKIE_AGE = 86400  # 1 day
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# JWT Configuration
JWT_SECRET = os.environ.get(
    "JWT_SECRET", "Z7zl2n_ee-DKHEr7e7Dek7zV6YxVZON-ypQMUNhfm4ioYBPXtjhxCX1syq8"
)
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_SECONDS = int(os.environ.get("JWT_EXPIRY_SECONDS", "86400"))  # 1 day
JWT_REFRESH_SIGNATURE = os.environ.get(
    "JWT_REFRESH_SIGNATURE", "JTrFGGbDCxNdf6YcjtoVpcXaw1_K4Ppt1m_YzoEZE5o"
)
JWT_FERNET_KEY = os.environ.get(
    "JWT_FERNET_KEY", "soJLqlAzc2ESzvr3NTbeZ8TqT7VgmmW5g-KUYiKyihE="
)

# Google reCAPTCHA Configuration
# v2 and v3 require different secret keys from Google Console
RECAPTCHA_V2_SECRET_KEY = os.environ.get("RECAPTCHA_V2_SECRET_KEY", "")
RECAPTCHA_V3_SECRET_KEY = os.environ.get("RECAPTCHA_V3_SECRET_KEY", "")

# Default version and settings
RECAPTCHA_DEFAULT_VERSION = os.environ.get(
    "RECAPTCHA_DEFAULT_VERSION", "v2"
)  # v2 or v3
RECAPTCHA_TIMEOUT = int(
    os.environ.get("RECAPTCHA_TIMEOUT", "10")
)  # Request timeout in seconds
RECAPTCHA_SCORE_THRESHOLD = float(
    os.environ.get("RECAPTCHA_SCORE_THRESHOLD", "0.5")
)  # v3 only (0.0-1.0)
