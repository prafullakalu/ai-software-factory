"""
🤖 DYNAMIC AGENT GENERATOR

Creates AI agents on-the-fly based on requirements!
Features:
- Generate agents from requirements
- Custom agent capabilities
- Dynamic skill assignment
- Agent templates
"""

import os
import json
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# AGENT TYPES
# ============================================================================

class AgentCapability(Enum):
    # Coding
    FRONTEND = "frontend"
    BACKEND = "backend"
    FULLSTACK = "fullstack"
    MOBILE = "mobile"
    
    # Data
    DATA_ENGINEER = "data_engineer"
    ML_ENGINEER = "ml_engineer"
    ANALYST = "analyst"
    
    # Infrastructure
    DEVOPS = "devops"
    SECURITY = "security"
    CLOUD = "cloud"
    
    # Business
    PRODUCT = "product"
    DESIGN = "design"
    QA = "qa"
    
    # Special
    WRITER = "writer"
    RESEARCHER = "researcher"
    ANALYZER = "analyzer"


class AgentComplexity(Enum):
    SIMPLE = "simple"         #Single task
    STANDARD = "standard"     #Multi-task
    ADVANCED = "advanced"    #Complex reasoning
    EXPERT = "expert"      #Specialized


# ============================================================================
# AGENT MODEL
# ============================================================================

@dataclass
class AgentConfig:
    """Configuration for a dynamic agent."""
    name: str
    role: str
    
    # Capabilities
    capabilities: List[AgentCapability]
    
    # Behavior
    complexity: AgentComplexity = AgentComplexity.STANDARD
    max_iterations: int = 10
    temperature: float = 0.7
    
    # Skills
    skills: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    
    # Goals
    goals: List[str] = field(default_factory=list)
    instructions: List[str] = field(default_factory=list)
    
    # Memory
    memory_enabled: bool = True
    verbose: bool = True
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "role": self.role,
            "capabilities": [c.value for c in self.capabilities],
            "complexity": self.complexity.value,
            "max_iterations": self.max_iterations,
            "temperature": self.temperature,
            "skills": self.skills,
            "tools": self.tools,
            "goals": self.goals,
            "instructions": self.instructions,
            "memory_enabled": self.memory_enabled,
            "verbose": self.verbose,
        }


# ============================================================================
# AGENT TEMPLATES
# ============================================================================

