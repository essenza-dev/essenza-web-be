from datetime import datetime, timedelta, timezone
from typing import Optional

from django.conf import settings
from utils.crypto import Signature, Fernet
import jwt


class JsonWebToken:
    _secret: str
    _algorithm: str = settings.JWT_ALGORITHM
    _expiry: int = settings.JWT_EXPIRY_SECONDS
    _sig: Signature = Signature(settings.JWT_REFRESH_SIGNATURE)
    _fernet: Fernet = Fernet(settings.JWT_FERNET_KEY)

    def __init__(self, secret: Optional[str] = None) -> None:
        self._secret = f"{secret or '-'}.{settings.JWT_SECRET}.{settings.SECRET_KEY}"

    def encode(self, sub: str) -> tuple[str, str]:
        now = datetime.now(timezone.utc)
        sub = self._fernet.encrypt(sub)
        payload = {"sub": sub, "exp": now + timedelta(seconds=self._expiry)}
        token = jwt.encode(payload, self._secret, algorithm=self._algorithm)
        refresh_token = self.get_signature(token)
        return token, refresh_token

    def decode(
        self, token: str, expiration: bool = True, signature: bool = True
    ) -> dict:
        return jwt.decode(
            token,
            self._secret,
            algorithms=[self._algorithm],
            options={"verify_exp": expiration, "verify_signature": signature},
        )

    def verify(self, token: str, expiration: bool = True) -> bool:
        try:
            self.decode(token, expiration=expiration)
            return True
        except jwt.PyJWTError:
            return False

    def refresh(self, token: str) -> tuple[str, str]:
        decoded = self.decode(token, expiration=False)
        sub = decoded.get("sub", "")
        return self.encode(sub)

    def get_subject(
        self, token: str, expiration: bool = True, signature: bool = True
    ) -> str:
        decoded = self.decode(token, expiration, signature)
        sub = decoded.get("sub", "")
        decrypted_sub = self._fernet.decrypt(sub)
        return decrypted_sub.decode("utf-8")

    def verify_refresh_token(self, token: str, refresh_token: str) -> bool:
        return self._sig.verify_signature(token, refresh_token)

    def get_signature(self, token: str) -> str:
        return self._sig.generate_signature(token)
