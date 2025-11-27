"""
DEPRECATED: This file has been moved to utils.captcha package for better modularity.

Please import from utils.captcha instead:
    from utils.captcha import verify_recaptcha, RecaptchaService, RecaptchaConfig
"""

import warnings
from .captcha import (
    RecaptchaService,
    RecaptchaConfig,
    RecaptchaVersion,
    RecaptchaResponseDTO,
    RecaptchaError,
    RecaptchaVerificationError,
    verify_recaptcha,
    get_recaptcha_service,
)

# Issue deprecation warning
warnings.warn(
    "utils.captcha module has been moved to utils.captcha package. "
    "Please update your imports to use: from utils.captcha import ...",
    DeprecationWarning,
    stacklevel=2
)

__all__ = [
    'RecaptchaService',
    'RecaptchaConfig',
    'RecaptchaVersion',
    'RecaptchaResponseDTO',
    'RecaptchaError',
    'RecaptchaVerificationError',
    'verify_recaptcha',
    'get_recaptcha_service',
]
