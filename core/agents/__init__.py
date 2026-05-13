"""
🏗️ CORE AGENTS

Specialized AI agents for the software factory.
Built without external dependencies - works standalone!
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# AGENT TYPES
# ============================================================================

class AgentRole(Enum):
    PRODUCT_MANAGER = "product_manager"
    ARCHITECT = "architect"
    DESIGNER = "designer"
    FRONTEND_DEV = "frontend_developer"
    BACKEND_DEV = "backend_developer"
    FULLSTACK_DEV = "fullstack_developer"
    DATABASE = "database_engineer"
    QA = "qa_engineer"
    SECURITY = "security_engineer"
    DEVOPS = "devops_engineer"
    WRITER = "technical_writer"
    RESEARCHER = "researcher"


# ============================================================================
# AGENT MODEL
# ============================================================================

@dataclass
class Agent:
    """Base agent definition."""
    name: str
    role: str
    goal: str
    backstory: str
    tools: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    llm: str = "openai"
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "role": self.role,
            "goal": self.goal,
            "backstory": self.backstory,
            "tools": self.tools,
            "skills": self.skills,
            "llm": self.llm,
        }


# ============================================================================
# BUILT-IN AGENTS
# ============================================================================

AGENTS = {
    "product_manager": Agent(
        name="Product Manager",
        role="Product Manager",
        goal="Analyze requirements and create actionable sprint plans",
        backstory="Expert agile product manager with 15+ years experience.",
        tools=["research", "analysis", "planning"],
        skills=["agile", "roadmapping", "requirements"],
    ),
    
    "architect": Agent(
        name="System Architect",
        role="System Architect",
        goal="Design scalable, maintainable system architecture",
        backstory="Expert software architect with deep knowledge of design patterns.",
        tools=["architecture", "design", "analysis"],
        skills=["system-design", "microservices", "api-design"],
    ),
    
    "designer": Agent(
        name="UI/UX Designer",
        role="Designer",
        goal="Create beautiful, user-friendly interfaces",
        backstory="Expert designer skilled in design systems.",
        tools=["design", "prototyping"],
        skills=["design-systems", "accessibility"],
    ),
    
    "frontend": Agent(
        name="Frontend Developer",
        role="Frontend Developer",
        goal="Build responsive, performant user interfaces",
        backstory="Expert in React, Next.js, Vue.",
        tools=["code", "testing", "debugging"],
        skills=["react", "nextjs", "typescript", "tailwind"],
    ),
    
    "backend": Agent(
        name="Backend Developer",
        role="Backend Developer",
        goal="Build robust, scalable APIs",
        backstory="Expert in FastAPI, Django, Express.",
        tools=["code", "database", "api"],
        skills=["fastapi", "postgresql", "redis"],
    ),
    
    "fullstack": Agent(
        name="Full Stack Developer",
        role="Full Stack Developer",
        goal="Build complete applications",
        backstory="Expert developer comfortable with both frontend and backend.",
        tools=["code", "testing", "deployment"],
        skills=["react", "fastapi", "postgresql"],
    ),
    
    "database": Agent(
        name="Database Engineer",
        role="Database Engineer",
        goal="Design efficient database schemas",
        backstory="Expert database administrator.",
        tools=["database", "migration"],
        skills=["sql", "postgresql", "mongodb"],
    ),
    
    "qa": Agent(
        name="QA Engineer",
        role="QA Engineer",
        goal="Ensure high quality through testing",
        backstory="Expert QA engineer.",
        tools=["testing", "automation"],
        skills=["pytest", "playwright"],
    ),
    
    "security": Agent(
        name="Security Engineer",
        role="Security Engineer",
        goal="Identify and fix vulnerabilities",
        backstory="Expert security researcher.",
        tools=["security", "audit"],
        skills=["owasp", "penetration-testing"],
    ),
    
    "devops": Agent(
        name="DevOps Engineer",
        role="DevOps Engineer",
        goal="Build CI/CD pipelines",
        backstory="Expert DevOps engineer.",
        tools=["deployment", "monitoring"],
        skills=["docker", "kubernetes", "github-actions"],
    ),
    
    "writer": Agent(
        name="Technical Writer",
        role="Technical Writer",
        goal="Create clear documentation",
        backstory="Expert technical writer.",
        tools=["documentation"],
        skills=["markdown", "api-docs"],
    ),
    
    "researcher": Agent(
        name="Researcher",
        role="Researcher",
        goal="Research topics",
        backstory="Expert researcher.",
        tools=["research", "web-search"],
        skills=["analysis"],
    ),
}


# ============================================================================
# AGENT FACTORY
# ============================================================================

class AgentFactory:
    """Factory for creating agents."""
    
    def __init__(self):
        self.custom_agents: Dict[str, Agent] = {}
    
    def get(self, name: str) -> Optional[Agent]:
        return AGENTS.get(name) or self.custom_agents.get(name)
    
    def create(self, name: str, role: str, goal: str, backstory: str, 
             tools: List[str] = None, skills: List[str] = None, llm: str = "openai") -> Agent:
        agent = Agent(name=name, role=role, goal=goal, backstory=backstory,
                   tools=tools or [], skills=skills or [], llm=llm)
        self.custom_agents[name] = agent
        return agent
    
    def list_all(self) -> List[Dict]:
        all_agents = list(AGENTS.values()) + list(self.custom_agents.values())
        return [a.to_dict() for a in all_agents]
    
    def search(self, query: str) -> List[Agent]:
        query = query.lower()
        return [a for a in AGENTS.values() 
                if query in a.role.lower() or query in a.goal.lower()]


# ============================================================================
# EXPORTS
# ============================================================================

agent_factory = AgentFactory()

def get_agent(name: str) -> Optional[Agent]:
    return agent_factory.get(name)

def list_agents() -> List[Dict]:
    return agent_factory.list_all()

def create_agent(name: str, role: str, goal: str, backstory: str, **kwargs) -> Agent:
    return agent_factory.create(name, role, goal, backstory, **kwargs)

__all__ = ["Agent", "AgentRole", "AgentFactory", "AGENTS", "agent_factory",
          "get_agent", "list_agents", "create_agent"]