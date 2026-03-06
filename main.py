from crewai import Crew, Process
from agents.agents import (
    pmAgent, architectAgent, frontendAgent, 
    backendAgent, qaAgent, devopsAgent
)
from agents.tasks import (
    productPlanningTask, architectureTask, frontendTask, 
    backendTask, testingTask, deploymentTask
)

# Assemble the Crew
ai_agency = Crew(
    agents=[pmAgent, architectAgent, frontendAgent, backendAgent, qaAgent, devopsAgent],
    tasks=[productPlanningTask, architectureTask, frontendTask, backendTask, testingTask, deploymentTask],
    process=Process.sequential,
    verbose=True
)

if __name__ == "__main__":
    print("### Starting AI Agent Agency ###")
    inputs = {'goal': 'Build a professional sneaker e-commerce website with user auth and a cart.'}
    result = ai_agency.kickoff(inputs=inputs)
    print("\n\n########################")
    print("## PROJECT COMPLETE ##")
    print("########################\n")
    print(result)