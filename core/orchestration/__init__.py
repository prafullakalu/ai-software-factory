"""
🎯 ORCHESTRATION

Coordinates agents to work together.
Handles task distribution and execution flow.
"""

from crewai import Crew, Process
from core.agents import all_agents
from core.tasks import all_tasks


class SoftwareFactory:
    """Main orchestrator for the AI Software Factory."""
    
    def __init__(self, agents=None, tasks=None, process=Process.sequential):
        self.agents = agents or []
        self.tasks = tasks or []
        self.process = process
        self.crew = None
    
    def build(self):
        """Build the crew with agents and tasks."""
        self.crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=self.process,
            verbose=True,
        )
        return self
    
    def run(self, inputs=None):
        """Execute the crew."""
        if not self.crew:
            self.build()
        return self.crew.kickoff(inputs=inputs or {})
    
    def execute(self, goal):
        """Execute with a single goal."""
        return self.run({"goal": goal})


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_fullstack_factory():
    """Create a fullstack development factory."""
    from core.agents import (
        ProductManager, SystemArchitect, FrontendDeveloper, 
        BackendDeveloper, QAEngineer, DevOpsEngineer,
    )
    from core.tasks import (
        planning_task, architecture_task, frontend_task,
        backend_task, qa_task, deployment_task,
    )
    
    return SoftwareFactory(
        agents=[
            ProductManager, SystemArchitect, FrontendDeveloper,
            BackendDeveloper, QAEngineer, DevOpsEngineer,
        ],
        tasks=[
            planning_task, architecture_task, frontend_task,
            backend_task, qa_task, deployment_task,
        ],
    )


def create_ecommerce_factory():
    """Create an e-commerce factory."""
    # Add specialized e-commerce agents
    return create_fullstack_factory()


def create_saas_factory():
    """Create a SaaS factory."""
    return create_fullstack_factory()


__all__ = ["SoftwareFactory", "create_fullstack_factory"]