from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from prompts.templates import CAREER_RECOMMENDER_PROMPT
from utils.data_models import CareerRecommendations, CareerRecommendation


class CareerRecommenderAgent(BaseAgent):
    """Agent that synthesizes all previous agent outputs to recommend careers."""
    
    def __init__(self):
        super().__init__("Career Recommender", CAREER_RECOMMENDER_PROMPT)
    
    def _get_input_variables(self) -> List[str]:
        """Get the list of input variables for the prompt template."""
        return ["interest_profile", "skill_profile", "personality_profile", 
                "market_trends", "name", "education_level"]
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process all agent outputs and synthesize career recommendations."""
        user_input = state["user_input"]
        
        # Prepare input for the agent
        input_data = {
            "interest_profile": self._format_agent_output(state.get("interest_profile")),
            "skill_profile": self._format_agent_output(state.get("skill_profile")),
            "personality_profile": self._format_agent_output(state.get("personality_profile")),
            "market_trends": self._format_agent_output(state.get("market_trends")),
            "name": user_input.name,
            "education_level": user_input.education_level
        }
        
        # Invoke the chain
        result = self._invoke_chain(input_data)
        
        # Create CareerRecommendations object
        try:
            # Parse individual recommendations
            top_recommendations = []
            for rec_data in result.get("top_recommendations", []):
                try:
                    recommendation = CareerRecommendation(
                        title=rec_data.get("title", ""),
                        match_score=float(rec_data.get("match_score", 0)),
                        required_skills=rec_data.get("required_skills", []),
                        education_requirements=rec_data.get("education_requirements", ""),
                        salary_range=rec_data.get("salary_range", ""),
                        job_outlook=rec_data.get("job_outlook", ""),
                        why_recommended=rec_data.get("why_recommended", "")
                    )
                    top_recommendations.append(recommendation)
                except Exception as e:
                    print(f"Error parsing recommendation: {e}")
                    continue
            
            career_recommendations = CareerRecommendations(
                top_recommendations=top_recommendations or self._get_fallback_recommendations(),
                alternative_paths=result.get("alternative_paths", []),
                next_steps=result.get("next_steps", []),
                reasoning=result.get("reasoning", "")
            )
            
            # Update state
            state["career_recommendations"] = career_recommendations
            
        except Exception as e:
            print(f"Error creating CareerRecommendations: {e}")
            state["career_recommendations"] = self._get_fallback_career_recommendations()
        
        return state

    def _get_fallback_response(self) -> Dict[str, Any]:
        """Get a fallback response when the agent fails."""
        return {
            "top_recommendations": [
                {
                    "title": "Business Analyst",
                    "match_score": 75,
                    "required_skills": ["Data Analysis", "Communication", "Problem Solving"],
                    "education_requirements": "Bachelor's degree preferred",
                    "salary_range": "$50,000 - $80,000 annually",
                    "job_outlook": "Positive growth expected",
                    "why_recommended": "Good match for analytical thinking and business interests"
                },
                {
                    "title": "Project Coordinator",
                    "match_score": 70,
                    "required_skills": ["Organization", "Communication", "Time Management"],
                    "education_requirements": "Bachelor's degree or equivalent experience",
                    "salary_range": "$45,000 - $70,000 annually",
                    "job_outlook": "Steady demand across industries",
                    "why_recommended": "Suitable for organized individuals who enjoy coordinating tasks"
                },
                {
                    "title": "Customer Success Specialist",
                    "match_score": 68,
                    "required_skills": ["Communication", "Empathy", "Problem Solving"],
                    "education_requirements": "Bachelor's degree preferred",
                    "salary_range": "$40,000 - $65,000 annually",
                    "job_outlook": "Growing field with high demand",
                    "why_recommended": "Perfect for people-oriented individuals who enjoy helping others"
                }
            ],
            "alternative_paths": [
                "Sales Representative",
                "Administrative Assistant",
                "Marketing Coordinator"
            ],
            "next_steps": [
                "Research the recommended career paths in detail",
                "Consider taking relevant online courses or certifications",
                "Network with professionals in these fields",
                "Update resume to highlight relevant skills",
                "Apply for entry-level positions or internships"
            ],
            "reasoning": "Unable to provide detailed analysis. Recommended versatile career paths suitable for various backgrounds."
        }
    
    def _get_fallback_recommendations(self) -> List[CareerRecommendation]:
        """Get fallback career recommendations."""
        fallback_data = self._get_fallback_response()
        recommendations = []
        
        for rec_data in fallback_data["top_recommendations"]:
            recommendation = CareerRecommendation(
                title=rec_data["title"],
                match_score=rec_data["match_score"],
                required_skills=rec_data["required_skills"],
                education_requirements=rec_data["education_requirements"],
                salary_range=rec_data["salary_range"],
                job_outlook=rec_data["job_outlook"],
                why_recommended=rec_data["why_recommended"]
            )
            recommendations.append(recommendation)
        
        return recommendations
    
    def _get_fallback_career_recommendations(self) -> CareerRecommendations:
        """Get a fallback CareerRecommendations when processing fails."""
        fallback_data = self._get_fallback_response()
        return CareerRecommendations(
            top_recommendations=self._get_fallback_recommendations(),
            alternative_paths=fallback_data["alternative_paths"],
            next_steps=fallback_data["next_steps"],
            reasoning=fallback_data["reasoning"]
        )
