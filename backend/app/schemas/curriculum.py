from typing import Any, List, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


# ---------- Learning Path ----------
class LearningPathBase(BaseModel):
    key: str
    title: str
    description: Optional[str] = None
    target_audience: Optional[str] = None
    estimated_hours: Optional[int] = None
    order: int = 0
    is_active: bool = True


class LearningPathCreate(LearningPathBase):
    pass


class LearningPathOut(LearningPathBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------- Module ----------
class ModuleBase(BaseModel):
    path_id: Optional[int] = None
    key: str
    title: str
    description: Optional[str] = None
    stage: Optional[str] = None
    order: int = 0
    estimated_hours: Optional[int] = None
    prerequisites: Optional[str] = None
    is_active: bool = True


class ModuleCreate(ModuleBase):
    pass


class ModuleOut(ModuleBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------- Lesson ----------
class LessonBase(BaseModel):
    module_id: int
    key: str
    title: str
    slug: str
    order: int = 0
    difficulty: str = "beginner"
    estimated_minutes: int = 15
    summary: Optional[str] = None
    content: Optional[Any] = None
    prerequisites: Optional[str] = None
    has_lab: bool = False
    has_quiz: bool = False
    completion_criteria: Optional[str] = None
    is_active: bool = True


class LessonCreate(LessonBase):
    pass


class LessonOut(LessonBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------- Lab ----------
class LabBase(BaseModel):
    lesson_id: int
    title: str
    objective: str
    completion_criteria: str  # JSON
    initial_state: Optional[str] = None  # JSON
    safe_commands: Optional[str] = None  # JSON
    is_active: bool = True


class LabCreate(LabBase):
    pass


class LabOut(LabBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ---------- Cheat Sheet ----------
class CheatSheetBase(BaseModel):
    key: str
    title: str
    topic: str
    category: Optional[str] = None
    content: Optional[Any] = None
    is_active: bool = True


class CheatSheetCreate(CheatSheetBase):
    pass


class CheatSheetOut(CheatSheetBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------- Progress ----------
class ProgressBase(BaseModel):
    lesson_id: int
    module_id: int
    status: str = "not_started"
    quiz_score: Optional[int] = None
    lab_passed: bool = False
    time_spent_minutes: int = 0


class ProgressOut(ProgressBase):
    id: int
    user_id: int
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ---------- Auth ----------
class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserBase(BaseModel):
    email: str
    username: str
    full_name: Optional[str] = None
    learning_goal: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    is_active: bool
    is_guest: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
