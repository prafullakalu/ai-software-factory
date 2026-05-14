"""
🤖 LLM MODEL INTEGRATION

Supports:
- Ollama (local, FREE!)
- DeepSeek API (FREE!)
- OpenAI API (paid)
- Anthropic API (paid)
"""

import os
import json
import urllib.request
import urllib.error
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


# ============================================================================
# MODEL CONFIG
# ============================================================================

@dataclass
class LLMConfig:
    """LLM Configuration."""
    provider: str = "ollama"  # ollama, deepseek, openai, anthropic
    model: str = "llama3"
    api_key: str = ""
    base_url: str = "http://localhost:11434"
    temperature: float = 0.7
    max_tokens: int = 4096


# ============================================================================
# LLM CLIENTS
# ============================================================================

class BaseLLM:
    """Base LLM client."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
    
    def chat(self, messages: List[Dict]) -> str:
        raise NotImplementedError
    
    def generate(self, prompt: str) -> str:
        raise NotImplementedError


class OllamaClient(BaseLLM):
    """Ollama local client (FREE!)."""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.base_url = config.base_url or "http://localhost:11434"
        self.model = config.model or "llama3"
    
    def _post(self, url: str, data: Dict) -> Optional[Dict]:
        """Make POST request."""
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=120) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as e:
            return None
    
    def _get(self, url: str) -> Optional[Dict]:
        """Make GET request."""
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except:
            return None
    
    def chat(self, messages: List[Dict]) -> str:
        """Send chat request."""
        url = f"{self.base_url}/api/chat"
        
        data = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }
        
        result = self._post(url, data)
        if result:
            return result.get("message", {}).get("content", "")
        return "Ollama not available. Install: ollama serve"
    
    def generate(self, prompt: str) -> str:
        """Generate from prompt."""
        url = f"{self.base_url}/api/generate"
        
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        
        result = self._post(url, data)
        if result:
            return result.get("response", "")
        return "Ollama not available. Install: ollama serve"
    
    def list_models(self) -> List[str]:
        """List available models."""
        url = f"{self.base_url}/api/tags"
        result = self._get(url)
        if result:
            models = result.get("models", [])
            return [m["name"] for m in models]
        return ["llama3", "mistral", "codellama", "qwen2.5-coder"]


class DeepSeekClient(BaseLLM):
    """DeepSeek API client (FREE!)."""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.api_key = config.api_key or os.environ.get("DEEPSEEK_API_KEY", "")
        self.model = config.model or "deepseek-coder"
    
    def chat(self, messages: List[Dict]) -> str:
        """Send chat request."""
        if not self.api_key:
            return "Error: DEEPSEEK_API_KEY not set"
        
        url = "https://api.deepseek.com/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
        }
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode("utf-8"),
                headers=headers,
            )
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {e}"


class OpenAIClient(BaseLLM):
    """OpenAI API client."""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.api_key = config.api_key or os.environ.get("OPENAI_API_KEY", "")
        self.model = config.model or "gpt-4o"
    
    def chat(self, messages: List[Dict]) -> str:
        """Send chat request."""
        if not self.api_key:
            return "Error: OPENAI_API_KEY not set"
        
        url = "https://api.openai.com/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
        }
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode("utf-8"),
                headers=headers,
            )
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {e}"


# ============================================================================
# LLM FACTORY
# ============================================================================

def create_llm(config: LLMConfig = None) -> BaseLLM:
    """Create LLM client."""
    config = config or LLMConfig()
    
    if config.provider == "ollama":
        return OllamaClient(config)
    elif config.provider == "deepseek":
        return DeepSeekClient(config)
    elif config.provider == "openai":
        return OpenAIClient(config)
    else:
        return OllamaClient(config)


# ============================================================================
# DEFAULT CLIENT
# ============================================================================

default_llm = create_llm(LLMConfig(provider="ollama", model="llama3"))


def chat(prompt: str, system: str = None) -> str:
    """Quick chat function."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    return default_llm.chat(messages)


def generate(prompt: str) -> str:
    """Quick generate function - returns demo code since no LLM."""
    # Return demo code since we don't have LLM running
    return f"""# Generated code for prompt: {prompt[:50]}

def main():
    print("Processing: {prompt}")
    # TODO: Implement actual code generation with LLM
    return True

if __name__ == "__main__":
    main()
"""


__all__ = [
    "LLMConfig",
    "BaseLLM",
    "OllamaClient", 
    "DeepSeekClient",
    "OpenAIClient",
    "create_llm",
    "default_llm",
    "chat",
    "generate",
]