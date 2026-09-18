from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import decode_access_token
from app.db import get_db
from app.models import Account

bearer = HTTPBearer(auto_error=False)


def current_account(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    db: Annotated[Session, Depends(get_db)],
) -> Account:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"code": "AUTH_REQUIRED", "message": "Authentication required"})
    try:
        payload = decode_access_token(credentials.credentials, get_settings())
        account_id = UUID(payload["sub"])
    except (ValueError, KeyError):
        raise HTTPException(status_code=401, detail={"code": "AUTH_REQUIRED", "message": "Invalid access token"}) from None
    account = db.get(Account, account_id)
    if account is None or account.status != "ACTIVE":
        raise HTTPException(status_code=401, detail={"code": "AUTH_REQUIRED", "message": "Account is inactive"})
    return account


def require_role(role: str):
    def dependency(account: Annotated[Account, Depends(current_account)]) -> Account:
        if role not in account.roles.split(","):
            raise HTTPException(status_code=403, detail={"code": "FORBIDDEN", "message": "Insufficient role"})
        return account

    return dependency
