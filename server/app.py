"""
🏭 AI SOFTWARE FACTORY API SERVER

WebSocket + REST API server that bridges CLI and UI.
"""

import asyncio
import json
import uuid
from pathlib import Path
from typing import Dict, List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(title="AI Software Factory API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# WEBSOCKET MANAGER
# ============================================================================

class ConnectionManager:
    """Manage WebSocket connections."""
    
    def __init__(self):
        self.active: Dict[str, WebSocket] = {}
    
    async def connect(self, ws: WebSocket, client_id: str):
        await ws.accept()
        self.active[client_id] = ws
    
    def disconnect(self, client_id: str):
        self.active.pop(client_id, None)
    
    async def send(self, client_id: str, message: dict):
        ws = self.active.get(client_id)
        if ws:
            await ws.send_json(message)
    
    async def broadcast(self, message: dict):
        dead = []
        for cid, ws in self.active.items():
            try:
                await ws.send_json(message)
            except:
                dead.append(cid)
        for cid in dead:
            self.disconnect(cid)


manager = ConnectionManager()


# ============================================================================
# MODELS
# ============================================================================

class ProjectRequest(BaseModel):
    name: str
    requirements: str


class AgentChatRequest(BaseModel):
    agent: str
    message: str


# ============================================================================
# WEBSOCKET ENDPOINT
# ============================================================================

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(ws: WebSocket, client_id: str):
    """WebSocket for real-time events."""
    await manager.connect(ws, client_id)
    try:
        while True:
            data = await ws.receive_json()
            await handle_message(client_id, data)
    except WebSocketDisconnect:
        manager.disconnect(client_id)


async def handle_message(client_id: str, data: dict):
    """Handle WebSocket messages."""
    msg_type = data.get("type")
    
    if msg_type == "run_project":
        name = data.get("name")
        requirements = data.get("requirements")
        asyncio.create_task(run_project(client_id, name, requirements))
    
    elif msg_type == "agent_chat":
        agent = data.get("agent")
        message = data.get("message")
        asyncio.create_task(agent_chat(client_id, agent, message))
    
    elif msg_type == "analyze":
        path = data.get("path", ".")
        asyncio.create_task(run_analyze(client_id, path))


async def run_project(client_id: str, name: str, requirements: str):
    """Run project generation."""
    from tools.fullstack_generator import generate_fullstack
    
    await manager.send(client_id, {
        "type": "step_start",
        "step": "generate",
        "description": f"Generating {name}..."
    })
    
    result = generate_fullstack(name)
    
    await manager.send(client_id, {
        "type": "file_list",
        "files": result.get("frontend", []) + result.get("backend", [])
    })
    
    await manager.send(client_id, {
        "type": "project_done",
        "project": name,
        "files": result
    })


async def agent_chat(client_id: str, agent_type: str, message: str):
    """Chat with an agent."""
    from core.agents.real import run_agent
    
    await manager.send(client_id, {
        "type": "agent_start",
        "agent": agent_type,
        "message": message
    })
    
    response = run_agent(agent_type, message)
    
    # Stream response
    for word in response.split():
        await manager.send(client_id, {
            "type": "agent_token",
            "agent": agent_type,
            "token": word
        })
        await asyncio.sleep(0.02)
    
    await manager.send(client_id, {
        "type": "agent_done",
        "agent": agent_type,
        "full_response": response
    })


async def run_analyze(client_id: str, path: str):
    """Run codebase analysis."""
    from core.analyzer.codebase import analyze_and_report
    
    await manager.send(client_id, {"type": "analyze_start", "path": path})
    
    report = analyze_and_report(path)
    
    await manager.send(client_id, {
        "type": "analyze_done",
        "report": report
    })


# ============================================================================
# REST API
# ============================================================================

@app.get("/")
def root():
    return {"message": "AI Software Factory API", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/api/projects")
async def list_projects():
    """List all projects."""
    workspace = Path("workspace")
    if not workspace.exists():
        return []
    
    projects = []
    for p in workspace.iterdir():
        if p.is_dir():
            projects.append({
                "name": p.name,
                "path": str(p),
                "files": len(list(p.rglob("*")))
            })
    return projects


@app.post("/api/projects")
async def create_project(req: ProjectRequest):
    """Create a new project."""
    from tools.fullstack_generator import generate_fullstack
    
    result = generate_fullstack(req.name)
    
    await manager.broadcast({
        "type": "project_created",
        "name": req.name,
        "result": result
    })
    
    return {"name": req.name, "result": result}


@app.get("/api/projects/{name}")
async def get_project(name: str):
    """Get project details."""
    path = Path(f"workspace/{name}")
    if not path.exists():
        raise HTTPException(404, "Project not found")
    
    files = []
    for f in path.rglob("*"):
        if f.is_file():
            files.append({
                "path": str(f.relative_to(path)),
                "size": f.stat().st_size
            })
    
    return {"name": name, "path": str(path), "files": files}


@app.get("/api/projects/{name}/files/{path:path}")
async def get_file(name: str, path: str):
    """Get file content."""
    file_path = Path(f"workspace/{name}/{path}")
    if not file_path.exists():
        raise HTTPException(404, "File not found")
    
    content = file_path.read_text()
    return {"path": path, "content": content}


@app.get("/api/agents")
async def list_agents():
    """List all agents."""
    from core.agents.real import list_agents
    return list_agents()


@app.post("/api/agents/{agent_type}/chat")
async def agent_chat_api(agent_type: str, req: AgentChatRequest):
    """Chat with an agent via REST."""
    from core.agents.real import run_agent
    
    response = run_agent(agent_type, req.message)
    return {"agent": agent_type, "response": response}


@app.get("/api/analyze")
async def analyze(path: str = "."):
    """Analyze a codebase."""
    from core.analyzer.codebase import analyze_and_report
    return {"report": analyze_and_report(path)}


@app.post("/api/analyze")
async def analyze_post(path: str = "."):
    """Analyze a codebase."""
    from core.analyzer.codebase import analyze_and_report
    return {"report": analyze_and_report(path)}


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)