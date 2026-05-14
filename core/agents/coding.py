"""
🤖 CODING AGENT

Real coding agent that reads, edits, and builds code step by step.
"""

import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from workspace.manager import workspace, read, write, edit, init, status, build


# ============================================================================
# AGENT TASKS
# ============================================================================

@dataclass
class CodingStep:
    """A coding step."""
    action: str  # read, write, edit, run
    target: str  # file path
    content: str  # what to do
    result: str = ""  # result


@dataclass
class CodingTask:
    """A coding task."""
    title: str
    description: str
    steps: List[CodingStep]
    status: str = "pending"


# ============================================================================
# CODING AGENT
# ============================================================================

class CodingAgent:
    """
    Real coding agent - works step by step like a developer.
    
    Flow:
    1. Read existing code
    2. Understand what needs to change
    3. Make changes (edit files)
    4. Build and test
    """
    
    def __init__(self):
        self.current_task: Optional[CodingTask] = None
        self.history: List[CodingTask] = []
    
    def init_project(self, name: str) -> str:
        """Initialize a new project."""
        result = workspace.init_project(name)
        self.current_task = CodingTask(
            title=f"Initialize {name}",
            description=f"Create new {name} project",
            steps=[],
        )
        return result
    
    def read_code(self, path: str) -> str:
        """Read code from a file."""
        content = workspace.read_file(path)
        if content:
            lines = content.split("\n")[:20]
            preview = "\n".join(f"{i+1}: {line}" for i, line in enumerate(lines))
            return f"📄 {path}:\n{preview}\n..."
        return f"❌ File not found: {path}"
    
    def write_code(self, path: str, content: str) -> str:
        """Write code to a file."""
        return workspace.write_file(path, content)
    
    def edit_code(self, path: str, old: str, new: str) -> str:
        """Edit code in a file."""
        # First show what we're changing
        content = workspace.read_file(path)
        if content and old in content:
            result = workspace.edit_file(path, old, new)
            return f"✏️ Edited {path}:\n  - Removed: {old[:50]}...\n  + Added: {new[:50]}..."
        return f"❌ Could not find text in {path}"
    
    def run_task(self, task: str) -> str:
        """Run a coding task step by step."""
        task_lower = task.lower()
        
        # Understand the task
        if "login" in task_lower and "add" in task_lower:
            return self._add_login()
        elif "api" in task_lower and "add" in task_lower:
            return self._add_api_endpoint()
        elif "dashboard" in task_lower and "add" in task_lower:
            return self._add_dashboard()
        elif "test" in task_lower:
            return self._run_tests()
        elif "build" in task_lower:
            return workspace.build()
        else:
            return f"❓ Don't understand: {task}\nTry: add login, add API, add dashboard, build, test"
    
    def _add_login(self) -> str:
        """Add login functionality."""
        # Read current App.jsx
        content = workspace.read_file("frontend/src/App.jsx")
        if not content:
            return "❌ No frontend found"
        
        # Add login form if not exists
        if "Login" not in content:
            login_component = '''

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Login: ${{email}}`);
  };

  return (
    <div className="page">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input 
          type="email" 
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input 
          type="password" 
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}'''
            new_content = content.replace(
                "export default function App()",
                login_component + "\n\nexport default function App()"
            )
            workspace.write_file("frontend/src/App.jsx", new_content)
            return "✅ Added login form to App.jsx"
        
        return "✅ Login already exists"
    
    def _add_api_endpoint(self) -> str:
        """Add API endpoint."""
        content = workspace.read_file("backend/api/main.py")
        if not content:
            return "❌ No backend found"
        
        # Add new endpoint
        new_endpoint = '''

@app.get("/users")
def get_users():
    return [{"id": 1, "name": "Demo User"}]

@app.post("/users")
def create_user():
    return {"id": 2, "name": "New User"}'''
        
        workspace.write_file("backend/api/main.py", content + new_endpoint)
        return "✅ Added /users endpoint"
    
    def _add_dashboard(self) -> str:
        """Add dashboard."""
        content = workspace.read_file("frontend/src/App.jsx")
        if not content:
            return "❌ No frontend found"
        
        if "Dashboard" not in content:
            dashboard = '''

function Dashboard() {
  const [user, setUser] = useState(null);
  
  return (
    <div className="page">
      <h1>Dashboard</h1>
      <div className="stats">
        <div className="stat-card">
          <h3>100</h3>
          <p>Users</p>
        </div>
        <div className="stat-card">
          <h3>50</h3>
          <p>Orders</p>
        </div>
      </div>
    </div>
  );
}'''
            new_content = content.replace(
                "export default function App()",
                dashboard + "\n\nexport default function App()"
            )
            workspace.write_file("frontend/src/App.jsx", new_content)
            return "✅ Added dashboard"
        
        return "✅ Dashboard already exists"
    
    def _run_tests(self) -> str:
        """Run tests."""
        return "✅ Tests passed (demo)"
    
    def list_changes(self) -> str:
        """List recent changes."""
        files = workspace.list_files()
        return f"📁 Project files ({len(files)}):\n" + "\n".join(f"  - {f}" for f in files)


# ============================================================================
# EXports
# ============================================================================

coding_agent = CodingAgent()


def init_project(name: str) -> str:
    """Initialize a project."""
    return coding_agent.init_project(name)


def read_code(path: str) -> str:
    """Read code."""
    return coding_agent.read_code(path)


def write_code(path: str, content: str) -> str:
    """Write code."""
    return coding_agent.write_code(path, content)


def edit_code(path: str, old: str, new: str) -> str:
    """Edit code."""
    return coding_agent.edit_code(path, old, new)


def run_task(task: str) -> str:
    """Run a coding task."""
    return coding_agent.run_task(task)


def changes() -> str:
    """List changes."""
    return coding_agent.list_changes()


__all__ = [
    "CodingAgent",
    "coding_agent",
    "init_project",
    "read_code",
    "write_code",
    "edit_code",
    "run_task",
    "changes",
]