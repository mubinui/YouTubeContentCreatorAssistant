import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_instruction_from_file(file_path):
    """Load instruction content from a text file."""
    try:
        # Resolve path relative to this file's directory for package compatibility
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, file_path)
        with open(full_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Warning: Instruction file {file_path} not found")
        return ""
    except Exception as e:
        print(f"Error loading instruction file {file_path}: {e}")
        return ""

def get_model_config():
    """Get model configuration from environment variables."""
    return {
        'name': os.getenv('MODEL_NAME', 'gemini-2.0-flash-exp'),
        'api_key': os.getenv('GOOGLE_API_KEY'),
        'project_id': os.getenv('GOOGLE_CLOUD_PROJECT_ID'),
        'max_tokens': int(os.getenv('MAX_TOKENS', '2048')),
        'temperature': float(os.getenv('TEMPERATURE', '0.7'))
    }

def validate_env_config():
    """Validate that required environment variables are set."""
    required_vars = ['GOOGLE_API_KEY', 'MODEL_NAME']
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    return True
