from google.adk.agents import LlmAgent
from .config import config

# Sub agent 01: Scriptwriter Agent (without tools for now)
scriptwriter_agent = LlmAgent(
    name="scriptwriter_agent",
    model=config.model_config['name'],
    instruction=config.load_instruction_from_file("scriptwriter_agent.txt"),
    tools=[],  # Empty tools list until proper tools are available
    output_key="generated_script" # for saving results to state
)

# Sub agent 02: Visualizer Agent
visualizer_agent = LlmAgent(
    name="visualizer_agent",
    model=config.model_config['name'],
    description="You are a visual content creator. Your task is to generate detailed visual concepts and scene descriptions based on the provided video script.",
    instruction=config.load_instruction_from_file("visualizer_agent.txt"),
    output_key="visual_concepts" # for saving results to state
)

# Root agent that coordinates the sub-agents
root_agent = LlmAgent(
    name="youtube_shorts_root_agent",
    model=config.model_config['name'],
    instruction=config.load_instruction_from_file("youtube_shorts_agent.txt"),
    # Note: Using 'tools' parameter instead of 'agents' - check ADK documentation for correct parameter
    tools=[],  # Will contain sub-agents when properly configured
    output_key="final_output"
)

# ----- Run the root agent -----
if __name__ == "__main__":
    root_agent.run()
