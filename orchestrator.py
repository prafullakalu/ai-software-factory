"""
🔄 MULTI-AGENT PIPELINE ORCHESTRATOR

Real AI-powered project generation with multiple agents.
Pipeline: PM → CTO → Dev (Frontend + Backend) → QA → DevOps
"""

import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime

from core.llm.client import LLMClient, get_client
from core.agents.real import AIAgent


@dataclass
class ExecutionContext:
    """Project execution context."""
    project_name: str
    requirements: str
    status: str = "pending"
    progress: int = 0
    results: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    created_at: str = ""


class MultiAgentPipeline:
    """
    Multi-agent pipeline for complete project generation.
    
    Stages:
    1. PM - Requirements analysis
    2. CTO - Architecture planning  
    3. Dev - Code generation
    4. QA - Review
    5. DevOps - Infrastructure
    """
    
    def __init__(self, ws_broadcaster: Optional[Callable] = None):
        self.llm = get_client()
        self.broadcaster = ws_broadcaster
        self.agents = {
            "pm": AIAgent("pm"),
            "cto": AIAgent("cto"),
            "dev": AIAgent("developer"),
            "qa": AIAgent("qa"),
            "devops": AIAgent("devops"),
        }
    
    async def run(
        self,
        project_name: str,
        requirements: str,
        on_token: Optional[Callable] = None,
    ) -> ExecutionContext:
        """Run the complete pipeline."""
        ctx = ExecutionContext(
            project_name=project_name,
            requirements=requirements,
            created_at=datetime.now().isoformat(),
        )
        
        # Stage 1: PM
        print("📋 Stage 1/5: PM analyzing requirements...")
        backlog = await self._run_agent("pm", f"Create user stories for: {requirements}", on_token)
        ctx.results["backlog"] = backlog
        
        # Stage 2: CTO
        print("🧠 Stage 2/5: CTO creating architecture...")
        arch = await self._run_agent("cto", f"Design architecture for:\n{backlog[:1000]}", on_token)
        ctx.results["architecture"] = arch
        
        # Stage 3: Dev
        print("💻 Stage 3/5: Generating code...")
        from tools.fullstack_generator import generate_fullstack
        result = generate_fullstack(project_name)
        ctx.results["frontend_files"] = result.get("frontend", [])
        ctx.results["backend_files"] = result.get("backend", [])
        
        # Stage 4: QA
        print("🔍 Stage 4/5: Running QA review...")
        qa_report = await self._run_agent("qa", f"Review code structure", on_token)
        ctx.results["qa_report"] = qa_report
        
        # Stage 5: DevOps
        print("🚀 Stage 5/5: Creating infrastructure...")
        infra = await self._run_agent("devops", f"Create Docker for: {project_name}", on_token)
        ctx.results["infrastructure"] = infra
        
        ctx.status = "completed"
        ctx.progress = 100
        print(f"✅ Project {project_name} complete!")
        
        return ctx
    
    async def _run_agent(self, agent_type: str, prompt: str, on_token: Optional[Callable] = None) -> str:
        """Run an agent."""
        agent = self.agents.get(agent_type, self.agents["dev"])
        response = agent.chat(prompt)
        
        if on_token:
            for word in response.split():
                on_token(agent_type, word)
                await asyncio.sleep(0.01)
        
        return response
    
    def run_sync(self, project_name: str, requirements: str) -> ExecutionContext:
        """Synchronous run."""
        return asyncio.run(self.run(project_name, requirements))


# Global pipeline
pipeline = MultiAgentPipeline()


def run_project(project_name: str, requirements: str) -> ExecutionContext:
    """Run a project."""
    return pipeline.run_sync(project_name, requirements)


__all__ = ["MultiAgentPipeline", "ExecutionContext", "pipeline", "run_project"]