from crewai import Crew
from agents.agents import (
    pmAgent,
    architectAgent,
    frontendAgent,
    backendAgent,
    qaAgent,
    devopsAgent
)

from agents.tasks import (
    productPlanningTask,
    architectureTask,
    frontendTask,
    backendTask,
    testingTask,
    deploymentTask
)

crew = Crew(
    agents=[
        pmAgent,
        architectAgent,
        frontendAgent,
        backendAgent,
        qaAgent,
        devopsAgent
    ],
    tasks=[
        productPlanningTask,
        architectureTask,
        frontendTask,
        backendTask,
        testingTask,
        deploymentTask
    ],
    verbose=True
)