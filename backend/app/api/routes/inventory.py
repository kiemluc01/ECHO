from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import current_account
from app.db import get_db
from app.models import Account, Character, InventoryItem
from app.schemas import InventoryItemResponse

router = APIRouter()


@router.get("/characters/{character_id}/inventory", response_model=dict)
def inventory(character_id: str, account: Account = Depends(current_account), db: Session = Depends(get_db)) -> dict:
    character = db.scalar(select(Character).where(Character.id == character_id, Character.account_id == account.id, Character.status == "ACTIVE"))
    if character is None:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Character not found"})
    items = db.scalars(select(InventoryItem).where(InventoryItem.character_id == character.id, InventoryItem.status == "ACTIVE")).all()
    return {"data": [InventoryItemResponse.model_validate(item).model_dump(mode="json") for item in items]}


@router.get("/wallet", response_model=dict)
def wallet(account: Account = Depends(current_account)) -> dict:
    return {"data": {"gold": 0, "premiumCoin": 0, "status": "skeleton"}}
