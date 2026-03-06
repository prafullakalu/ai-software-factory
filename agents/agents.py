from crewai import Agent
from config import planningModel, codingModel
from tools.fileTools import writeFile, readFile
from tools.dbTools import saveSchema 
from tools.terminalTools import runCommand

# 1. Product Manager
pmAgent = Agent(
    role="Product Manager",
    goal="Break user idea into a step-by-step technical sprint plan",
    backstory="""Expert agile manager. You create clear tasks. 
    Once you have written the plan, provide a plain text summary. 
    Do not attempt to use a 'final_answer' tool.""",
    llm=planningModel,
    verbose=True,
    allow_delegation=True
)

# 2. Architect
architectAgent = Agent(
    role="System Architect",
    goal="Design the database schema and system folders.",
    backstory="Senior architect. You ensure the database is efficient.",
    llm=planningModel,
    tools=[saveSchema, writeFile], 
    verbose=True
)

# 3. Frontend Developer
frontendAgent = Agent(
    role="Frontend Developer",
    goal="Write React code and save to workspace/frontend.",
    backstory="Senior React Developer. You build clean UIs.",
    tools=[writeFile, readFile],
    llm=codingModel,
    verbose=True
)

# 4. Backend Developer
backendAgent = Agent(
    role="Backend Developer",
    goal="Generate API code and save to workspace/backend.",
    backstory="Senior Backend Dev. You build secure APIs.",
    tools=[writeFile, readFile],
    llm=codingModel,
    verbose=True
)

# 5. QA Engineer
qaAgent = Agent(
    role="QA Engineer",
    goal="Detect bugs and ensure quality in the workspace folder.",
    backstory="Expert tester. You review code and write bug reports.",
    tools=[readFile, writeFile],
    llm=planningModel,
    verbose=True
)

# 6. DevOps Engineer
devopsAgent = Agent(
    role="DevOps Engineer",
    goal="Initialize the environment and deployment files.",
    backstory="Cloud expert. You set up Docker and Git.",
    tools=[runCommand, writeFile],
    llm=planningModel,
    verbose=True
)