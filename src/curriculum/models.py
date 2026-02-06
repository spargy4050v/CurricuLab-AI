"""
Pydantic models for structured curriculum data.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class Course(BaseModel):
    """Individual course in a curriculum."""
    code: str = Field(..., description="Course code (e.g., CS101)")
    name: str = Field(..., description="Course name")
    credits: int = Field(..., description="Credit hours", ge=1, le=6)
    description: str = Field(..., description="Course description")
    prerequisites: Optional[List[str]] = Field(default=None, description="Prerequisite course codes")
    category: str = Field(..., description="Course category (Core/Elective/Lab)")


class Semester(BaseModel):
    """Semester structure with courses."""
    semester_number: int = Field(..., description="Semester number", ge=1)
    courses: List[Course] = Field(..., description="List of courses in this semester")
    total_credits: int = Field(..., description="Total credits for the semester")


class CurriculumRequest(BaseModel):
    """User input for curriculum generation."""
    skill: str = Field(..., description="Subject/Skill area (e.g., Machine Learning)")
    level: str = Field(..., description="Education level (BTech/Masters/Diploma/Certification)")
    duration_semesters: int = Field(..., description="Number of semesters", ge=1, le=12)
    specialization: Optional[str] = Field(default=None, description="Specialization area")
    focus_areas: Optional[List[str]] = Field(default=None, description="Specific focus areas")


class Curriculum(BaseModel):
    """Complete curriculum structure."""
    title: str = Field(..., description="Curriculum title")
    level: str = Field(..., description="Education level")
    duration_semesters: int = Field(..., description="Total semesters")
    total_credits: int = Field(..., description="Total credits required")
    semesters: List[Semester] = Field(..., description="Semester-wise breakdown")
    overview: str = Field(..., description="Curriculum overview")
    learning_outcomes: List[str] = Field(..., description="Expected learning outcomes")
    career_paths: Optional[List[str]] = Field(default=None, description="Career opportunities")
