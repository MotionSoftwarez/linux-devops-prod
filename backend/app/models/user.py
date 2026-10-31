from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)  # nullable for OAuth/guest
    full_name = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)
    is_guest = Column(Boolean, default=False)
    learning_goal = Column(String(100), nullable=True)  # beginner, administrator, devops, etc.
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    progress = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")
    attempts = relationship("AssessmentAttempt", back_populates="user", cascade="all, delete-orphan")
    lab_attempts = relationship("LabAttempt", back_populates="user", cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")
