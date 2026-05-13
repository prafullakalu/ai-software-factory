"""
⚙️ CONFIGURATION

Project settings and environment configuration.
"""

import os
from pathlib import Path

# ============================================================================
# PATHS
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
WORKSPACE_ROOT = PROJECT_ROOT / "workspace"
SRC_ROOT = PROJECT_ROOT / "src"
INFRA_ROOT = PROJECT_ROOT / "infrastructure"
TESTS_ROOT = PROJECT_ROOT / "tests"

# ============================================================================
# ENVIRONMENT
# ============================================================================

class Env:
    """Environment configuration."""
    
    # Development
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    DEV_MODE = os.getenv("DEV_MODE", "true").lower() == "true"
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost:5432/ai_factory")
    
    # LLM Providers
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Deployment
    DEPLOY_TARGET = os.getenv("DEPLOY_TARGET", "vercel")
    VERCEL_TOKEN = os.getenv("VERCEL_TOKEN", "")
    DOCKER_REGISTRY = os.getenv("DOCKER_REGISTRY", "")


env = Env()


# ============================================================================
# PROJECT CONFIG
# ============================================================================

class ProjectConfig:
    """Project configuration."""
    
    name = "ai-software-factory"
    version = "2.0.0"
    description = "AI-powered multi-agent software factory"
    
    # Tech stack defaults
    frontend_stack = ["react", "nextjs", "typescript", "tailwind"]
    backend_stack = ["fastapi", "python", "postgresql"]
    
    # Features
    features = {
        "auth": True,
        "api": True,
        "database": True,
        "testing": True,
        "deployment": True,
    }


config = ProjectConfig()


__all__ = ["env", "config", "PROJECT_ROOT", "WORKSPACE_ROOT"]