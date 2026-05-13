# 🤖 AI Software Factory

An AI Agent platform like Hermes Agent / Paperclip AI - runs with simple commands!

## 🚀 Quick Start

```bash
git clone https://github.com/prafullakalu/ai-software-factory.git
cd ai-software-factory
python factory.py
```

Or run a goal directly:

```bash
python main.py "Build a payment gateway"
python main.py "Create REST API with auth"
```

---

## 💬 CLI Commands (Interactive)

```bash
python factory.py
```

Then type commands:

```
> run build an API
> python print(1+1)
> $ ls -la
> remember API uses JWT
> agents
> tasks
> status
> help
> exit
```

---

## 📁 Project Structure

```
ai-software-factory/
├── factory.py          # Main CLI shell (interactive)
├── main.py           # Direct goal runner
├── orchestrator.py    # Project runner
├── core/
│   ├── agents/     # AI Agents (12+)
│   ├── memory/    # Persistent memory
│   └── tasks/    # Task management
├── sandbox/          # Code execution
├── tools/            # All tools
└── README.md
```

---

## ✨ Features

| Feature | Command | Status |
|---------|---------|--------|
| Run Project | `run build API` | ✅ |
| Python Code | `python print(1+1)` | ✅ |
| Bash | `$ ls` | ✅ |
| Terminal | `! command` | ✅ |
| Memory | `remember fact` | ✅ |
| 12+ Agents | `agents` | ✅ |
| Tasks | `tasks` | ✅ |
| Git Ops | `git status` | ✅ |
| Database | `sql query` | ✅ |

---

## ⌨️ Keyboard Shortcuts

- `Ctrl+C` - Cancel input
- `Ctrl+D` / `exit` - Quit

---

## 📊 Stats

- **Lines**: 9,721+
- **Dependencies**: 0 (standalone!)
- **Agents**: 12+
- **Tools**: 10+

---

**Just run `python factory.py`!** 🚀