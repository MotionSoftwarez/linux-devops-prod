from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import DbDep, UserDep
from app.models.curriculum import Lesson, Assignment, Question
from app.models.progress import AssessmentAttempt

router = APIRouter(prefix="/assessments", tags=["assessments"])


@router.get("/lessons/{slug}")
def get_lesson_assessment(slug: str, db: DbDep):
    lesson = db.query(Lesson).filter(Lesson.slug == slug).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    assignments = (
        db.query(Assignment)
        .filter(Assignment.lesson_id == lesson.id)
        .order_by(Assignment.order)
        .all()
    )
    result = []
    for a in assignments:
        questions = (
            db.query(Question)
            .filter(Question.assignment_id == a.id)
            .order_by(Question.order)
            .all()
        )
        result.append(
            {
                "id": a.id,
                "level": a.level,
                "title": a.title,
                "instructions": a.instructions,
                "points": a.points,
                "questions": [
                    {
                        "id": q.id,
                        "type": q.type,
                        "prompt": q.prompt,
                        "options": q.options,
                        "points": q.points,
                        # correct_answer excluded from client; validated server-side
                    }
                    for q in questions
                ],
            }
        )
    return result


@router.post("/lessons/{slug}/submit")
def submit_assessment(slug: str, payload: Dict[str, Any], db: DbDep, current_user: UserDep):
    lesson = db.query(Lesson).filter(Lesson.slug == slug).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    answers = payload.get("answers", {})  # {question_id: answer}

    total_points = 0
    earned = 0
    question_results = []
    assignments = db.query(Assignment).filter(Assignment.lesson_id == lesson.id).all()
    for a in assignments:
        for q in db.query(Question).filter(Question.assignment_id == a.id).all():
            total_points += q.points
            user_answer = str(answers.get(str(q.id), ""))
            correct = str(q.correct_answer).strip().strip('"').strip("'")
            is_correct = user_answer.strip().lower() == correct.lower() or user_answer.strip() == correct
            if is_correct:
                earned += q.points
            question_results.append(
                {
                    "question_id": q.id,
                    "correct": is_correct,
                    "correct_answer": q.correct_answer,
                    "explanation": q.explanation,
                }
            )

    passed = earned >= total_points * 0.7
    attempt = AssessmentAttempt(
        user_id=current_user.id if current_user else 0,
        assignment_id=assignments[0].id if assignments else 0,
        score=earned,
        total_points=total_points,
        answers=str(answers),
        passed=passed,
    )
    db.add(attempt)
    db.commit()

    return {
        "passed": passed,
        "score": earned,
        "total_points": total_points,
        "percentage": round((earned / total_points) * 100, 1) if total_points else 0,
        "results": question_results,
    }
