# 🤖 AI Software Factory

An AI Agent platform like Hermes Agent / Paperclip AI.

## 🚀 Run

```bash
git clone https://github.com/prafullakalu/ai-software-factory.git
cd ai-software-factory
python main.py "Build a payment gateway"
```

Or interactive CLI:

```bash
python factory.py
> help
> project new MyApp
> generate frontend
> agents
> exit
```

---

## Commands

### Project
- `project new <name>` - Create project
- `project list` - List projects
- `project status` - Show status
- `project run` - Run project

### Generate
- `generate frontend` - Generate React frontend
- `generate backend` - Generate FastAPI backend
- `generate api` - Generate REST API
- `generate fullstack` - Generate fullstack app

### Agent
- `agent list` - List agents
- `agent use <name>` - Switch agent
- `agent run <task>` - Run task
- `agent chat <msg>` - Chat with agent

### Memory
- `remember <fact>` - Remember fact
- `recall <query>` - Recall memories

### Task
- `task new <title>` - Create task
- `task list` - List tasks
- `task complete <id>` - Complete task

### Git
- `git status` - Show status
- `git log` - Show commits
- `git commit <msg>` - Commit

### Database
- `db query <sql>` - Execute query
- `db schema <table>` - Generate schema

### Security
- `security scan` - Scan vulnerabilities
- `security audit` - Full audit

### Deploy
- `deploy docker` - Generate Docker
- `deploy k8s` - Generate K8s
- `deploy ci` - Generate CI/CD

### Quick
- `run <project>` - Run project
- `build <what>` - Build something
- `python <code>` - Execute Python
- `$ <cmd>` - Execute bash

---

## Quick Start

Interactive:

```bash
python factory.py
> project new MySaaS
> generate fullstack
> exit
```

Direct:

```bash
python main.py "Build API with auth"
```

---

## Models

Supported LLM providers:
- **Ollama** (local, FREE!) - `ollama serve`
- **DeepSeek** (FREE!) - Set DEEPSEEK_API_KEY
- **OpenAI** (paid) - Set OPENAI_API_KEY
- **Anthropic** (paid) - Set ANTHROPIC_API_KEY

---

## 📁 Structure

```
ai-software-factory/
├── factory.py         # Full CLI (900+ lines)
├── main.py          # Direct runner
├── orchestrator.py  # Project runner
├── core/
│   ├── agents/    # Real AI agents
│   ├── llm/      # LLM integration
│   ├── memory/   # Persistent memory
│   └── tasks/    # Task management
├── sandbox/         # Code execution
└── tools/           # All tools
```