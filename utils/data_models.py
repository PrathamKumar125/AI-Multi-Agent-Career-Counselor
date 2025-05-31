from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum

class PersonalityTrait(str, Enum):
    """Big Five personality traits."""
    OPENNESS = "Openness to Experience"
    CONSCIENTIOUSNESS = "Conscientiousness"
    EXTRAVERSION = "Extraversion"
    AGREEABLENESS = "Agreeableness"
    NEUROTICISM = "Neuroticism"

class InterestCategory(str, Enum):
    """Career interest categories."""
    TECHNOLOGY = "Technology & Engineering"
    HEALTHCARE = "Healthcare & Medicine"
    BUSINESS = "Business & Finance"
    ARTS = "Arts & Creative"
    EDUCATION = "Education & Training"
    SCIENCE = "Science & Research"
    SOCIAL = "Social Services"
    LAW = "Law & Government"
    SPORTS = "Sports & Recreation"
    AGRICULTURE = "Agriculture & Environment"

class UserInput(BaseModel):
    """User input data model."""
    name: str = Field(..., description="User's name")
    age: Optional[int] = Field(None, description="User's age")
    education_level: str = Field(..., description="Current education level")
    resume_text: Optional[str] = Field(None, description="Resume content")
    interests: List[str] = Field(default=[], description="User's interests")
    personality_responses: Dict[str, float] = Field(default={}, description="Personality questionnaire responses")

class InterestProfile(BaseModel):
    """Interest analysis results."""
    primary_interests: List[str] = Field(..., description="Top 3 interest categories")
    interest_scores: Dict[str, float] = Field(..., description="Scores for each interest category")
    reasoning: str = Field(..., description="Explanation of interest analysis")

class SkillProfile(BaseModel):
    """Skill evaluation results."""
    technical_skills: List[str] = Field(default=[], description="Technical skills identified")
    soft_skills: List[str] = Field(default=[], description="Soft skills identified")
    skill_levels: Dict[str, str] = Field(default={}, description="Skill proficiency levels")
    experience_years: Optional[float] = Field(None, description="Years of experience")
    reasoning: str = Field(..., description="Explanation of skill analysis")

class PersonalityProfile(BaseModel):
    """Personality mapping results."""
    trait_scores: Dict[PersonalityTrait, float] = Field(..., description="Big Five trait scores")
    work_style_preferences: List[str] = Field(..., description="Preferred work styles")
    team_dynamics: str = Field(..., description="Team interaction preferences")
    reasoning: str = Field(..., description="Explanation of personality analysis")

class MarketTrends(BaseModel):
    """Market trend analysis results."""
    trending_careers: List[str] = Field(..., description="Currently trending careers")
    growth_sectors: List[str] = Field(..., description="High-growth industry sectors")
    salary_insights: Dict[str, str] = Field(default={}, description="Salary information for relevant careers")
    job_outlook: Dict[str, str] = Field(default={}, description="Job outlook for recommended careers")
    reasoning: str = Field(..., description="Explanation of market analysis")

class CareerRecommendation(BaseModel):
    """Individual career recommendation."""
    title: str = Field(..., description="Career title")
    match_score: float = Field(..., description="Match score (0-100)")
    required_skills: List[str] = Field(..., description="Skills needed for this career")
    education_requirements: str = Field(..., description="Education requirements")
    salary_range: str = Field(..., description="Expected salary range")
    job_outlook: str = Field(..., description="Job market outlook")
    why_recommended: str = Field(..., description="Explanation of why this career fits")

class CareerRecommendations(BaseModel):
    """Complete career recommendations."""
    top_recommendations: List[CareerRecommendation] = Field(..., description="Top 3-5 career recommendations")
    alternative_paths: List[str] = Field(default=[], description="Alternative career paths to consider")
    next_steps: List[str] = Field(..., description="Recommended next steps")
    reasoning: str = Field(..., description="Overall recommendation reasoning")

class FormattedOutput(BaseModel):
    """Final formatted output."""
    summary: str = Field(..., description="Executive summary of recommendations")
    detailed_report: str = Field(..., description="Detailed career counseling report")
    action_plan: List[str] = Field(..., description="Actionable steps for the user")
    resources: List[str] = Field(default=[], description="Helpful resources and links")

class AgentState(BaseModel):
    """State object passed between agents in the workflow."""
    user_input: UserInput
    interest_profile: Optional[InterestProfile] = None
    skill_profile: Optional[SkillProfile] = None
    personality_profile: Optional[PersonalityProfile] = None
    market_trends: Optional[MarketTrends] = None
    career_recommendations: Optional[CareerRecommendations] = None
    formatted_output: Optional[FormattedOutput] = None
    
    class Config:
        arbitrary_types_allowed = True
