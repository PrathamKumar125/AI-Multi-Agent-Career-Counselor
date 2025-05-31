import json
from abc import ABC, abstractmethod
from typing import Dict, Any
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_mistralai import ChatMistralAI
from config.settings import settings


class BaseAgent(ABC):
    """Base class for all career counselor agents."""
    
    def __init__(self, agent_name: str, prompt_template: str):
        """Initialize the base agent."""
        self.agent_name = agent_name
        self.prompt_template = prompt_template
        
        # Initialize the language model
        self.llm = ChatMistralAI(
            model=settings.MISTRAL_MODEL,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
            mistral_api_key=settings.MISTRAL_API_KEY
        )
        
        # Create prompt template
        self.prompt = PromptTemplate(
            template=prompt_template,
            input_variables=self._get_input_variables()
        )
        
        # JSON output parser
        self.output_parser = JsonOutputParser()
        
        # Create the chain
        self.chain = self.prompt | self.llm | self.output_parser
    
    @abstractmethod
    def _get_input_variables(self) -> list:
        """Get the list of input variables for the prompt template."""
        pass
    
    @abstractmethod
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the input and return the agent's output."""
        pass
    
    def _invoke_chain(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke the agent's chain with error handling."""
        try:
            result = self.chain.invoke(input_data)
            return result
        except json.JSONDecodeError as e:
            print(f"JSON parsing error in {self.agent_name}: {e}")
            return self._get_fallback_response()
        except Exception as e:
            print(f"Error in {self.agent_name}: {e}")
            return self._get_fallback_response()
    
    @abstractmethod
    def _get_fallback_response(self) -> Dict[str, Any]:
        """Get a fallback response when the agent fails."""
        pass
    
    def _format_list_for_prompt(self, items: list) -> str:
        """Format a list for inclusion in a prompt."""
        if not items:
            return "None provided"
        return ", ".join(str(item) for item in items)
    
    def _format_dict_for_prompt(self, data: Dict[str, Any]) -> str:
        """Format a dictionary for inclusion in a prompt."""
        if not data:
            return "None provided"
        return json.dumps(data, indent=2)

    def _format_agent_output(self, agent_output) -> str:
        """Format agent output for inclusion in prompts."""
        if not agent_output:
            return "No data available"

        try:
            # Convert Pydantic model to dict for formatting
            if hasattr(agent_output, 'dict'):
                data = agent_output.dict()
            else:
                data = agent_output

            return self._format_dict_for_prompt(data)
        except Exception:
            return str(agent_output)

    def _extract_basic_context(self, user_input, state: Dict[str, Any]) -> str:
        """Extract basic additional context from user input and previous agent results."""
        context_parts = []

        # Add interests from previous agent or user input
        if "interest_profile" in state and state["interest_profile"]:
            interests = state["interest_profile"].primary_interests
            context_parts.append(f"Primary interests: {', '.join(interests)}")
        elif user_input.interests:
            context_parts.append(f"User stated interests: {', '.join(user_input.interests)}")

        # Add skills from previous agent
        if "skill_profile" in state and state["skill_profile"]:
            skills = state["skill_profile"].technical_skills + state["skill_profile"].soft_skills
            context_parts.append(f"Key skills: {', '.join(skills[:5])}")  # Top 5 skills

        # Add education context
        context_parts.append(f"Education level: {user_input.education_level}")

        return " | ".join(context_parts) if context_parts else "No additional context"

    def _create_profile_safely(self, result: Dict[str, Any], profile_class, profile_key: str, state: Dict[str, Any], fallback_method):
        """Safely create a profile object with error handling."""
        try:
            profile = profile_class(**{k: v for k, v in result.items() if k in profile_class.__fields__})
            state[profile_key] = profile
        except Exception as e:
            print(f"Error creating {profile_class.__name__}: {e}")
            state[profile_key] = fallback_method()

        return state
