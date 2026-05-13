# 🤖 AI Software Factory

A powerful AI Agent platform like Hermes Agent / Paperclip AI for building SaaS/Fintech applications. Built with 10+ specialized AI agents, persistent memory, sandbox execution, and complete tooling.

## ✨ Features

| Feature | Description |
|--------|-------------|
| **Persistent Memory** | Remembers everything (stores in `~/.hermes/`) |
| **Sandbox Execution** | Run Python, JavaScript, Bash safely |
| **12+ AI Agents** | PM, Architect, Designer, Dev, QA, Security, etc. |
| **Agent Communication** | Agents can talk to each other |
| **Task Management** | Goals with subtasks and progress |
| **Git Operations** | Full git integration |
| **Browser Automation** | HTTP requests + Playwright support |
| **Terminal Execution** | Run real terminal commands |
| **Code Generation** | Generate SaaS/Fintech apps |
| **Cost Calculator** | FREE tier estimation |

---

## 🚀 Quick Start

### Run a Project

```python
from orchestrator import runner

# Run a simple project
ctx = runner.run('My SaaS App', 'Build an API with authentication')
print(ctx.status)  # completed
print(ctx.progress)  # 100
```

### Execute Code

```python
from sandbox.executor import run_python, run_javascript, run_bash

# Run Python
result = run_python('print(1+1)')
print(result.output)  # 2

# Run JavaScript  
result = run_javascript('console.log("hello")')
print(result.output)  # hello

# Run Bash
result = run_bash('ls -la')
print(result.output)
```

### Use Memory

```python
from core.memory.persistent import memory, remember, recall

# Remember facts
remember('User prefers dark mode')
memory.learn_fact('API uses JWT tokens')

# Recall facts
facts = recall('dark mode', limit=5)

# Build context for AI
context = memory.build_context()
```

### Manage Tasks

```python
from core.tasks.manager import task_manager

# Create goal with tasks
goal_id = task_manager.create_goal_with_tasks(
    'Build API',
    'Create routes', 'Add auth', 'Write tests'
)

# Get pending tasks
tasks = task_manager.get_pending_tasks()
task = task_manager.get_next_task()
task_manager.complete_task(task.id)
```

### Use Agents

```python
from core.agents import list_agents, get_agent, create_agent

# List all agents
agents = list_agents()
print(f'Available: {len(agents)} agents')

# Get specific agent
agent = get_agent('frontend')
print(f'Role: {agent.role}')
print(f'Goal: {agent.goal}')

# Create custom agent
custom = create_agent(
    name='My Agent',
    role='Developer',
    goal='Build apps',
    backstory='Expert developer',
    skills=['python', 'react']
)
```

---

## 🛠️ Tools

### Terminal

```python
from tools.terminal import terminal

# Execute commands
result = terminal.execute('npm install')
print(result.stdout)

# Get system info
info = terminal.get_system_info()
```

### Git

```python
from tools.git import git

git.init()
git.add_all()
git.commit('Initial commit')
git.push()

# Branch operations
git.branch('new-feature', create=True)
git.checkout('new-feature')
```

### Database

```python
from tools.database import DatabaseConfig, SQLQueryBuilder

# Build queries
query = SQLQueryBuilder('users')
query.select('id', 'name').where_eq('active', True)
print(query.build())

# Or use Prisma/SQLAlchemy generators
```

### API

```python
from tools.api import RESTAPIGenerator, OpenAPIGenerator

# Generate FastAPI code
api = RESTAPIGenerator('myapi')
api.add_endpoint('/users', 'GET', 'get_users')
code = api.generate_fastapi()
```

### Security

```python
from tools.security import scanner, crypto

# Scan for vulnerabilities
issues = scanner.scan_file('app.py', code)
print(issues)

# Hash password
hashed, salt = crypto.hash_password('password123')
crypto.verify_password('password123', hashed, salt)
```

### Testing

```python
from tools.testing import test_generator, fixtures

# Generate tests
tests = test_generator.generate_unit_tests('myapp.py')

# Use fixtures
user = fixtures.user(name='John', email='john@example.com')
```

### Deployment

```python
from tools.deployment import docker_gen

# Generate Docker config
docker = docker_gen.set_port(8000).add_env('DEBUG', 'false')
dockerfile = docker.generate_docker_compose()
```

---

## 📁 Project Structure

```
ai-software-factory/
├── core/
│   ├── agents/          # AI Agents
│   │   ├── __init__.py
│   │   ├── dynamic.py  # Dynamic agent generator
│   │   ├── skills.py   # Skills system
│   │   └── communication.py
│   ├── memory/         # Persistent memory
│   └── tasks/         # Task management
├── sandbox/           # Code execution
├── tools/              # All tools
│   ├── terminal/
│   ├── git/
│   ├── browser/
│   ├── database/
│   ├── api/
│   ├── security/
│   ├── testing/
│   └── deployment/
├── orchestrator.py     # Main orchestrator
└── README.md
```

---

## 🔧 Requirements

```bash
# No external dependencies needed!
# Works with Python 3.8+
python3 --version
```

---

## 📊 Statistics

| Metric | Count |
|--------|-------|
| **Total Lines** | 9,721+ |
| **AI Agents** | 12+ |
| **Skills** | 50+ |
| **Tools** | 10+ |
| **Dependencies** | 0 (standalone!) |

---

## 🆚 vs Other Tools

| Feature | This Project | Hermes | Paperclip |
|--------|--------------|--------|----------|
| **Dependencies** | 0 | Many | Many |
| **Memory** | ✅ | ✅ | ✅ |
| **Sandbox** | ✅ | ✅ | ✅ |
| **Git** | ✅ | ✅ | ✅ |
| **Terminal** | ✅ | ✅ | ✅ |
| **Browser** | ✅ | ✅ | ✅ |
| **Cost** | FREE | $$ | $$$ |

---

## 🤖 Running Examples

### Example 1: Create and Run Project

```python
from orchestrator import runner

ctx = runner.run(
    'Ecommerce API',
    'Build REST API with products, orders, payments',
    project_type='saas'
)

print(f'Status: {ctx.status}')
print(f'Progress: {ctx.progress}%')
```

### Example 2: Use Agents with Memory

```python
from core.agents import get_agent
from core.memory import memory

agent = get_agent('backend')
print(f'Building with: {agent.name}')

# Remember the agent's choice
memory.learn_fact('Using FastAPI for backend')

# Later recall
facts = recall('FastAPI')
for fact in facts:
    print(fact.content)
```

### Example 3: Task-Driven Workflow

```python
from core.tasks.manager import task_manager

# Create multiple tasks
task_id1 = task_manager.create_task('Design API', priority=10)
task_id2 = task_manager.create_task('Add auth', priority=5)

# Mark complete
task_manager.complete_task(task_id1)
```

---

## 📝 License

MIT License - Free to use!

---

## 🙏 Credits

Built with inspiration from:
- [Hermes Agent](https://hermes-agent.nousresearch.com/)
- [Paperclip AI](https://paperclip.ai/)
- [Manus Agent](https://manus.im/)

---

**⭐ Star us on GitHub!** ⭐