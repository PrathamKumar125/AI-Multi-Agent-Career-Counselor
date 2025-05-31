from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from prompts.templates import SKILL_EVALUATOR_PROMPT
from utils.data_models import SkillProfile


class SkillEvaluatorAgent(BaseAgent):
    """Agent that analyzes and evaluates user skills from resumes and input."""
    
    def __init__(self):
        super().__init__("Skill Evaluator", SKILL_EVALUATOR_PROMPT)
    
    def _get_input_variables(self) -> List[str]:
        """Get the list of input variables for the prompt template."""
        return ["name", "education_level", "resume_text", "additional_context"]
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process user input and analyze skills."""
        user_input = state["user_input"]
        
        # Prepare input for the agent
        input_data = {
            "name": user_input.name,
            "education_level": user_input.education_level,
            "resume_text": user_input.resume_text or "No resume provided",
            "additional_context": self._extract_basic_context(user_input, state)
        }
        
        # Invoke the chain
        result = self._invoke_chain(input_data)
        
        # Create SkillProfile object safely
        return self._create_profile_safely(result, SkillProfile, "skill_profile", state, self._get_fallback_skill_profile)

    def _get_fallback_response(self) -> Dict[str, Any]:
        """Get a fallback response when the agent fails."""
        return {
            "technical_skills": ["Communication", "Problem Solving", "Teamwork"],
            "soft_skills": ["Leadership", "Time Management", "Adaptability"],
            "skill_levels": {
                "Communication": "Intermediate",
                "Problem Solving": "Intermediate",
                "Teamwork": "Intermediate"
            },
            "experience_years": 0,
            "reasoning": "Unable to analyze skills from provided information. Provided general foundational skills."
        }
    
    def _get_fallback_skill_profile(self) -> SkillProfile:
        """Get a fallback SkillProfile when processing fails."""
        fallback_data = self._get_fallback_response()
        return SkillProfile(
            technical_skills=fallback_data["technical_skills"],
            soft_skills=fallback_data["soft_skills"],
            skill_levels=fallback_data["skill_levels"],
            experience_years=fallback_data["experience_years"],
            reasoning=fallback_data["reasoning"]
        )
