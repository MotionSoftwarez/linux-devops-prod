from typing import Any, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import DbDep
from app.models.curriculum import CheatSheet
from app.schemas.curriculum import CheatSheetOut

router = APIRouter(prefix="/cheatsheets", tags=["cheat-sheets"])


@router.get("", response_model=List[CheatSheetOut])
def list_cheatsheets(
    db: DbDep,
    topic: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
):
    q = db.query(CheatSheet).filter(CheatSheet.is_active == True)  # noqa: E712
    if topic:
        q = q.filter(CheatSheet.topic == topic)
    if category:
        q = q.filter(CheatSheet.category == category)
    if search:
        like = f"%{search}%"
        q = q.filter(CheatSheet.title.ilike(like) | CheatSheet.topic.ilike(like))
    return q.order_by(CheatSheet.topic, CheatSheet.title).all()


@router.get("/topics")
def list_topics(db: DbDep):
    topics = (
        db.query(CheatSheet.topic)
        .filter(CheatSheet.is_active == True)  # noqa: E712
        .distinct()
        .all()
    )
    return [t[0] for t in topics]


@router.get("/{key}", response_model=CheatSheetOut)
def get_cheatsheet(key: str, db: DbDep):
    cs = db.query(CheatSheet).filter(CheatSheet.key == key).first()
    if not cs:
        raise HTTPException(status_code=404, detail="Cheat sheet not found")
    return cs
