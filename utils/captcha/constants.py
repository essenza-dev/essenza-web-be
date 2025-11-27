"""reCAPTCHA constants and error messages."""

from typing import Dict

# Google reCAPTCHA API endpoint
VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"

# Error code descriptions based on Google documentation
ERROR_MESSAGES: Dict[str, str] = {
    "missing-input-secret": "The secret parameter is missing",
    "invalid-input-secret": "The secret parameter is invalid or malformed",
    "missing-input-response": "The response parameter is missing",
    "invalid-input-response": "The response parameter is invalid or malformed",
    "bad-request": "The request is invalid or malformed",
    "timeout-or-duplicate": "The response is no longer valid: either too old or already used",
    "low-score": "reCAPTCHA score is below the required threshold",
}

# Default configuration values
DEFAULT_TIMEOUT = 10
DEFAULT_SCORE_THRESHOLD = 0.5
DEFAULT_VERSION = "v2"
DEFAULT_CAPTCHA_TOKEN = "TestTokenDontChange!"
