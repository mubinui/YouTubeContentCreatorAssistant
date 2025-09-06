from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from .config import config

# Sub agent 01: Scriptwriter Agent (with search capability)
scriptwriter_agent = LlmAgent(
    name="scriptwriter_agent",
    model=config.model_config['name'],
    instruction=config.load_instruction_from_file("scriptwriter_agent.txt"),
    tools=[google_search],
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

# Sub agent 03: Formatter Agent (combines script and visuals into final package)
formatter_agent = LlmAgent(
    name="formatter_agent",
    model=config.model_config['name'],
    instruction=config.load_instruction_from_file("formatter_agent.txt"),
    output_key="formatted_output" # for saving final formatted results to state
)

# Root agent coordinates the workflow
root_agent = LlmAgent(
    name="youtube_shorts_root_agent",
    model=config.model_config['name'],
    instruction=config.load_instruction_from_file("youtube_shorts_agent.txt"),
    sub_agents=[scriptwriter_agent, visualizer_agent, formatter_agent],
    output_key="final_output"
)

# ----- Run the root agent -----
if __name__ == "__main__":
    root_agent.run()
