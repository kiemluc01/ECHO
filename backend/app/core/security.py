from datetime import datetime, timedelta, timezone
from uuid import UUID

from jose import JWTError, jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError

from app.core.config import Settings

password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return password_hasher.verify(password_hash, password)
    except (InvalidHashError, VerifyMismatchError):
        return False


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


def decode_refresh_token(token: str, settings: Settings) -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"], issuer=settings.jwt_issuer)
    except JWTError as exc:
        raise ValueError("invalid token") from exc
    if payload.get("type") != "refresh" or not payload.get("sub"):
        raise ValueError("invalid refresh token")
    return payload


def verify_oidc_token(token: str, jwks: dict, issuer: str, audience: str) -> dict:
    try:
        header = jwt.get_unverified_header(token)
        key = next(key for key in jwks.get("keys", []) if key.get("kid") == header.get("kid"))
        return jwt.decode(token, key, algorithms=[header.get("alg", "RS256")], issuer=issuer, audience=audience)
    except (JWTError, StopIteration) as exc:
        raise ValueError("invalid oidc token") from exc


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
