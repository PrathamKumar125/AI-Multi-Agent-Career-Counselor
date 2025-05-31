import re
from typing import List, Dict, Tuple
from utils.data_models import UserInput, PersonalityTrait

class InputValidator:
    """Utility class for validating user inputs."""
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        """Validate user name input."""
        if not name or not name.strip():
            return False, "Name cannot be empty"
        
        if len(name.strip()) < 2:
            return False, "Name must be at least 2 characters long"
        
        if len(name.strip()) > 50:
            return False, "Name must be less than 50 characters"
        
        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        if not re.match(r"^[a-zA-Z\s\-']+$", name.strip()):
            return False, "Name can only contain letters, spaces, hyphens, and apostrophes"
        
        return True, "Valid name"
    
    @staticmethod
    def validate_age(age: int) -> Tuple[bool, str]:
        """Validate age input."""
        if age is None:
            return True, "Age is optional"
        
        if not isinstance(age, int):
            return False, "Age must be a number"
        
        if age < 16 or age > 100:
            return False, "Age must be between 16 and 100"
        
        return True, "Valid age"
    
    @staticmethod
    def validate_education_level(education: str) -> Tuple[bool, str]:
        """Validate education level input."""
        valid_levels = [
            "High School",
            "Associate Degree",
            "Bachelor's Degree",
            "Master's Degree",
            "Doctoral Degree",
            "Professional Degree",
            "Some College",
            "Trade/Vocational School",
            "Other"
        ]
        
        if not education or not education.strip():
            return False, "Education level is required"
        
        if education not in valid_levels:
            return False, f"Education level must be one of: {', '.join(valid_levels)}"
        
        return True, "Valid education level"
    
    @staticmethod
    def validate_interests(interests: List[str]) -> Tuple[bool, str]:
        """Validate interest selections."""
        if not interests:
            return False, "At least one interest must be selected"
        
        if len(interests) > 10:
            return False, "Please select no more than 10 interests"
        
        # Check for empty or invalid interests
        for interest in interests:
            if not interest or not interest.strip():
                return False, "Interest cannot be empty"
            if len(interest) > 100:
                return False, "Interest description too long (max 100 characters)"
        
        return True, "Valid interests"
    
    @staticmethod
    def validate_personality_responses(responses: Dict[str, float]) -> Tuple[bool, str]:
        """Validate personality questionnaire responses."""
        required_traits = [trait.value for trait in PersonalityTrait]
        
        # Check if all required traits have responses
        for trait in required_traits:
            if trait not in responses:
                return False, f"Missing response for {trait}"
            
            score = responses[trait]
            if not isinstance(score, (int, float)) or score < 1 or score > 5:
                return False, f"Score for {trait} must be between 1 and 5"
        
        return True, "Valid personality responses"
    
    @staticmethod
    def validate_resume_text(resume_text: str) -> Tuple[bool, str]:
        """Validate resume text content."""
        if not resume_text:
            return True, "Resume is optional"
        
        if len(resume_text.strip()) < 50:
            return False, "Resume text seems too short (minimum 50 characters)"
        
        if len(resume_text) > 50000:
            return False, "Resume text is too long (maximum 50,000 characters)"
        
        return True, "Valid resume text"
    
    @staticmethod
    def validate_file_upload(file_content: bytes, file_type: str, max_size_mb: int = 5) -> Tuple[bool, str]:
        """Validate uploaded file."""
        if not file_content:
            return False, "File content is empty"
        
        # Check file size
        file_size_mb = len(file_content) / (1024 * 1024)
        if file_size_mb > max_size_mb:
            return False, f"File size exceeds {max_size_mb}MB limit"
        
        # Check file type
        allowed_types = ['pdf', 'docx', 'doc', 'txt']
        if file_type.lower() not in allowed_types:
            return False, f"File type '{file_type}' not supported. Allowed types: {', '.join(allowed_types)}"
        
        return True, "Valid file"
    
    @classmethod
    def validate_user_input(cls, user_input: UserInput) -> Tuple[bool, List[str]]:
        """Validate complete user input object."""
        errors = []
        
        # Validate name
        is_valid, message = cls.validate_name(user_input.name)
        if not is_valid:
            errors.append(f"Name: {message}")
        
        # Validate age
        if user_input.age is not None:
            is_valid, message = cls.validate_age(user_input.age)
            if not is_valid:
                errors.append(f"Age: {message}")
        
        # Validate education level
        is_valid, message = cls.validate_education_level(user_input.education_level)
        if not is_valid:
            errors.append(f"Education: {message}")
        
        # Validate interests
        is_valid, message = cls.validate_interests(user_input.interests)
        if not is_valid:
            errors.append(f"Interests: {message}")
        
        # Validate personality responses
        if user_input.personality_responses:
            is_valid, message = cls.validate_personality_responses(user_input.personality_responses)
            if not is_valid:
                errors.append(f"Personality: {message}")
        
        # Validate resume text
        if user_input.resume_text:
            is_valid, message = cls.validate_resume_text(user_input.resume_text)
            if not is_valid:
                errors.append(f"Resume: {message}")
        
        return len(errors) == 0, errors
