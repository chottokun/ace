import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class LLMConfig:
    """
    Configuration for Large Language Models.
    """
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    DEFAULT_MODEL_OPENAI: str = os.getenv("DEFAULT_MODEL_OPENAI", "gpt-4o")
    DEFAULT_MODEL_GOOGLE: str = os.getenv("DEFAULT_MODEL_GOOGLE", "gemini-2.5-flash-lite")
    DEFAULT_MODEL_ANTHROPIC: str = os.getenv("DEFAULT_MODEL_ANTHROPIC", "claude-3-opus-20240229")
    DEFAULT_MODEL_OLLAMA: str = os.getenv("DEFAULT_MODEL_OLLAMA", "llama3")
    TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "1024"))

class ACEConfig:
    """
    Configuration for the Agentic Context Engineering framework.
    """
    NUM_ITERATIONS: int = int(os.getenv("ACE_NUM_ITERATIONS", "5"))
    OUTPUT_DIR: str = os.getenv("ACE_OUTPUT_DIR", "ace_runs")
    LOG_LEVEL: str = os.getenv("ACE_LOG_LEVEL", "INFO")
    # Define a default reflection prompt template
    DEFAULT_REFLECTION_PROMPT: str = (
        "You are an expert critic and an LLM engineer. Analyze the following agent's performance:\n\n"
        "Task: {task_description}\n"
        "Current Context (System Prompt): {current_context}\n"
        "LLM Response: {llm_response}\n"
        "Evaluation Score: {evaluation_score}\n"
        "Desired Outcome: {desired_outcome}\n\n"
        "Based on this, identify specific weaknesses or areas for improvement in the 'Current Context' "
        "(the system prompt). Suggest a refined, more effective system prompt that would lead to better performance "
        "for the given task and desired outcome. "
        "Provide ONLY the new system prompt in your response, without any additional commentary."
    )

    EVALUATION_THRESHOLD: float = float(os.getenv("ACE_EVALUATION_THRESHOLD", "0.9")) # e.g., stop if score > 0.9

# Ensure output directory exists
os.makedirs(ACEConfig.OUTPUT_DIR, exist_ok=True)