AGENT_TEMPLATES = {
    # ========================================
    # CODING AGENTS
    # ========================================
    "frontend_dev": AgentConfig(
        name="Frontend Developer",
        role="Expert in React, Next.js, Vue, and modern frontend frameworks",
        capabilities=[AgentCapability.FRONTEND],
        complexity=AgentComplexity.STANDARD,
        skills=["react", "nextjs", "tailwind", "typescript", "shadcn"],
        tools=["file_editor", "terminal", "browser"],
        goals=[
            "Create responsive UI components",
            "Implement design systems",
            "Optimize performance",
            "Ensure accessibility",
        ],
        instructions=[
            "Use modern React patterns (hooks, context)",
            "Follow accessibility guidelines",
            "Implement responsive designs",
        ],
    ),
    
    "backend_dev": AgentConfig(
        name="Backend Developer",
        role="Expert in FastAPI, Django, Express, and server-side development",
        capabilities=[AgentCapability.BACKEND],
        complexity=AgentComplexity.STANDARD,
        skills=["fastapi", "django", "express", "postgresql", "redis"],
        tools=["database", "terminal", "api"],
        goals=[
            "Design REST APIs",
            "Implement authentication",
            "Optimize database queries",
            "Handle caching",
        ],
        instructions=[
            "Follow REST best practices",
            "Use parameterized queries",
            "Implement proper error handling",
        ],
    ),
    
    "fullstack_dev": AgentConfig(
        name="Full Stack Developer",
        role="Expert in both frontend and backend development",
        capabilities=[AgentCapability.FRONTEND, AgentCapability.BACKEND],
        complexity=AgentComplexity.ADVANCED,
        skills=["react", "fastapi", "postgresql", "docker"],
        tools=["file_editor", "database", "terminal", "deployment"],
        goals=[
            "Build complete applications",
            "Connect frontend to backend",
            "Deploy to production",
        ],
    ),
    
    "mobile_dev": AgentConfig(
        name="Mobile Developer",
        role="Expert in React Native, Flutter, and mobile development",
        capabilities=[AgentCapability.MOBILE],
        complexity=AgentComplexity.ADVANCED,
        skills=["react-native", "flutter", "expo", "mobile-ui"],
        tools=["file_editor", "mobile-emulator"],
        goals=[
            "Create mobile apps",
            "Implement native features",
            "Build for iOS and Android",
        ],
    ),
    
    # ========================================
    # DATA AGENTS
    # ========================================
    "data_engineer": AgentConfig(
        name="Data Engineer",
        role="Expert in data pipelines, ETL, and data processing",
        capabilities=[AgentCapability.DATA_ENGINEER],
        complexity=AgentComplexity.ADVANCED,
        skills=["sql", "pandas", "spark", "airflow", "dbt"],
        tools=["database", "data-pipeline"],
        goals=[
            "Build data pipelines",
            "Design data models",
            "Optimize ETL processes",
        ],
    ),
    
    "ml_engineer": AgentConfig(
        name="ML Engineer",
        role="Expert in machine learning and AI models",
        capabilities=[AgentCapability.ML_ENGINEER],
        complexity=AgentComplexity.EXPERT,
        skills=["pytorch", "tensorflow", "scikit-learn", "mlops"],
        tools=["ml-training", "model-serving"],
        goals=[
            "Train ML models",
            "Optimize hyperparameters",
            "Deploy models",
        ],
    ),
    
    # ========================================
    # INFRASTRUCTURE AGENTS
    # ========================================
    "devops": AgentConfig(
        name="DevOps Engineer",
        role="Expert in deployment, Docker, Kubernetes, and CI/CD",
        capabilities=[AgentCapability.DEVOPS],
        complexity=AgentComplexity.STANDARD,
        skills=["docker", "kubernetes", "terraform", "github-actions"],
        tools=["docker", "k8s", "ci-cd"],
        goals=[
            "Set up CI/CD pipelines",
            "Containerize applications",
            "Deploy to Kubernetes",
        ],
    ),
    
    "security_eng": AgentConfig(
        name="Security Engineer",
        role="Expert in security auditing and vulnerability scanning",
        capabilities=[AgentCapability.SECURITY],
        complexity=AgentComplexity.ADVANCED,
        skills=["owasp", "penetration-testing", "encryption"],
        tools=["security-scanner", "vulnerability-scan"],
        goals=[
            "Find security vulnerabilities",
            "Fix security issues",
            "Implement security best practices",
        ],
    ),
    
    "cloud_architect": AgentConfig(
        name="Cloud Architect",
        role="Expert in AWS, GCP, Azure cloud infrastructure",
        capabilities=[AgentCapability.CLOUD],
        complexity=AgentComplexity.EXPERT,
        skills=["aws", "gcp", "azure", "serverless"],
        tools=["cloud-deployment", "infrastructure"],
        goals=[
            "Design cloud architecture",
            "Set up auto-scaling",
            "Optimize costs",
        ],
    ),
    
    # ========================================
    # BUSINESS AGENTS
    # ========================================
    "product_manager": AgentConfig(
        name="Product Manager",
        role="Expert in product planning and requirements",
        capabilities=[AgentCapability.PRODUCT],
        complexity=AgentComplexity.ADVANCED,
        skills=["product-management", "agile", "roadmapping"],
        tools=["research", "analysis"],
        goals=[
            "Define product requirements",
            "Create roadmaps",
            "Prioritize features",
        ],
    ),
    
    "designer": AgentConfig(
        name="UI/UX Designer",
        role="Expert in user interface and experience design",
        capabilities=[AgentCapability.DESIGN],
        complexity=AgentComplexity.STANDARD,
        skills=["figma", "design-systems", "prototyping"],
        tools=["design", "prototyping"],
        goals=[
            "Create design systems",
            "Design user interfaces",
            "Improve user experience",
        ],
    ),
    
    "qa_engineer": AgentConfig(
        name="QA Engineer",
        role="Expert in testing and quality assurance",
        capabilities=[AgentCapability.QA],
        complexity=AgentComplexity.STANDARD,
        skills=["testing", "test-automation", "cypress", "playwright"],
        tools=["testing", "test-runner"],
        goals=[
            "Write tests",
            "Automate testing",
            "Ensure code quality",
        ],
    ),
    
    # ========================================
    # SPECIAL AGENTS
    # ========================================
    "writer": AgentConfig(
        name="Technical Writer",
        role="Expert in documentation and content creation",
        capabilities=[AgentCapability.WRITER],
        complexity=AgentComplexity.STANDARD,
        skills=["markdown", "api-docs", "technical-writing"],
        tools=["documentation"],
        goals=[
            "Write documentation",
            "Create API docs",
            "Maintain guides",
        ],
    ),
    
    "researcher": AgentConfig(
        name="Researcher",
        role="Expert in research and information gathering",
        capabilities=[AgentCapability.RESEARCHER],
        complexity=AgentComplexity.ADVANCED,
        skills=["research", "analysis", "web-scraping"],
        tools=["research", "web-search"],
        goals=[
            "Research topics",
            "Gather information",
            "Analyze findings",
        ],
    ),
    
    "code_reviewer": AgentConfig(
        name="Code Reviewer",
        role="Expert in code review and quality analysis",
        capabilities=[AgentCapability.ANALYZER],
        complexity=AgentComplexity.STANDARD,
        skills=["code-review", "best-practices", "security"],
        tools=["code-analysis"],
        goals=[
            "Review code quality",
            "Find bugs",
            "Suggest improvements",
        ],
    ),
}


