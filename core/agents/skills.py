"""
🛠️ DYNAMIC SKILLS SYSTEM

Add new skills to agents dynamically!
Features:
- Skill registry
- Skill categories
- Tool integration
- Agent skill assignment
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# SKILL CATEGORIES
# ============================================================================

class SkillCategory(Enum):
    # Coding
    FRONTEND = "frontend"
    BACKEND = "backend"
    MOBILE = "mobile"
    DATABASE = "database"
    
    # DevOps
    DEVOPS = "devops"
    CLOUD = "cloud"
    SECURITY = "security"
    
    # Data/ML
    DATA = "data"
    ML = "ml"
    ANALYTICS = "analytics"
    
    # Design
    DESIGN = "design"
    UX = "ux"
    
    # Business
    PRODUCT = "product"
    MARKETING = "marketing"
    
    # General
    TOOLS = "tools"
    COMMUNICATION = "communication"


class SkillLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


# ============================================================================
# SKILL MODEL
# ============================================================================

@dataclass
class Skill:
    """Individual skill definition."""
    id: str
    name: str
    description: str
    category: SkillCategory
    
    # Technical details
    level: SkillLevel = SkillLevel.INTERMEDIATE
    tools: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    
    # Implementation
    functions: List[str] = field(default_factory=list)
    code_patterns: List[str] = field(default_factory=list)
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "level": self.level.value,
            "tools": self.tools,
            "prerequisites": self.prerequisites,
            "functions": self.functions,
            "tags": self.tags,
        }


@dataclass
class SkillSet:
    """Collection of skills for an agent."""
    agent_name: str
    skills: List[Skill] = field(default_factory=list)
    
    def add(self, skill: Skill):
        self.skills.append(skill)
    
    def has(self, skill_id: str) -> bool:
        return any(s.id == skill_id for s in self.skills)
    
    def get(self, skill_id: str) -> Optional[Skill]:
        for s in self.skills:
            if s.id == skill_id:
                return s
        return None
    
    def by_category(self, category: SkillCategory) -> List[Skill]:
        return [s for s in self.skills if s.category == category]


# ============================================================================
# COMPREHENSIVE SKILL REGISTRY
# ============================================================================

class SkillManager:
    """Manage all available skills."""
    
    def __init__(self):
        self.skills: Dict[str, Skill] = {}
        self.skill_sets: Dict[str, SkillSet] = {}
        self._register_all_skills()
    
    def _register_all_skills(self):
        """Register all skills."""
        
        # ======================
        # FRONTEND SKILLS
        # ======================
        self.register(Skill(
            id="react",
            name="React",
            description="React.js library for building UIs",
            category=SkillCategory.FRONTEND,
            tools=["jsx", "tsx", "react-dom"],
            functions=["useState", "useEffect", "useContext"],
            examples=["function Counter() {...}"],
        ))
        
        self.register(Skill(
            id="nextjs",
            name="Next.js",
            description="React framework with SSR/SSG",
            category=SkillCategory.FRONTEND,
            level=SkillLevel.ADVANCED,
            tools=["next", "api-routes"],
            prerequisites=["react"],
            functions=["getServerSideProps", "getStaticProps"],
            examples=["export async function getServerSideProps() {...}"],
        ))
        
        self.register(Skill(
            id="vue",
            name="Vue.js",
            description="Progressive JavaScript framework",
            category=SkillCategory.FRONTEND,
            tools=["vue3", "composition-api"],
            functions=["ref", "reactive", "computed"],
        ))
        
        self.register(Skill(
            id="tailwind",
            name="Tailwind CSS",
            description="Utility-first CSS framework",
            category=SkillCategory.FRONTEND,
            tools=["postcss"],
            tags=["css", "styling"],
        ))
        
        self.register(Skill(
            id="shadcn",
            name="shadcn/ui",
            description="Component library built on Radix UI",
            category=SkillCategory.FRONTEND,
            tools=["radix-ui", "clsx"],
            prerequisites=["react", "tailwind"],
            tags=["components", "ui"],
        ))
        
        self.register(Skill(
            id="typescript",
            name="TypeScript",
            description="Typed JavaScript",
            category=SkillCategory.FRONTEND,
            level=SkillLevel.INTERMEDIATE,
            tools=["tsc"],
            tags=["types", "type-checking"],
        ))
        
        self.register(Skill(
            id="astro",
            name="Astro",
            description="Static site builder",
            category=SkillCategory.FRONTEND,
            tools=["astro-components"],
        ))
        
        self.register(Skill(
            id="react-native",
            name="React Native",
            description="Cross-platform mobile framework",
            category=SkillCategory.MOBILE,
            level=SkillLevel.ADVANCED,
            tools=["expo", "react-native"],
            prerequisites=["react"],
        ))
        
        self.register(Skill(
            id="flutter",
            name="Flutter",
            description="Google's mobile SDK",
            category=SkillCategory.MOBILE,
            level=SkillLevel.ADVANCED,
            tools=["dart", "widgets"],
        ))
        
        # ======================
        # BACKEND SKILLS
        # ======================
        self.register(Skill(
            id="fastapi",
            name="FastAPI",
            description="Modern Python web framework",
            category=SkillCategory.BACKEND,
            tools=["pydantic", "uvicorn"],
            functions=["APIRouter", "Depends"],
            tags=["api", "rest"],
        ))
        
        self.register(Skill(
            id="django",
            name="Django",
            description="Python web framework",
            category=SkillCategory.BACKEND,
            level=SkillLevel.ADVANCED,
            tools=["orm", "admin"],
            functions=["views", "models", "urls"],
            tags=["mvc", "rest"],
        ))
        
        self.register(Skill(
            id="express",
            name="Express",
            description="Node.js web framework",
            category=SkillCategory.BACKEND,
            tools=["nodejs"],
            functions=["router", "middleware"],
            tags=["api", "rest"],
        ))
        
        self.register(Skill(
            id="nestjs",
            name="NestJS",
            description="Scalable Node.js framework",
            category=SkillCategory.BACKEND,
            level=SkillLevel.ADVANCED,
            tools=["typescript", "injection"],
            functions=["Controller", "Service"],
            tags=["enterprise", "api"],
        ))
        
        self.register(Skill(
            id="graphql",
            name="GraphQL",
            description="Query language for APIs",
            category=SkillCategory.BACKEND,
            level=SkillLevel.ADVANCED,
            tools=["apollo", "prisma"],
            functions=["typeDefs", "resolvers"],
        ))
        
        self.register(Skill(
            id="websockets",
            name="WebSockets",
            description="Real-time communication",
            category=SkillCategory.BACKEND,
            tools=["socket.io"],
            tags=["real-time"],
        ))
        
        # ======================
        # DATABASE SKILLS
        # ======================
        self.register(Skill(
            id="postgresql",
            name="PostgreSQL",
            description="Advanced relational database",
            category=SkillCategory.DATABASE,
            tools=["psycopg2", "sqlalchemy"],
            tags=["sql", "relational"],
        ))
        
        self.register(Skill(
            id="mongodb",
            name="MongoDB",
            description="NoSQL database",
            category=SkillCategory.DATABASE,
            tools=["pymongo"],
            tags=["nosql", "document"],
        ))
        
        self.register(Skill(
            id="redis",
            name="Redis",
            description="In-memory data store",
            category=SkillCategory.DATABASE,
            tools=["redis-py"],
            tags=["caching", "sessions"],
        ))
        
        self.register(Skill(
            id="prisma",
            name="Prisma",
            description="ORM for Node.js/TypeScript",
            category=SkillCategory.DATABASE,
            level=SkillLevel.INTERMEDIATE,
            tools=["prisma-client"],
            prerequisites=["postgresql"],
            tags=["orm", "type-safe"],
        ))
        
        self.register(Skill(
            id="sqlalchemy",
            name="SQLAlchemy",
            description="Python ORM",
            category=SkillCategory.DATABASE,
            tools=["orm"],
            tags=["sql", "python"],
        ))
        
        self.register(Skill(
            id="supabase",
            name="Supabase",
            description="Open source Firebase alternative",
            category=SkillCategory.DATABASE,
            tools=["postgresql", "realtime"],
            tags=["backend", "auth"],
        ))
        
        # ======================
        # DEVOPS SKILLS
        # ======================
        self.register(Skill(
            id="docker",
            name="Docker",
            description="Containerization platform",
            category=SkillCategory.DEVOPS,
            tools=["dockerfile", "docker-compose"],
            functions=["build", "run"],
            tags=["containers"],
        ))
        
        self.register(Skill(
            id="kubernetes",
            name="Kubernetes",
            description="Container orchestration",
            category=SkillCategory.DEVOPS,
            level=SkillLevel.EXPERT,
            tools=["kubectl", "helm"],
            prerequisites=["docker"],
            tags=["orchestration", "deploy"],
        ))
        
        self.register(Skill(
            id="github-actions",
            name="GitHub Actions",
            description="CI/CD platform",
            category=SkillCategory.DEVOPS,
            tools=["workflows", "actions"],
            tags=["ci-cd"],
        ))
        
        self.register(Skill(
            id="terraform",
            name="Terraform",
            description="Infrastructure as code",
            category=SkillCategory.DEVOPS,
            level=SkillLevel.ADVANCED,
            tools=["terraform"],
            tags=["iac", "cloud"],
        ))
        
        self.register(Skill(
            id="github-actions",
            name="GitHub Actions",
            description="CI/CD pipelines",
            category=SkillCategory.DEVOPS,
            tools=["yaml"],
        ))
        
        # ======================
        # CLOUD SKILLS
        # ======================
        self.register(Skill(
            id="aws",
            name="AWS",
            description="Amazon Web Services",
            category=SkillCategory.CLOUD,
            level=SkillLevel.ADVANCED,
            tools=["boto3", "cdk"],
            tags=["cloud", "serverless"],
        ))
        
        self.register(Skill(
            id="gcp",
            name="Google Cloud",
            description="Google Cloud Platform",
            category=SkillCategory.CLOUD,
            level=SkillLevel.ADVANCED,
            tools=["gcloud", "terraform"],
            tags=["cloud"],
        ))
        
        self.register(Skill(
            id="azure",
            name="Azure",
            description="Microsoft Azure",
            category=SkillCategory.CLOUD,
            level=SkillLevel.ADVANCED,
            tools=["az-cli"],
            tags=["cloud", "enterprise"],
        ))
        
        self.register(Skill(
            id="vercel",
            name="Vercel",
            description="Serverless deployment platform",
            category=SkillCategory.CLOUD,
            tools=["vercel-cli"],
            tags=["deploy", "serverless"],
        ))
        
        self.register(Skill(
            id="netlify",
            name="Netlify",
            description="Modern web hosting",
            category=SkillCategory.CLOUD,
            tools=["netlify-cli"],
            tags=["deploy", "jamstack"],
        ))
        
        # ======================
        # SECURITY SKILLS
        # ======================
        self.register(Skill(
            id="owasp",
            name="OWASP",
            description="Web security guidelines",
            category=SkillCategory.SECURITY,
            level=SkillLevel.ADVANCED,
            tags=["audit", "vulnerabilities"],
        ))
        
        self.register(Skill(
            id="jwt",
            name="JWT",
            description="JSON Web Tokens",
            category=SkillCategory.SECURITY,
            tools=["pyjwt", "jose"],
            tags=["auth", "tokens"],
        ))
        
        self.register(Skill(
            id="oauth",
            name="OAuth",
            description="Authorization framework",
            category=SkillCategory.SECURITY,
            tags=["auth", "social-login"],
        ))
        
        # ======================
        # DATA/ML SKILLS
        # ======================
        self.register(Skill(
            id="pandas",
            name="Pandas",
            description="Data analysis library",
            category=SkillCategory.DATA,
            tools=["dataframes"],
            functions=["read_csv", "merge", "groupby"],
            tags=["analysis"],
        ))
        
        self.register(Skill(
            id="spark",
            name="Apache Spark",
            description="Big data processing",
            category=SkillCategory.DATA,
            level=SkillLevel.EXPERT,
            tools=["pyspark"],
            tags=["big-data", "etl"],
        ))
        
        self.register(Skill(
            id="pytorch",
            name="PyTorch",
            description="Deep learning framework",
            category=SkillCategory.ML,
            level=SkillLevel.EXPERT,
            tools=["torch", "nn"],
            tags=["ai", "neural-networks"],
        ))
        
        self.register(Skill(
            id="tensorflow",
            name="TensorFlow",
            description="ML framework by Google",
            category=SkillCategory.ML,
            level=SkillLevel.EXPERT,
            tools=["keras", "tf-serving"],
            tags=["ai", "ml"],
        ))
        
        self.register(Skill(
            id="langchain",
            name="LangChain",
            description="LLM application framework",
            category=SkillCategory.ML,
            tools=["chains", "agents"],
            prerequisites=["openai"],
            tags=["llm", "ai"],
        ))
        
        # ======================
        # TESTING SKILLS
        # ======================
        self.register(Skill(
            id="pytest",
            name="pytest",
            description="Python testing framework",
            category=SkillCategory.TOOLS,
            tools=["pytest"],
            functions=["test", "fixture"],
            tags=["testing"],
        ))
        
        self.register(Skill(
            id="jest",
            name="Jest",
            description="JavaScript testing",
            category=SkillCategory.TOOLS,
            tools=["jest"],
            functions=["test", "describe"],
            tags=["testing", "javascript"],
        ))
        
        self.register(Skill(
            id="playwright",
            name="Playwright",
            description="E2E testing framework",
            category=SkillCategory.TOOLS,
            level=SkillLevel.INTERMEDIATE,
            tools=["playwright"],
            tags=["e2e", "browser"],
        ))
        
        self.register(Skill(
            id="cypress",
            name="Cypress",
            description="JavaScript E2E testing",
            category=SkillCategory.TOOLS,
            tools=["cypress"],
            tags=["e2e", "testing"],
        ))
        
        # ======================
        # ANALYTICS
        # ======================
        self.register(Skill(
            id="google-analytics",
            name="Google Analytics",
            description="Web analytics",
            category=SkillCategory.ANALYTICS,
            tools=["gtag"],
            tags=["analytics", "tracking"],
        ))
        
        self.register(Skill(
            id="mixpanel",
            name="Mixpanel",
            description="Product analytics",
            category=SkillCategory.ANALYTICS,
            tools=["mixpanel-sdk"],
            tags=["analytics", "events"],
        ))
        
        self.register(Skill(
            id="segment",
            name="Segment",
            description="Customer data platform",
            category=SkillCategory.ANALYTICS,
            tools=["analytics.js"],
            tags=["analytics", "cdp"],
        ))
        
        # ======================
        # PAYMENTS
        # ======================
        self.register(Skill(
            id="stripe",
            name="Stripe",
            description="Payment processing",
            category=SkillCategory.TOOLS,
            level=SkillLevel.ADVANCED,
            tools=["stripe-py", "elements"],
            tags=["payments", "billing"],
        ))
        
        self.register(Skill(
            id="paypal",
            name="PayPal",
            description="Payment platform",
            category=SkillCategory.TOOLS,
            tools=["paypal-sdk"],
            tags=["payments"],
        ))
    
    def register(self, skill: Skill):
        """Register a new skill."""
        self.skills[skill.id] = skill
    
    def get(self, skill_id: str) -> Optional[Skill]:
        """Get skill by ID."""
        return self.skills.get(skill_id)
    
    def list_all(self) -> Dict[str, Skill]:
        """List all skills."""
        return self.skills
    
    def by_category(self, category: SkillCategory) -> List[Skill]:
        """List skills by category."""
        return [s for s in self.skills.values() if s.category == category]
    
    def search(self, query: str) -> List[Skill]:
        """Search skills."""
        query = query.lower()
        results = []
        for skill in self.skills.values():
            if (query in skill.id or
                query in skill.name.lower() or
                query in skill.description.lower() or
                any(query in tag for tag in skill.tags)):
                results.append(skill)
        return results
    
    def create_skill_set(self, agent_name: str, skill_ids: List[str]) -> SkillSet:
        """Create a skill set for an agent."""
        skill_set = SkillSet(agent_name=agent_name)
        for skill_id in skill_ids:
            skill = self.get(skill_id)
            if skill:
                skill_set.add(skill)
        self.skill_sets[agent_name] = skill_set
        return skill_set
    
    def get_skill_set(self, agent_name: str) -> Optional[SkillSet]:
        """Get skill set for agent."""
        return self.skill_sets.get(agent_name)
    
    def add_skill_to_agent(self, agent_name: str, skill_id: str) -> bool:
        """Add skill to agent's skill set."""
        if agent_name not in self.skill_sets:
            self.skill_sets[agent_name] = SkillSet(agent_name=agent_name)
        
        skill = self.get(skill_id)
        if skill:
            self.skill_sets[agent_name].add(skill)
            return True
        return False


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================

