from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class QuestionnaireAnswers:
    name: str
    current_year: int
    total_years: int
    degree_type: str
    preferred_work_style: str
    answers: Dict  # { "Q1": ["A"], "Q12": ["A", "C"] }


@dataclass
class UserInput:
    name: str
    current_year: int
    total_years: int
    degree_type: str
    interests: List[str]
    skill_level: str
    preferred_work_style: str = "both"
    knows_git: bool = False
    knows_docker: bool = False
    target_role: Optional[str] = None
    languages_known: List[str] = field(default_factory=list)


@dataclass
class Resource:
    title: str
    url: str
    type: str
    estimated_hours: int
    difficulty: str


@dataclass
class Milestone:
    month: int
    title: str
    description: str
    skills_to_gain: List[str]
    resources: List[Resource]
    projects: List[str]


@dataclass
class CareerPathResponse:
    user_name: str
    recommended_domain: str
    confidence_score: float
    years_remaining: float
    career_goal: str
    summary: str
    path_id: str
    inferred_profile: Dict
    skill_gap_analysis: Dict
    monthly_milestones: List[Milestone]
    essential_tools: List[Resource]
    job_roles: List[str]
    salary_range_india: str
    salary_range_global: str
    top_companies_hiring: List[str]
    certifications: List[str]
    advice: str
    generated_at: str