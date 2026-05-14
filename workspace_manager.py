"""
🏗️ PROJECT WORKSPACE MANAGER
"""

import os
from typing import Optional, List


WORKSPACE_DIR = "workspace"


class Workspace:
    """Manage project workspace."""
    
    def __init__(self):
        self.current_project: str = None
    
    def init_project(self, name: str) -> str:
        """Initialize a new project."""
        self.current_project = name
        base = f"{WORKSPACE_DIR}/{name}"
        os.makedirs(f"{base}/frontend/src", exist_ok=True)
        os.makedirs(f"{base}/backend", exist_ok=True)
        
        # Create React app
        with open(f"{base}/frontend/package.json", "w") as f:
            f.write(f'{{"name": "{name}", "scripts": {{"dev": "vite"}}, "dependencies": {{"react": "^18.2.0"}}}}')
        with open(f"{base}/frontend/index.html", "w") as f:
            f.write(f'<div id="root"></div><script src="/src/main.jsx"></script>')
        os.makedirs(f"{base}/frontend/src", exist_ok=True)
        with open(f"{base}/frontend/src/main.jsx", "w") as f:
            f.write('import React from "react"; import ReactDOM from "react-dom/client"; import App from "./App.jsx"; ReactDOM.createRoot(document.getElementById("root")).render(<App />)')
        with open(f"{base}/frontend/src/App.jsx", "w") as f:
            f.write('''import React from "react"; function Home() { return <div><h1>''' + name + '''</h1></div> }}
function App() { return <div><Home /></div> }}
export default App''')
        
        # Create FastAPI
        with open(f"{base}/backend/main.py", "w") as f:
            content = 'from fastapi import FastAPI\napp = FastAPI(title="' + name + '")\n@app.get("/")\ndef root(): return {"message": "' + name + ' API"}\nif __name__ == "__main__": import uvicorn; uvicorn.run(app)'
            f.write(content)
        with open(f"{base}/backend/requirements.txt", "w") as f:
            f.write("fastapi\nuvicorn\n")
        
        return f"✅ Project '{name}' initialized"
    
    def read_file(self, path: str) -> Optional[str]:
        """Read a file."""
        full = f"{WORKSPACE_DIR}/{self.current_project}/{path}"
        if os.path.exists(full):
            with open(full) as f:
                return f.read()
        return None
    
    def write_file(self, path: str, content: str) -> str:
        """Write a file."""
        full = f"{WORKSPACE_DIR}/{self.current_project}/{path}"
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f:
            f.write(content)
        return f"✅ Written: {path}"
    
    def edit_file(self, path: str, old: str, new: str) -> str:
        """Edit a file."""
        content = self.read_file(path)
        if content and old in content:
            content = content.replace(old, new)
            return self.write_file(path, content)
        return f"❌ Could not find in {path}"
    
    def list_files(self) -> List[str]:
        """List files."""
        base = f"{WORKSPACE_DIR}/{self.current_project}"
        if not os.path.exists(base):
            return []
        files = []
        for root, _, filenames in os.walk(base):
            for f in filenames:
                rel = os.path.relpath(os.path.join(root, f), base)
                files.append(rel)
        return files
    
    def get_status(self) -> str:
        """Get status."""
        files = self.list_files()
        return f"📁 Project: {self.current_project}\n📄 Files: {len(files)}"


workspace = Workspace()

def init(name: str) -> str:
    return workspace.init_project(name)

def read(path: str) -> Optional[str]:
    return workspace.read_file(path)

def write(path: str, content: str) -> str:
    return workspace.write_file(path, content)

def edit(path: str, old: str, new: str) -> str:
    return workspace.edit_file(path, old, new)

def status() -> str:
    return workspace.get_status()

def build() -> str:
    return f"cd workspace/{workspace.current_project} && npm install"