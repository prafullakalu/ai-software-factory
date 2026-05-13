#!/usr/bin/env python3
"""
🤖 AI SOFTWARE FACTORY - CLI Shell

Run like Hermes Agent - just type commands!
"""

import sys
import os

# Add current dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all modules
from orchestrator import runner
from sandbox.executor import run_python, run_javascript, run_bash
from core.memory.persistent import memory, remember, recall
from core.agents import list_agents, get_agent, create_agent
from core.tasks.manager import task_manager
from tools.git import git
from tools.terminal import terminal
from tools.database import DatabaseConfig, SQLQueryBuilder
from tools.api import RESTAPIGenerator
from tools.security import scanner
from tools.testing import test_generator
from tools.deployment import docker_gen
from tools.file import file_manager


# ============================================================================
# COMMAND HANDLERS
# ============================================================================

class CommandHandler:
    """Handle natural language commands."""
    
    def __init__(self):
        self.session_active = True
    
    def run_command(self, cmd: str) -> str:
        """Run a command."""
        cmd = cmd.strip().lower()
        
        # Help
        if cmd in ['help', '?']:
            return self.help()
        
        # Exit
        if cmd in ['exit', 'quit', 'q']:
            self.session_active = False
            return "Goodbye! 👋"
        
        # Clear
        if cmd == 'clear':
            return "cleared"
        
        # Status
        if cmd == 'status':
            return self.status()
        
        # Run project
        if cmd.startswith('run '):
            project = cmd[4:].strip()
            ctx = runner.run(project, project)
            return f"✅ Project '{project}' - {ctx.status} ({ctx.progress}%)"
        
        # Build
        if cmd.startswith('build '):
            what = cmd[6:].strip()
            ctx = runner.run(what, what)
            return f"🔨 Building: {what}\n✅ Status: {ctx.status}"
        
        # Create project
        if cmd.startswith('create project '):
            name = cmd[14:].strip()
            ctx = runner.run(name, name)
            return f"✅ Created project: {name}"
        
        # Execute code
        if cmd.startswith('exec ') or cmd.startswith('run code '):
            code = cmd.split(' ', 1)[1] if ' ' in cmd else ''
            if code:
                result = run_python(code)
                return f"📦 Output:\n{result.output}"
            return "Usage: exec <python code>"
        
        # Run python
        if cmd.startswith('python '):
            code = cmd[7:].strip()
            result = run_python(code)
            return f"🐍 Output:\n{result.output}"
        
        # Run bash
        if cmd.startswith('bash ') or cmd.startswith('$ '):
            code = cmd.split(' ', 1)[1] if ' ' in cmd else ''
            if code:
                result = run_bash(code)
                return f"💻 Output:\n{result.output}"
            return "Usage: $ <command>"
        
        # Remember
        if cmd.startswith('remember '):
            fact = cmd[9:].strip()
            remember(fact)
            return f"💾 Remembered: {fact}"
        
        # Recall / remember
        if cmd.startswith('recall '):
            query = cmd[7:].strip()
            facts = recall(query)
            if facts:
                return "📚 Found:\n" + "\n".join(f"- {f.content}" for f in facts)
            return "No memories found."
        
        # List agents
        if cmd in ['agents', 'list agents', 'list agents']:
            agents = list_agents()
            return "🤖 Agents:\n" + "\n".join(
                f"- {a['name']}: {a['goal']}" for a in agents
            )
        
        # Get agent
        if cmd.startswith('agent '):
            name = cmd[6:].strip()
            agent = get_agent(name)
            if agent:
                return f"👤 {agent.name}\n   Role: {agent.role}\n   Goal: {agent.goal}"
            return f"Agent '{name}' not found"
        
        # Tasks
        if cmd in ['tasks', 'pending tasks']:
            tasks = task_manager.get_pending_tasks()
            if tasks:
                return "📋 Tasks:\n" + "\n".join(
                    f"- {t.title} ({t.status.value})" for t in tasks
                )
            return "No pending tasks."
        
        # Create task
        if cmd.startswith('task '):
            title = cmd[5:].strip()
            task_id = task_manager.create_task(title)
            return f"✅ Created task: {title}"
        
        # Complete task
        if cmd.startswith('complete '):
            title = cmd[9:].strip()
            tasks = task_manager.get_pending_tasks()
            for t in tasks:
                if title.lower() in t.title.lower():
                    task_manager.complete_task(t.id)
                    return f"✅ Completed: {t.title}"
            return f"Task '{title}' not found"
        
        # Git commands
        if cmd.startswith('git '):
            git_cmd = cmd[4:].strip()
            if git_cmd == 'status':
                status = git.status()
                return f"Git Status: {status.value}"
            if git_cmd == 'log':
                commits = git.log(5)
                return "📜 Recent commits:\n" + "\n".join(
                    f"- {c.hash[:7]}: {c.message}" for c in commits
                )
            return f"Git: {git_cmd}"
        
        # Terminal
        if cmd.startswith('! '):
            code = cmd[2:].strip()
            result = terminal.execute(code)
            return f"💻 Output:\n{result.stdout}"
        
        # Database query
        if cmd.startswith('sql '):
            query = cmd[4:].strip()
            q = SQLQueryBuilder('users')
            q.where_eq('id', query)
            return f"🔍 Query:\n{q.build()}"
        
        # System info
        if cmd in ['system', 'sys info', 'info']:
            info = terminal.get_system_info()
            return "💻 System:\n" + "\n".join(f"- {k}: {v}" for k, v in info.items())
        
        # Stats
        if cmd in ['stats', 'statistics']:
            stats = {
                "memory": memory.get_stats(),
                "tasks": task_manager.get_stats(),
            }
            return "📊 Statistics:\n" + "\n".join(f"- {k}: {v}" for k, v in stats.items())
        
        # Templates
        if cmd in ['templates', 'list templates']:
            return """📦 Templates:
- saas: SaaS Starter
- api: REST API
- fintech: Payment Gateway
- ecommerce: E-commerce Store
- admin: Admin Dashboard
- blog: Blog CMS"""
        
        # Use template
        if cmd.startswith('use template '):
            template = cmd[13:].strip()
            return f"📦 Using template: {template}"
        
        # Unknown
        return f"❓ Unknown command: {cmd}\nType 'help' for available commands."
    
    def help(self) -> str:
        return """📖 Available Commands:

Projects:
  run <project>      - Run a new project
  build <what>     - Build something
  create project <name> - Create new project

Code Execution:
  python <code>     - Run Python code
  $ <command>       - Run bash command
  ! <command>      - Run terminal command

Memory:
  remember <fact>   - Remember a fact
  recall <query>    - Recall memories

Agents:
  agents           - List all agents
  agent <name>     - Get agent info

Tasks:
  tasks            - List pending tasks
  task <title>     - Create new task
  complete <title> - Complete task

Git:
  git status       - Check git status
  git log         - View recent commits

System:
  system          - System info
  stats           - Statistics
  help            - Show this help

Tips:
  - Type naturally, e.g. "remember API uses JWT"
  - Use Ctrl+C to cancel
  - Type 'exit' to quit
"""
    
    def status(self) -> str:
        """Get system status."""
        ctx = runner.get_status()
        stats = memory.get_stats()
        task_stats = task_manager.get_stats()
        
        return f"""
🤖 AI Software Factory - Status
{'='*40}
Project: {ctx.get('project', 'None')}
Status: {ctx.get('status', 'idle')}
Progress: {ctx.get('progress', 0)}%

Memory: {stats.get('total_facts', 0)} facts, {stats.get('total_skills', 0)} skills
Tasks: {task_stats.get('completed', 0)} completed, {task_stats.get('pending', 0)} pending
Agents: {stats.get('total_agents', 12)} available
"""


# ============================================================================
# MAIN SHELL
# ============================================================================

def main():
    print("="*60)
    print("🤖 AI SOFTWARE FACTORY")
    print("="*60)
    print()
    print("Type 'help' for commands, 'exit' to quit")
    print()
    
    handler = CommandHandler()
    
    # Welcome status
    print(handler.status())
    
    # Interactive loop
    while handler.session_active:
        try:
            cmd = input("\n> ").strip()
            
            if not cmd:
                continue
            
            # Check for special commands
            if cmd == 'clear':
                print("\n" * 50)
                continue
            
            # Run command
            result = handler.run_command(cmd)
            
            # Handle special output
            if result == "cleared":
                print("\n" * 50)
            elif result:
                print(result)
        
        except KeyboardInterrupt:
            print("\n\nUse 'exit' to quit")
        except EOFError:
            break
    
    print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()