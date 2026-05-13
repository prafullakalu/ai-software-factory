"""
🧠 MULTI-LLM PROVIDER SYSTEM

Supports all major LLM providers:
- OpenAI (GPT-4, GPT-4 Turbo, GPT-3.5)
- Anthropic (Claude 3 Opus, Sonnet, Haiku)
- Google (Gemini Pro/Ultra)
- Azure OpenAI
- Ollama (local models)
- AWS Bedrock
"""

import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# PROVIDER ENUMS
# ============================================================================

class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    AZURE = "azure"
    OLLAMA = "ollama"
    BEDROCK = "bedrock"


class ModelPurpose(Enum):
    PLANNING = "planning"      # Reasoning, architecture
    CODING = "coding"         # Code generation
    FAST = "fast"            # Quick tasks
    CHEAP = "cheap"         # Low cost tasks


# ============================================================================
# PROVIDER MODELS
# ============================================================================

PROVIDER_MODELS = {
    # OpenAI Models
    "openai": {
        "gpt-4": {
            "name": "GPT-4",
            "purpose": "fast",
            "max_tokens": 8192,
            "cost": 0.03,  # per 1k input
            "speed": "moderate",
        },
        "gpt-4-turbo": {
            "name": "GPT-4 Turbo",
            "purpose": "coding",
            "max_tokens": 128000,
            "cost": 0.01,
            "speed": "fast",
        },
        "gpt-4o": {
            "name": "GPT-4o",
            "purpose": "coding",
            "max_tokens": 128000,
            "cost": 0.005,
            "speed": "fast",
        },
        "gpt-3.5-turbo": {
            "name": "GPT-3.5 Turbo",
            "purpose": "cheap",
            "max_tokens": 16385,
            "cost": 0.0005,
            "speed": "very-fast",
        },
    },
    
    # Anthropic Models
    "anthropic": {
        "claude-3-opus": {
            "name": "Claude 3 Opus",
            "purpose": "planning",
            "max_tokens": 200000,
            "cost": 0.015,
            "speed": "moderate",
        },
        "claude-3-sonnet": {
            "name": "Claude 3 Sonnet",
            "purpose": "coding",
            "max_tokens": 200000,
            "cost": 0.003,
            "speed": "fast",
        },
        "claude-3-haiku": {
            "name": "Claude 3 Haiku",
            "purpose": "fast",
            "max_tokens": 200000,
            "cost": 0.00025,
            "speed": "very-fast",
        },
        "claude-3-5-sonnet": {
            "name": "Claude 3.5 Sonnet",
            "purpose": "coding",
            "max_tokens": 200000,
            "cost": 0.003,
            "speed": "fast",
        },
    },
    
    # Google Models
    "google": {
        "gemini-pro": {
            "name": "Gemini Pro",
            "purpose": "fast",
            "max_tokens": 32768,
            "cost": 0.00125,
            "speed": "fast",
        },
        "gemini-ultra": {
            "name": "Gemini Ultra",
            "purpose": "planning",
            "max_tokens": 32768,
            "cost": 0.01,
            "speed": "moderate",
        },
        "gemini-1.5-pro": {
            "name": "Gemini 1.5 Pro",
            "purpose": "coding",
            "max_tokens": 1000000,
            "cost": 0.00125,
            "speed": "fast",
        },
        "gemini-1.5-flash": {
            "name": "Gemini 1.5 Flash",
            "purpose": "fast",
            "max_tokens": 1000000,
            "cost": 0,
            "speed": "very-fast",
        },
    },
    
    # Azure OpenAI
    "azure": {
        "gpt-4": {
            "name": "Azure GPT-4",
            "purpose": "planning",
            "max_tokens": 8192,
            "cost": 0.03,
            "speed": "moderate",
        },
        "gpt-4-turbo": {
            "name": "Azure GPT-4 Turbo",
            "purpose": "coding",
            "max_tokens": 128000,
            "cost": 0.01,
            "speed": "fast",
        },
    },
    
    # Ollama Models (Local)
    "ollama": {
        "llama3": {
            "name": "Llama 3",
            "purpose": "planning",
            "max_tokens": 8192,
            "cost": 0,  # Free (local)
            "speed": "local",
        },
        "llama3:70b": {
            "name": "Llama 3 70B",
            "purpose": "planning",
            "max_tokens": 8192,
            "cost": 0,
            "speed": "slow",
        },
        "mixtral": {
            "name": "Mixtral",
            "purpose": "coding",
            "max_tokens": 32768,
            "cost": 0,
            "speed": "moderate",
        },
        "qwen2.5-coder": {
            "name": "Qwen Coder",
            "purpose": "coding",
            "max_tokens": 32768,
            "cost": 0,
            "speed": "local",
        },
        "codellama": {
            "name": "Code Llama",
            "purpose": "coding",
            "max_tokens": 16384,
            "cost": 0,
            "speed": "local",
        },
        "mistral": {
            "name": "Mistral",
            "purpose": "fast",
            "max_tokens": 8192,
            "cost": 0,
            "speed": "fast",
        },
    },
    
    # AWS Bedrock
    "bedrock": {
        "claude-3-sonnet": {
            "name": "Claude 3 Sonnet (Bedrock)",
            "purpose": "coding",
            "max_tokens": 200000,
            "cost": 0.003,
            "speed": "fast",
        },
        "claude-3-haiku": {
            "name": "Claude 3 Haiku (Bedrock)",
            "purpose": "fast",
            "max_tokens": 200000,
            "cost": 0.00025,
            "speed": "very-fast",
        },
        "llama3-70b": {
            "name": "Llama 3 70B (Bedrock)",
            "purpose": "planning",
            "max_tokens": 8192,
            "cost": 0.00195,
            "speed": "moderate",
        },
    },
}


