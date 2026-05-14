"""
🏗️ PROJECT WORKSPACE

Manages the working project - read, edit, build code.
"""

import os
import shutil
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


# ============================================================================
# WORKSPACE STRUCTURE
# ============================================================================

WORKSPACE_DIR = "workspace/project"

DEFAULT_STRUCTURE = {
    "frontend": {
        "src": ["App.jsx", "index.jsx", "App.css"],
        "public": ["index.html"],
    },
    "backend": {
        "api": ["main.py", "models.py", "routes.py"],
        "db": ["database.py"],
    },
}


@dataclass
class ProjectFile:
    """A project file."""
    path: str
    content: str
    file_type: str = "code"


# ============================================================================
# WORKSPACE MANAGER
# ============================================================================

class Workspace:
    """Manage project workspace."""
    
    def __init__(self, root: str = WORKSPACE_DIR):
        self.root = root
        self.current_project: str = None
        self.files: Dict[str, ProjectFile] = {}
    
    def init_project(self, name: str) -> str:
        """Initialize a new project."""
        self.current_project = name
        self.root = f"workspace/{name}"
        
        # Create directories
        for folder in ["frontend/src", "frontend/public", "backend/api", "backend/db"]:
            path = os.path.join(self.root, folder)
            os.makedirs(path, exist_ok=True)
        
        # Create default files
        self._create_default_files()
        
        return f"✅ Project '{name}' initialized at {self.root}/"
    
    def _create_default_files(self):
        """Create default project files."""
        # Frontend
        self.files["frontend/src/App.jsx"] = ProjectFile(
            "frontend/src/App.jsx",
            DEFAULT_REACT_APP,
            "jsx",
        )
        self.files["frontend/src/index.jsx"] = ProjectFile(
            "frontend/src/index.jsx",
            DEFAULT_REACT_INDEX,
            "jsx",
        )
        self.files["frontend/src/App.css"] = ProjectFile(
            "frontend/src/App.css",
            DEFAULT_CSS,
            "css",
        )
        
        # Backend
        self.files["backend/api/main.py"] = ProjectFile(
            "backend/api/main.py",
            DEFAULT_FASTAPI,
            "py",
        )
        
        # Write files
        for file_path, pf in self.files.items():
            full_path = os.path.join(self.root, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w") as f:
                f.write(pf.content)
    
    def read_file(self, path: str) -> Optional[str]:
        """Read a file."""
        full_path = os.path.join(self.root, path)
        if os.path.exists(full_path):
            with open(full_path, "r") as f:
                return f.read()
        return None
    
    def write_file(self, path: str, content: str) -> str:
        """Write a file."""
        full_path = os.path.join(self.root, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
        return f"✅ Written: {path}"
    
    def edit_file(self, path: str, old: str, new: str) -> str:
        """Edit a file (replace old with new)."""
        content = self.read_file(path)
        if content is None:
            return f"❌ File not found: {path}"
        
        if old not in content:
            return f"❌ Text not found in {path}"
        
        content = content.replace(old, new)
        return self.write_file(path, content)
    
    def list_files(self) -> List[str]:
        """List all files."""
        files = []
        for root, dirs, filenames in os.walk(self.root):
            for f in filenames:
                if not f.startswith('.'):
                    rel = os.path.relpath(os.path.join(root, f), self.root)
                    files.append(rel)
        return files
    
    def get_status(self) -> str:
        """Get project status."""
        files = self.list_files()
        return f"""
📁 Project: {self.current_project or 'None'}
📄 Files: {len(files)}
📂 Location: {self.root}/
"""
    
    def build(self) -> str:
        """Build the project."""
        if not self.current_project:
            return "❌ No project initialized"
        
        # Check what tools are available
        has_frontend = os.path.exists(os.path.join(self.root, "frontend"))
        has_backend = os.path.exists(os.path.join(self.root, "backend"))
        
        result = [f"🔨 Building {self.current_project}..."]
        
        if has_frontend:
            result.append("  ✅ Frontend ready")
        if has_backend:
            result.append("  ✅ Backend ready")
        
        result.append("\n📦 To run:")
        if has_frontend:
            result.append("  cd frontend && npm install && npm start")
        if has_backend:
            result.append("  cd backend && pip install -r requirements.txt && uvicorn main:app")
        
        return "\n".join(result)


# ============================================================================
# DEFAULT TEMPLATES
# ============================================================================

DEFAULT_REACT_APP = """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './App.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
"""

DEFAULT_REACT_INDEX = """import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function Home() {
  return (
    <div className="page">
      <h1>Welcome to My App</h1>
      <p>Start building your amazing project!</p>
      <Link to="/login" className="btn">Get Started</Link>
    </div>
  );
}

function Login() {
  return (
    <div className="page">
      <h2>Login</h2>
      <form>
        <input type="email" placeholder="Email" />
        <input type="password" placeholder="Password" />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

function Dashboard() {
  return (
    <div className="page">
      <h1>Dashboard</h1>
      <p>Welcome back!</p>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}
"""

DEFAULT_CSS = """* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f5f5f5;
  color: #333;
}

.page {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 400px;
  margin: 0 auto;
}

input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

button, .btn {
  padding: 0.75rem 1.5rem;
  background: #0070f3;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
}

button:hover, .btn:hover {
  background: #0051cc;
}
"""

DEFAULT_FASTAPI = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="My API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None

items_db: List[Item] = []
item_id = 1

@app.get("/")
def root():
    return {"message": "My API", "version": "1.0.0"}

@app.get("/items")
def get_items():
    return items_db

@app.post("/items")
def create_item(item: Item):
    global item_id
    item.id = item_id
    item_id += 1
    items_db.append(item)
    return item

@app.get("/health")
def health():
    return {"status": "healthy"}
"""

# ============================================================================
# EXPORTS
# ============================================================================

workspace = Workspace()


def read(path: str) -> Optional[str]:
    """Read a file."""
    return workspace.read_file(path)


def write(path: str, content: str) -> str:
    """Write a file."""
    return workspace.write_file(path, content)


def edit(path: str, old: str, new: str) -> str:
    """Edit a file."""
    return workspace.edit_file(path, old, new)


def init(name: str) -> str:
    """Initialize project."""
    return workspace.init_project(name)


def status() -> str:
    """Get status."""
    return workspace.get_status()


def build() -> str:
    """Build project."""
    return workspace.build()


__all__ = [
    "Workspace",
    "workspace",
    "read",
    "write", 
    "edit",
    "init",
    "status",
    "build",
]