"""
🏗️ FULLSTACK CODE GENERATOR

Generates COMPLETE working applications!
"""

import os
from typing import Dict, List


# ============================================================================
# REACT + VITE FRONTEND
# ============================================================================

def generate_react(name: str) -> List[str]:
    """Generate React + Vite frontend."""
    base = f"workspace/{name}/frontend"
    files = []
    
    # package.json
    pkg = f'''{{
  "name": "{name}",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {{
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }},
  "dependencies": {{
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0"
  }},
  "devDependencies": {{
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.8"
  }}
}}'''
    write_file(f"{base}/package.json", pkg)
    files.append("package.json")
    
    # vite.config.js
    write_file(f"{base}/vite.config.js", "import { defineConfig } from 'vite'\nexport default defineConfig({ plugins: [] })")
    files.append("vite.config.js")
    
    # index.html
    write_file(f"{base}/index.html", f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{name}</title>
</head>
<body>
  <div id="root"></div>
  <script type="module" src="/src/main.jsx"></script>
</body>
</html>''')
    files.append("index.html")
    
    # src/main.jsx
    write_file(f"{base}/src/main.jsx", '''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)''')
    files.append("src/main.jsx")
    
    # src/index.css
    write_file(f"{base}/src/index.css", '''* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #0a0a0a;
  color: #fff;
  min-height: 100vh;
}
#root { min-height: 100vh; }
.container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
.navbar {
  background: #111;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.nav-links a {
  color: #888;
  text-decoration: none;
  margin-left: 1.5rem;
}
.nav-links a:hover { color: #fff; }
.page { padding: 2rem; }
.page h1 { font-size: 2.5rem; margin-bottom: 1rem; }
.page p { color: #888; margin-bottom: 2rem; }
.btn {
  background: #3b82f6;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
.btn:hover { background: #2563eb; }
input {
  background: #111;
  border: 1px solid #333;
  padding: 0.75rem;
  border-radius: 8px;
  color: #fff;
  width: 100%;
  margin-bottom: 1rem;
}
form { max-width: 400px; }
.card {
  background: #111;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 1rem;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}
.status-badge {
  background: #22c55e;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.75rem;
}''')
    files.append("src/index.css")
    
    # src/App.jsx - Full app with routes!
    write_file(f"{base}/src/App.jsx", f'''import React, {{ useState }} from 'react'
import {{ BrowserRouter, Routes, Route, Link }} from 'react-router-dom'

function Home() {{
  return (
    <div className="page">
      <h1>Welcome to {name}</h1>
      <p>A beautiful modern application</p>
      <Link to="/app" className="btn">Get Started</Link>
    </div>
  )
}}

function Login() {{
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  
  const handleSubmit = (e) => {{
    e.preventDefault()
    alert(`Login: ${{email}}`)
  }}
  
  return (
    <div className="page">
      <h2>Sign In</h2>
      <form onSubmit={{handleSubmit}}>
        <input type="email" placeholder="Email" value={{email}} onChange={{e => setEmail(e.target.value)}} />
        <input type="password" placeholder="Password" value={{password}} onChange={{e => setPassword(e.target.value)}} />
        <button type="submit" className="btn">Sign In</button>
      </form>
    </div>
  )
}}

function Register() {{
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  
  const handleSubmit = (e) => {{
    e.preventDefault()
    alert(`Welcome ${name}!`)
  }}
  
  return (
    <div className="page">
      <h2>Create Account</h2>
      <form onSubmit={{handleSubmit}}>
        <input type="text" placeholder="Name" value={name} onChange={{e => setName(e.target.value)}} />
        <input type="email" placeholder="Email" value={{email}} onChange={{e => setEmail(e.target.value)}} />
        <input type="password" placeholder="Password" value={{password}} onChange={{e => setPassword(e.target.value)}} />
        <button type="submit" className="btn">Create Account</button>
      </form>
    </div>
  )
}}

function Dashboard() {{
  const items = [
    {{ id: 1, title: 'Dashboard', value: '100', label: 'Total' }},
    {{ id: 2, title: 'Active', value: '45', label: 'Active' }},
    {{ id: 3, title: 'Pending', value: '12', label: 'Pending' }},
  ]
  
  return (
    <div className="page">
      <h1>Dashboard</h1>
      <div className="grid">
        {{items.map(item => (
          <div key={{item.id}} className="card">
            <p style={{{{color: '#888'}}}}>{{item.label}}</p>
            <h2>{{item.value}}</h2>
          </div>
        ))}}
      </div>
    </div>
  )
}}

function App() {{
  return (
    <BrowserRouter>
      <div className="navbar">
        <Link to="/" style={{{{color: '#fff', textDecoration: 'none', fontWeight: 'bold'}}}}>{name}</Link>
        <div className="nav-links">
          <Link to="/">Home</Link>
          <Link to="/app">App</Link>
          <Link to="/login">Login</Link>
        </div>
      </div>
      <Routes>
        <Route path="/" element={{<Home />}} />
        <Route path="/app" element={{<Dashboard />}} />
        <Route path="/login" element={{<Login />}} />
        <Route path="/register" element={{<Register />}} />
      </Routes>
    </BrowserRouter>
  )
}}

export default App''')
    files.append("src/App.jsx")
    
    return files


# ============================================================================
# FASTAPI BACKEND
# ============================================================================

def generate_fastapi(name: str) -> List[str]:
    """Generate FastAPI backend."""
    base = f"workspace/{name}/backend"
    files = []
    
    # requirements.txt
    write_file(f"{base}/requirements.txt", """fastapi==0.104.1
uvicorn[standard]==0.24.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.4.4
python-multipart==0.0.6
sqlalchemy==2.0.23
pydantic==2.5.2
""")
    files.append("requirements.txt")
    
    # main.py - Full API!
    write_file(f"{base}/main.py", f'''"""{name} - FastAPI Backend"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, timedelta
import hashlib
import secrets

app = FastAPI(
    title="{name} API",
    description="Complete REST API for {name}",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database
users_db = {{}}
items_db = []
user_id = 1
item_id = 1

# Models
class User(BaseModel):
    id: Optional[int] = None
    email: str
    name: str
    password: str

class Item(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    user_id: int

class Token(BaseModel):
    access_token: str
    token_type: str

def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_pw(plain: str, hashed: str) -> bool:
    return hash_pw(plain) == hashed

def new_token() -> str:
    return secrets.token_urlsafe(32)

# Routes
@app.get("/")
def root():
    return {{"message": "{name} API", "version": "1.0.0"}}

@app.get("/health")
def health():
    return {{"status": "healthy", "time": datetime.now().isoformat()}}

@app.post("/register", status_code=201)
def register(user: User):
    global user_id
    if user.email in users_db:
        raise HTTPException(400, "Email exists")
    users_db[user.email] = {{"id": user_id, "email": user.email, "name": user.name, "password": hash_pw(user.password)}}
    user_id += 1
    return {{"email": user.email, "name": user.name}}

@app.post("/token", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form.username)
    if not user or not verify_pw(form.password, user.get("password", "")):
        raise HTTPException(400, "Wrong credentials")
    return {{"access_token": new_token(), "token_type": "bearer"}}

@app.get("/items", response_model=List[Item])
def get_items():
    return items_db

@app.post("/items", response_model=Item)
def create_item(item: Item):
    global item_id
    item.id = item_id
    item_id += 1
    items_db.append(item)
    return item

@app.get("/items/{{item_id}}", response_model=Item)
def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(404, "Not found")

@app.put("/items/{{item_id}}", response_model=Item)
def update_item(item_id: int, item: Item):
    for i, existing in enumerate(items_db):
        if existing.id == item_id:
            item.id = item_id
            items_db[i] = item
            return item
    raise HTTPException(404, "Not found")

@app.delete("/items/{{item_id}}")
def delete_item(item_id: int):
    for i, item in enumerate(items_db):
        if item.id == item_id:
            items_db.pop(i)
            return {{"deleted": True}}
    raise HTTPException(404, "Not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
''')
    files.append("main.py")
    
    return files


# ============================================================================
# GENERATOR
# ============================================================================

def write_file(path: str, content: str):
    """Write a file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def generate_fullstack(name: str) -> Dict[str, List]:
    """Generate fullstack app."""
    os.makedirs(f"workspace/{name}", exist_ok=True)
    
    frontend_files = generate_react(name)
    backend_files = generate_fastapi(name)
    
    return {
        "frontend": frontend_files,
        "backend": backend_files,
    }


__all__ = ["generate_fullstack", "generate_react", "generate_fastapi"]