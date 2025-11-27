"""CAPTCHA serializer fields and base classes."""

import os
from typing import Any, Optional

from django.conf import settings
from rest_framework import serializers

from .config import RecaptchaVersion
from .constants import DEFAULT_CAPTCHA_TOKEN


class CaptchaTokenField(serializers.CharField):
    """
    Custom serializer field for CAPTCHA tokens with environment-aware behavior.

    Automatically configures field requirements and defaults based on the current environment:
    - Production: Required field without default value
    - Non-production: Optional field with configurable default value
    - Includes appropriate help text for API documentation
    """

    def __init__(self, default: Optional[str] = None, **kwargs: Any) -> None:
        """
        Initialize the CAPTCHA token field with environment-aware configuration.

        Args:
            default: Default value to use in non-production environments
            **kwargs: Additional serializer field arguments
        """
        django_env = os.getenv("DJANGO_ENV", "development").lower()
        is_production = django_env == "production"

        # Configure field requirements based on environment
        kwargs.setdefault("required", is_production)

        # Apply default value only in non-production environments
        if default is not None and not is_production:
            kwargs.setdefault("default", default)
        elif is_production:
            kwargs.pop("default", None)

        # Set descriptive help text for API documentation
        kwargs.setdefault("help_text", "CAPTCHA token for bot verification.")

        super().__init__(**kwargs)


class CaptchaVersionField(serializers.ChoiceField):
    """
    Custom serializer field for CAPTCHA version selection.

    Provides choices between reCAPTCHA v2 and v3 with appropriate defaults.
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize the CAPTCHA version field.

        Args:
            **kwargs: Additional serializer field arguments
        """
        # Define version choices
        choices = [
            (version.value, version.value.upper()) for version in RecaptchaVersion
        ]

        # Set default values
        kwargs.setdefault("choices", choices)
        kwargs.setdefault("default", RecaptchaVersion.V2.value)
        kwargs.setdefault("required", False)
        kwargs.setdefault(
            "help_text", "reCAPTCHA version to use for verification (v2 or v3)."
        )

        super().__init__(**kwargs)


class UseCaptchaSerializer(serializers.Serializer):
    """
    Base serializer for forms that require CAPTCHA verification.

    Includes common CAPTCHA fields:
    - captcha_token: The CAPTCHA response token
    - captcha_version: The reCAPTCHA version to use (optional)

    Automatically validates CAPTCHA when is_valid() is called.
    """

    captcha_token = CaptchaTokenField(default=DEFAULT_CAPTCHA_TOKEN)

    captcha_version = CaptchaVersionField()

    def validate_captcha_token(self, value: str) -> str:
        """
        Validate CAPTCHA token format.

        Args:
            value: The CAPTCHA token value

        Returns:
            The validated token

        Raises:
            serializers.ValidationError: If token format is invalid
        """
        if not value or not isinstance(value, str):
            raise serializers.ValidationError(
                "CAPTCHA token must be a non-empty string."
            )

        # Basic format validation - token should be reasonable length
        if len(value.strip()) < 10:
            raise serializers.ValidationError("CAPTCHA token appears to be invalid.")

        return value.strip()

    def validate_captcha_version(self, value: str) -> str:
        """
        Validate CAPTCHA version.

        Args:
            value: The CAPTCHA version value

        Returns:
            The validated version

        Raises:
            serializers.ValidationError: If version is not supported
        """
        valid_versions = [version.value for version in RecaptchaVersion]
        if value not in valid_versions:
            raise serializers.ValidationError(
                f"Invalid CAPTCHA version. Must be one of: {', '.join(valid_versions)}"
            )

        return value

    def validate(self, attrs):
        """
        Perform CAPTCHA validation automatically during serializer validation.

        Args:
            attrs: The validated attributes dictionary

        Returns:
            The validated attributes

        Raises:
            serializers.ValidationError: If CAPTCHA verification fails
        """
        # Call parent validation first
        attrs = super().validate(attrs)

        # Perform CAPTCHA validation if required
        if self._should_verify_captcha():
            self._validate_captcha_token(attrs)

        return attrs

    def _should_verify_captcha(self) -> bool:
        """Check if CAPTCHA verification should be performed."""
        # Always verify - the actual logic is in _validate_captcha_token
        return True

    def _validate_captcha_token(self, attrs: dict) -> None:
        """
        Validate CAPTCHA token with Google's API.

        Args:
            attrs: The validated attributes dictionary

        Raises:
            serializers.ValidationError: If CAPTCHA verification fails
        """
        from .service import verify_recaptcha

        token = attrs.get("captcha_token", "")
        version = attrs.get("captcha_version", "v2")

        # Check if it's development environment and using default test token
        django_env = os.getenv("DJANGO_ENV", "development").lower()
        is_development = django_env != "production"

        if is_development and token == DEFAULT_CAPTCHA_TOKEN:
            # In development, accept the default test token without API call
            return

        # If not using default token, always verify (even in development)

        # Get remote IP from request context if available
        remote_ip = None
        context = getattr(self, "context", {})
        if "request" in context:
            request = context["request"]
            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
            if x_forwarded_for:
                remote_ip = x_forwarded_for.split(",")[0].strip()
            else:
                remote_ip = request.META.get("REMOTE_ADDR")

        # Set expected action for v3
        expected_action = "form_submit" if version == "v3" else None

        # Get version-specific config and perform verification
        from .config import RecaptchaVersion

        version_enum = RecaptchaVersion.V3 if version == "v3" else RecaptchaVersion.V2

        is_valid, error_message = verify_recaptcha(
            token=token,
            remote_ip=remote_ip,
            expected_action=expected_action,
            version=version_enum,
        )

        if not is_valid:
            raise serializers.ValidationError(
                {"captcha_token": f"CAPTCHA verification failed: {error_message}"}
            )


class CaptchaValidationMixin:
    """
    Mixin for serializers that need CAPTCHA validation functionality.

    Provides methods to handle CAPTCHA verification in serializer validation.
    """

    def get_captcha_data(self) -> tuple[str, str, Optional[str]]:
        """
        Extract CAPTCHA data from validated data.

        Returns:
            Tuple of (token, version, remote_ip)
        """
        validated_data = getattr(self, "validated_data", {})

        token = validated_data.get("captcha_token", "")
        version = validated_data.get("captcha_version", RecaptchaVersion.V2.value)

        # Try to get remote IP from context
        remote_ip = None
        context = getattr(self, "context", {})
        if "request" in context:
            request = context["request"]
            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
            if x_forwarded_for:
                remote_ip = x_forwarded_for.split(",")[0].strip()
            else:
                remote_ip = request.META.get("REMOTE_ADDR")

        return token, version, remote_ip

    def should_verify_captcha(self) -> bool:
        """
        Determine if CAPTCHA verification should be performed.

        Returns:
            True if verification is required, False otherwise
        """
        django_env = os.getenv("DJANGO_ENV", "development").lower()
        force_verification = getattr(settings, "FORCE_RECAPTCHA_VERIFICATION", False)

        return django_env == "production" or force_verification
