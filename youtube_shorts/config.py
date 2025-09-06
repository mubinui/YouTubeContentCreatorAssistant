import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

class Config:
    """Centralized configuration management for Google ADK project."""

    def __init__(self):
        # Model provider configuration - supports both Google Gemini and OpenRouter
        self.model_provider = os.getenv('MODEL_PROVIDER', 'openrouter')  # Default to OpenRouter
        
        if self.model_provider == 'openrouter':
            # OpenRouter configuration for GPT OSS 20B
            # Note: We'll use a special model string that our wrapper can recognize
            self.model_config = {
                'name': f"openrouter:{os.getenv('OPENROUTER_MODEL', 'openai/gpt-oss-20b')}",  # Special prefix for OpenRouter models
                'api_key': os.getenv('OPENROUTER_API_KEY'),
                'base_url': 'https://openrouter.ai/api/v1',
                'max_tokens': int(os.getenv('MAX_TOKENS', '8192')),
                'temperature': float(os.getenv('TEMPERATURE', '0.1')),
                'provider': 'openrouter'
            }
            
            # OpenRouter specific configuration
            self.openrouter_config = {
                'api_key': os.getenv('OPENROUTER_API_KEY'),
                'model': os.getenv('OPENROUTER_MODEL', 'openai/gpt-oss-20b'),
                'base_url': 'https://openrouter.ai/api/v1',
                'max_tokens': int(os.getenv('MAX_TOKENS', '8192')),
                'temperature': float(os.getenv('TEMPERATURE', '0.1')),
                'app_name': os.getenv('APP_NAME', 'YouTube Shorts Creator'),
                'site_url': os.getenv('SITE_URL', 'https://github.com/mubinui/YouTubeContentCreatorAssistant')
            }
        else:
            # Fallback to Google Gemini configuration
            self.model_config = {
                'name': os.getenv('MODEL_NAME', 'gemini-2.5-flash'),  # Latest Gemini model with function calling
                'api_key': os.getenv('GOOGLE_API_KEY'),
                'max_tokens': int(os.getenv('MAX_TOKENS', '8192')),
                'temperature': float(os.getenv('TEMPERATURE', '0.1')),
                'provider': 'google'
            }
            
            self.openrouter_config = None

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