# ============================================================================
# SKILL REGISTRY
# ============================================================================

class SkillRegistry:
    """Registry of available skills."""
    
    def __init__(self):
        self.skills: Dict[str, Dict] = {}
        self._register_default_skills()
    
    def _register_default_skills(self):
        """Register default skills."""
        self.skills = {
            # Coding Skills
            "react": {
                "name": "React",
                "description": "React.js development",
                "tools": ["jsx", "tsx", "hooks"],
            },
            "nextjs": {
                "name": "Next.js",
                "description": "Next.js framework",
                "tools": ["api-routes", "ssr"],
            },
            "typescript": {
                "name": "TypeScript",
                "description": "Type-safe JavaScript",
                "tools": ["type-checking"],
            },
            "tailwind": {
                "name": "Tailwind CSS",
                "description": "Utility-first CSS",
                "tools": ["classes"],
            },
            "fastapi": {
                "name": "FastAPI",
                "description": "Python web framework",
                "tools": ["openapi", "pydantic"],
            },
            
            # Database Skills
            "postgresql": {
                "name": "PostgreSQL",
                "description": "Relational database",
                "tools": ["sql", "migrations"],
            },
            "mongodb": {
                "name": "MongoDB",
                "description": "NoSQL database",
                "tools": ["aggregation"],
            },
            "redis": {
                "name": "Redis",
                "description": "In-memory cache",
                "tools": ["caching"],
            },
            
            # DevOps Skills
            "docker": {
                "name": "Docker",
                "description": "Containerization",
                "tools": ["containers", "dockerfile"],
            },
            "kubernetes": {
                "name": "Kubernetes",
                "description": "Container orchestration",
                "tools": ["k8s", "helm"],
            },
            "github-actions": {
                "name": "GitHub Actions",
                "description": "CI/CD pipelines",
                "tools": ["workflows"],
            },
            
            # ML/AI Skills
            "pytorch": {
                "name": "PyTorch",
                "description": "Deep learning",
                "tools": ["tensors", "models"],
            },
            "tensorflow": {
                "name": "TensorFlow",
                "description": "ML framework",
                "tools": ["keras", "serving"],
            },
            
            # Testing Skills
            "pytest": {
                "name": "pytest",
                "description": "Python testing",
                "tools": ["fixtures"],
            },
            "playwright": {
                "name": "Playwright",
                "description": "E2E testing",
                "tools": ["browser-automation"],
            },
            
            # Cloud Skills
            "aws": {
                "name": "AWS",
                "description": "Amazon Web Services",
                "tools": ["ec2", "s3", "lambda"],
            },
            "gcp": {
                "name": "Google Cloud",
                "description": "Google Cloud Platform",
                "tools": ["gke", "cloud-functions"],
            },
            "vercel": {
                "name": "Vercel",
                "description": "Serverless deployment",
                "tools": ["edge-functions"],
            },
        }
    
    def register(self, skill_id: str, skill_info: Dict):
        """Register a new skill."""
        self.skills[skill_id] = skill_info
    
    def get(self, skill_id: str) -> Optional[Dict]:
        """Get skill info."""
        return self.skills.get(skill_id)
    
    def list_all(self) -> Dict[str, Dict]:
        """List all skills."""
        return self.skills
    
    def search(self, query: str) -> List[Dict]:
        """Search skills."""
        query = query.lower()
        results = []
        for skill_id, info in self.skills.items():
            if query in skill_id or query in info.get("description", "").lower():
                results.append({"id": skill_id, **info})
        return results


