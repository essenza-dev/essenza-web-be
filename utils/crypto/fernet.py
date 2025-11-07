"""
Fernet encryption utility module for secure symmetric encryption and decryption.

This module provides a simplified interface for Fernet encryption with optimized
performance and comprehensive type safety using Python 3.10+ features.
"""

from __future__ import annotations

from typing import Union, Optional, Final
from cryptography.fernet import Fernet as CryptoFernet, InvalidToken
from cryptography.exceptions import InvalidSignature


class FernetError(Exception):
    """Base exception for Fernet operations."""
    pass


class FernetEncryptionError(FernetError):
    """Raised when encryption fails."""
    pass


class FernetDecryptionError(FernetError):
    """Raised when decryption fails."""
    pass


class Fernet:
    """
    Optimized Fernet encryption utility with enhanced type safety and performance.

    This class provides symmetric encryption/decryption using Fernet algorithm
    with automatic key generation, efficient data conversion, and comprehensive
    error handling.
    """

    __slots__ = ("_fernet",)

    # Constants for better performance and type safety
    _ENCODING: Final[str] = "utf-8"
    _ASCII_ENCODING: Final[str] = "ascii"

    def __init__(self, secret_key: Optional[Union[str, bytes]] = None) -> None:
        """
        Initialize Fernet encryption with optional secret key.

        Args:
            secret_key: Base64-encoded secret key for Fernet encryption.
                       If None, generates a new cryptographically secure key.
                       Accepts both string and bytes formats.

        Raises:
            FernetError: If the provided secret key is invalid.
        """
        try:
            if secret_key is None:
                key = CryptoFernet.generate_key()
            elif isinstance(secret_key, str):
                key = secret_key.encode(self._ASCII_ENCODING)
            else:
                key = secret_key

            self._fernet = CryptoFernet(key)
        except (ValueError, TypeError, InvalidSignature) as e:
            raise FernetError(f"Invalid secret key provided: {e}") from e

    @property
    def secret_key_b64(self) -> str:
        """
        Get the secret key as base64-encoded string for storage/transmission.

        Returns:
            Base64-encoded secret key string.
        """
        # Extract the full key from Fernet instance and encode as base64
        full_key = self._fernet._signing_key + self._fernet._encryption_key
        return full_key.decode(self._ASCII_ENCODING)

    @classmethod
    def generate_key(cls) -> str:
        """
        Generate a new cryptographically secure Fernet key.

        Returns:
            Base64-encoded Fernet key suitable for initialization.
        """
        return CryptoFernet.generate_key().decode("ascii")

    def _prepare_data(self, data: Union[str, bytes]) -> bytes:
        """
        Efficiently convert input data to bytes.

        Args:
            data: Input data as string or bytes.

        Returns:
            Data as bytes object.
        """
        return data.encode(self._ENCODING) if isinstance(data, str) else data

    def encrypt(self, data: Union[str, bytes]) -> str:
        """
        Encrypt data using Fernet symmetric encryption.

        Args:
            data: Data to encrypt. Strings are automatically UTF-8 encoded.

        Returns:
            Base64-encoded encrypted token as string.

        Raises:
            FernetEncryptionError: If encryption fails.
        """
        try:
            data_bytes = self._prepare_data(data)
            encrypted_token = self._fernet.encrypt(data_bytes)
            return encrypted_token.decode(self._ASCII_ENCODING)
        except Exception as e:
            raise FernetEncryptionError(f"Encryption failed: {e}") from e

    def decrypt(self, token: str) -> bytes:
        """
        Decrypt Fernet token back to original data.

        Args:
            token: Base64-encoded encrypted token string.

        Returns:
            Decrypted data as bytes.

        Raises:
            FernetDecryptionError: If decryption fails or token is invalid.
        """
        try:
            token_bytes = token.encode(self._ASCII_ENCODING)
            return self._fernet.decrypt(token_bytes)
        except (InvalidToken, ValueError, TypeError) as e:
            raise FernetDecryptionError(f"Decryption failed: {e}") from e

    def decrypt_to_string(self, token: str, encoding: str = "utf-8") -> str:
        """
        Decrypt Fernet token and return as decoded string.

        Args:
            token: Base64-encoded encrypted token string.
            encoding: Text encoding for decoding bytes (default: utf-8).

        Returns:
            Decrypted data as string.

        Raises:
            FernetDecryptionError: If decryption or decoding fails.
        """
        try:
            decrypted_bytes = self.decrypt(token)
            return decrypted_bytes.decode(encoding)
        except UnicodeDecodeError as e:
            raise FernetDecryptionError(f"Failed to decode decrypted data: {e}") from e

    def encrypt_json_safe(self, data: Union[str, bytes]) -> str:
        """
        Encrypt data and return JSON-safe base64 string.

        This method ensures the output is safe for JSON serialization
        by using URL-safe base64 encoding internally.

        Args:
            data: Data to encrypt.

        Returns:
            JSON-safe encrypted token string.

        Raises:
            FernetEncryptionError: If encryption fails.
        """
        return self.encrypt(data)  # Fernet already uses URL-safe base64


# Utility functions for quick operations
def encrypt_data(data: Union[str, bytes], secret_key: Optional[Union[str, bytes]] = None) -> str:
    """
    Quick utility function for encrypting data.

    Args:
        data: Data to encrypt.
        secret_key: Optional secret key. If None, generates a new one.

    Returns:
        Encrypted token as base64 string.
    """
    fernet = Fernet(secret_key)
    return fernet.encrypt(data)


def decrypt_data(token: str, secret_key: Union[str, bytes]) -> bytes:
    """
    Quick utility function for decrypting data.

    Args:
        token: Encrypted token to decrypt.
        secret_key: Secret key used for encryption.

    Returns:
        Decrypted data as bytes.
    """
    fernet = Fernet(secret_key)
    return fernet.decrypt(token)


def decrypt_to_string(token: str, secret_key: Union[str, bytes], encoding: str = "utf-8") -> str:
    """
    Quick utility function for decrypting data to string.

    Args:
        token: Encrypted token to decrypt.
        secret_key: Secret key used for encryption.
        encoding: Text encoding for the result.

    Returns:
        Decrypted data as string.
    """
    fernet = Fernet(secret_key)
    return fernet.decrypt_to_string(token, encoding)
