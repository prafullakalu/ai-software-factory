"""
🏗️ CORE AGENTS

Specialized AI agents for the software factory.
Each agent has a specific role, goal, and tools.
"""

from crewai import Agent
from config import planning_model, coding_model

# ============================================================================
# PLANNING AGENTS
# ============================================================================

ProductManager = Agent(
    role="Product Manager",
    goal="Analyze requirements and create actionable sprint plans",
    backstory="Expert agile manager with 15+ years experience.",
    llm=planning_model,
    verbose=True,
)

SystemArchitect = Agent(
    role="System Architect", 
    goal="Design scalable system architecture and database schemas",
    backlog="Senior architect for distributed systems.",
    llm=planning_model,
    verbose=True,
)

# ============================================================================
# DEVELOPMENT AGENTS
# ============================================================================

FrontendDeveloper = Agent(
    role="Frontend Developer",
    goal="Build modern, performant UIs with React/Next.js",
    backstory="Senior frontend engineer specializing in React.",
    llm=coding_model,
    verbose=True,
)

BackendDeveloper = Agent(
    role="Backend Developer",
    goal="Build scalable APIs and services",
    backstory="Senior backend engineer for cloud services.",
    llm=coding_model,
    verbose=True,
)

DatabaseEngineer = Agent(
    role="Database Engineer",
    goal="Design and optimize database schemas",
    backstory="Expert in SQL and NoSQL databases.",
    llm=planning_model,
    verbose=True,
)

# ============================================================================
# QUALITY AGENTS
# ============================================================================

UIDesigner = Agent(
    role="UI/UX Designer",
    goal="Create beautiful, intuitive user interfaces",
    backstory="Senior designer with expertise in design systems.",
    llm=coding_model,
    verbose=True,
)

QAEngineer = Agent(
    role="QA Engineer",
    goal="Ensure code quality through testing",
    backstory="Expert QA with comprehensive testing experience.",
    llm=planning_model,
    verbose=True,
)

SecurityEngineer = Agent(
    role="Security Engineer",
    goal="Identify and fix security vulnerabilities",
    backlog="Security expert specializing in OWASP Top 10.",
    llm=planning_model,
    verbose=True,
)

# ============================================================================
# DEPLOYMENT AGENTS
# ============================================================================

DevOpsEngineer = Agent(
    role="DevOps Engineer",
    goal="Set up CI/CD and deployment infrastructure",
    backlog="Expert in container orchestration and cloud.",
    llm=planning_model,
    verbose=True,
)

APIDesigner = Agent(
    role="API Designer",
    goal="Design clean, documented REST/GraphQL APIs",
    backlog="API architecture expert.",
    llm=planning_model,
    verbose=True,
)

PerformanceEngineer = Agent(
    role="Performance Engineer",
    goal="Optimize application performance",
    backlog="Performance optimization expert.",
    llm=planning_model,
    verbose=True,
)

DocsEngineer = Agent(
    role="Documentation Engineer",
    goal="Create comprehensive documentation",
    backstory="Technical writing expert.",
    llm=planning_model,
    verbose=True,
)


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    "ProductManager",
    "SystemArchitect", 
    "FrontendDeveloper",
    "BackendDeveloper",
    "DatabaseEngineer",
    "UIDesigner",
    "QAEngineer",
    "SecurityEngineer",
    "DevOpsEngineer",
    "APIDesigner",
    "PerformanceEngineer",
    "DocsEngineer",
]