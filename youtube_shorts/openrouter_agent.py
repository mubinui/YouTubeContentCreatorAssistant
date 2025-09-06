"""
OpenRouter Agent Wrapper for Google ADK
This module provides a wrapper that intercepts agent calls and redirects to OpenRouter when needed.
"""

from typing import Any, Dict, List, Optional
from google.adk.agents import LlmAgent
from .openrouter_model import get_openrouter_client, is_openrouter_model, extract_openrouter_model


class OpenRouterLlmAgent(LlmAgent):
    """Extended LlmAgent that can use OpenRouter models."""
    
    def __init__(self, *args, **kwargs):
        # Check if this is an OpenRouter model
        model = kwargs.get('model', '')
        self.is_openrouter = is_openrouter_model(model)
        
        if self.is_openrouter:
            # Store OpenRouter client and actual model name
            self.openrouter_client = get_openrouter_client()
            self.actual_model = extract_openrouter_model(model)
            print(f"🔄 Initialized OpenRouter agent with model: {self.actual_model}")
        
        super().__init__(*args, **kwargs)
    
    async def _llm_flow(self, *args, **kwargs):
        """Override the LLM flow to use OpenRouter when appropriate."""
        if not self.is_openrouter:
            # Use the default Google ADK flow
            return await super()._llm_flow(*args, **kwargs)
        
        try:
            # Extract the prompt and system instruction from the flow
            prompt = self._extract_prompt_from_flow(*args, **kwargs)
            system_instruction = self._extract_system_instruction()
            
            # Check if we have tools
            tools = getattr(self, 'tools', [])
            
            if tools:
                # Use OpenRouter with tools
                result = self.openrouter_client.generate_content_with_tools(
                    prompt=prompt,
                    tools=tools,
                    system_instruction=system_instruction
                )
                
                # Handle tool calls if present
                if result.get('tool_calls'):
                    # Process tool calls and get responses
                    tool_results = await self._process_tool_calls(result['tool_calls'])
                    
                    # Continue conversation with tool results
                    follow_up_prompt = f"{prompt}\n\nTool results: {tool_results}"
                    final_result = self.openrouter_client.generate_content(
                        prompt=follow_up_prompt,
                        system_instruction=system_instruction
                    )
                    return self._format_response(final_result)
                else:
                    return self._format_response(result['content'])
            else:
                # Use OpenRouter without tools
                result = self.openrouter_client.generate_content(
                    prompt=prompt,
                    system_instruction=system_instruction
                )
                return self._format_response(result)
                
        except Exception as e:
            print(f"❌ OpenRouter LLM flow error: {e}")
            # Fallback to default flow
            return await super()._llm_flow(*args, **kwargs)
    
    def _extract_prompt_from_flow(self, *args, **kwargs) -> str:
        """Extract the user prompt from the LLM flow arguments."""
        # Try to extract from various argument positions
        if args:
            for arg in args:
                if isinstance(arg, str) and len(arg) > 10:
                    return arg
                elif hasattr(arg, 'contents') and arg.contents:
                    # Extract from contents
                    texts = []
                    for content in arg.contents:
                        if hasattr(content, 'parts'):
                            for part in content.parts:
                                if hasattr(part, 'text'):
                                    texts.append(part.text)
                    return " ".join(texts) if texts else "Please help me."
        
        return "Please help me with this request."
    
    def _extract_system_instruction(self) -> Optional[str]:
        """Extract system instruction from the agent."""
        instruction = getattr(self, 'instruction', '')
        if callable(instruction):
            try:
                return instruction([])  # Call with empty list as default
            except:
                return None
        return instruction if instruction else None
    
    async def _process_tool_calls(self, tool_calls: List[Dict]) -> str:
        """Process tool calls and return results."""
        results = []
        
        for tool_call in tool_calls:
            tool_name = tool_call.get('name', '')
            tool_args = tool_call.get('arguments', '{}')
            
            # Find the tool in our tools list
            tool_obj = None
            for tool in getattr(self, 'tools', []):
                if hasattr(tool, 'name') and tool.name == tool_name:
                    tool_obj = tool
                    break
            
            if tool_obj:
                try:
                    # Execute the tool
                    import json
                    args_dict = json.loads(tool_args) if isinstance(tool_args, str) else tool_args
                    result = await tool_obj(**args_dict) if hasattr(tool_obj, '__call__') else str(tool_obj)
                    results.append(f"{tool_name}: {result}")
                except Exception as e:
                    results.append(f"{tool_name}: Error - {str(e)}")
            else:
                results.append(f"{tool_name}: Tool not found")
        
        return "\n".join(results)
    
    def _format_response(self, content: str) -> Any:
        """Format the response to match Google ADK expectations."""
        # Create a simple response structure that Google ADK can handle
        class SimpleResponse:
            def __init__(self, text: str):
                self.text = text
                self.content = text
            
            def __str__(self):
                return self.text
        
        return SimpleResponse(content)


def create_openrouter_agent(**kwargs) -> OpenRouterLlmAgent:
    """Factory function to create OpenRouter-enabled agents."""
    return OpenRouterLlmAgent(**kwargs)
