"""
🏗️ REAL AI AGENTS

Real AI agents that generate code using LLM!
Each agent has a specific role and generates actual code.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from core.llm import chat, generate, LLMConfig, create_llm


# ============================================================================
# AGENT TYPES
# ============================================================================

@dataclass
class Agent:
    """AI Agent definition."""
    name: str
    role: str
    goal: str
    instructions: str
    tools: List[str]
    model: str = "llama3"


# ============================================================================
# BUILT-IN AGENTS
# ============================================================================

AGENTS = {
    "pm": Agent(
        name="Product Manager",
        role="Product Manager",
        goal="Analyze requirements and create project plans",
        instructions="You are an expert product manager. Analyze the user's requirements and create a detailed project specification including features, timeline, and deliverables.",
        tools=["research", "planning"],
    ),
    
    "architect": Agent(
        name="System Architect",
        role="System Architect", 
        goal="Design system architecture",
        instructions="Design a scalable, maintainable system architecture. Include diagrams, technology stack, and data models.",
        tools=["design", "architecture"],
    ),
    
    "frontend": Agent(
        name="Frontend Developer",
        role="Frontend Developer",
        goal="Build user interfaces",
        instructions="Generate clean, modern frontend code using React, Next.js, TypeScript, and Tailwind CSS. Create responsive components.",
        tools=["react", "typescript", "tailwind"],
    ),
    
    "backend": Agent(
        name="Backend Developer", 
        role="Backend Developer",
        goal="Build APIs and services",
        instructions="Generate robust backend code using FastAPI, Express, or Django. Include authentication, APIs, and database models.",
        tools=["fastapi", "postgresql", "redis"],
    ),
    
    "designer": Agent(
        name="UI/UX Designer",
        role="Designer",
        goal="Create beautiful interfaces",
        instructions="Design beautiful, user-friendly interfaces with modern aesthetics. Use design systems and best practices.",
        tools=["design", "css", "animation"],
    ),
    
    "qa": Agent(
        name="QA Engineer",
        role="QA Engineer",
        goal="Ensure quality",
        instructions="Write comprehensive tests and ensure code quality. Include unit tests, integration tests, and E2E tests.",
        tools=["pytest", "playwright"],
    ),
    
    "devops": Agent(
        name="DevOps Engineer",
        role="DevOps",
        goal="Setup deployment",
        instructions="Configure Docker, Kubernetes, CI/CD pipelines, and cloud deployment.",
        tools=["docker", "github-actions", "k8s"],
    ),
    
    "security": Agent(
        name="Security Engineer",
        role="Security",
        goal="Secure the application",
        instructions="Audit code for security vulnerabilities. Implement authentication, encryption, and security best practices.",
        tools=["owasp", "encryption"],
    ),
}


# ============================================================================
# AGENT EXECUTION
# ============================================================================

class AIAgent:
    """Real AI Agent that generates code."""
    
    def __init__(self, agent_type: str = None, llm_config: LLMConfig = None):
        self.agent_type = agent_type or "frontend"
        self.agent = AGENTS.get(agent_type) if agent_type else AGENTS["frontend"]
        self.llm = create_llm(llm_config)
        self.history: List[Dict] = []
    
    def run(self, task: str) -> str:
        """Run agent on task."""
        prompt = f"""You are {self.agent.name}.
{self.agent.instructions}

Task: {task}

Generate the code for this task. Output only the code, no explanations.
Use best practices and modern frameworks.
"""
        result = generate(prompt)
        
        self.history.append({
            "task": task,
            "result": result,
        })
        
        return result
    
    def chat(self, message: str, system: str = None) -> str:
        """Chat with agent."""
        messages = [
            {"role": "system", "content": f"{self.agent.name}: {self.agent.instructions}"},
            {"role": "user", "content": message},
        ]
        
        result = self.llm.chat(messages)
        
        self.history.append({
            "message": message,
            "response": result,
        })
        
        return result


# ============================================================================
# FACTORY
# ============================================================================

def get_agent(agent_type: str) -> Agent:
    """Get agent by type."""
    return AGENTS.get(agent_type, AGENTS["frontend"])


def run_agent(agent_type: str, task: str) -> str:
    """Run agent on task."""
    agent = AIAgent(agent_type)
    return agent.run(task)


def list_agents() -> List[Dict]:
    """List all agents."""
    return [
        {
            "type": k,
            "name": v.name,
            "goal": v.goal,
            "tools": v.tools,
        }
        for k, v in AGENTS.items()
    ]


__all__ = [
    "Agent",
    "AGENTS",
    "AIAgent",
    "get_agent",
    "run_agent",
    "list_agents",
]