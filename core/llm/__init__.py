"""
🤖 LLM CONFIGURATION

Model configuration for different providers.
"""

import os
from crewai import LLM


# ============================================================================
# PROVIDER FUNCTIONS
# ============================================================================

def get_ollama(model: str = "llama3", base_url: str = "http://localhost:11434") -> LLM:
    """Create Ollama model."""
    return LLM(model=f"ollama/{model}", base_url=base_url)


def get_openai(model: str = "gpt-4-turbo", api_key: str = None) -> LLM:
    """Create OpenAI model."""
    return LLM(
        model=f"openai/{model}",
        api_key=api_key or os.getenv("OPENAI_API_KEY"),
    )


def get_anthropic(model: str = "claude-3-sonnet-20240229", api_key: str = None) -> LLM:
    """Create Anthropic model."""
    return LLM(
        model=f"anthropic/{model}",
        api_key=api_key or os.getenv("ANTHROPIC_API_KEY"),
    )


def get_azure(model: str = "gpt-4", **kwargs) -> LLM:
    """Create Azure OpenAI model."""
    return LLM(
        model=f"azure/{model}",
        api_key=kwargs.get("api_key") or os.getenv("AZURE_OPENAI_API_KEY"),
        base_url=kwargs.get("base_url") or os.getenv("AZURE_OPENAI_API_BASE"),
        api_version=kwargs.get("api_version", "2024-02-01"),
    )


# ============================================================================
# DEFAULT MODELS
# ============================================================================

# Planning model - for reasoning
planning_model = get_ollama("llama3")

# Coding model - for code generation  
coding_model = get_ollama("qwen2.5-coder:7b")


# ============================================================================
# MODEL REGISTRY
# ============================================================================

MODEL_REGISTRY = {
    # Ollama models
    "ollama/llama3": lambda: get_ollama("llama3"),
    "ollama/llama3:70b": lambda: get_ollama("llama3:70b"),
    "ollama/mixtral": lambda: get_ollama("mixtral"),
    "ollama/qwen": lambda: get_ollama("qwen"),
    "ollama/qwen2.5-coder:7b": lambda: get_ollama("qwen2.5-coder:7b"),
    
    # OpenAI models
    "openai/gpt-4": lambda: get_openai("gpt-4"),
    "openai/gpt-4-turbo": lambda: get_openai("gpt-4-turbo"),
    "openai/gpt-3.5-turbo": lambda: get_openai("gpt-3.5-turbo"),
    
    # Anthropic models
    "anthropic/claude-3-opus": lambda: get_anthropic("claude-3-opus-20240229"),
    "anthropic/claude-3-sonnet": lambda: get_anthropic("claude-3-sonnet-20240229"),
    "anthropic/claude-3-haiku": lambda: get_anthropic("claude-3-haiku-20240307"),
}


def get_model(model_name: str) -> LLM:
    """Get model by name."""
    factory = MODEL_REGISTRY.get(model_name)
    if factory:
        return factory()
    # Default fallback
    return planning_model


__all__ = [
    "get_ollama",
    "get_openai", 
    "get_anthropic",
    "get_azure",
    "get_model",
    "planning_model",
    "coding_model",
    "MODEL_REGISTRY",
]