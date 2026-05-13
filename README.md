# 🤖 AI Software Factory

An AI Agent platform like Hermes Agent / Paperclip AI - runs with simple commands!

## 🚀 Quick Start

```bash
# Clone and run!
git clone https://github.com/prafullakalu/ai-software-factory.git
cd ai-software-factory
python3 factory.py
```

---

## 💬 CLI Commands

Type commands like chatting with an assistant:

### Projects
```
> run build an API
> build SaaS app
> create project MyApp
```

### Execute Code
```
> python print(1+1)
> $ ls -la
> ! echo hello
```

### Memory
```
> remember API uses JWT
> recall JWT
```

### Agents
```
> agents
> agent frontend
```

### Tasks
```
> tasks
> task fix bug
> complete fix bug
```

### System
```
> status
> stats
> system
> help
> exit
```

---

## 📁 Project Structure

```
ai-software-factory/
├── factory.py          # Main CLI shell
├── orchestrator.py    # Project runner
├── core/
│   ├── agents/    # AI Agents
│   ├── memory/   # Persistent memory
│   └── tasks/    # Task management
├── sandbox/         # Code execution
├── tools/           # All tools
└── README.md
```

---

## ✨ Features

| Feature | Command | Status |
|---------|--------|--------|
| Run Project | `run build API` | ✅ |
| Python Code | `python print(1+1)` | ✅ |
| Bash | `$ ls` | ✅ |
| Terminal | `! command` | ✅ |
| Memory | `remember fact` | ✅ |
| 12+ Agents | `agent frontend` | ✅ |
| Tasks | `task do something` | ✅ |
| Git | `git status` | ✅ |
| Database | `sql SELECT *` | ✅ |
| Security | scans automatically | ✅ |

---

## 📊 Stats

- **Total Lines**: 9,721+
- **External Dependencies**: 0 (standalone!)
- **Agents**: 12+
- **Tools**: 10+

---

**Just run `python3 factory.py` and start typing!** 🚀