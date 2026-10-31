from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, func, Text
from sqlalchemy.orm import relationship

from app.models.base import Base


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, nullable=False, index=True)
    module_id = Column(Integer, nullable=False, index=True)
    status = Column(String(30), default="not_started")  # not_started, in_progress, completed
    completed_at = Column(DateTime(timezone=True), nullable=True)
    quiz_score = Column(Integer, nullable=True)
    lab_passed = Column(Boolean, default=False)
    time_spent_minutes = Column(Integer, default=0)

    user = relationship("User", back_populates="progress")


class LabAttempt(Base):
    __tablename__ = "lab_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lab_id = Column(Integer, nullable=False, index=True)
    status = Column(String(30), default="in_progress")  # in_progress, passed, failed, reset
    final_state = Column(Text, nullable=True)  # JSON
    score = Column(Integer, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="lab_attempts")


class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assignment_id = Column(Integer, nullable=False, index=True)
    score = Column(Integer, nullable=False)
    total_points = Column(Integer, nullable=False)
    answers = Column(Text, nullable=True)  # JSON
    passed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="attempts")


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, nullable=True, index=True)
    command_id = Column(Integer, nullable=True, index=True)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="bookmarks")


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    badge_icon = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
