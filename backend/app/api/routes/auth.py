from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import create_oauth_state, create_token, decode_oauth_state, decode_refresh_token, hash_password, verify_oidc_token, verify_password
from app.db import get_db
from app.models import Account
from app.schemas import LoginRequest, RefreshRequest, RegisterRequest, TokenResponse

router = APIRouter()


def issue_tokens(account: Account) -> TokenResponse:
    settings = get_settings()
    roles = account.roles.split(",")
    return TokenResponse(
        access_token=create_token(account.id, roles, settings, "access", timedelta(minutes=settings.access_token_minutes)),
        refresh_token=create_token(account.id, roles, settings, "refresh", timedelta(days=settings.refresh_token_days)),
    )


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> TokenResponse:
    email = str(payload.email).lower()
    if db.scalar(select(Account).where(Account.email == email)) is not None:
        raise HTTPException(status_code=409, detail={"code": "EMAIL_TAKEN", "message": "Email is already registered"})
    account = Account(
        external_auth_id=f"local:{email}",
        email=email,
        display_name=payload.display_name,
        password_hash=hash_password(payload.password),
        provider="LOCAL",
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return issue_tokens(account)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    email = str(payload.email).lower()
    account = db.scalar(select(Account).where(Account.email == email, Account.provider == "LOCAL"))
    if account is None or account.password_hash is None or not verify_password(payload.password, account.password_hash):
        raise HTTPException(status_code=401, detail={"code": "INVALID_CREDENTIALS", "message": "Email or password is incorrect"})
    if account.status != "ACTIVE":
        raise HTTPException(status_code=401, detail={"code": "AUTH_REQUIRED", "message": "Account is inactive"})
    account.last_login_at = datetime.now(timezone.utc)
    db.commit()
    return issue_tokens(account)

PROVIDERS = {
    "google": {
        "authorization": "https://accounts.google.com/o/oauth2/v2/auth",
        "token": "https://oauth2.googleapis.com/token",
        "jwks": "https://www.googleapis.com/oauth2/v3/certs",
        "issuer": "https://accounts.google.com",
    },
    "apple": {
        "authorization": "https://appleid.apple.com/auth/authorize",
        "token": "https://appleid.apple.com/auth/token",
        "jwks": "https://appleid.apple.com/auth/keys",
        "issuer": "https://appleid.apple.com",
    },
}


@router.get("/{provider}/start")
def oauth_start(provider: str) -> dict:
    settings = get_settings()
    if provider not in PROVIDERS:
        raise HTTPException(status_code=404, detail={"code": "OAUTH_PROVIDER_UNSUPPORTED", "message": "Unsupported provider"})
    client_id = getattr(settings, f"{provider}_client_id")
    if not client_id:
        raise HTTPException(status_code=503, detail={"code": "OAUTH_NOT_CONFIGURED", "message": "Provider is not configured"})
    state = create_oauth_state(provider, settings)
    query = urlencode({"client_id": client_id, "redirect_uri": f"{settings.oauth_redirect_base_url}/{provider}/callback", "response_type": "code", "scope": "openid email", "state": state})
    return {"data": {"provider": provider, "authorization_url": f"{PROVIDERS[provider]['authorization']}?{query}"}}


@router.get("/{provider}/callback")
def oauth_callback(provider: str, code: str, state: str, db: Session = Depends(get_db)) -> RedirectResponse:
    settings = get_settings()
    try:
        decode_oauth_state(state, settings, provider)
    except ValueError:
        raise HTTPException(status_code=400, detail={"code": "INVALID_OAUTH_STATE", "message": "OAuth state is invalid or expired"}) from None

    provider_config = PROVIDERS[provider]
    client_id = getattr(settings, f"{provider}_client_id")
    client_secret = getattr(settings, f"{provider}_client_secret")
    form = {"client_id": client_id, "client_secret": client_secret, "code": code, "grant_type": "authorization_code", "redirect_uri": f"{settings.oauth_redirect_base_url}/{provider}/callback"}
    try:
        with httpx.Client(timeout=10) as client:
            token_response = client.post(provider_config["token"], data=form)
            token_response.raise_for_status()
            token_data = token_response.json()
            id_token = token_data.get("id_token")
            if not id_token:
                raise ValueError("provider did not return an id token")
            jwks_response = client.get(provider_config["jwks"])
            jwks_response.raise_for_status()
            claims = verify_oidc_token(id_token, jwks_response.json(), provider_config["issuer"], client_id)
    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(status_code=401, detail={"code": "OAUTH_EXCHANGE_FAILED", "message": "Provider authentication failed"}) from exc

    external_auth_id = f"{provider}:{claims['sub']}"
    account = db.scalar(select(Account).where(Account.external_auth_id == external_auth_id))
    if account is None:
        account = Account(external_auth_id=external_auth_id, email=claims.get("email"), provider=provider)
        db.add(account)
    account.last_login_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(account)
    issued_tokens = issue_tokens(account)
    callback_url = "echo://auth/callback?" + urlencode({"access_token": issued_tokens.access_token, "refresh_token": issued_tokens.refresh_token})
    return RedirectResponse(callback_url, status_code=302)


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)) -> TokenResponse:
    settings = get_settings()
    try:
        claims = decode_refresh_token(payload.refresh_token, settings)
    except ValueError:
        raise HTTPException(status_code=401, detail={"code": "AUTH_REQUIRED", "message": "Invalid refresh token"}) from None
    account = db.get(Account, claims["sub"])
    if account is None or account.status != "ACTIVE":
        raise HTTPException(status_code=401, detail={"code": "AUTH_REQUIRED", "message": "Account is inactive"})
    roles = account.roles.split(",")
    return TokenResponse(
        access_token=create_token(account.id, roles, settings, "access", timedelta(minutes=settings.access_token_minutes)),
        refresh_token=create_token(account.id, roles, settings, "refresh", timedelta(days=settings.refresh_token_days)),
    )
