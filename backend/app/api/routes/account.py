from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import current_account
from app.db import get_db
from app.models import Account
from app.schemas import AccountResponse

router = APIRouter()


def account_response(account: Account) -> dict:
    return {"id": account.id, "email": account.email, "displayName": account.display_name, "provider": account.provider, "status": account.status, "roles": account.roles.split(",")}


@router.get("/me")
def me(account: Account = Depends(current_account)) -> dict:
    return {"data": account_response(account)}


@router.delete("/me")
def archive_me(account: Account = Depends(current_account), db: Session = Depends(get_db)) -> dict:
    account.status = "ARCHIVED"
    db.commit()
    return {"data": {"status": "ARCHIVED"}}
