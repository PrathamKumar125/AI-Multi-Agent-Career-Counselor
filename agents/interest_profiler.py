from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from prompts.templates import INTEREST_PROFILER_PROMPT
from utils.data_models import InterestProfile


class InterestProfilerAgent(BaseAgent):
    """Agent that analyzes user interests and maps them to career categories."""
    
    def __init__(self):
        super().__init__("Interest Profiler", INTEREST_PROFILER_PROMPT)
    
    def _get_input_variables(self) -> List[str]:
        """Get the list of input variables for the prompt template."""
        return ["name", "age", "education_level", "interests", "additional_context"]
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process user input and analyze interests."""
        user_input = state["user_input"]
        
        # Prepare input for the agent
        input_data = {
            "name": user_input.name,
            "age": user_input.age or "Not specified",
            "education_level": user_input.education_level,
            "interests": self._format_list_for_prompt(user_input.interests),
            "additional_context": self._extract_additional_context(user_input)
        }
        
        # Invoke the chain
        result = self._invoke_chain(input_data)
        
        # Create InterestProfile object safely
        return self._create_profile_safely(result, InterestProfile, "interest_profile", state, self._get_fallback_interest_profile)
    
    def _extract_additional_context(self, user_input) -> str:
        """Extract additional context from user input."""
        context_parts = []
        
        if user_input.resume_text:
            context_parts.append(f"Resume mentions: {user_input.resume_text[:200]}...")
        
        if user_input.personality_responses:
            context_parts.append("Personality responses provided")
        
        return " | ".join(context_parts) if context_parts else "No additional context"
    
    def _get_fallback_response(self) -> Dict[str, Any]:
        """Get a fallback response when the agent fails."""
        return {
            "primary_interests": ["Technology & Engineering", "Business & Finance", "Education & Training"],
            "interest_scores": {
                "Technology & Engineering": 70,
                "Healthcare & Medicine": 30,
                "Business & Finance": 60,
                "Arts & Creative": 40,
                "Education & Training": 50,
                "Science & Research": 45,
                "Social Services": 35,
                "Law & Government": 25,
                "Sports & Recreation": 20,
                "Agriculture & Environment": 15
            },
            "reasoning": "Unable to analyze interests fully. Provided general recommendations based on common career paths."
        }
    
    def _get_fallback_interest_profile(self) -> InterestProfile:
        """Get a fallback InterestProfile when processing fails."""
        fallback_data = self._get_fallback_response()
        return InterestProfile(
            primary_interests=fallback_data["primary_interests"],
            interest_scores=fallback_data["interest_scores"],
            reasoning=fallback_data["reasoning"]
        )