# ============================================================================
# DYNAMIC AGENT GENERATOR
# ============================================================================

class DynamicAgentGenerator:
    """Generate agents based on requirements."""
    
    def __init__(self):
        self.templates = AGENT_TEMPLATES
        self.skills = SkillRegistry()
        self.custom_agents: Dict[str, AgentConfig] = {}
    
    def from_template(self, template_name: str) -> Optional[AgentConfig]:
        """Create agent from template."""
        return self.templates.get(template_name)
    
    def from_requirement(self, requirement: str) -> List[AgentConfig]:
        """Generate agents from requirement description."""
        requirement = requirement.lower()
        agents = []
        
        # Detect needed capabilities
        if any(word in requirement for word in ["frontend", "ui", "interface", "react", "vue", "web"]):
            agents.append(self.templates["frontend_dev"])
        
        if any(word in requirement for word in ["backend", "api", "server", "fastapi", "database"]):
            agents.append(self.templates["backend_dev"])
        
        if any(word in requirement for word in ["full stack", "complete", "end-to-end"]):
            agents.append(self.templates["fullstack_dev"])
        
        if any(word in requirement for word in ["mobile", "ios", "android", "react native"]):
            agents.append(self.templates["mobile_dev"])
        
        if any(word in requirement for word in ["data", "pipeline", "etl", "warehouse"]):
            agents.append(self.templates["data_engineer"])
        
        if any(word in requirement for word in ["ml", "machine learning", "ai", "model", "training"]):
            agents.append(self.templates["ml_engineer"])
        
        if any(word in requirement for word in ["deploy", "docker", "kubernetes", "devops"]):
            agents.append(self.templates["devops"])
        
        if any(word in requirement for word in ["security", "vulnerability", "audit"]):
            agents.append(self.templates["security_eng"])
        
        if any(word in requirement for word in ["cloud", "aws", "gcp", "azure"]):
            agents.append(self.templates["cloud_architect"])
        
        if any(word in requirement for word in ["product", "requirement", "planning"]):
            agents.append(self.templates["product_manager"])
        
        if any(word in requirement for word in ["design", "ui", "ux", "figma"]):
            agents.append(self.templates["designer"])
        
        if any(word in requirement for word in ["test", "qa", "quality"]):
            agents.append(self.templates["qa_engineer"])
        
        if any(word in requirement for word in ["document", "write", "docs"]):
            agents.append(self.templates["writer"])
        
        if any(word in requirement for word in ["research", "investigate"]):
            agents.append(self.templates["researcher"])
        
        if any(word in requirement for word in ["review", "analyze", "audit code"]):
            agents.append(self.templates["code_reviewer"])
        
        # Default: at least one agent
        if not agents:
            agents.append(self.templates["fullstack_dev"])
        
        return agents
    
    def create_custom(
        self,
        name: str,
        role: str,
        capabilities: List[str],
        skills: List[str] = None,
        goals: List[str] = None,
    ) -> AgentConfig:
        """Create custom agent."""
        # Convert string capabilities to enums
        cap_enums = []
        for cap in capabilities:
            try:
                cap_enums.append(AgentCapability(cap))
            except:
                pass
        
        agent = AgentConfig(
            name=name,
            role=role,
            capabilities=cap_enums,
            skills=skills or [],
            goals=goals or [],
        )
        
        self.custom_agents[name] = agent
        return agent
    
    def add_skill(self, skill_id: str, skill_info: Dict):
        """Add new skill."""
        self.skills.register(skill_id, skill_info)
    
    def list_templates(self) -> List[Dict]:
        """List all templates."""
        return [
            {"id": k, **v.to_dict()}
            for k, v in self.templates.items()
        ]
    
    def search_templates(self, query: str) -> List[str]:
        """Search templates."""
        query = query.lower()
        results = []
        for template_id, config in self.templates.items():
            if (query in config.name.lower() or
                query in config.role.lower() or
                any(query in s for s in config.skills)):
                results.append(template_id)
        return results


