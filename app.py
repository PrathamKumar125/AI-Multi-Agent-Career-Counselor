import streamlit as st
import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Import project modules
from config.settings import settings
from utils.data_models import UserInput
from utils.input_validator import InputValidator
from utils.resume_parser import ResumeParser
from workflow.career_counselor_workflow import career_counselor_workflow


class CareerCounselorUI:
    """Streamlit UI for the Multi-Agent Career Counselor."""
    
    def __init__(self):
        """Initialize the UI."""
        self.setup_page_config()
        self.initialize_session_state()
    
    def setup_page_config(self):
        """Setup Streamlit page configuration."""
        st.set_page_config(
            page_title=settings.APP_TITLE,
            page_icon="🎯",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def initialize_session_state(self):
        """Initialize session state variables."""
        if 'current_step' not in st.session_state:
            st.session_state.current_step = 1
        if 'user_data' not in st.session_state:
            st.session_state.user_data = {}
        if 'analysis_result' not in st.session_state:
            st.session_state.analysis_result = None
        if 'personality_responses' not in st.session_state:
            st.session_state.personality_responses = {}
    
    def run(self):
        """Run the Streamlit application."""
        self.render_header()
        self.render_sidebar()
        
        # Check if API key is configured
        if not settings.MISTRAL_API_KEY:
            self.render_api_key_warning()
            return
        
        # Main content based on current step
        if st.session_state.current_step == 1:
            self.render_basic_info_step()
        elif st.session_state.current_step == 2:
            self.render_interests_step()
        elif st.session_state.current_step == 3:
            self.render_personality_step()
        elif st.session_state.current_step == 4:
            self.render_resume_step()
        elif st.session_state.current_step == 5:
            self.render_analysis_step()
        elif st.session_state.current_step == 6:
            self.render_results_step()
    
    def render_header(self):
        """Render the application header."""
        st.title("🎯 " + settings.APP_TITLE)
        st.markdown(
            """
            <div style='text-align: center; margin-bottom: 2rem;'>
                <h3>Discover Your Perfect Career Path with AI-Powered Guidance</h3>
                <p>Our specialized AI agents analyze your interests, skills, personality, and market trends 
                to provide personalized career recommendations.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    def render_sidebar(self):
        """Render the sidebar with progress and navigation."""
        with st.sidebar:
            st.header("📊 Progress")
            
            # Progress bar
            progress = (st.session_state.current_step - 1) / 5
            st.progress(progress)
            
            # Step indicators
            steps = [
                "Basic Information",
                "Interests & Preferences",
                "Personality Assessment",
                "Resume Upload",
                "AI Analysis",
                "Career Recommendations"
            ]
            
            for i, step in enumerate(steps, 1):
                if i < st.session_state.current_step:
                    st.success(f"✅ {step}")
                elif i == st.session_state.current_step:
                    st.info(f"🔄 {step}")
                else:
                    st.write(f"⏳ {step}")
            
            st.markdown("---")
            
            # Navigation buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.session_state.current_step > 1:
                    if st.button("⬅️ Back"):
                        st.session_state.current_step -= 1
                        st.rerun()
            
            with col2:
                if st.session_state.current_step < 6:
                    if st.button("Next ➡️", disabled=not self.can_proceed()):
                        st.session_state.current_step += 1
                        st.rerun()
            
            # Reset button
            st.markdown("---")
            if st.button("🔄 Start Over"):
                self.reset_session()
                st.rerun()
    
    def render_api_key_warning(self):
        """Render API key configuration warning."""
        st.error("⚠️ Mistral API Key Not Configured")
        st.markdown("""
        To use this application, you need to configure your Mistral API key:
        
        1. Create a `.env` file in the project root
        2. Add your Mistral API key: `MISTRAL_API_KEY=your_api_key_here`
        3. Restart the application
        
        You can get a Mistral API key from: https://console.mistral.ai/
        """)
    
    def render_basic_info_step(self):
        """Render basic information collection step."""
        st.header("1️⃣ Basic Information")
        st.markdown("Let's start with some basic information about you.")
        
        with st.form("basic_info_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input(
                    "Full Name *",
                    value=st.session_state.user_data.get("name", ""),
                    placeholder="Enter your full name"
                )
                
                education_level = st.selectbox(
                    "Education Level *",
                    options=[
                        "High School",
                        "Some College",
                        "Associate Degree",
                        "Bachelor's Degree",
                        "Master's Degree",
                        "Doctoral Degree",
                        "Professional Degree",
                        "Trade/Vocational School",
                        "Other"
                    ],
                    index=0 if "education_level" not in st.session_state.user_data else [
                        "High School", "Some College", "Associate Degree", "Bachelor's Degree",
                        "Master's Degree", "Doctoral Degree", "Professional Degree",
                        "Trade/Vocational School", "Other"
                    ].index(st.session_state.user_data["education_level"])
                )
            
            with col2:
                age = st.number_input(
                    "Age (Optional)",
                    min_value=16,
                    max_value=100,
                    value=st.session_state.user_data.get("age", 25),
                    help="This helps us provide age-appropriate recommendations"
                )
            
            submitted = st.form_submit_button("Save & Continue")
            
            if submitted:
                # Validate and save form data
                data = {"name": name, "age": age, "education_level": education_level}
                validations = {
                    "name": InputValidator.validate_name,
                    "age": InputValidator.validate_age,
                    "education_level": InputValidator.validate_education_level
                }
                self._validate_and_save_form_data(data, validations, "Basic information saved!", 2)
    
    def render_interests_step(self):
        """Render interests and preferences collection step."""
        st.header("2️⃣ Interests & Preferences")
        st.markdown("Tell us about your interests and career preferences.")
        
        with st.form("interests_form"):
            st.subheader("Select Your Areas of Interest")
            st.markdown("Choose all areas that interest you (select at least one):")
            
            # Create columns for better layout
            col1, col2 = self._create_two_column_layout()
            
            interests = []
            saved_interests = st.session_state.user_data.get("interests", [])
            
            with col1:
                for i, category in enumerate(settings.INTEREST_CATEGORIES[:5]):
                    if st.checkbox(category, value=category in saved_interests):
                        interests.append(category)
            
            with col2:
                for i, category in enumerate(settings.INTEREST_CATEGORIES[5:]):
                    if st.checkbox(category, value=category in saved_interests):
                        interests.append(category)
            
            # Additional interests text area
            st.subheader("Additional Interests (Optional)")
            additional_interests = st.text_area(
                "Describe any other interests or career areas not listed above:",
                value=st.session_state.user_data.get("additional_interests", ""),
                placeholder="e.g., Environmental sustainability, blockchain technology, social entrepreneurship..."
            )
            
            submitted = st.form_submit_button("Save & Continue")
            
            if submitted:
                # Add additional interests to the list
                if additional_interests:
                    additional_list = [interest.strip() for interest in additional_interests.split(",")]
                    interests.extend(additional_list)
                
                # Validate interests
                interests_valid, interests_msg = InputValidator.validate_interests(interests)
                
                if interests_valid:
                    st.session_state.user_data.update({
                        "interests": interests,
                        "additional_interests": additional_interests
                    })
                    st.success("✅ Interests saved!")
                    st.session_state.current_step = 3
                    st.rerun()
                else:
                    st.error(f"Interests: {interests_msg}")
    
    def render_personality_step(self):
        """Render personality assessment step."""
        st.header("3️⃣ Personality Assessment")
        st.markdown("""
        This brief personality assessment helps us understand your work style preferences.
        Rate each statement on a scale of 1-5:
        """)
        
        # Personality questions
        personality_questions = {
            "Openness to Experience": [
                "I enjoy exploring new ideas and concepts",
                "I am curious about many different things",
                "I like to think about abstract or theoretical problems"
            ],
            "Conscientiousness": [
                "I am always prepared and organized",
                "I pay attention to details and follow through on tasks",
                "I like to have a clear plan and stick to schedules"
            ],
            "Extraversion": [
                "I enjoy being around other people and socializing",
                "I feel comfortable being the center of attention",
                "I get energy from interacting with others"
            ],
            "Agreeableness": [
                "I try to be cooperative and avoid conflicts",
                "I am sympathetic and concerned about others",
                "I trust others and assume good intentions"
            ],
            "Neuroticism": [
                "I often feel stressed or anxious",
                "I worry about things that might go wrong",
                "I get upset easily when things don't go as planned"
            ]
        }
        
        with st.form("personality_form"):
            responses = {}
            
            for trait, questions in personality_questions.items():
                st.subheader(f"📋 {trait}")
                
                trait_scores = []
                for i, question in enumerate(questions):
                    score = st.radio(
                        question,
                        options=[1, 2, 3, 4, 5],
                        format_func=lambda x: ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"][x-1],
                        horizontal=True,
                        key=f"{trait}_{i}",
                        index=st.session_state.personality_responses.get(f"{trait}_{i}", 2)
                    )
                    trait_scores.append(score)
                
                # Calculate average score for this trait
                responses[trait] = sum(trait_scores) / len(trait_scores)
                st.markdown("---")
            
            submitted = st.form_submit_button("Save & Continue")
            
            if submitted:
                # Validate personality responses
                responses_valid, responses_msg = InputValidator.validate_personality_responses(responses)
                
                if responses_valid:
                    st.session_state.user_data["personality_responses"] = responses
                    st.session_state.personality_responses = {f"{trait}_{i}": 2 for trait in personality_questions for i in range(len(personality_questions[trait]))}
                    st.success("✅ Personality assessment completed!")
                    st.session_state.current_step = 4
                    st.rerun()
                else:
                    st.error(f"Personality Assessment: {responses_msg}")
    
    def render_resume_step(self):
        """Render resume upload step."""
        st.header("4️⃣ Resume Upload (Optional)")
        st.markdown("""
        Upload your resume to help us better understand your skills and experience.
        Supported formats: PDF, DOCX, TXT
        """)
        
        # Resume upload options
        upload_option = st.radio(
            "Choose an option:",
            ["Upload file", "Paste text", "Skip this step"],
            index=0
        )
        
        resume_text = ""
        
        if upload_option == "Upload file":
            uploaded_file = st.file_uploader(
                "Choose your resume file",
                type=["pdf", "docx", "txt"],
                help="Maximum file size: 5MB"
            )
            
            if uploaded_file is not None:
                try:
                    # Get file details
                    file_content = uploaded_file.read()
                    file_type = uploaded_file.name.split('.')[-1].lower()
                    
                    # Validate file
                    file_valid, file_msg = InputValidator.validate_file_upload(file_content, file_type)
                    
                    if file_valid:
                        # Parse resume
                        with st.spinner("Parsing your resume..."):
                            resume_text = ResumeParser.parse_resume(file_content, file_type)
                            resume_text = ResumeParser.clean_text(resume_text)
                        
                        st.success("✅ Resume uploaded and parsed successfully!")
                        st.text_area("Parsed content (preview):", value=resume_text[:500] + "...", disabled=True)
                    else:
                        st.error(f"File validation error: {file_msg}")
                
                except Exception as e:
                    st.error(f"Error parsing resume: {str(e)}")
        
        elif upload_option == "Paste text":
            resume_text = st.text_area(
                "Paste your resume content here:",
                height=300,
                placeholder="Copy and paste your resume content here..."
            )
        
        # Save and continue
        if st.button("Save & Continue"):
                if resume_text:
                    # Validate resume text
                    resume_valid, resume_msg = InputValidator.validate_resume_text(resume_text)
                    
                    if resume_valid:
                        st.session_state.user_data["resume_text"] = resume_text
                        st.success("✅ Resume information saved!")
                        st.session_state.current_step = 5
                        st.rerun()
                    else:
                        st.error(f"Resume: {resume_msg}")
                else:
                    # Skip resume upload
                    st.session_state.user_data["resume_text"] = None
                    st.info("ℹ️ Skipping resume upload.")
                    st.session_state.current_step = 5
                    st.rerun()
    
    def render_analysis_step(self):
        """Render the AI analysis step."""
        st.header("5️⃣ AI Analysis in Progress")
        st.markdown("Our AI agents are analyzing your profile to generate personalized career recommendations...")
        
        # Create user input object
        try:
            user_input = UserInput(
                name=st.session_state.user_data["name"],
                age=st.session_state.user_data.get("age"),
                education_level=st.session_state.user_data["education_level"],
                interests=st.session_state.user_data.get("interests", []),
                personality_responses=st.session_state.user_data.get("personality_responses", {}),
                resume_text=st.session_state.user_data.get("resume_text")
            )
            
            # Validate complete user input
            input_valid, input_errors = InputValidator.validate_user_input(user_input)
            
            if not input_valid:
                st.error("Input validation errors:")
                for error in input_errors:
                    st.error(f"• {error}")
                
                if st.button("Go Back to Fix Issues"):
                    st.session_state.current_step = 1
                    st.rerun()
                return
            
        except Exception as e:
            st.error(f"Error creating user input: {str(e)}")
            if st.button("Go Back to Fix Issues"):
                st.session_state.current_step = 1
                st.rerun()
            return
        
        # Display analysis progress
        if st.session_state.analysis_result is None:
            # Show analysis in progress
            self.show_analysis_progress()
            
            # Run analysis
            if st.button("🚀 Start Analysis", type="primary"):
                with st.spinner("Running AI analysis..."):
                    try:
                        result = career_counselor_workflow.process_user_input(user_input)
                        st.session_state.analysis_result = result
                        st.success("✅ Analysis completed successfully!")
                        st.session_state.current_step = 6
                        st.rerun()
                    except Exception as e:
                        st.error(f"Analysis error: {str(e)}")
                        st.error("Please try again or contact support if the issue persists.")
        else:
            # Analysis already completed
            st.success("✅ Analysis completed!")
            if st.button("View Results"):
                st.session_state.current_step = 6
                st.rerun()
    
    def show_analysis_progress(self):
        """Show the analysis progress and agent descriptions."""
        st.subheader("🤖 Our AI Agents Will Analyze:")
        
        agents_info = [
            ("🔍", "Interest Profiler", "Analyzes your interests and maps them to career categories"),
            ("💪", "Skill Evaluator", "Extracts and evaluates your skills from resume and input"),
            ("🧠", "Personality Mapper", "Maps your personality traits to work style preferences"),
            ("📈", "Market Trend Analyzer", "Analyzes current job market trends and opportunities"),
            ("🎯", "Career Recommender", "Synthesizes all insights to recommend suitable careers"),
            ("📋", "Output Formatter", "Creates a comprehensive and actionable career report")
        ]
        
        for icon, name, description in agents_info:
            with st.container():
                col1, col2 = st.columns([1, 5])
                with col1:
                    st.markdown(f"### {icon}")
                with col2:
                    st.markdown(f"**{name}**")
                    st.markdown(description)
                st.markdown("---")
    
    def render_results_step(self):
        """Render the final results step."""
        if st.session_state.analysis_result is None:
            st.error("No analysis results found. Please run the analysis first.")
            if st.button("Go Back to Analysis"):
                st.session_state.current_step = 5
                st.rerun()
            return
        
        st.header("6️⃣ Your Personalized Career Recommendations")
        
        result = st.session_state.analysis_result
        formatted_output = result.get("formatted_output")
        career_recommendations = result.get("career_recommendations")
        
        if not formatted_output or not career_recommendations:
            st.error("Incomplete analysis results. Please run the analysis again.")
            return
        
        # Executive Summary
        st.subheader("📋 Executive Summary")
        st.info(formatted_output.summary)
        
        # Top Career Recommendations
        st.subheader("🎯 Top Career Recommendations")
        
        for i, recommendation in enumerate(career_recommendations.top_recommendations, 1):
            with st.expander(f"{i}. {recommendation.title} (Match: {recommendation.match_score}%)", expanded=i==1):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Match Score:** {recommendation.match_score}%")
                    st.markdown(f"**Salary Range:** {recommendation.salary_range}")
                    st.markdown(f"**Job Outlook:** {recommendation.job_outlook}")
                
                with col2:
                    st.markdown(f"**Education Requirements:** {recommendation.education_requirements}")
                    st.markdown(f"**Required Skills:**")
                    for skill in recommendation.required_skills:
                        st.markdown(f"• {skill}")
                
                st.markdown(f"**Why Recommended:** {recommendation.why_recommended}")
        
        # Visualizations
        self.render_visualizations(result)
        
        # Detailed Report
        with st.expander("📄 Detailed Report", expanded=False):
            st.markdown(formatted_output.detailed_report)
        
        # Action Plan
        st.subheader("🚀 Your Action Plan")
        for i, step in enumerate(formatted_output.action_plan, 1):
            st.markdown(f"{i}. {step}")
        
        # Resources
        st.subheader("📚 Helpful Resources")
        for resource in formatted_output.resources:
            st.markdown(f"• {resource}")
        
        # Download options
        st.subheader("💾 Download Your Report")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Download as Text"):
                self.download_text_report(formatted_output, career_recommendations)
        
        with col2:
            if st.button("📊 Download as JSON"):
                self.download_json_report(result)
    
    def render_visualizations(self, result):
        """Render data visualizations."""
        st.subheader("📊 Visual Insights")
        
        # Career match scores chart
        career_recommendations = result.get("career_recommendations")
        if career_recommendations and career_recommendations.top_recommendations:
            fig_scores = go.Figure(data=[
                go.Bar(
                    x=[rec.title for rec in career_recommendations.top_recommendations],
                    y=[rec.match_score for rec in career_recommendations.top_recommendations],
                    marker_color='lightblue'
                )
            ])
            fig_scores.update_layout(
                title="Career Match Scores",
                xaxis_title="Career",
                yaxis_title="Match Score (%)",
                yaxis=dict(range=[0, 100])
            )
            st.plotly_chart(fig_scores, use_container_width=True)
        
        # Interest scores chart
        interest_profile = result.get("interest_profile")
        if interest_profile and interest_profile.interest_scores:
            # Create DataFrame for better visualization
            df_interests = pd.DataFrame(
                list(interest_profile.interest_scores.items()),
                columns=['Interest Category', 'Score']
            ).sort_values('Score', ascending=True)
            
            fig_interests = px.bar(
                df_interests,
                x='Score',
                y='Interest Category',
                orientation='h',
                title="Interest Profile Scores"
            )
            st.plotly_chart(fig_interests, use_container_width=True)
    
    def download_text_report(self, formatted_output, career_recommendations):
        """Generate downloadable text report."""
        report_content = f"""
# Career Counseling Report

## Executive Summary
{formatted_output.summary}

## Top Career Recommendations
"""
        
        for i, rec in enumerate(career_recommendations.top_recommendations, 1):
            report_content += f"""
### {i}. {rec.title} (Match: {rec.match_score}%)
- **Salary Range:** {rec.salary_range}
- **Job Outlook:** {rec.job_outlook}
- **Education Requirements:** {rec.education_requirements}
- **Required Skills:** {', '.join(rec.required_skills)}
- **Why Recommended:** {rec.why_recommended}
"""
        
        report_content += f"""
## Action Plan
"""
        for i, step in enumerate(formatted_output.action_plan, 1):
            report_content += f"{i}. {step}\n"
        
        report_content += f"""
## Resources
"""
        for resource in formatted_output.resources:
            report_content += f"• {resource}\n"
        
        st.download_button(
            label="📄 Download Report",
            data=report_content,
            file_name="career_counseling_report.txt",
            mime="text/plain"
        )
    
    def download_json_report(self, result):
        """Generate downloadable JSON report."""
        # Convert Pydantic models to dictionaries
        json_data = {}
        for key, value in result.items():
            if hasattr(value, 'dict'):
                json_data[key] = value.dict()
            else:
                json_data[key] = value
        
        st.download_button(
            label="📊 Download JSON",
            data=json.dumps(json_data, indent=2),
            file_name="career_analysis_data.json",
            mime="application/json"
        )
    
    def can_proceed(self) -> bool:
        """Check if user can proceed to next step."""
        if st.session_state.current_step == 1:
            return all(key in st.session_state.user_data for key in ["name", "education_level"])
        elif st.session_state.current_step == 2:
            return "interests" in st.session_state.user_data
        elif st.session_state.current_step == 3:
            return "personality_responses" in st.session_state.user_data
        elif st.session_state.current_step == 4:
            return True  # Resume is optional
        elif st.session_state.current_step == 5:
            return st.session_state.analysis_result is not None
        return False
    
    def reset_session(self):
        """Reset the session state."""
        st.session_state.current_step = 1
        st.session_state.user_data = {}
        st.session_state.analysis_result = None
        st.session_state.personality_responses = {}

    def _validate_and_save_form_data(self, data_dict: dict, validation_funcs: list, success_message: str, next_step: int):
        """Helper method to validate form data and proceed to next step."""
        errors = []

        for field, value in data_dict.items():
            if field in validation_funcs:
                is_valid, message = validation_funcs[field](value)
                if not is_valid:
                    errors.append(f"{field.title()}: {message}")

        if not errors:
            st.session_state.user_data.update(data_dict)
            st.success(f"✅ {success_message}")
            st.session_state.current_step = next_step
            st.rerun()
        else:
            for error in errors:
                st.error(error)

    def _create_two_column_layout(self):
        """Helper method to create consistent two-column layout."""
        return st.columns(2)


def main():
    """Main function to run the Streamlit app."""
    app = CareerCounselorUI()
    app.run()


if __name__ == "__main__":
    main()
