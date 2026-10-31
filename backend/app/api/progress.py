from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import DbDep, UserDep
from app.models.curriculum import Lesson
from app.models.progress import UserProgress
from app.schemas.curriculum import ProgressOut

router = APIRouter(prefix="/progress", tags=["progress"])


@router.post("/lessons/{slug}")
def update_lesson_progress(
    slug: str,
    payload: dict,
    db: DbDep,
    current_user: UserDep,
):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication required to save progress")
    lesson = db.query(Lesson).filter(Lesson.slug == slug).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    progress = (
        db.query(UserProgress)
        .filter(UserProgress.user_id == current_user.id, UserProgress.lesson_id == lesson.id)
        .first()
    )
    status_val = payload.get("status", "in_progress")
    if progress is None:
        progress = UserProgress(
            user_id=current_user.id,
            lesson_id=lesson.id,
            module_id=lesson.module_id,
            status=status_val,
            quiz_score=payload.get("quiz_score"),
            lab_passed=payload.get("lab_passed", False),
            time_spent_minutes=payload.get("time_spent_minutes", 0),
        )
        if status_val == "completed":
            from datetime import datetime

            progress.completed_at = datetime.utcnow()
        db.add(progress)
    else:
        progress.status = status_val
        if payload.get("quiz_score") is not None:
            progress.quiz_score = payload["quiz_score"]
        progress.lab_passed = payload.get("lab_passed", progress.lab_passed)
        progress.time_spent_minutes = payload.get("time_spent_minutes", progress.time_spent_minutes)
        if status_val == "completed" and not progress.completed_at:
            from datetime import datetime

            progress.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(progress)
    return ProgressOut.model_validate(progress)


@router.get("/summary")
def get_progress_summary(db: DbDep, current_user: UserDep):
    if current_user is None:
        return {"completed": 0, "total": 0, "lessons": []}
    total = db.query(Lesson).filter(Lesson.is_active == True).count()  # noqa: E712
    completed = (
        db.query(UserProgress)
        .filter(UserProgress.user_id == current_user.id, UserProgress.status == "completed")
        .count()
    )
    return {"completed": completed, "total": total}
