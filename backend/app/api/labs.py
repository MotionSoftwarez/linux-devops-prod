import json
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import DbDep, UserDep
from app.models.curriculum import Lab, LabScenario, Lesson
from app.models.progress import LabAttempt
from app.db.session import SessionLocal

router = APIRouter(prefix="/labs", tags=["labs"])


@router.get("/lessons/{slug}")
def get_lab(slug: str, db: DbDep, current_user: UserDep):
    lesson = db.query(Lesson).filter(Lesson.slug == slug).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    if not lesson.has_lab:
        raise HTTPException(status_code=404, detail="This lesson has no lab")
    lab = db.query(Lab).filter(Lab.lesson_id == lesson.id).first()
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    scenarios = (
        db.query(LabScenario)
        .filter(LabScenario.lab_id == lab.id)
        .order_by(LabScenario.order)
        .all()
    )
    return {
        "lab": {
            "id": lab.id,
            "title": lab.title,
            "objective": lab.objective,
            "completion_criteria": json.loads(lab.completion_criteria) if lab.completion_criteria else {},
            "safe_commands": json.loads(lab.safe_commands) if lab.safe_commands else [],
        },
        "scenarios": [
            {
                "id": s.id,
                "key": s.key,
                "title": s.title,
                "context": s.context,
                "symptoms": s.symptoms,
                "evidence": s.evidence,
                "root_cause": s.root_cause,
                "solution": s.solution,
                "verification": s.verification,
                "prevention": s.prevention,
                "is_guided": s.is_guided,
            }
            for s in scenarios
        ],
        "initial_state": json.loads(lab.initial_state) if lab.initial_state else {},
    }


@router.post("/lessons/{slug}/attempt")
def submit_lab_attempt(
    slug: str,
    payload: Dict[str, Any],
    db: DbDep,
    current_user: UserDep,
):
    lesson = db.query(Lesson).filter(Lesson.slug == slug).first()
    if not lesson or not lesson.has_lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    lab = db.query(Lab).filter(Lab.lesson_id == lesson.id).first()
    criteria = json.loads(lab.completion_criteria) if lab.completion_criteria else {}

    final_state = payload.get("final_state", {})
    commands_run = payload.get("commands_run", [])

    # Validate against completion criteria
    checks = criteria.get("checks", [])
    passed = True
    details = []
    for check in checks:
        check_type = check.get("type")
        result = _run_check(check_type, check, final_state, commands_run)
        details.append({"check": check.get("id"), "passed": result, "message": check.get("message", "")})
        if not result:
            passed = False

    attempt = LabAttempt(
        user_id=current_user.id if current_user else 0,
        lab_id=lab.id,
        status="passed" if passed else "failed",
        final_state=json.dumps(final_state),
        score=100 if passed else 0,
    )
    db.add(attempt)
    db.commit()

    return {"passed": passed, "score": attempt.score, "details": details}


def _run_check(check_type: str, check: Dict, final_state: Dict, commands_run: List) -> bool:
    if check_type == "command_run":
        return check.get("command", "") in commands_run
    if check_type == "file_exists":
        return final_state.get("files", {}).get(check.get("path"), False) is not False
    if check_type == "service_running":
        return final_state.get("services", {}).get(check.get("service"), False) is True
    if check_type == "port_listening":
        return final_state.get("ports", {}).get(check.get("port"), False) is True
    if check_type == "file_content_contains":
        files = final_state.get("files", {})
        content = files.get(check.get("path"), "")
        return check.get("substring", "") in str(content)
    return False
