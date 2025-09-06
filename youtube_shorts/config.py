import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

class Config:
    """Centralized configuration management for Google ADK project."""

    def __init__(self):
        # Model configuration
        self.model_config = {
            'name': os.getenv('MODEL_NAME', 'gemini-2.0-flash-exp'),
            'api_key': os.getenv('GOOGLE_API_KEY'),
            'project_id': os.getenv('GOOGLE_CLOUD_PROJECT_ID'),
            'max_tokens': int(os.getenv('MAX_TOKENS', '2048')),
            'temperature': float(os.getenv('TEMPERATURE', '0.7'))
        }

        # Project paths
        self.project_root = Path(__file__).parent

        self.validate_env_config()

    def validate_env_config(self):
        """Validate that required environment variables are set."""
        required_vars = ['GOOGLE_API_KEY', 'MODEL_NAME']
        missing_vars = []

        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)

        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

        return True

    def load_instruction_from_file(self, filename):
        """Load instruction text from a file"""
        file_path = self.project_root / filename
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        else:
            # Return a default instruction if file doesn't exist
            return f"You are an AI assistant for the {filename.replace('_', ' ').replace('.txt', '')} task."

# Create global config instance
config = Config()
