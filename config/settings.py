import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings and configuration."""
    
    # API Keys
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
    
    # Model Configuration
    MISTRAL_MODEL = "ministral-8b-latest"
    TEMPERATURE = 0.7
    MAX_TOKENS = 1000
    
    # Application Settings
    APP_TITLE = "AI Multi-Agent Career Counselor"
    APP_DESCRIPTION = "Intelligent career guidance through specialized AI agents"
    
    # Agent Configuration
    AGENTS = {
        "interest_profiler": {
            "name": "Interest Profiler",
            "description": "Analyzes user preferences and interests"
        },
        "skill_evaluator": {
            "name": "Skill Evaluator", 
            "description": "Extracts and evaluates skills from resume/input"
        },
        "personality_mapper": {
            "name": "Personality Mapper",
            "description": "Maps personality traits to work preferences"
        },
        "market_trend_analyzer": {
            "name": "Market Trend Analyzer",
            "description": "Analyzes current job market trends"
        },
        "career_recommender": {
            "name": "Career Recommender",
            "description": "Synthesizes recommendations from all agents"
        },
        "output_formatter": {
            "name": "Output Formatter",
            "description": "Formats final recommendations"
        }
    }
    
    # Big Five Personality Traits
    BIG_FIVE_TRAITS = [
        "Openness to Experience",
        "Conscientiousness", 
        "Extraversion",
        "Agreeableness",
        "Neuroticism"
    ]
    
    # Career Interest Categories
    INTEREST_CATEGORIES = [
        "Technology & Engineering",
        "Healthcare & Medicine",
        "Business & Finance",
        "Arts & Creative",
        "Education & Training",
        "Science & Research",
        "Social Services",
        "Law & Government",
        "Sports & Recreation",
        "Agriculture & Environment"
    ]

# Global settings instance
settings = Settings()
