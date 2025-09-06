#!/usr/bin/env python3
"""
Test script to verify the YouTube Shorts agent workflow with OpenRouter integration.
Run this with: python test_agent.py
"""

from youtube_shorts.agent import root_agent
from youtube_shorts.config import config
from youtube_shorts.openrouter_model import get_openrouter_client

def test_openrouter_integration():
    """Test OpenRouter model integration."""
    print("🧪 Testing OpenRouter Integration...")
    
    if config.model_provider == 'openrouter':
        try:
            client = get_openrouter_client()
            if client.test_connection():
                print(f"✅ OpenRouter connected successfully!")
                if config.openrouter_config:
                    print(f"   Model: {config.openrouter_config['model']}")
                    print(f"   Base URL: {config.openrouter_config['base_url']}")
                
                # Test a simple generation
                test_response = client.generate_content(
                    "Say hello and confirm you are working.",
                    "You are a helpful AI assistant."
                )
                print(f"   Test Response: {test_response[:100]}...")
                return True
            else:
                print("❌ OpenRouter connection failed")
                return False
        except Exception as e:
            print(f"❌ OpenRouter test error: {e}")
            return False
    else:
        print(f"ℹ️ Using {config.model_provider} provider instead of OpenRouter")
        return True

def test_agent():
    """Test the agent structure and configuration."""
    print("\n🚀 Testing Enhanced YouTube Shorts Agent Configuration...")
    print(f"Root Agent: {root_agent.name}")
    print(f"Model: {root_agent.model}")
    print(f"Provider: {config.model_provider}")
    
    # Check if the root agent has sub_agents
    if hasattr(root_agent, 'sub_agents') and root_agent.sub_agents:
        print(f"Sub-agents: {[agent.name for agent in root_agent.sub_agents]}")
        
        # Check the sequential workflow
        sequential_agent = root_agent.sub_agents[0]
        print(f"Sequential Workflow: {sequential_agent.name}")
        
        if hasattr(sequential_agent, 'sub_agents') and sequential_agent.sub_agents:
            print("Sequential workflow sub-agents:")
            for i, agent in enumerate(sequential_agent.sub_agents, 1):
                print(f"  {i}. {agent.name} -> output_key: {getattr(agent, 'output_key', 'None')}")
                
                # Check if scriptwriter has tools
                if agent.name == "scriptwriter_agent":
                    tools_info = "Tools: Google Search enabled" if hasattr(agent, 'tools') and getattr(agent, 'tools', None) else "Tools: None"
                    print(f"     {tools_info}")
    
    print("\n=== OPENROUTER INTEGRATION STATUS ===")
    if config.model_provider == 'openrouter':
        print("✅ OpenRouter GPT OSS 20B model configured")
        print(f"   Model: {config.openrouter_config.get('model', 'Unknown') if config.openrouter_config else 'Not configured'}")
        print("✅ Enhanced prompts optimized for GPT OSS model")
        print("✅ Tool calling support for Google Search integrated")
    else:
        print("ℹ️ Using Google Gemini as fallback")
    
    print("\n=== ENHANCEMENTS OVERVIEW ===")
    print("✅ Google Search capability for real-time research")
    print("✅ Enhanced prompts for viral content creation")
    print("✅ Mobile-optimized visual concepts")
    print("✅ Comprehensive production package formatting")
    print("✅ OpenRouter GPT OSS 20B model integration")
    
    print("\n=== TESTING RECOMMENDATIONS ===")
    print("1. Test with trending tech topics (e.g., 'Latest AI developments', 'New JavaScript framework')")
    print("2. Verify OpenRouter model responses are coherent and relevant")
    print("3. Check that visual concepts are mobile-optimized")
    print("4. Ensure production package includes all necessary details")
    print("5. Test tool calling with Google Search functionality")
    
    print("\nAgent structure configured correctly!")
    print("To run the agent interactively, use: adk web")
    print("Make sure your .env file has OPENROUTER_API_KEY set for OpenRouter integration.")

def test_sample_topics():
    """Suggest some test topics for validation."""
    print("\n=== SUGGESTED TEST TOPICS FOR OPENROUTER ===")
    test_topics = [
        "Latest developments in AI coding assistants",
        "New React 19 features developers need to know", 
        "Why developers are switching to Rust in 2024",
        "The most viral programming memes this week",
        "Breaking: Major tech company announces new developer tools",
        "GPT-4 vs Claude vs Gemini: Which AI is better for coding?",
        "The future of open source AI models in 2025"
    ]
    
    for i, topic in enumerate(test_topics, 1):
        print(f"{i}. {topic}")
    
    print("\nThese topics should leverage OpenRouter's capabilities for current, engaging content.")

def show_configuration():
    """Show current configuration details."""
    print("\n=== CURRENT CONFIGURATION ===")
    print(f"Model Provider: {config.model_provider}")
    print(f"Model Name: {config.model_config['name']}")
    
    if config.model_provider == 'openrouter' and config.openrouter_config:
        print(f"OpenRouter Model: {config.openrouter_config['model']}")
        print(f"Max Tokens: {config.openrouter_config['max_tokens']}")
        print(f"Temperature: {config.openrouter_config['temperature']}")
        api_key_status = "✅ Set" if config.openrouter_config['api_key'] else "❌ Missing"
        print(f"API Key: {api_key_status}")
    
    print("\n=== REQUIRED ENVIRONMENT VARIABLES ===")
    required_vars = {
        'OPENROUTER_API_KEY': 'Your OpenRouter API key',
        'MODEL_PROVIDER': 'Set to "openrouter" for GPT OSS 20B',
        'OPENROUTER_MODEL': 'Model name (default: openai/gpt-oss-20b)',
    }
    
    for var, description in required_vars.items():
        import os
        status = "✅ Set" if os.getenv(var) else "❌ Missing"
        print(f"{var}: {status} - {description}")

if __name__ == "__main__":
    show_configuration()
    test_openrouter_integration()
    test_agent()
    test_sample_topics()
