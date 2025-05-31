from typing import Dict, Any
from langgraph.graph import StateGraph, END
from utils.data_models import AgentState
from agents.interest_profiler import InterestProfilerAgent
from agents.skill_evaluator import SkillEvaluatorAgent
from agents.personality_mapper import PersonalityMapperAgent
from agents.market_trend_analyzer import MarketTrendAnalyzerAgent
from agents.career_recommender import CareerRecommenderAgent
from agents.output_formatter import OutputFormatterAgent


class CareerCounselorWorkflow:
    """LangGraph workflow for the Multi-Agent Career Counselor system."""
    
    def __init__(self):
        """Initialize the workflow with all agents."""
        # Initialize agents
        self.interest_profiler = InterestProfilerAgent()
        self.skill_evaluator = SkillEvaluatorAgent()
        self.personality_mapper = PersonalityMapperAgent()
        self.market_trend_analyzer = MarketTrendAnalyzerAgent()
        self.career_recommender = CareerRecommenderAgent()
        self.output_formatter = OutputFormatterAgent()
        
        # Create the workflow graph
        self.workflow = self._create_workflow()
    
    def _create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow."""
        # Create state graph
        workflow = StateGraph(dict)
        
        # Add nodes (agents)
        workflow.add_node("interest_profiler", self._interest_profiler_node)
        workflow.add_node("skill_evaluator", self._skill_evaluator_node)
        workflow.add_node("personality_mapper", self._personality_mapper_node)
        workflow.add_node("market_trend_analyzer", self._market_trend_analyzer_node)
        workflow.add_node("career_recommender", self._career_recommender_node)
        workflow.add_node("output_formatter", self._output_formatter_node)
        
        # Define the flow
        workflow.set_entry_point("interest_profiler")
        
        # Sequential flow through agents
        workflow.add_edge("interest_profiler", "skill_evaluator")
        workflow.add_edge("skill_evaluator", "personality_mapper")
        workflow.add_edge("personality_mapper", "market_trend_analyzer")
        workflow.add_edge("market_trend_analyzer", "career_recommender")
        workflow.add_edge("career_recommender", "output_formatter")
        workflow.add_edge("output_formatter", END)
        
        # Compile the workflow
        return workflow.compile()
    
    def _interest_profiler_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Interest Profiler agent node."""
        print("🔍 Analyzing interests and preferences...")
        return self.interest_profiler.process(state)
    
    def _skill_evaluator_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Skill Evaluator agent node."""
        print("💪 Evaluating skills and experience...")
        return self.skill_evaluator.process(state)
    
    def _personality_mapper_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Personality Mapper agent node."""
        print("🧠 Mapping personality to work preferences...")
        return self.personality_mapper.process(state)
    
    def _market_trend_analyzer_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Market Trend Analyzer agent node."""
        print("📈 Analyzing market trends and opportunities...")
        return self.market_trend_analyzer.process(state)
    
    def _career_recommender_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Career Recommender agent node."""
        print("🎯 Generating career recommendations...")
        return self.career_recommender.process(state)
    
    def _output_formatter_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Output Formatter agent node."""
        print("📋 Formatting final report...")
        return self.output_formatter.process(state)
    
    def process_user_input(self, user_input) -> Dict[str, Any]:
        """Process user input through the entire workflow."""
        # Initialize state
        initial_state = {
            "user_input": user_input,
            "interest_profile": None,
            "skill_profile": None,
            "personality_profile": None,
            "market_trends": None,
            "career_recommendations": None,
            "formatted_output": None
        }
        
        print("🚀 Starting Multi-Agent Career Counselor Analysis...")
        print("=" * 60)
        
        try:
            # Run the workflow
            result = self.workflow.invoke(initial_state)
            print("✅ Analysis complete!")
            return result
            
        except Exception as e:
            print(f"❌ Error in workflow: {e}")
            # Return a fallback result
            return self._get_fallback_result(user_input)
    
    def _get_fallback_result(self, user_input) -> Dict[str, Any]:
        """Get a fallback result when the workflow fails."""
        from utils.data_models import (
            InterestProfile, SkillProfile, PersonalityProfile, 
            MarketTrends, CareerRecommendations, CareerRecommendation, FormattedOutput
        )
        
        # Create basic fallback profiles
        fallback_state = {
            "user_input": user_input,
            "interest_profile": InterestProfile(
                primary_interests=["Technology & Engineering", "Business & Finance"],
                interest_scores={"Technology & Engineering": 70, "Business & Finance": 60},
                reasoning="Fallback analysis due to system error."
            ),
            "skill_profile": SkillProfile(
                technical_skills=["Communication", "Problem Solving"],
                soft_skills=["Teamwork", "Leadership"],
                skill_levels={"Communication": "Intermediate"},
                reasoning="Fallback analysis due to system error."
            ),
            "personality_profile": PersonalityProfile(
                trait_scores={},
                work_style_preferences=["Collaborative environment"],
                team_dynamics="Works well in teams",
                reasoning="Fallback analysis due to system error."
            ),
            "market_trends": MarketTrends(
                trending_careers=["Business Analyst", "Project Manager"],
                growth_sectors=["Technology", "Business Services"],
                salary_insights={},
                job_outlook={},
                reasoning="Fallback analysis due to system error."
            ),
            "career_recommendations": CareerRecommendations(
                top_recommendations=[
                    CareerRecommendation(
                        title="Business Analyst",
                        match_score=75,
                        required_skills=["Analysis", "Communication"],
                        education_requirements="Bachelor's degree",
                        salary_range="$50,000 - $80,000",
                        job_outlook="Positive",
                        why_recommended="Good general career option"
                    )
                ],
                alternative_paths=["Project Coordinator"],
                next_steps=["Research careers", "Update resume"],
                reasoning="Fallback recommendations due to system error."
            ),
            "formatted_output": FormattedOutput(
                summary="We've provided general career recommendations for you.",
                detailed_report="Due to a system error, we've provided general recommendations. Please try again later for a more detailed analysis.",
                action_plan=["Research recommended careers", "Consider skill development"],
                resources=["LinkedIn Learning", "Professional associations"]
            )
        }
        
        return fallback_state


# Global workflow instance
career_counselor_workflow = CareerCounselorWorkflow()
