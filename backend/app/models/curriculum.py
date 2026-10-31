from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Boolean,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship

from app.models.base import Base


class LearningPath(Base):
    __tablename__ = "learning_paths"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    target_audience = Column(Text, nullable=True)
    estimated_hours = Column(Integer, nullable=True)
    order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    modules = relationship("Module", back_populates="path", cascade="all, delete-orphan")


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    path_id = Column(Integer, ForeignKey("learning_paths.id"), nullable=True)
    key = Column(String(100), index=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    stage = Column(String(50), nullable=True)  # stage 1..5
    order = Column(Integer, default=0)
    estimated_hours = Column(Integer, nullable=True)
    prerequisites = Column(Text, nullable=True)  # JSON-ish or module keys
    is_active = Column(Boolean, default=True)

    path = relationship("LearningPath", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    key = Column(String(100), index=True, nullable=False)
    title = Column(String(200), nullable=False)
    slug = Column(String(120), unique=True, index=True, nullable=False)
    order = Column(Integer, default=0)
    difficulty = Column(String(20), default="beginner")  # beginner, intermediate, advanced
    estimated_minutes = Column(Integer, default=15)
    summary = Column(Text, nullable=True)
    content = Column(Text, nullable=True)  # JSON-encoded structured lesson content
    prerequisites = Column(Text, nullable=True)  # lesson keys
    has_lab = Column(Boolean, default=False)
    has_quiz = Column(Boolean, default=False)
    completion_criteria = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    module = relationship("Module", back_populates="lessons")
    objectives = relationship("LearningObjective", back_populates="lesson", cascade="all, delete-orphan")
    examples = relationship("CommandExample", back_populates="lesson", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="lesson", cascade="all, delete-orphan")


class LearningObjective(Base):
    __tablename__ = "learning_objectives"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    text = Column(Text, nullable=False)
    order = Column(Integer, default=0)

    lesson = relationship("Lesson", back_populates="objectives")


class CommandExample(Base):
    __tablename__ = "command_examples"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    command = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    expected_output = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)
    is_dangerous = Column(Boolean, default=False)
    order = Column(Integer, default=0)

    lesson = relationship("Lesson", back_populates="examples")


class Lab(Base):
    __tablename__ = "labs"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), unique=True, nullable=False)
    title = Column(String(200), nullable=False)
    objective = Column(Text, nullable=False)
    completion_criteria = Column(Text, nullable=False)  # JSON-encoded validation rules
    initial_state = Column(Text, nullable=True)  # JSON-encoded scenario initial state
    safe_commands = Column(Text, nullable=True)  # JSON list of allowed commands
    is_active = Column(Boolean, default=True)


class LabScenario(Base):
    __tablename__ = "lab_scenarios"

    id = Column(Integer, primary_key=True, index=True)
    lab_id = Column(Integer, ForeignKey("labs.id"), nullable=False)
    key = Column(String(100), index=True, nullable=False)
    title = Column(String(200), nullable=False)
    context = Column(Text, nullable=True)
    symptoms = Column(Text, nullable=True)
    evidence = Column(Text, nullable=True)
    root_cause = Column(Text, nullable=True)
    solution = Column(Text, nullable=True)
    verification = Column(Text, nullable=True)
    prevention = Column(Text, nullable=True)
    is_guided = Column(Boolean, default=True)
    order = Column(Integer, default=0)


class CheatSheet(Base):
    __tablename__ = "cheat_sheets"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    topic = Column(String(100), index=True, nullable=False)
    category = Column(String(100), nullable=True)
    content = Column(Text, nullable=True)  # JSON-encoded entries
    is_active = Column(Boolean, default=True)


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    level = Column(String(20), nullable=False)  # foundation, practical, challenge
    title = Column(String(200), nullable=False)
    instructions = Column(Text, nullable=False)
    points = Column(Integer, default=10)
    order = Column(Integer, default=0)

    lesson = relationship("Lesson", back_populates="assignments")
    questions = relationship("Question", back_populates="assignment", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    type = Column(String(30), nullable=False)  # multiple_choice, command_completion, output_interpretation, diagnosis
    prompt = Column(Text, nullable=False)
    options = Column(Text, nullable=True)  # JSON for multiple choice
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    points = Column(Integer, default=1)
    order = Column(Integer, default=0)

    assignment = relationship("Assignment", back_populates="questions")
