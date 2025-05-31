from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from prompts.templates import PERSONALITY_MAPPER_PROMPT
from utils.data_models import PersonalityProfile, PersonalityTrait


class PersonalityMapperAgent(BaseAgent):
    """Agent that maps personality traits to work style preferences."""
    
    def __init__(self):
        super().__init__("Personality Mapper", PERSONALITY_MAPPER_PROMPT)
    
    def _get_input_variables(self) -> List[str]:
        """Get the list of input variables for the prompt template."""
        return ["name", "personality_responses", "additional_context", 
                "openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process personality responses and map to work preferences."""
        user_input = state["user_input"]
        
        # Extract personality scores or use defaults
        personality_responses = user_input.personality_responses or {}
        
        # Prepare input for the agent
        input_data = {
            "name": user_input.name,
            "personality_responses": self._format_dict_for_prompt(personality_responses),
            "additional_context": self._extract_basic_context(user_input, state),
            "openness": personality_responses.get("Openness to Experience", 3),
            "conscientiousness": personality_responses.get("Conscientiousness", 3),
            "extraversion": personality_responses.get("Extraversion", 3),
            "agreeableness": personality_responses.get("Agreeableness", 3),
            "neuroticism": personality_responses.get("Neuroticism", 3)
        }
        
        # Invoke the chain
        result = self._invoke_chain(input_data)
        
        # Create PersonalityProfile object
        try:
            # Convert trait scores to proper enum keys
            trait_scores = {}
            for trait_name, score in result.get("trait_scores", {}).items():
                try:
                    trait_enum = PersonalityTrait(trait_name)
                    trait_scores[trait_enum] = float(score)
                except (ValueError, TypeError):
                    # Handle case where trait name doesn't match enum
                    pass
            
            personality_profile = PersonalityProfile(
                trait_scores=trait_scores or self._get_default_trait_scores(),
                work_style_preferences=result.get("work_style_preferences", []),
                team_dynamics=result.get("team_dynamics", ""),
                reasoning=result.get("reasoning", "")
            )
            
            # Update state
            state["personality_profile"] = personality_profile
            
        except Exception as e:
            print(f"Error creating PersonalityProfile: {e}")
            state["personality_profile"] = self._get_fallback_personality_profile()
        
        return state

    def _get_default_trait_scores(self) -> Dict[PersonalityTrait, float]:
        """Get default trait scores when personality responses are not provided."""
        return {
            PersonalityTrait.OPENNESS: 3.0,
            PersonalityTrait.CONSCIENTIOUSNESS: 3.0,
            PersonalityTrait.EXTRAVERSION: 3.0,
            PersonalityTrait.AGREEABLENESS: 3.0,
            PersonalityTrait.NEUROTICISM: 3.0
        }
    
    def _get_fallback_response(self) -> Dict[str, Any]:
        """Get a fallback response when the agent fails."""
        return {
            "trait_scores": {
                "Openness to Experience": 3.0,
                "Conscientiousness": 3.0,
                "Extraversion": 3.0,
                "Agreeableness": 3.0,
                "Neuroticism": 3.0
            },
            "work_style_preferences": [
                "Collaborative environment",
                "Structured tasks",
                "Learning opportunities"
            ],
            "team_dynamics": "Works well in balanced team environments with clear communication.",
            "reasoning": "Unable to analyze personality responses. Provided balanced work preferences."
        }
    
    def _get_fallback_personality_profile(self) -> PersonalityProfile:
        """Get a fallback PersonalityProfile when processing fails."""
        fallback_data = self._get_fallback_response()
        return PersonalityProfile(
            trait_scores=self._get_default_trait_scores(),
            work_style_preferences=fallback_data["work_style_preferences"],
            team_dynamics=fallback_data["team_dynamics"],
            reasoning=fallback_data["reasoning"]
        )
