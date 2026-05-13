"""
🎯 FREE AI MODELS GUIDE

A comprehensive guide to using completely FREE AI models!
No credit card required!
"""

# ============================================================================
# FREE MODELS BY PROVIDER
# ============================================================================

FREE_MODELS = {
    # =========================================================================
    # OLLAMA (Run locally - 100% FREE!)
    # =========================================================================
    "ollama": {
        "description": "Run AI models locally on your computer",
        "website": "https://ollama.ai",
        "install": "curl -fsSL https://ollama.ai/install.sh | sh",
        "models": {
            "llama3": {
                "name": "Llama 3",
                "strengths": "General purpose, reasoning",
                "cost": "FREE",
                "rating": "⭐⭐⭐⭐⭐",
            },
            "llama3:70b": {
                "name": "Llama 3 70B",
                "strengths": "Best reasoning, GPT-4 level",
                "cost": "FREE",
                "rating": "⭐⭐⭐⭐⭐",
            },
            "mixtral": {
                "name": "Mixtral",
                "strengths": "Coding, fast",
                "cost": "FREE",
                "rating": "⭐⭐⭐⭐⭐",
            },
            "qwen2.5-coder": {
                "name": "Qwen Coder",
                "strengths": "BEST for coding!",
                "cost": "FREE",
                "rating": "⭐⭐⭐⭐⭐",
            },
            "codellama": {
                "name": "Code Llama",
                "strengths": "Coding专用",
                "cost": "FREE",
                "rating": "⭐⭐⭐⭐",
            },
            "mistral": {
                "name": "Mistral",
                "strengths": "Fast, efficient",
                "cost": "FREE",
                "rating": "⭐⭐⭐⭐",
            },
            "phi3": {
                "name": "Phi-3",
                "strengths": "Lightweight, fast",
                "cost": "FREE",
                "rating": "⭐⭐⭐",
            },
            "gemma": {
                "name": "Gemma",
                "strengths": "Google's model",
                "cost": "FREE",
                "rating": "⭐⭐⭐⭐",
            },
        },
    },
    
    # =========================================================================
    # DEEPSEEK (Completely FREE!)
    # =========================================================================
    "deepseek": {
        "description": "Open source AI, completely free API",
        "website": "https://platform.deepseek.com",
        "api_key": "Get from https://platform.deepseek.com/",
        "models": {
            "deepseek-coder": {
                "name": "DeepSeek Coder",
                "strengths": "EXCELLENT for coding, matches GPT-4",
                "cost": "FREE",
                "rating": "⭐⭐⭐⭐⭐",
            },
            "deepseek-chat": {
                "name": "DeepSeek Chat",
                "strengths": "General chat, reasoning",
                "cost": "FREE",
                "rating": "⭐⭐⭐⭐",
            },
        },
    },
    
    # =========================================================================
    # HUGGINGFACE (100+ FREE MODELS!)
    # =========================================================================
    "huggingface": {
        "description": "Largest collection of free models",
        "website": "https://huggingface.co",
        "api_key": "Get from https://huggingface.co/settings/tokens",
        "models": {
            "codellama-70b": {
                "name": "CodeLlama 70B",
                "strengths": "Best open source coder",
                "cost": "FREE (via Inference API)",
                "rating": "⭐⭐⭐⭐⭐",
            },
            "mistral-7b": {
                "name": "Mistral 7B",
                "strengths": "Fast, efficient",
                "cost": "FREE",
                "rating": "⭐⭐⭐⭐",
            },
            "starcoder2-15b": {
                "name": "StarCoder2 15B",
                "strengths": "Great for code generation",
                "cost": "FREE",
                "rating": "⭐⭐⭐⭐",
            },
            "falcon-40b": {
                "name": "Falcon 40B",
                "strengths": "General purpose",
                "cost": "FREE",
                "rating": "⭐⭐⭐",
            },
        },
    },
    
    # =========================================================================
    # COHERE (Free Tier Available)
    # =========================================================================
    "cohere": {
        "description": "Enterprise AI with free tier",
        "website": "https://cohere.com",
        "api_key": "Get from https://dashboard.cohere.com/",
        "models": {
            "command-r": {
                "name": "Command R",
                "strengths": "Great for reasoning, 128K context",
                "cost": "FREE (free tier)",
                "rating": "⭐⭐⭐⭐⭐",
            },
            "command": {
                "name": "Command",
                "strengths": "Fast, lightweight",
                "cost": "FREE (free tier)",
                "rating": "⭐⭐⭐⭐",
            },
        },
    },
    
    # =========================================================================
    # GOOGLE (Gemini has free tier)
    # =========================================================================
    "google": {
        "description": "Google's AI models",
        "website": "https://aistudio.google.com",
        "api_key": "Get from https://aistudio.google.com/app/apikey",
        "models": {
            "gemini-1.5-flash": {
                "name": "Gemini 1.5 Flash",
                "strengths": "1M context window, FAST, multi-modal",
                "cost": "FREE (generous free tier)",
                "rating": "⭐⭐⭐⭐⭐",
            },
            "gemini-pro": {
                "name": "Gemini Pro",
                "strengths": "Great reasoning",
                "cost": "FREE (limited)",
                "rating": "⭐⭐⭐⭐",
            },
        },
    },
    
    # =========================================================================
    # MISTRAL (Free tier + Codestral)
    # =========================================================================
    "mistral": {
        "description": "European AI, excellent for coding",
        "website": "https://console.mistral.ai",
        "models": {
            "mistral-small": {
                "name": "Mistral Small",
                "strengths": "Fast, cheap",
                "cost": "FREE (first 14 days)",
                "rating": "⭐⭐⭐⭐",
            },
            "codestral": {
                "name": "Codestral",
                "strengths": "BEST for coding!",
                "cost": "FREE (beta)",
                "rating": "⭐⭐⭐⭐⭐",
            },
        },
    },
}


