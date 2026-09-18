from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import get_db

router = APIRouter()


@router.get("")
def health() -> dict:
    return {"data": {"status": "ok"}}


@router.get("/ready")
def readiness(db: Session = Depends(get_db)) -> dict:
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        return {"data": {"status": "not_ready", "database": "unavailable"}}
    return {"data": {"status": "ready", "database": "ok"}}
