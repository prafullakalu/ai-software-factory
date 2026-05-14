"""
🏗️ CODE GENERATOR

Generates actual code files from templates.
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass


# ============================================================================
# FRONTEND TEMPLATES
# ============================================================================

REACT_APP_TEMPLATE = """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""

REACT_APP_COMPONENT = """import React, {{ useState, useEffect }} from 'react';
import {{ BrowserRouter, Routes, Route, Link }} from 'react-router-dom';
import './App.css';

function Home() {{
  return (
    <div className="home">
      <h1>Welcome to {project_name}</h1>
      <p>Build amazing things with React</p>
    </div>
  );
}}

function Login() {{
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {{
    e.preventDefault();
    console.log('Login:', {{ email, password }});
  }};

  return (
    <div className="login">
      <h2>Login</h2>
      <form onSubmit={{handleSubmit}}>
        <input
          type="email"
          placeholder="Email"
          value={{email}}
          onChange={{(e) => setEmail(e.target.value)}}
        />
        <input
          type="password"
          placeholder="Password"
          value={{password}}
          onChange={{(e) => setPassword(e.target.value)}}
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}}

function Dashboard() {{
  return (
    <div className="dashboard">
      <nav>
        <Link to="/">Home</Link>
        <Link to="/settings">Settings</Link>
      </nav>
      <main>
        <h1>Dashboard</h1>
        <p>Welcome back!</p>
      </main>
    </div>
  );
}}

export default function App() {{
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={{<Home />}} />
        <Route path="/login" element={{<Login />}} />
        <Route path="/dashboard" element={{<Dashboard />}} />
      </Routes>
    </BrowserRouter>
  );
}}
"""

REACT_CSS = """* {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}

body {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f5f5f5;
  color: #333;
}}

.home, .login, .dashboard {{
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}}

h1 {{
  font-size: 2rem;
  margin-bottom: 1rem;
}}

form {{
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 400px;
}}

input {{
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}}

button {{
  padding: 0.75rem 1.5rem;
  background: #0070f3;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}}

button:hover {{
  background: #0051cc;
}}

nav {{
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: white;
  border-bottom: 1px solid #eee;
}}

nav a {{
  color: #0070f3;
  text-decoration: none;
}}
"""

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{project_name}</title>
</head>
<body>
  <div id="root"></div>
</body>
</html>
"""

PACKAGE_JSON = """{{
  "name": "{project_name}",
  "version": "1.0.0",
  "private": true,
  "dependencies": {{
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "react-scripts": "5.0.1"
  }},
  "scripts": {{
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }},
  "browserslist": {{
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }}
}}
"""

# ============================================================================
# BACKEND TEMPLATES
# ============================================================================

FASTAPI_MAIN = '''"""{project_name} - FastAPI Backend"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

app = FastAPI(title="{project_name}", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class User(BaseModel):
    id: Optional[int] = None
    email: str
    name: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

# In-memory database
users_db: List[User] = []
user_id_counter = 1

@app.get("/")
def root():
    return {{"message": "{project_name} API", "version": "1.0.0"}}

@app.get("/health")
def health():
    return {{"status": "healthy"}}

@app.get("/api/users")
def get_users():
    return users_db

@app.post("/api/users")
def create_user(user: User):
    global user_id_counter
    user.id = user_id_counter
    user_id_counter += 1
    users_db.append(user)
    return user

@app.post("/api/auth/login")
def login(request: LoginRequest):
    for user in users_db:
        if user.email == request.email:
            return {{"token": "demo-token", "user": user}}
    raise HTTPException(status_code=401, detail="Invalid credentials")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

# ============================================================================
# CODE GENERATOR
# ============================================================================

@dataclass
class GeneratedFile:
    """A generated file."""
    path: str
    content: str


class CodeGenerator:
    """Generate code from templates."""
    
    def __init__(self):
        self.output_dir = "workspace/generated"
    
    def generate_react_app(self, project_name: str = "my-app") -> List[GeneratedFile]:
        """Generate a React app."""
        os.makedirs(self.output_dir, exist_ok=True)
        
        files = [
            GeneratedFile(f"{self.output_dir}/src/main.jsx", REACT_APP_TEMPLATE),
            GeneratedFile(f"{self.output_dir}/src/App.jsx", REACT_APP_COMPONENT.format(project_name=project_name)),
            GeneratedFile(f"{self.output_dir}/src/index.css", REACT_CSS),
            GeneratedFile(f"{self.output_dir}/public/index.html", INDEX_HTML.format(project_name=project_name)),
            GeneratedFile(f"{self.output_dir}/package.json", PACKAGE_JSON.format(project_name=project_name)),
        ]
        
        # Write files
        for f in files:
            os.makedirs(os.path.dirname(f.path), exist_ok=True)
            with open(f.path, "w") as file:
                file.write(f.content)
        
        return files
    
    def generate_fastapi_app(self, project_name: str = "my-api") -> List[GeneratedFile]:
        """Generate a FastAPI app."""
        os.makedirs(self.output_dir, exist_ok=True)
        
        main_content = FASTAPI_MAIN.format(project_name=project_name)
        
        files = [
            GeneratedFile(f"{self.output_dir}/main.py", main_content),
            GeneratedFile(f"{self.output_dir}/requirements.txt", "fastapi\nuvicorn\npydantic\npython-multipart\n"),
        ]
        
        for f in files:
            with open(f.path, "w") as file:
                file.write(f.content)
        
        return files
    
    def generate_fullstack(self, project_name: str = "my-app") -> Dict[str, List[GeneratedFile]]:
        """Generate fullstack app."""
        return {
            "frontend": self.generate_react_app(project_name),
            "backend": self.generate_fastapi_app(project_name),
        }


# ============================================================================
# EXPORTS
# ============================================================================

code_generator = CodeGenerator()

def generate_frontend(project_name: str = "my-app") -> List[GeneratedFile]:
    """Generate frontend."""
    return code_generator.generate_react_app(project_name)

def generate_backend(project_name: str = "my-api") -> List[GeneratedFile]:
    """Generate backend."""
    return code_generator.generate_fastapi_app(project_name)

def generate_fullstack(project_name: str = "my-app") -> Dict[str, List[GeneratedFile]]:
    """Generate fullstack."""
    return code_generator.generate_fullstack(project_name)


__all__ = [
    "CodeGenerator",
    "code_generator",
    "generate_frontend",
    "generate_backend",
    "generate_fullstack",
]