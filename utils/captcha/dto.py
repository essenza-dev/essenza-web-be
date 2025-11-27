"""reCAPTCHA data models and response structures."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class RecaptchaResponseDTO:
    """Response from reCAPTCHA verification."""

    success: bool
    error_codes: List[str]
    challenge_ts: Optional[str] = None
    hostname: Optional[str] = None
    score: Optional[float] = None  # Only for v3
    action: Optional[str] = None  # Only for v3
    apk_package_name: Optional[str] = None  # Only for Android
