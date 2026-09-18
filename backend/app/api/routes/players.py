from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import current_account
from app.db import get_db
from app.models import Account, Character
from app.schemas import CharacterCreate, CharacterResponse

router = APIRouter()


@router.get("/characters", response_model=dict)
def list_characters(account: Account = Depends(current_account), db: Session = Depends(get_db)) -> dict:
    characters = db.scalars(select(Character).where(Character.account_id == account.id, Character.status == "ACTIVE")).all()
    return {"data": [CharacterResponse.model_validate(item).model_dump(mode="json") for item in characters]}


@router.post("/characters", response_model=dict, status_code=201)
def create_character(payload: CharacterCreate, account: Account = Depends(current_account), db: Session = Depends(get_db)) -> dict:
    if db.scalar(select(Character).where(Character.name == payload.name)) is not None:
        raise HTTPException(status_code=409, detail={"code": "CHARACTER_NAME_TAKEN", "message": "Character name is already in use"})
    character = Character(account_id=account.id, name=payload.name)
    db.add(character)
    db.commit()
    db.refresh(character)
    return {"data": CharacterResponse.model_validate(character).model_dump(mode="json")}


@router.get("/characters/{character_id}", response_model=dict)
def get_character(character_id: str, account: Account = Depends(current_account), db: Session = Depends(get_db)) -> dict:
    character = db.scalar(select(Character).where(Character.id == character_id, Character.account_id == account.id, Character.status == "ACTIVE"))
    if character is None:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Character not found"})
    return {"data": CharacterResponse.model_validate(character).model_dump(mode="json")}
