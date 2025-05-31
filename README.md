# AI Multi-Agent Career Counselor

A sophisticated multi-agent system that provides personalized career guidance through specialized AI agents. This system leverages the power of multiple AI agents working collaboratively to analyze user profiles and deliver comprehensive career recommendations.

## Live Demo

**Try the application now:** [AI Multi-Agent Career Counselor on Hugging Face Spaces](https://huggingface.co/spaces/pratham0011/AI-Multi-Agent-Career-Counselor)


## Problem Statement

### The Challenge
Career guidance and counseling is a complex, multi-faceted problem that requires expertise across multiple domains:

- **Fragmented Analysis**: Traditional career counseling often focuses on single aspects (interests OR skills OR personality) rather than a holistic view
- **Limited Personalization**: Generic career advice doesn't account for individual personality traits, market conditions, and skill combinations
- **Scalability Issues**: Human career counselors are expensive and not accessible to everyone
- **Market Disconnect**: Career advice often lacks current market trends and industry insights
- **Inconsistent Quality**: Varying expertise levels among human counselors lead to inconsistent advice quality

### Why Multi-Agent AI?
AI agents are particularly well-suited for this problem because:

1. **Specialized Expertise**: Each agent can focus on a specific domain (personality analysis, skill evaluation, market trends) with deep, specialized knowledge
2. **Efficient Processing**: Multiple agents can process different aspects of a user's profile simultaneously
3. **Consistent Quality**: AI agents provide standardized, reproducible analysis every time
4. **Real-time Analysis**: Instant processing of complex multi-dimensional data
5. **Collaborative Intelligence**: Agents can share insights and build upon each other's analysis for more comprehensive recommendations

## Project Description

### System Overview
The AI Multi-Agent Career Counselor is an intelligent career guidance system that employs six specialized AI agents working in a coordinated workflow. The system takes user inputs (personal information, interests, personality responses, and optional resume) and processes them through a sophisticated multi-agent pipeline to generate personalized career recommendations.

### Key Features
- **Interactive Web Interface**: User-friendly Streamlit application with step-by-step guidance
- **Comprehensive Input Collection**: Gathers personal info, interests, Big Five personality assessment, and resume data
- **Multi-Agent Processing**: Six specialized agents analyze different aspects of career fit
- **Visual Analytics**: Charts and graphs displaying career match scores and insights
- **Detailed Reporting**: Downloadable reports in both text and JSON formats
- **Fallback Mechanisms**: Robust error handling with fallback responses for reliable operation
- **🌐 Live Deployment**: Available on Hugging Face Spaces for immediate access

## Agent Interactions and Workflow

### Agent Architecture
Our system employs a **sequential collaborative workflow** where agents build upon each other's outputs:

```
User Input → Interest Profiler → Skill Evaluator → Personality Mapper 
                ↓
Market Trend Analyzer → Career Recommender → Output Formatter → Final Report
```

### Individual Agent Responsibilities

#### 1. **Interest Profiler Agent** 
- **Purpose**: Analyzes user's stated interests and maps them to career categories
- **Input**: User's selected interests, additional interest descriptions, basic demographics
- **Output**: `InterestProfile` with primary interests, interest scores, and reasoning
- **Specialization**: Understanding career interest categories and their professional applications

#### 2. **Skill Evaluator Agent** 
- **Purpose**: Extracts and evaluates technical and soft skills from resumes and user input
- **Input**: Resume text, education level, context from Interest Profiler
- **Output**: `SkillProfile` with technical skills, soft skills, skill levels, and analysis
- **Specialization**: Skill extraction, categorization, and proficiency assessment

#### 3. **Personality Mapper Agent** 
- **Purpose**: Maps Big Five personality traits to work environment and career preferences
- **Input**: Personality questionnaire responses, context from previous agents
- **Output**: `PersonalityProfile` with trait scores, work style preferences, team dynamics
- **Specialization**: Personality psychology and workplace behavior mapping

#### 4. **Market Trend Analyzer Agent** 
- **Purpose**: Analyzes current job market trends and provides industry insights
- **Input**: Interests and skills from previous agents, education level
- **Output**: `MarketTrends` with trending careers, growth sectors, salary insights, job outlook
- **Specialization**: Labor market analysis and industry trend identification

#### 5. **Career Recommender Agent** 
- **Purpose**: Synthesizes all agent outputs to generate top career recommendations
- **Input**: All previous agent outputs (interests, skills, personality, market trends)
- **Output**: `CareerRecommendations` with top 3-5 career matches, scores, and explanations
- **Specialization**: Career matching algorithms and recommendation synthesis

#### 6. **Output Formatter Agent** 
- **Purpose**: Creates user-friendly, comprehensive career counseling reports
- **Input**: All agent outputs, particularly career recommendations
- **Output**: `FormattedOutput` with summary, detailed report, action plan, and resources
- **Specialization**: Report generation and user communication

### Agent Collaboration Patterns

#### **Sequential Processing**
Agents work in a defined sequence, each building upon the previous agent's analysis:
- Interest analysis informs skill evaluation context
- Skill evaluation provides technical background for personality mapping
- All three profiles inform market trend analysis
- Complete profile drives career recommendations
- Final formatting synthesizes all insights

#### **Context Sharing**
Each agent receives not only direct inputs but also context from previous agents:
- Later agents have richer context for more informed decisions
- Cross-validation occurs as agents consider multiple data points
- Consistency is maintained across the analysis pipeline

#### **Fallback Coordination**
Robust error handling ensures system reliability:
- Each agent has predefined fallback responses
- Failed agents don't break the entire workflow
- Alternative recommendations are provided when primary analysis fails

## Technologies Used

### Core Framework & Tools
- **LangChain**: Framework for building LLM applications with prompt chaining
- **LangGraph**: Orchestrates multi-agent workflows using stateful, directed graphs
- **Streamlit**: Interactive web application framework for user interface
- **Pydantic**: Data validation and settings management using Python type annotations

### Language Models & AI
- **Mistral AI**: Primary LLM provider for agent processing
- **LangChain-MistralAI**: Integration layer for Mistral models in LangChain

### Data Processing & Utilities
- **PyPDF2**: PDF resume parsing
- **python-docx**: Microsoft Word document processing
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing support

### Visualization & UI
- **Plotly**: Interactive charts and data visualizations
- **streamlit-chat**: Enhanced chat interface components

### Configuration & Environment
- **python-dotenv**: Environment variable management
- **typing-extensions**: Enhanced type hints for Python

### Development Tools
- **requests**: HTTP requests for potential API integrations
- **beautifulsoup4**: Web scraping capabilities for market data

## LLM Selection and Justification

### Ideal LLM Choice: Claude 4 (Sonnet)
For production deployment, **Claude 4 (Sonnet)** would be the optimal choice for this project due to:

#### **Advantages of Claude 4:**
- **Superior Reasoning**: Excellent analytical capabilities for complex career matching logic
- **Context Understanding**: Better comprehension of nuanced personality and skill relationships
- **Structured Output**: More reliable JSON generation and formatting consistency
- **Safety and Reliability**: Lower hallucination rates, crucial for career advice accuracy
- **Long Context Window**: Better handling of comprehensive resume text and multi-agent context
- **Professional Writing**: Higher quality output formatting for career reports


### Current Implementation: Mistral "ministral-8b-latest"
We currently use **Mistral's ministral-8b-latest** as our free-tier option:

#### **Advantages of Mistral 8B:**
- **Cost-Effective**: Free tier available, making the project accessible
- **Fast Processing**: Smaller model size enables quicker response times
- **Good Performance**: Adequate accuracy for structured analysis tasks
- **JSON Output**: Reliable structured output generation
- **Privacy-Friendly**: Can be run locally if needed

#### **Limitations Addressed:**
- **Smaller Context Window**: Managed through careful prompt design and context summarization
- **Less Sophisticated Reasoning**: Compensated by clear, structured prompts and fallback mechanisms
- **Lower Quality Output**: Enhanced through post-processing and template-based formatting

### LLM Selection Justification

#### **Why These Models Work for Career Counseling:**

1. **Structured Analysis Tasks**: Both models excel at following structured prompts and generating consistent JSON outputs, essential for our agent-based approach

2. **Domain Knowledge**: Pre-trained on diverse text including career-related content, providing good baseline knowledge for career analysis

3. **Multi-step Reasoning**: Capable of analyzing multiple factors (interests + skills + personality + market trends) to generate coherent recommendations

4. **Scalable Architecture**: Our multi-agent design allows for easy model switching as better options become available

#### **Future-Proofing Strategy:**
- **Model-Agnostic Design**: Our base agent architecture can easily switch between different LLMs
- **Configurable Models**: Settings allow for different models per agent type based on specialization needs
- **Hybrid Approach**: Could potentially use Claude 4 for critical agents (Career Recommender) and Mistral for others to balance cost and quality

## Setup and Run Instructions

### Option 1: Use the Live Demo (Recommended)
**🎯 Quickest Way to Get Started:**
Visit the [live deployment on Hugging Face Spaces](https://huggingface.co/spaces/pratham0011/AI-Multi-Agent-Career-Counselor) - no installation required!

### Option 2: Local Installation

### Prerequisites
- **Python 3.9 or higher**: Ensure you have a compatible Python version installed
- **Mistral AI API Key**: Sign up and get your API key from [Mistral Console](https://console.mistral.ai/)
- **Git**: For cloning the repository (optional)

### Step 1: Project Setup
```powershell
# Clone or download the project to your local machine
# If using Git:
git clone https://github.com/PrathamKumar125/AI-Multi-Agent-Career-Counselor.git
cd "AI-Multi-Agent-Career-Counselor"

# If downloaded as ZIP, extract and navigate to the folder
```

### Step 2: Environment Setup
```powershell
# Create and activate a virtual environment (recommended)
python -m venv career_counselor_env
career_counselor_env\Scripts\activate

# Install required dependencies
pip install -r requirements.txt
```

### Step 3: Configuration
```powershell
# Copy the example environment file
copy .env.example .env

# Edit the .env file and add your Mistral API key
# Open .env in your preferred text editor and set:
# MISTRAL_API_KEY=your_actual_api_key_here
```

### Step 4: Run the Application
```powershell
# Start the Streamlit application
streamlit run app.py
```

### Step 5: Access the Application
1. **Open your web browser**
2. **Navigate to the URL** displayed in the terminal (typically `http://localhost:8501`)
3. **Start using the career counselor!**

### Performance Optimization

#### **For Better Performance:**
1. **Use SSD Storage**: Install on solid-state drive for faster file access
2. **Stable Internet**: Ensure reliable connection for API calls
3. **Sufficient RAM**: 4GB+ recommended for smooth operation
4. **Close Unnecessary Applications**: Free up system resources

### Security Considerations

#### **Protecting Your API Key:**
- Never commit `.env` files to version control
- Use environment variables in production
- Rotate API keys regularly
- Monitor API usage for unusual activity

### Next Steps After Setup
1. **Explore Configuration**: Modify settings in `config/settings.py` if needed
2. **Read Documentation**: Review the full README for usage guidelines
3. **Provide Feedback**: Report any issues or suggestions for improvement

---

**🎉 Congratulations! Your AI Multi-Agent Career Counselor is now ready to help users discover their ideal career paths.**