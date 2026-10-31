from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.api.deps import DbDep, UserDep
from app.models.curriculum import (
    LearningPath,
    Module,
    Lesson,
    LearningObjective,
    CommandExample,
)
from app.models.progress import UserProgress
from app.schemas.curriculum import (
    LearningPathOut,
    ModuleOut,
    LessonOut,
    ProgressOut,
)

router = APIRouter(prefix="/curriculum", tags=["curriculum"])


@router.get("/paths", response_model=List[LearningPathOut])
def list_paths(db: DbDep):
    return db.query(LearningPath).filter(LearningPath.is_active == True).order_by(LearningPath.order).all()  # noqa: E712


@router.get("/outline")
def get_outline(db: DbDep):
    """Full syllabus outline: every active module (in chapter order) with its lessons."""
    modules = (
        db.query(Module)
        .filter(Module.is_active == True)  # noqa: E712
        .options(joinedload(Module.lessons))
        .order_by(Module.order)
        .all()
    )
    out = []
    for m in modules:
        lessons = sorted(
            [l for l in m.lessons if l.is_active], key=lambda l: l.order
        )
        out.append(
            {
                "id": m.id,
                "key": m.key,
                "title": m.title,
                "stage": m.stage,
                "description": m.description,
                "order": m.order,
                "lessons": [
                    {"slug": l.slug, "title": l.title, "order": l.order}
                    for l in lessons
                ],
            }
        )
    return out


@router.get("/paths/{path_key}/modules", response_model=List[ModuleOut])
def list_modules(path_key: str, db: DbDep):
    # Modules are shared across learning paths; return the full syllabus.
    # path_key is validated so callers can confirm a valid path was requested.
    path = db.query(LearningPath).filter(LearningPath.key == path_key).first()
    if not path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    return db.query(Module).filter(Module.is_active == True).order_by(Module.order).all()  # noqa: E712


@router.get("/modules/{module_key}/lessons", response_model=List[LessonOut])
def list_lessons(module_key: str, db: DbDep):
    module = db.query(Module).filter(Module.key == module_key).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return (
        db.query(Lesson)
        .filter(Lesson.module_id == module.id, Lesson.is_active == True)  # noqa: E712
        .order_by(Lesson.order)
        .all()
    )


@router.get("/lessons/{slug}", response_model=LessonOut)
def get_lesson(slug: str, db: DbDep, current_user: UserDep):
    lesson = db.query(Lesson).filter(Lesson.slug == slug).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.get("/lessons/{slug}/progress", response_model=Optional[ProgressOut])
def get_lesson_progress(slug: str, db: DbDep, current_user: UserDep):
    if current_user is None:
        return None
    lesson = db.query(Lesson).filter(Lesson.slug == slug).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    progress = (
        db.query(UserProgress)
        .filter(UserProgress.user_id == current_user.id, UserProgress.lesson_id == lesson.id)
        .first()
    )
    return progress
