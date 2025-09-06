import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

class Config:
    """Centralized configuration management for Google ADK project."""

    def __init__(self):
        # Model configuration - use latest Gemini model that supports function calling
        self.model_config = {
            'name': os.getenv('MODEL_NAME', 'gemini-2.5-flash'),  # Latest Gemini model with function calling
            'api_key': os.getenv('GOOGLE_API_KEY'),
            'max_tokens': int(os.getenv('MAX_TOKENS', '8192')),
            'temperature': float(os.getenv('TEMPERATURE', '0.1'))
        }

        # Project paths
        self.project_root = Path(__file__).parent

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
