"""
💾 MEMORY

Shared memory and context management for agents.
"""

from typing import Any, Dict, Optional
from datetime import datetime


class AgentMemory:
    """Memory storage for individual agent."""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.history = []
        self.context = {}
        self.created_at = datetime.now()
    
    def add(self, key: str, value: Any):
        """Add to memory."""
        self.context[key] = value
        self.history.append({"key": key, "value": value, "time": datetime.now()})
    
    def get(self, key: str, default=None) -> Any:
        """Get from memory."""
        return self.context.get(key, default)
    
    def clear(self):
        """Clear memory."""
        self.context.clear()
        self.history.clear()


class SharedMemory:
    """Shared memory across all agents."""
    
    def __init__(self):
        self.agents: Dict[str, AgentMemory] = {}
        self.global_context = {}
    
    def get_agent_memory(self, agent_id: str) -> AgentMemory:
        """Get or create agent memory."""
        if agent_id not in self.agents:
            self.agents[agent_id] = AgentMemory(agent_id)
        return self.agents[agent_id]
    
    def set_global(self, key: str, value: Any):
        """Set global context."""
        self.global_context[key] = value
    
    def get_global(self, key: str, default=None) -> Any:
        """Get global context."""
        return self.global_context.get(key, default)


# Global instance
shared_memory = SharedMemory()


__all__ = ["AgentMemory", "SharedMemory", "shared_memory"]