# ============================================================================
# QUICK START GUIDES
# ============================================================================

QUICK_STARTS = {
    "ollama": """
# 🚀 QUICK START: Ollama (Recommended!)

1. Install Ollama:
   curl -fsSL https://ollama.ai/install.sh | sh

2. Start Ollama:
   ollama serve

3. Pull a model:
   ollama pull llama3
   ollama pull qwen2.5-coder
   ollama pull mixtral

4. Use in your project:
   Set DEFAULT_LLM_PROVIDER=ollama in .env
   Set OLLAMA_URL=http://localhost:11434
""",
    
    "deepseek": """
# 🚀 QUICK START: DeepSeek (Best FREE for coding!)

1. Get API key:
   Visit https://platform.deepseek.com/
   Create account → API Keys → Create new key

2. Add to .env:
   DEEPSEEK_API_KEY=your-api-key-here

3. Use in project:
   Set DEFAULT_LLM_PROVIDER=deepseek
""",
    
    "huggingface": """
# 🚀 QUICK START: HuggingFace

1. Get API key:
   https://huggingface.co/settings/tokens

2. Add to .env:
   HF_TOKEN=your-token-here

3. Use with Inference API:
   https://api-inference.huggingface.co/
""",
    
    "cohere": """
# 🚀 QUICK START: Cohere

1. Get API key:
   https://dashboard.cohere.com/

2. Add to .env:
   COHERE_API_KEY=your-api-key

3. Use free tier commands!
""",
}


# ============================================================================
# RECOMMENDATIONS
# ============================================================================

RECOMMENDATIONS = {
    "best_for_coding": [
        "1. Ollama qwen2.5-coder (FREE, local)",
        "2. DeepSeek Coder (FREE, API)",
        "3. Mistral Codestral (FREE)",
        "4. Ollama codellama (FREE, local)",
    ],
    "best_for_reasoning": [
        "1. Ollama llama3:70b (FREE, local)",
        "2. DeepSeek Chat (FREE)",
        "3. Google Gemini 1.5 Flash (FREE tier)",
    ],
    "best_free_option": [
        "1. Ollama (100% free, runs locally)",
        "2. DeepSeek (Completely free API)",
        "3. HuggingFace Inference API (Free tier)",
    ],
    "fastest": [
        "1. Ollama phi3 (lightweight)",
        "2. Google Gemini 1.5 Flash",
        "3. Cohere Command",
    ],
}


def show_free_models():
    """Display all free models."""
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                    🎯 FREE AI MODELS GUIDE                              ║
║                 No Credit Card Required!                                ║
╠══════════════════════════════════════════════════════════════════════════╣
""")
    
    for provider, info in FREE_MODELS.items():
        print(f"\n║ 📦 {provider.upper()}")
        print(f"║    {info['description']}")
        print(f"║    🌐 {info['website']}")
        
        for model_id, model_info in info.get("models", {}).items():
            print(f"║      • {model_info['name']}: {model_info['strengths']}")
            print(f"║        Cost: {model_info['cost']} | {model_info['rating']}")
    
    print("\n" + "="*80)
    print("\n🏆 RECOMMENDATIONS:\n")
    
    print("Best for Coding:")
    for r in RECOMMENDATIONS["best_for_coding"]:
        print(f"  {r}")
    
    print("\nBest for Reasoning:")
    for r in RECOMMENDATIONS["best_for_reasoning"]:
        print(f"  {r}")
    
    print("\n" + "="*80)


__all__ = [
    "FREE_MODELS",
    "QUICK_STARTS",
    "RECOMMENDATIONS",
    "show_free_models",
]