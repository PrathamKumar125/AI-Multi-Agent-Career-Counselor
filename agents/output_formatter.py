from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from prompts.templates import OUTPUT_FORMATTER_PROMPT
from utils.data_models import FormattedOutput


class OutputFormatterAgent(BaseAgent):
    """Agent that formats career recommendations into user-friendly reports."""
    
    def __init__(self):
        super().__init__("Output Formatter", OUTPUT_FORMATTER_PROMPT)
    
    def _get_input_variables(self) -> List[str]:
        """Get the list of input variables for the prompt template."""
        return ["name", "career_recommendations", "interest_profile", 
                "skill_profile", "personality_profile"]
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process all agent outputs and create formatted report."""
        user_input = state["user_input"]
        
        # Prepare input for the agent
        input_data = {
            "name": user_input.name,
            "career_recommendations": self._format_agent_output(state.get("career_recommendations")),
            "interest_profile": self._format_agent_output(state.get("interest_profile")),
            "skill_profile": self._format_agent_output(state.get("skill_profile")),
            "personality_profile": self._format_agent_output(state.get("personality_profile"))
        }
        
        # Invoke the chain
        result = self._invoke_chain(input_data)
        
        # Create FormattedOutput object safely
        return self._create_profile_safely(result, FormattedOutput, "formatted_output", state, self._get_fallback_formatted_output)
    
    def _get_fallback_response(self) -> Dict[str, Any]:
        """Get a fallback response when the agent fails."""
        return {
            "summary": "We've analyzed your profile and identified several promising career paths that align with your interests, skills, and the current job market.",
            "detailed_report": """
Based on our comprehensive analysis, we've identified several career opportunities that match your profile:

**Top Career Recommendations:**
1. **Business Analyst** - A great fit for analytical thinking and business problem-solving
2. **Project Coordinator** - Perfect for organized individuals who enjoy managing tasks and timelines
3. **Customer Success Specialist** - Ideal for people-oriented professionals who want to help others succeed

**Your Strengths:**
- Strong analytical and problem-solving abilities
- Good communication and interpersonal skills
- Adaptable and eager to learn new things

**Market Outlook:**
The recommended careers are in high demand with positive growth projections. They offer competitive salaries and opportunities for advancement.

**Next Steps:**
We recommend starting with research and skill development in your areas of interest. Consider networking with professionals in these fields and exploring relevant certifications or training programs.
            """,
            "action_plan": [
                "Research the recommended career paths in detail",
                "Identify skill gaps and create a learning plan",
                "Update your resume to highlight relevant experiences",
                "Start networking with professionals in your target fields",
                "Consider informational interviews to learn more",
                "Apply for relevant entry-level positions or internships"
            ],
            "resources": [
                "LinkedIn Learning for skill development",
                "Industry-specific professional associations",
                "Local networking events and meetups",
                "Online job boards (Indeed, LinkedIn, Glassdoor)",
                "Career counseling services at educational institutions"
            ]
        }
    
    def _get_fallback_formatted_output(self) -> FormattedOutput:
        """Get a fallback FormattedOutput when processing fails."""
        fallback_data = self._get_fallback_response()
        return FormattedOutput(
            summary=fallback_data["summary"],
            detailed_report=fallback_data["detailed_report"],
            action_plan=fallback_data["action_plan"],
            resources=fallback_data["resources"]
        )
