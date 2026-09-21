from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import current_account
from app.db import get_db
from app.models import Account, Character, CharacterQuest, Quest
from app.schemas import QuestProgressUpdate, QuestResponse

router = APIRouter()


def _owned_character(character_id: str, account: Account, db: Session) -> Character:
    character = db.scalar(
        select(Character).where(
            Character.id == character_id,
            Character.account_id == account.id,
            Character.status == "ACTIVE",
        )
    )
    if character is None:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Character not found"})
    return character


def _merge(quest: Quest, progress: CharacterQuest | None) -> dict:
    return QuestResponse(
        code=quest.code,
        title=quest.title,
        summary=quest.summary,
        objective=quest.objective,
        required_progress=quest.required_progress,
        reward_xp=quest.reward_xp,
        state=progress.state if progress is not None else "NOT_STARTED",
        progress=progress.progress if progress is not None else 0,
    ).model_dump(mode="json")


@router.get("/characters/{character_id}/quests", response_model=dict)
def list_quests(character_id: str, account: Account = Depends(current_account), db: Session = Depends(get_db)) -> dict:
    character = _owned_character(character_id, account, db)
    quests = db.scalars(select(Quest).where(Quest.status == "ACTIVE").order_by(Quest.sort_order)).all()
    progress_by_code = {
        row.quest_code: row
        for row in db.scalars(select(CharacterQuest).where(CharacterQuest.character_id == character.id)).all()
    }
    return {"data": [_merge(quest, progress_by_code.get(quest.code)) for quest in quests]}


@router.post("/characters/{character_id}/quests/{quest_code}/progress", response_model=dict)
def update_progress(
    character_id: str,
    quest_code: str,
    payload: QuestProgressUpdate,
    account: Account = Depends(current_account),
    db: Session = Depends(get_db),
) -> dict:
    character = _owned_character(character_id, account, db)
    quest = db.scalar(select(Quest).where(Quest.code == quest_code, Quest.status == "ACTIVE"))
    if quest is None:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Quest not found"})

    row = db.scalar(
        select(CharacterQuest).where(
            CharacterQuest.character_id == character.id,
            CharacterQuest.quest_code == quest.code,
        )
    )
    if row is None:
        row = CharacterQuest(character_id=character.id, quest_code=quest.code)
        db.add(row)

    row.progress = min(payload.progress, quest.required_progress)
    row.state = "COMPLETED" if row.progress >= quest.required_progress else "IN_PROGRESS"
    db.commit()
    db.refresh(row)
    return {"data": _merge(quest, row)}
