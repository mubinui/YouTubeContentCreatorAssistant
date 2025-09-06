"""
OpenRouter Model Integration for Google ADK
This module provides a simplified OpenRouter integration using direct API calls.
"""

import os
import json
import asyncio
from typing import List, Dict, Any, Optional
from openai import OpenAI
from .config import config


class OpenRouterClient:
    """Simplified OpenRouter client for direct API integration."""
    
    def __init__(self):
        if not config.openrouter_config:
            raise ValueError("OpenRouter configuration not found. Set MODEL_PROVIDER=openrouter in .env")
        
        self.config = config.openrouter_config
        self.api_key = self.config['api_key']
        self.model = self.config['model']
        self.base_url = self.config['base_url']
        
        if not self.api_key:
            raise ValueError("OpenRouter API key is required. Set OPENROUTER_API_KEY in .env")
        
        # Initialize OpenAI client with OpenRouter configuration
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )
    
    def generate_content(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Generate content using OpenRouter API."""
        try:
            messages = []
            
            # Add system instruction if provided
            if system_instruction:
                messages.append({
                    "role": "system",
                    "content": system_instruction
                })
            
            # Add user prompt
            messages.append({
                "role": "user", 
                "content": prompt
            })
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.config['max_tokens'],
                temperature=self.config['temperature'],
                extra_headers={
                    "HTTP-Referer": self.config.get('site_url', ''),
                    "X-Title": self.config.get('app_name', 'YouTube Shorts Creator'),
                }
            )
            
            return response.choices[0].message.content or ""
            
        except Exception as e:
            print(f"❌ OpenRouter API Error: {e}")
            return f"Error: {str(e)}"
    
    def generate_content_with_tools(self, prompt: str, tools: List[Any], system_instruction: Optional[str] = None) -> Dict[str, Any]:
        """Generate content with tool calling support."""
        try:
            messages = []
            
            # Add system instruction if provided
            if system_instruction:
                messages.append({
                    "role": "system",
                    "content": system_instruction
                })
            
            # Add user prompt
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Convert tools to OpenAI format
            openai_tools = []
            for tool in tools:
                if hasattr(tool, 'name') and hasattr(tool, 'description'):
                    openai_tools.append({
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": getattr(tool, 'input_schema', {})
                        }
                    })
            
            # Prepare completion parameters
            completion_params = {
                "model": self.model,
                "messages": messages,
                "max_tokens": self.config['max_tokens'],
                "temperature": self.config['temperature'],
                "extra_headers": {
                    "HTTP-Referer": self.config.get('site_url', ''),
                    "X-Title": self.config.get('app_name', 'YouTube Shorts Creator'),
                }
            }
            
            # Add tools if available
            if openai_tools:
                completion_params["tools"] = openai_tools
                completion_params["tool_choice"] = "auto"
            
            # Make API call
            response = self.client.chat.completions.create(**completion_params)
            
            choice = response.choices[0]
            result = {
                "content": choice.message.content or "",
                "tool_calls": [],
                "finish_reason": choice.finish_reason
            }
            
            # Handle tool calls if present
            if hasattr(choice.message, 'tool_calls') and choice.message.tool_calls:
                for tool_call in choice.message.tool_calls:
                    if hasattr(tool_call, 'function'):
                        result["tool_calls"].append({
                            "id": getattr(tool_call, 'id', ''),
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        })
            
            return result
            
        except Exception as e:
            print(f"❌ OpenRouter API Error with tools: {e}")
            return {
                "content": f"Error: {str(e)}",
                "tool_calls": [],
                "finish_reason": "error"
            }

    def test_connection(self) -> bool:
        """Test the OpenRouter connection."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            print(f"✅ Successfully connected to OpenRouter model: {self.model}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to OpenRouter: {e}")
            return False


# Global OpenRouter client instance
_openrouter_client = None

def get_openrouter_client() -> OpenRouterClient:
    """Get or create the global OpenRouter client."""
    global _openrouter_client
    if _openrouter_client is None:
        _openrouter_client = OpenRouterClient()
    return _openrouter_client


def is_openrouter_model(model_name: str) -> bool:
    """Check if a model name refers to OpenRouter."""
    return model_name.startswith("openrouter:")


def extract_openrouter_model(model_name: str) -> str:
    """Extract the actual model name from OpenRouter prefix."""
    if model_name.startswith("openrouter:"):
        return model_name[11:]  # Remove "openrouter:" prefix
    return model_name
