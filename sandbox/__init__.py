"""
🏖️ CODE SANDBOX

Sandbox environment for testing and running generated code.
"""

import os
import subprocess
import tempfile
import shutil
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


# ============================================================================
# SANDBOX CONFIG
# ============================================================================

@dataclass
class SandboxConfig:
    """Sandbox configuration."""
    workspace: str = "sandbox/workspace"
    timeout: int = 60
    max_memory_mb: int = 512
    allow_network: bool = True


class Sandbox:
    """Code sandbox for testing."""
    
    def __init__(self, config: SandboxConfig = None):
        self.config = config or SandboxConfig()
        self.workspace = self.config.workspace
        self._init_workspace()
    
    def _init_workspace(self):
        """Initialize workspace."""
        os.makedirs(self.workspace, exist_ok=True)
        os.makedirs(f"{self.workspace}/projects", exist_ok=True)
    
    def create_project(self, name: str, template: str = "blank") -> str:
        """Create a new project in sandbox."""
        project_path = f"{self.workspace}/projects/{name}"
        
        if template == "nextjs":
            # Create Next.js project
            os.makedirs(project_path, exist_ok=True)
            with open(f"{project_path}/package.json", "w") as f:
                f.write('{"name": "' + name + '", "version": "1.0.0"}')
        
        elif template == "fastapi":
            os.makedirs(project_path, exist_ok=True)
            with open(f"{project_path}/main.py", "w") as f:
                f.write('from fastapi import FastAPI\napp = FastAPI()\n@app.get("/")\ndef root():\n    return {"message": "Hello"}')
        
        return project_path
    
    def write_file(self, project: str, path: str, content: str):
        """Write file to project."""
        project_path = f"{self.workspace}/projects/{project}"
        filepath = f"{project_path}/{path}"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            f.write(content)
    
    def read_file(self, project: str, path: str) -> str:
        """Read file from project."""
        project_path = f"{self.workspace}/projects/{project}"
        filepath = f"{project_path}/{path}"
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                return f.read()
        return ""
    
    def run_command(self, project: str, command: str, cwd: str = None) -> Dict[str, Any]:
        """Run command in project."""
        project_path = f"{self.workspace}/projects/{project}"
        work_dir = cwd or project_path
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.config.timeout,
                cwd=work_dir,
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Timeout",
                "stdout": "",
                "stderr": f"Command exceeded {self.config.timeout}s",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "stdout": "",
                "stderr": str(e),
            }
    
    def install_dependencies(self, project: str, manager: str = "pip") -> Dict[str, Any]:
        """Install project dependencies."""
        project_path = f"{self.workspace}/projects/{project}"
        
        if manager == "pip":
            return self.run_command(project, "pip install -r requirements.txt")
        elif manager == "npm":
            return self.run_command(project, "npm install")
        
        return {"success": False, "error": f"Unknown manager: {manager}"}
    
    def run_dev_server(self, project: str, port: int = 3000) -> Dict[str, Any]:
        """Start development server."""
        project_path = f"{self.workspace}/projects/{project}"
        
        # Check if package.json exists
        if os.path.exists(f"{project_path}/package.json"):
            # Start npm dev server
            return self.run_command(project, f"npm run dev -- -p {port}")
        
        # Check if main.py exists (FastAPI)
        if os.path.exists(f"{project_path}/main.py"):
            return self.run_command(project, f"uvicorn main:app --host 0.0.0.0 --port {port}")
        
        return {"success": False, "error": "No known entry point found"}
    
    def build_project(self, project: str) -> Dict[str, Any]:
        """Build project."""
        project_path = f"{self.workspace}/projects/{project}"
        
        if os.path.exists(f"{project_path}/package.json"):
            return self.run_command(project, "npm run build")
        
        return {"success": False, "error": "No build system found"}
    
    def list_projects(self) -> List[str]:
        """List all sandbox projects."""
        projects_path = f"{self.workspace}/projects"
        if os.path.exists(projects_path):
            return [d for d in os.listdir(projects_path) 
                    if os.path.isdir(f"{projects_path}/{d}")]
        return []
    
    def delete_project(self, project: str) -> bool:
        """Delete project from sandbox."""
        project_path = f"{self.workspace}/projects/{project}"
        if os.path.exists(project_path):
            shutil.rmtree(project_path)
            return True
        return False
    
    def get_project_files(self, project: str) -> Dict[str, Any]:
        """Get file tree of project."""
        project_path = f"{self.workspace}/projects/{project}"
        
        if not os.path.exists(project_path):
            return {"error": "Project not found"}
        
        files = []
        for root, dirs, filenames in os.walk(project_path):
            for f in filenames:
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, project_path)
                size = os.path.getsize(full_path)
                files.append({
                    "path": rel_path,
                    "size": size,
                })
        
        return {"files": files, "count": len(files)}


# ============================================================================
# SANDBOX TEMPLATES
# ============================================================================

SANDBOX_TEMPLATES = {
    "blank": {
        "description": "Empty project",
        "files": {},
    },
    "nextjs": {
        "description": "Next.js application",
        "files": {
            "package.json": '{"name": "app", "scripts": {"dev": "next dev", "build": "next build"}}',
        },
    },
    "fastapi": {
        "description": "FastAPI application",
        "files": {
            "main.py": "from fastapi import FastAPI\napp = FastAPI()\n@app.get('/')\ndef root():\n    return {'message': 'Hello'}",
            "requirements.txt": "fastapi\nuvicorn",
        },
    },
    "saas": {
        "description": "Full SaaS starter",
        "files": {
            "README.md": "# SaaS App\n\nA SaaS application.",
        },
    },
    "fintech": {
        "description": "Fintech starter",
        "files": {
            "README.md": "# Fintech App\n\nA fintech application.",
        },
    },
}


# ============================================================================
# EXPORTS
# ============================================================================

sandbox = Sandbox()


__all__ = [
    "Sandbox",
    "SandboxConfig",
    "sandbox",
    "SANDBOX_TEMPLATES",
]