# ============================================================================
# AGENT FACTORY
# ============================================================================

class AgentFactory:
    """Factory for creating and managing agents."""
    
    def __init__(self):
        self.generator = DynamicAgentGenerator()
        self.active_agents: Dict[str, AgentConfig] = {}
    
    def create_for_project(self, requirements: str) -> List[AgentConfig]:
        """Create agents for project requirements."""
        agents = self.generator.from_requirement(requirements)
        
        # Store as active
        for agent in agents:
            self.active_agents[agent.name] = agent
        
        return agents
    
    def create_from_template(self, template_name: str) -> Optional[AgentConfig]:
        """Create agent from known template."""
        agent = self.generator.from_template(template_name)
        if agent:
            self.active_agents[agent.name] = agent
        return agent
    
    def get_agent(self, name: str) -> Optional[AgentConfig]:
        """Get active agent."""
        return self.active_agents.get(name)
    
    def list_agents(self) -> List[Dict]:
        """List all active agents."""
        return [a.to_dict() for a in self.active_agents.values()]
    
    def remove_agent(self, name: str) -> bool:
        """Remove agent."""
        if name in self.active_agents:
            del self.active_agents[name]
            return True
        return False


# ============================================================================
# EXPORTS
# ============================================================================

# Global instances
agent_generator = DynamicAgentGenerator()
agent_factory = AgentFactory()
skill_registry = SkillRegistry()


# Factory functions
def create_agents_from_requirement(requirements: str) -> List[AgentConfig]:
    """Create agents based on requirement string."""
    return agent_generator.from_requirement(requirements)


def create_agent_from_template(template: str) -> Optional[AgentConfig]:
    """Create agent from template."""
    return agent_generator.from_template(template)


def create_custom_agent(
    name: str,
    role: str,
    capabilities: List[str],
    **kwargs,
) -> AgentConfig:
    """Create custom agent."""
    return agent_generator.create_custom(name, role, capabilities, **kwargs)


def register_skill(skill_id: str, skill_info: Dict):
    """Register new skill."""
    agent_generator.add_skill(skill_id, skill_info)


def list_all_templates() -> List[Dict]:
    """List all agent templates."""
    return agent_generator.list_templates()


__all__ = [
    "AgentConfig",
    "AgentCapability",
    "AgentComplexity",
    "DynamicAgentGenerator",
    "AgentFactory",
    "SkillRegistry",
    "agent_generator",
    "agent_factory",
    "skill_registry",
    "create_agents_from_requirement",
    "create_agent_from_template",
    "create_custom_agent",
    "register_skill",
    "list_all_templates",
    "AGENT_TEMPLATES",
]