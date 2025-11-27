"""reCAPTCHA configuration classes and enums."""

import os
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from django.conf import settings

from .exceptions import RecaptchaError


class RecaptchaVersion(Enum):
    """Supported reCAPTCHA versions."""

    V2 = "v2"
    V3 = "v3"


@dataclass
class RecaptchaConfig:
    """Configuration for reCAPTCHA verification."""

    secret_key: str
    version: RecaptchaVersion = RecaptchaVersion.V2
    timeout: int = 10
    score_threshold: float = 0.5  # Only used for v3

    @classmethod
    def from_settings(
        cls, version: Optional[RecaptchaVersion] = None
    ) -> "RecaptchaConfig":
        """Load reCAPTCHA configuration from Django settings or environment variables."""
        # Determine version first
        if version is None:
            version_str = (
                getattr(settings, "RECAPTCHA_DEFAULT_VERSION", "v2")
                or os.getenv("RECAPTCHA_DEFAULT_VERSION", "v2")
            ).lower()
            version = (
                RecaptchaVersion.V3 if version_str == "v3" else RecaptchaVersion.V2
            )

        # Get the appropriate secret key based on version
        if version == RecaptchaVersion.V3:
            secret_key = getattr(
                settings, "RECAPTCHA_V3_SECRET_KEY", None
            ) or os.getenv("RECAPTCHA_V3_SECRET_KEY")
            if not secret_key:
                raise RecaptchaError(
                    "reCAPTCHA v3 secret key not found. Set RECAPTCHA_V3_SECRET_KEY in settings or environment"
                )
        else:
            secret_key = getattr(
                settings, "RECAPTCHA_V2_SECRET_KEY", None
            ) or os.getenv("RECAPTCHA_V2_SECRET_KEY")
            if not secret_key:
                raise RecaptchaError(
                    "reCAPTCHA v2 secret key not found. Set RECAPTCHA_V2_SECRET_KEY in settings or environment"
                )

        timeout = int(
            getattr(settings, "RECAPTCHA_TIMEOUT", 10)
            or os.getenv("RECAPTCHA_TIMEOUT", "10")
        )

        score_threshold = float(
            getattr(settings, "RECAPTCHA_SCORE_THRESHOLD", 0.5)
            or os.getenv("RECAPTCHA_SCORE_THRESHOLD", "0.5")
        )

        return cls(
            secret_key=secret_key,
            version=version,
            timeout=timeout,
            score_threshold=score_threshold,
        )