# ============================================================================
# MODEL CONFIG
# ============================================================================

@dataclass
class ModelConfig:
    """Configuration for an LLM model."""
    provider: str
    model: str
    api_key: str
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4096
    organization: Optional[str] = None
    
    def get_model_info(self) -> Dict:
        """Get model information."""
        return PROVIDER_MODELS.get(self.provider, {}).get(self.model, {})


# ============================================================================
# PROVIDER MANAGER
# ============================================================================

class LLMManager:
    """Manages multiple LLM providers."""
    
    def __init__(self):
        self.configs: Dict[str, ModelConfig] = {}
        self.providers: Dict[str, object] = {}
        self.load_configs()
    
    def load_configs(self):
        """Load configurations from environment."""
        # OpenAI
        if openai_key := os.getenv("OPENAI_API_KEY"):
            self.configs["openai"] = ModelConfig(
                provider="openai",
                model="gpt-4o",
                api_key=openai_key,
            )
        
        # Anthropic
        if anthropic_key := os.getenv("ANTHROPIC_API_KEY"):
            self.configs["anthropic"] = ModelConfig(
                provider="anthropic",
                model="claude-3-5-sonnet",
                api_key=anthropic_key,
            )
        
        # Google
        if google_key := os.getenv("GOOGLE_API_KEY"):
            self.configs["google"] = ModelConfig(
                provider="google",
                model="gemini-1.5-pro",
                api_key=google_key,
            )
        
        # Azure
        if azure_key := os.getenv("AZURE_OPENAI_API_KEY"):
            self.configs["azure"] = ModelConfig(
                provider="azure",
                model="gpt-4-turbo",
                api_key=azure_key,
                base_url=os.getenv("AZURE_OPENAI_API_BASE", ""),
            )
        
        # Ollama (local default)
        self.configs["ollama"] = ModelConfig(
            provider="ollama",
            model="llama3",
            api_key="",
            base_url=os.getenv("OLLAMA_URL", "http://localhost:11434"),
        )
        
        # Bedrock
        if aws_access := os.getenv("AWS_ACCESS_KEY"):
            self.configs["bedrock"] = ModelConfig(
                provider="bedrock",
                model="claude-3-sonnet",
                api_key=aws_access,
            )
    
    def get_provider(self, name: str = "openai") -> Optional[ModelConfig]:
        """Get provider configuration."""
        return self.configs.get(name)
    
    def list_providers(self) -> List[Dict]:
        """List all available providers."""
        result = []
        for name, config in self.configs.items():
            model_info = config.get_model_info() or {}
            result.append({
                "name": name,
                "provider": config.provider,
                "model": config.model,
                "status": "configured" if config.api_key else "no-key",
                "info": model_info,
            })
        return result
    
    def add_provider(self, name: str, config: ModelConfig):
        """Add a new provider configuration."""
        self.configs[name] = config
    
    def remove_provider(self, name: str):
        """Remove a provider."""
        if name in self.configs:
            del self.configs[name]


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_model_config(
    provider: str,
    model: str,
    api_key: str = None,
    **kwargs,
) -> ModelConfig:
    """Create a model configuration."""
    return ModelConfig(
        provider=provider,
        model=model,
        api_key=api_key or os.getenv(f"{provider.upper()}_API_KEY", ""),
        **kwargs,
    )


def get_all_models() -> Dict[str, Dict]:
    """Get all available models."""
    return PROVIDER_MODELS


def get_models_by_purpose(purpose: str) -> List[Dict]:
    """Get models filtered by purpose."""
    models = []
    for provider, provider_models in PROVIDER_MODELS.items():
        for model_id, model_info in provider_models.items():
            if model_info.get("purpose") == purpose:
                models.append({
                    "provider": provider,
                    "model": model_id,
                    **model_info,
                })
    return models


def get_cheapest_models() -> List[Dict]:
    """Get models sorted by cost."""
    models = []
    for provider, provider_models in PROVIDER_MODELS.items():
        for model_id, model_info in provider_models.items():
            models.append({
                "provider": provider,
                "model": model_id,
                **model_info,
            })
    return sorted(models, key=lambda m: m.get("cost", 999))


def get_fastest_models() -> List[Dict]:
    """Get models sorted by speed."""
    speed_order = {"very-fast": 0, "fast": 1, "moderate": 2, "slow": 3}
    
    models = []
    for provider, provider_models in PROVIDER_MODELS.items():
        for model_id, model_info in provider_models.items():
            models.append({
                "provider": provider,
                "model": model_id,
                "speed_value": speed_order.get(model_info.get("speed", "moderate"), 2),
                **model_info,
            })
    return sorted(models, key=lambda m: m.get("speed_value", 2))


# ============================================================================
# EXPORTS
# ============================================================================

# Global manager
manager = LLMManager()


__all__ = [
    "LLMProvider",
    "ModelPurpose",
    "ModelConfig",
    "LLMManager",
    "PROVIDER_MODELS",
    "create_model_config",
    "get_all_models",
    "get_models_by_purpose",
    "get_cheapest_models",
    "get_fastest_models",
    "manager",
]