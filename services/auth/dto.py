from dataclasses import dataclass, field


@dataclass
class AuthTokensDTO:
    access_token: str = field(default="")
    refresh_token: str = field(default="")
