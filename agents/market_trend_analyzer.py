from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from prompts.templates import MARKET_TREND_ANALYZER_PROMPT
from utils.data_models import MarketTrends


class MarketTrendAnalyzerAgent(BaseAgent):
    """Agent that analyzes current job market trends and career opportunities."""
    
    def __init__(self):
        super().__init__("Market Trend Analyzer", MARKET_TREND_ANALYZER_PROMPT)
    
    def _get_input_variables(self) -> List[str]:
        """Get the list of input variables for the prompt template."""
        return ["primary_interests", "skills", "education_level"]
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process previous agent outputs and analyze market trends."""
        user_input = state["user_input"]
        interest_profile = state.get("interest_profile")
        skill_profile = state.get("skill_profile")
        
        # Extract data from previous agents
        primary_interests = []
        if interest_profile:
            primary_interests = interest_profile.primary_interests
        
        skills = []
        if skill_profile:
            skills = skill_profile.technical_skills + skill_profile.soft_skills
        
        # Prepare input for the agent
        input_data = {
            "primary_interests": self._format_list_for_prompt(primary_interests),
            "skills": self._format_list_for_prompt(skills),
            "education_level": user_input.education_level
        }
        
        # Invoke the chain
        result = self._invoke_chain(input_data)
        
        # Create MarketTrends object safely
        return self._create_profile_safely(result, MarketTrends, "market_trends", state, self._get_fallback_market_trends)
    
    def _get_fallback_response(self) -> Dict[str, Any]:
        """Get a fallback response when the agent fails."""
        return {
            "trending_careers": [
                "Data Analyst",
                "Software Developer",
                "Digital Marketing Specialist",
                "Project Manager",
                "UX/UI Designer"
            ],
            "growth_sectors": [
                "Technology",
                "Healthcare",
                "Renewable Energy",
                "E-commerce",
                "Remote Services"
            ],
            "salary_insights": {
                "Data Analyst": "$50,000 - $80,000 annually",
                "Software Developer": "$60,000 - $120,000 annually",
                "Digital Marketing Specialist": "$40,000 - $70,000 annually",
                "Project Manager": "$55,000 - $95,000 annually",
                "UX/UI Designer": "$50,000 - $90,000 annually"
            },
            "job_outlook": {
                "Data Analyst": "Very positive, high demand across industries",
                "Software Developer": "Excellent, continued growth expected",
                "Digital Marketing Specialist": "Positive, growing digital presence needs",
                "Project Manager": "Good, needed across all sectors",
                "UX/UI Designer": "Positive, increasing focus on user experience"
            },
            "reasoning": "Unable to analyze specific market trends. Provided general high-demand career paths with positive outlooks."
        }
    
    def _get_fallback_market_trends(self) -> MarketTrends:
        """Get a fallback MarketTrends when processing fails."""
        fallback_data = self._get_fallback_response()
        return MarketTrends(
            trending_careers=fallback_data["trending_careers"],
            growth_sectors=fallback_data["growth_sectors"],
            salary_insights=fallback_data["salary_insights"],
            job_outlook=fallback_data["job_outlook"],
            reasoning=fallback_data["reasoning"]
        )
