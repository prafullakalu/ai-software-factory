"""
🤖 LLM Client - Multi-provider LLM integration

Supports: Anthropic, OpenAI, DeepSeek, and Ollama (local)
"""

import os
import json
from typing import Generator, Optional, Dict, List, Any
from dataclasses import dataclass


@dataclass
class LLMConfig:
    """LLM Configuration."""
    provider: str = "stub"  # anthropic, openai, deepseek, ollama, stub
    model: str = "claude-3-sonnet-20240229"
    api_key: Optional[str] = None
    base_url: Optional[str] = None


class LLMClient:
    """
    Multi-provider LLM client.
    
    Priority: ANTHROPIC_API_KEY → OPENAI_API_KEY → DEEPSEEK_API_KEY → Ollama → stub
    """
    
    PROVIDERS = {
        "anthropic": {
            "model": "claude-3-sonnet-20240229",
            "env_key": "ANTHROPIC_API_KEY",
            "api_base": "https://api.anthropic.com/v1/messages",
        },
        "openai": {
            "model": "gpt-4-turbo",
            "env_key": "OPENAI_API_KEY",
            "api_base": "https://api.openai.com/v1/chat/completions",
        },
        "deepseek": {
            "model": "deepseek-chat",
            "env_key": "DEEPSEEK_API_KEY",
            "api_base": "https://api.deepseek.com/v1/chat/completions",
        },
        "ollama": {
            "model": "llama3",
            "env_key": None,
            "api_base": "http://localhost:11434/v1/chat/completions",
        },
    }
    
    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or self._auto_config()
    
    def _auto_config(self) -> LLMConfig:
        """Auto-detect provider from environment."""
        # Check each provider
        for provider, info in self.PROVIDERS.items():
            api_key = os.environ.get(info["env_key"]) if info["env_key"] else None
            if api_key:
                return LLMConfig(
                    provider=provider,
                    model=info["model"],
                    api_key=api_key,
                    base_url=info["api_base"],
                )
        
        # Try Ollama
        try:
            import httpx
            r = httpx.get("http://localhost:11434/api/tags", timeout=2)
            if r.status_code == 200:
                return LLMConfig(
                    provider="ollama",
                    model="llama3",
                    base_url="http://localhost:11434/v1/chat/completions",
                )
        except:
            pass
        
        # Fallback to stub
        return LLMConfig(provider="stub")
    
    def complete(self, system: str, user: str, stream: bool = False) -> str | Generator[str, None, None]:
        """Complete a prompt. Returns str or generator if stream=True."""
        if stream:
            return self._stream_complete(system, user)
        return self._complete(system, user)
    
    def _complete(self, system: str, user: str) -> str:
        """Synchronous completion."""
        provider = self.config.provider
        
        if provider == "anthropic":
            return self._anthropic_complete(system, user)
        elif provider == "openai":
            return self._openai_complete(system, user)
        elif provider == "deepseek":
            return self._deepseek_complete(system, user)
        elif provider == "ollama":
            return self._ollama_complete(system, user)
        else:
            return self._stub_complete(system, user)
    
    def _stream_complete(self, system: str, user: str) -> Generator[str, None, None]:
        """Streaming completion."""
        response = self._complete(system, user)
        for word in response.split():
            yield word + " "
    
    def _anthropic_complete(self, system: str, user: str) -> str:
        """Anthropic API."""
        import httpx
        headers = {
            "x-api-key": self.config.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        data = {
            "model": self.config.model,
            "max_tokens": 4096,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }
        try:
            response = httpx.post(
                self.config.base_url,
                headers=headers,
                json=data,
                timeout=60,
            )
            response.raise_for_status()
            result = response.json()
            return result["content"][0]["text"]
        except Exception as e:
            return f"[Anthropic Error: {e}]"
    
    def _openai_complete(self, system: str, user: str) -> str:
        """OpenAI API."""
        import httpx
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "content-type": "application/json",
        }
        data = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        try:
            response = httpx.post(
                self.config.base_url,
                headers=headers,
                json=data,
                timeout=60,
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[OpenAI Error: {e}]"
    
    def _deepseek_complete(self, system: str, user: str) -> str:
        """DeepSeek API."""
        return self._openai_complete(system, user)  # Same format
    
    def _ollama_complete(self, system: str, user: str) -> str:
        """Ollama local API."""
        import httpx
        data = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "stream": False,
        }
        try:
            response = httpx.post(
                "http://localhost:11434/api/chat",
                json=data,
                timeout=60,
            )
            response.raise_for_status()
            result = response.json()
            return result["message"]["content"]
        except Exception as e:
            return f"[Ollama Error: {e}]"
    
    def _stub_complete(self, system: str, user: str) -> str:
        """Stub response when no LLM available."""
        return f"""[Stub AI Response]

Based on my analysis of your request:

**System Prompt Context:**
{system[:200]}...

**Your Request:**
{user}

**Response:**
I'm ready to help with this request. To enable real AI responses, please set one of:
- ANTHROPIC_API_KEY (Anthropic Claude)
- OPENAI_API_KEY (OpenAI GPT)
- DEEPSEEK_API_KEY (DeepSeek)
- Or run: `ollama serve` (local, free)

The AI Software Factory is configured and ready - just needs an API key to enable full AI capabilities.
"""


# Global client
llm_client = LLMClient()


def get_client() -> LLMClient:
    """Get the global LLM client."""
    return llm_client


__all__ = ["LLMClient", "LLMConfig", "llm_client", "get_client"]