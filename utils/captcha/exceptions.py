"""reCAPTCHA exception classes."""

from typing import List, Optional


class RecaptchaError(Exception):
    """Base exception for reCAPTCHA related errors."""

    pass


class RecaptchaVerificationError(RecaptchaError):
    """Exception raised when reCAPTCHA verification fails."""

    def __init__(self, message: str, error_codes: Optional[List[str]] = None):
        super().__init__(message)
        self.error_codes = error_codes or []
