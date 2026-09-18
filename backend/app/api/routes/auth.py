from datetime import timedelta
from urllib.parse import urlencode

from fastapi import APIRouter, HTTPException

from app.core.config import get_settings
from app.core.security import create_oauth_state, decode_oauth_state

router = APIRouter()

PROVIDERS = {
    "google": "https://accounts.google.com/o/oauth2/v2/auth",
    "apple": "https://appleid.apple.com/auth/authorize",
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
    return {"data": {"provider": provider, "authorization_url": f"{PROVIDERS[provider]}?{query}"}}


@router.get("/{provider}/callback")
def oauth_callback(provider: str, code: str, state: str) -> dict:
    try:
        decode_oauth_state(state, get_settings(), provider)
    except ValueError:
        raise HTTPException(status_code=400, detail={"code": "INVALID_OAUTH_STATE", "message": "OAuth state is invalid or expired"}) from None
    raise HTTPException(status_code=501, detail={"code": "OAUTH_EXCHANGE_NOT_IMPLEMENTED", "message": "Exchange the authorization code through the configured provider adapter"})


@router.post("/refresh", response_model=dict)
def refresh() -> dict:
    raise HTTPException(status_code=501, detail={"code": "REFRESH_NOT_IMPLEMENTED", "message": "Refresh token rotation is pending provider integration"})
