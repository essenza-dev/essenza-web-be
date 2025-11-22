"""
Crypto utilities module for secure signature generation and verification.

This module provides secure HMAC-SHA256 based signature utilities with base64 encoding.
Uses Python's secrets module for cryptographically secure random generation.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
import time
from typing import Optional


class Signature:
    """
    Secure HMAC-SHA256 signature generator with base64 encoding.

    This class provides methods for generating and verifying cryptographic signatures
    using HMAC-SHA256 algorithm with proper security practices.
    """

    __slots__ = ("_secret_key",)

    def __init__(self, secret_key: Optional[str | bytes] = None) -> None:
        """
        Initialize the signature generator with a secret key.

        Args:
            secret_key: The secret key for HMAC. If None, a secure random key is generated.
                       Can be string or bytes. If string, it will be encoded as UTF-8.
        """
        if secret_key is None:
            self._secret_key: bytes = secrets.token_bytes(32)
        elif isinstance(secret_key, str):
            self._secret_key = secret_key.encode("utf-8")
        else:
            self._secret_key = secret_key

    @property
    def secret_key_b64(self) -> str:
        """Get the secret key encoded as base64 string for storage/transmission."""
        return base64.b64encode(self._secret_key).decode("ascii")

    @classmethod
    def from_base64_key(cls, b64_key: str) -> Signature:
        """
        Create Signature from base64 encoded key.

        Args:
            b64_key: Base64 encoded secret key

        Returns:
            Signature instance
        """
        secret_key = base64.b64decode(b64_key)
        return cls(secret_key)

    def _prepare_message(self, message: str | bytes) -> bytes:
        """Convert message to bytes efficiently."""
        return message.encode("utf-8") if isinstance(message, str) else message

    def generate_signature(self, message: str | bytes) -> str:
        """
        Generate HMAC-SHA256 signature for the given message.

        Args:
            message: The message to sign. If string, it will be encoded as UTF-8.

        Returns:
            Base64 encoded signature string
        """
        message_bytes = self._prepare_message(message)
        signature = hmac.new(self._secret_key, message_bytes, hashlib.sha256).digest()
        return base64.b64encode(signature).decode("ascii")

    def verify_signature(self, message: str | bytes, signature: str) -> bool:
        """
        Verify HMAC-SHA256 signature for the given message.

        Args:
            message: The original message that was signed
            signature: Base64 encoded signature to verify

        Returns:
            True if signature is valid, False otherwise
        """
        expected_signature = self.generate_signature(message)
        return secrets.compare_digest(signature, expected_signature)

    def generate_timestamped_signature(
        self, message: str | bytes, timestamp: Optional[int] = None
    ) -> tuple[str, int]:
        """
        Generate signature with timestamp for time-sensitive operations.

        Args:
            message: The message to sign
            timestamp: Unix timestamp. If None, current time is used.

        Returns:
            Tuple of (base64_signature, timestamp)
        """
        if timestamp is None:
            timestamp = int(time.time())

        timestamped_message = f"{message}:{timestamp}"
        signature = self.generate_signature(timestamped_message)
        return signature, timestamp

    def verify_timestamped_signature(
        self,
        message: str | bytes,
        signature: str,
        timestamp: int,
        max_age_seconds: int = 300,
    ) -> bool:
        """
        Verify timestamped signature with age validation.

        Args:
            message: The original message
            signature: Base64 encoded signature
            timestamp: The timestamp used in signature generation
            max_age_seconds: Maximum allowed age in seconds (default: 5 minutes)

        Returns:
            True if signature is valid and not expired, False otherwise
        """
        current_time = int(time.time())
        if current_time - timestamp > max_age_seconds:
            return False

        timestamped_message = f"{message}:{timestamp}"
        return self.verify_signature(timestamped_message, signature)


def generate_secure_key() -> str:
    """Generate a cryptographically secure random key as base64 string."""
    return base64.b64encode(secrets.token_bytes(32)).decode("ascii")


def create_signature(message: str | bytes, secret_key: str | bytes) -> str:
    """
    Quick function to create HMAC-SHA256 signature.

    Args:
        message: Message to sign
        secret_key: Secret key for HMAC

    Returns:
        Base64 encoded signature
    """
    generator = Signature(secret_key)
    return generator.generate_signature(message)


def verify_signature(
    message: str | bytes, signature: str, secret_key: str | bytes
) -> bool:
    """
    Quick function to verify HMAC-SHA256 signature.

    Args:
        message: Original message
        signature: Base64 encoded signature to verify
        secret_key: Secret key used for signing

    Returns:
        True if signature is valid, False otherwise
    """
    generator = Signature(secret_key)
    return generator.verify_signature(message, signature)
