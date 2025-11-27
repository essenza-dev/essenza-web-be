"""Main reCAPTCHA service implementation."""

import logging
import os
from typing import Dict, List, Optional, Tuple

import requests
from django.conf import settings

from .config import RecaptchaConfig, RecaptchaVersion
from .constants import VERIFY_URL, ERROR_MESSAGES
from .exceptions import RecaptchaError, RecaptchaVerificationError
from .dto import RecaptchaResponseDTO

logger = logging.getLogger(__name__)


class RecaptchaService:
    """Service for Google reCAPTCHA verification."""

    def __init__(
        self,
        config: Optional[RecaptchaConfig] = None,
        version: Optional[RecaptchaVersion] = None,
    ):
        """
        Initialize the reCAPTCHA service.

        Args:
            config: reCAPTCHA configuration. If None, will load from settings/environment
            version: Specific reCAPTCHA version to use (v2 or v3)
        """
        if config:
            self.config = config
        else:
            # Convert string version to enum if provided
            version_enum = None
            if version:
                version_enum = version
            elif isinstance(version, str):
                version_enum = (
                    RecaptchaVersion.V3
                    if version.lower() == "v3"
                    else RecaptchaVersion.V2
                )

            self.config = RecaptchaConfig.from_settings(version_enum)

    def verify_token(
        self,
        token: str,
        remote_ip: Optional[str] = None,
        expected_action: Optional[str] = None,
    ) -> RecaptchaResponseDTO:
        """
        Verify reCAPTCHA token with Google's API.

        Args:
            token: The reCAPTCHA response token from client
            remote_ip: Optional client IP address for additional validation
            expected_action: Expected action name (v3 only)

        Returns:
            RecaptchaResponseDTO object with verification results

        Raises:
            RecaptchaVerificationError: When verification fails
        """
        if not token or not token.strip():
            raise RecaptchaVerificationError(
                "reCAPTCHA token is required", ["missing-input-response"]
            )

        # Prepare request data
        data = {"secret": self.config.secret_key, "response": token.strip()}

        if remote_ip:
            data["remoteip"] = remote_ip

        try:
            # Make request to Google's verification API
            response = requests.post(
                VERIFY_URL,
                data=data,
                timeout=self.config.timeout,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": "Essenza-Backend/1.0",
                },
            )
            response.raise_for_status()

            # Parse response
            result = response.json()

        except requests.RequestException as e:
            logger.error(f"Failed to verify reCAPTCHA token: {e}")
            raise RecaptchaVerificationError(
                f"Failed to communicate with reCAPTCHA service: {e}",
                ["bad-request"],
            ) from e
        except ValueError as e:
            logger.error(f"Invalid JSON response from reCAPTCHA service: {e}")
            raise RecaptchaVerificationError(
                "Invalid response from reCAPTCHA service",
                ["bad-request"],
            ) from e

        # Parse the response
        recaptcha_response = self._parse_response(result)

        # Additional validation for v3
        if self.config.version == RecaptchaVersion.V3 and recaptcha_response.success:
            self._validate_v3_response(recaptcha_response, expected_action)

        return recaptcha_response

    def _parse_response(self, data: Dict) -> RecaptchaResponseDTO:
        """Parse the JSON response from Google reCAPTCHA API."""
        return RecaptchaResponseDTO(
            success=data.get("success", False),
            error_codes=data.get("error-codes", []),
            challenge_ts=data.get("challenge_ts"),
            hostname=data.get("hostname"),
            score=data.get("score"),
            action=data.get("action"),
            apk_package_name=data.get("apk_package_name"),
        )

    def _validate_v3_response(
        self, response: RecaptchaResponseDTO, expected_action: Optional[str]
    ) -> None:
        """Additional validation for reCAPTCHA v3 responses."""
        # Validate action name
        if expected_action and response.action != expected_action:
            logger.warning(
                f"reCAPTCHA action mismatch. Expected: {expected_action}, "
                f"Got: {response.action}"
            )
            raise RecaptchaVerificationError(
                f"Invalid action. Expected '{expected_action}', got '{response.action}'",
                ["invalid-input-response"],
            )

        # Validate score
        if response.score is not None and response.score < self.config.score_threshold:
            logger.warning(
                f"reCAPTCHA score {response.score} below threshold {self.config.score_threshold}"
            )
            raise RecaptchaVerificationError(
                f"reCAPTCHA score {response.score} below required threshold {self.config.score_threshold}",
                ["low-score"],
            )

    def get_error_message(self, error_codes: List[str]) -> str:
        """Get human-readable error message from error codes."""
        if not error_codes:
            return "Unknown reCAPTCHA error"

        messages = []
        for code in error_codes:
            message = ERROR_MESSAGES.get(code, f"Unknown error: {code}")
            messages.append(message)

        return "; ".join(messages)

    def is_verification_required(self) -> bool:
        """Check if reCAPTCHA verification should be enforced based on environment."""
        django_env = os.getenv("DJANGO_ENV", "development").lower()
        return django_env == "production" or getattr(
            settings, "FORCE_RECAPTCHA_VERIFICATION", False
        )


def verify_recaptcha(
    token: str,
    remote_ip: Optional[str] = None,
    expected_action: Optional[str] = None,
    config: Optional[RecaptchaConfig] = None,
    version: Optional[RecaptchaVersion] = None,
) -> Tuple[bool, Optional[str]]:
    """
    Convenience function to verify reCAPTCHA token.

    Args:
        token: The reCAPTCHA response token
        remote_ip: Optional client IP address
        expected_action: Expected action name (v3 only)
        config: Optional custom configuration

    Returns:
        Tuple of (is_valid: bool, error_message: Optional[str])
    """
    try:
        service = RecaptchaService(config, version)

        # Skip verification in non-production if not forced
        if not service.is_verification_required():
            logger.info("reCAPTCHA verification skipped in non-production environment")
            return True, None

        response = service.verify_token(token, remote_ip, expected_action)

        if not response.success:
            error_message = service.get_error_message(response.error_codes)
            logger.warning(f"reCAPTCHA verification failed: {error_message}")
            return False, error_message

        logger.info("reCAPTCHA verification successful")
        return True, None

    except RecaptchaVerificationError as e:
        logger.warning(f"reCAPTCHA verification error: {e}")
        return False, str(e)
    except RecaptchaError as e:
        logger.error(f"reCAPTCHA configuration error: {e}")
        return False, "reCAPTCHA service configuration error"
    except Exception as e:
        logger.error(f"Unexpected error during reCAPTCHA verification: {e}")
        return False, "Internal server error during verification"


def get_recaptcha_service(config: Optional[RecaptchaConfig] = None) -> RecaptchaService:
    """Get a configured reCAPTCHA service instance."""
    return RecaptchaService(config)
