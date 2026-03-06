from crewai import Task
from agents.agents import (
    pmAgent, architectAgent, frontendAgent, 
    backendAgent, qaAgent, devopsAgent
)

productPlanningTask = Task(
    description="Analyze user prompt and create a plan. Save as 'workspace/plan.md'.",
    expected_output="Detailed sprint plan saved to workspace.",
    agent=pmAgent
)

architectureTask = Task(
    description="Design the schema. Save as 'workspace/database/schema.sql'.",
    expected_output="SQL schema saved in workspace/database.",
    agent=architectAgent
)

frontendTask = Task(
    description="Generate React code. Save all files in 'workspace/frontend/'.",
    expected_output="Frontend code saved in workspace/frontend.",
    agent=frontendAgent
)

backendTask = Task(
    description="Generate API code. Save all files in 'workspace/backend/'.",
    expected_output="Backend code saved in workspace/backend.",
    agent=backendAgent
)

testingTask = Task(
    description="Review workspace files for bugs. Save 'workspace/qa_report.md'.",
    expected_output="Bug report saved to workspace.",
    agent=qaAgent
)

deploymentTask = Task(
    description="Create 'workspace/infrastructure/Dockerfile'. Run git init in workspace.",
    expected_output="Deployment files created.",
    agent=devopsAgent
)