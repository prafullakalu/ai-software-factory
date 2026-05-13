"""
📋 CORE TASKS

Task definitions for each agent.
Each task has a description and expected output.
"""

from crewai import Task
from core.agents import (
    ProductManager,
    SystemArchitect,
    FrontendDeveloper,
    BackendDeveloper,
    DatabaseEngineer,
    UIDesigner,
    QAEngineer,
    SecurityEngineer,
    DevOpsEngineer,
    APIDesigner,
    PerformanceEngineer,
    DocsEngineer,
)

# ============================================================================
# PLANNING TASKS
# ============================================================================

planning_task = Task(
    description="Analyze requirements and create sprint plan.",
    expected_output="Detailed plan in workspace/plan.md",
    agent=ProductManager,
)

architecture_task = Task(
    description="Design system architecture and database schema.",
    expected_output="Architecture docs in workspace/architecture/",
    agent=SystemArchitect,
)

# ============================================================================
# DEVELOPMENT TASKS  
# ============================================================================

frontend_task = Task(
    description="Generate frontend code (React/Next.js).",
    expected_output="Frontend code in workspace/frontend/",
    agent=FrontendDeveloper,
)

backend_task = Task(
    description="Generate backend API code.",
    expected_output="Backend code in workspace/backend/",
    agent=BackendDeveloper,
)

database_task = Task(
    description="Design and generate database schema.",
    expected_output="Schema in workspace/database/",
    agent=DatabaseEngineer,
)

# ============================================================================
# DESIGN TASKS
# ============================================================================

design_task = Task(
    description="Create UI/UX design specifications.",
    expected_output="Design files in workspace/design/",
    agent=UIDesigner,
)

# ============================================================================
# QUALITY TASKS
# ============================================================================

qa_task = Task(
    description="Write tests and perform QA.",
    expected_output="Tests in workspace/tests/, QA report",
    agent=QAEngineer,
)

security_task = Task(
    description="Perform security audit.",
    expected_output="Security report in workspace/security/",
    agent=SecurityEngineer,
)

# ============================================================================
# DEPLOYMENT TASKS
# ============================================================================

deployment_task = Task(
    description="Set up deployment infrastructure.",
    expected_output="Dockerfile, K8s manifests in workspace/infrastructure/",
    agent=DevOpsEngineer,
)

api_doc_task = Task(
    description="Generate API documentation.",
    expected_output="OpenAPI spec in workspace/api/",
    agent=APIDesigner,
)

performance_task = Task(
    description="Optimize performance.",
    expected_output="Performance report",
    agent=PerformanceEngineer,
)

docs_task = Task(
    description="Create project documentation.",
    expected_output="Docs in workspace/docs/",
    agent=DocsEngineer,
)


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    "planning_task",
    "architecture_task",
    "frontend_task",
    "backend_task",
    "database_task",
    "design_task",
    "qa_task",
    "security_task",
    "deployment_task",
    "api_doc_task",
    "performance_task",
    "docs_task",
]