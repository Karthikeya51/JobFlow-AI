from typing import List

from pydantic import BaseModel, Field, field_validator


class JobAnalysisResult(BaseModel):
    summary: str = Field(..., min_length=10, max_length=2000)
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    experience_requirements: str = Field(..., min_length=1, max_length=500)
    keywords: list[str] = Field(default_factory=list)

    @field_validator("required_skills", "preferred_skills", "responsibilities", "keywords")
    @classmethod
    def validate_lists(cls, value):
        return [str(item).strip() for item in value if str(item).strip()]


class ResumeMatchResult(BaseModel):
    match_score: int = Field(..., ge=0, le=100)
    summary: str = Field(..., min_length=10, max_length=2000)
    strengths: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)

    @field_validator("strengths", "missing_skills", "recommendations")
    @classmethod
    def validate_lists(cls, value):
        return [str(item).strip() for item in value if str(item).strip()]


class AnalysisResponseSchema(BaseModel):
    job_analysis: JobAnalysisResult | None = None
    resume_match: ResumeMatchResult | None = None