skill_manager = SkillManager()


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def register_skill(skill: Skill):
    """Register new skill."""
    skill_manager.register(skill)


def get_skill(skill_id: str) -> Optional[Skill]:
    """Get skill by ID."""
    return skill_manager.get(skill_id)


def list_skills(category: SkillCategory = None) -> Dict:
    """List all skills."""
    if category:
        return {s.id: s.to_dict() for s in skill_manager.by_category(category)}
    return {s.id: s.to_dict() for s in skill_manager.list_all().values()}


def search_skills(query: str) -> List[Dict]:
    """Search skills."""
    return [s.to_dict() for s in skill_manager.search(query)]


def create_skill_set(agent_name: str, skill_ids: List[str]) -> SkillSet:
    """Create skill set for agent."""
    return skill_manager.create_skill_set(agent_name, skill_ids)


def add_skill_to_agent(agent_name: str, skill_id: str) -> bool:
    """Add skill to agent."""
    return skill_manager.add_skill_to_agent(agent_name, skill_id)


__all__ = [
    "Skill",
    "SkillSet",
    "SkillManager",
    "SkillCategory",
    "SkillLevel",
    "skill_manager",
    "register_skill",
    "get_skill",
    "list_skills",
    "search_skills",
    "create_skill_set",
    "add_skill_to_agent",
]