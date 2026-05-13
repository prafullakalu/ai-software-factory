"""
⚙️ CONFIGURATION - AI Model Settings

Configure different LLM providers:
- Ollama (local): llama3, qwen, mistral, etc.
- OpenAI: gpt-4, gpt-4-turbo, gpt-3.5-turbo
- Anthropic: claude-3-opus, claude-3-sonnet
- Google: gemini-pro
- Azure OpenAI
"""

from crewai import LLM
import os


# ============================================================================
# MODEL PROVIDERS
# ============================================================================

def get_ollama_model(model: str = "llama3", base_url: str = "http://localhost:11434"):
    """Create an Ollama model"""
    return LLM(
        model=f"ollama/{model}",
        base_url=base_url,
    )


def get_openai_model(
    model: str = "gpt-4-turbo",
    api_key: str = None,
    temperature: float = 0.7,
):
    """Create an OpenAI model"""
    return LLM(
        model=f"openai/{model}",
        api_key=api_key or os.getenv("OPENAI_API_KEY"),
        temperature=temperature,
    )


def get_anthropic_model(
    model: str = "claude-3-sonnet-20240229",
    api_key: str = None,
):
    """Create an Anthropic model"""
    return LLM(
        model=f"anthropic/{model}",
        api_key=api_key or os.getenv("ANTHROPIC_API_KEY"),
    )


def get_azure_model(
    model: str = "gpt-4",
    api_key: str = None,
    api_base: str = None,
    api_version: str = "2024-02-01",
):
    """Create an Azure OpenAI model"""
    return LLM(
        model=f"azure/{model}",
        api_key=api_key or os.getenv("AZURE_OPENAI_API_KEY"),
        base_url=api_base or os.getenv("AZURE_OPENAI_API_BASE"),
        api_version=api_version,
    )


# ============================================================================
# DEFAULT MODELS
# ============================================================================

# Planning model - for reasoning and planning tasks
planningModel = get_ollama_model("llama3")

# Coding model - for code generation
codingModel = get_ollama_model("qwen2.5-coder:7b")

# Alternative: Use OpenAI for better results
# planningModel = get_openai_model("gpt-4-turbo")
# codingModel = get_openai_model("gpt-4-turbo")

# Alternative: Use Anthropic for planning
# planningModel = get_anthropic_model("claude-3-opus-20240229")
# codingModel = get_anthropic_model("claude-3-sonnet-20240229")


# ============================================================================
# MODEL CONFIGURATION
# ============================================================================

MODEL_CONFIG = {
    "provider": "ollama",  # ollama, openai, anthropic, azure
    "planning_model": "llama3",
    "coding_model": "qwen2.5-coder:7b",
    "temperature": 0.7,
    "max_tokens": 4096,
    "top_p": 0.9,
}


def update_config(
    provider: str = None,
    planning_model: str = None,
    coding_model: str = None,
    temperature: float = None,
):
    """Update the model configuration"""
    global planningModel, codingModel, MODEL_CONFIG
    
    if provider:
        MODEL_CONFIG["provider"] = provider
    if planning_model:
        MODEL_CONFIG["planning_model"] = planning_model
    if coding_model:
        MODEL_CONFIG["coding_model"] = coding_model
    if temperature:
        MODEL_CONFIG["temperature"] = temperature
    
    # Recreate models with new config
    if provider == "ollama":
        planningModel = get_ollama_model(MODEL_CONFIG["planning_model"])
        codingModel = get_ollama_model(MODEL_CONFIG["coding_model"])
    elif provider == "openai":
        planningModel = get_openai_model(MODEL_CONFIG["planning_model"])
        codingModel = get_openai_model(MODEL_CONFIG["coding_model"])
    elif provider == "anthropic":
        planningModel = get_anthropic_model(MODEL_CONFIG["planning_model"])
        codingModel = get_anthropic_model(MODEL_CONFIG["coding_model"])
    
    return MODEL_CONFIG


# ============================================================================
# PROVIDER COMPATIBILITY
# ============================================================================

# Models compatible with each provider
OLLAMA_MODELS = [
    "llama3",
    "llama3:70b",
    "mistral",
    "mixtral",
    "qwen",
    "qwen2.5-coder:7b",
    "codellama",
    "orca-mini",
    "neural-chat",
]

OPENAI_MODELS = [
    "gpt-4",
    "gpt-4-turbo",
    "gpt-4o",
    "gpt-3.5-turbo",
]

ANTHROPIC_MODELS = [
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
]


def list_available_models(provider: str = "ollama") -> list:
    """List available models for a provider"""
    if provider == "ollama":
        return OLLAMA_MODELS
    elif provider == "openai":
        return OPENAI_MODELS
    elif provider == "anthropic":
        return ANTHROPIC_MODELS
    return []