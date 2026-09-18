from datetime import datetime, timedelta, timezone
from uuid import UUID

from jose import JWTError, jwt

from app.core.config import Settings


def create_token(subject: UUID, roles: list[str], settings: Settings, token_type: str, lifetime: timedelta) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(subject),
        "roles": roles,
        "type": token_type,
        "iss": settings.jwt_issuer,
        "iat": now,
        "exp": now + lifetime,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def decode_access_token(token: str, settings: Settings) -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"], issuer=settings.jwt_issuer)
    except JWTError as exc:
        raise ValueError("invalid token") from exc
    if payload.get("type") != "access" or not payload.get("sub"):
        raise ValueError("invalid access token")
    return payload


def create_oauth_state(provider: str, settings: Settings) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "provider": provider,
        "type": "oauth_state",
        "iss": settings.jwt_issuer,
        "iat": now,
        "exp": now + timedelta(minutes=10),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def decode_oauth_state(state: str, settings: Settings, provider: str) -> dict:
    try:
        payload = jwt.decode(state, settings.jwt_secret, algorithms=["HS256"], issuer=settings.jwt_issuer)
    except JWTError as exc:
        raise ValueError("invalid oauth state") from exc
    if payload.get("type") != "oauth_state" or payload.get("provider") != provider:
        raise ValueError("invalid oauth state")
    return payload
