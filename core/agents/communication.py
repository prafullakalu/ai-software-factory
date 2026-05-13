"""
💬 AGENT COMMUNICATION

Agents can communicate and collaborate.
Like Hermes Agent - multiple agents working together.
"""

import uuid
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# MESSAGE TYPES
# ============================================================================

class MessageType(Enum):
    REQUEST = "request"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    ALERT = "alert"


# ============================================================================
# MESSAGE MODEL
# ============================================================================

@dataclass
class AgentMessage:
    """Message between agents."""
    id: str
    from_agent: str
    to_agent: str
    type: MessageType
    content: str
    timestamp: str
    metadata: Dict = field(default_factory=dict)


# ============================================================================
# AGENT BUS
# ============================================================================

class AgentBus:
    """
    Message bus for agent communication.
    Like Hermes Agent - agents can talk to each other.
    """
    
    def __init__(self):
        self.agents: Dict[str, str] = {}  # agent_name -> status
        self.messages: Dict[str, List[AgentMessage]] = {}
        self.message_queue: List[AgentMessage] = []
    
    def register(self, agent_name: str, status: str = "idle"):
        """Register an agent."""
        self.agents[agent_name] = status
        self.messages[agent_name] = []
    
    def unregister(self, agent_name: str):
        """Unregister agent."""
        if agent_name in self.agents:
            del self.agents[agent_name]
    
    def set_status(self, agent_name: str, status: str):
        """Set agent status."""
        if agent_name in self.agents:
            self.agents[agent_name] = status
    
    def get_status(self, agent_name: str) -> str:
        """Get agent status."""
        return self.agents.get(agent_name, "unknown")
    
    def send_message(
        self,
        from_agent: str,
        to_agent: str,
        content: str,
        msg_type: MessageType = MessageType.REQUEST,
        metadata: Dict = None,
    ) -> str:
        """Send message to another agent."""
        msg_id = str(uuid.uuid4())[:8]
        
        message = AgentMessage(
            id=msg_id,
            from_agent=from_agent,
            to_agent=to_agent,
            type=msg_type,
            content=content,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            metadata=metadata or {},
        )
        
        # Add to recipient's inbox
        if to_agent not in self.messages:
            self.messages[to_agent] = []
        self.messages[to_agent].append(message)
        
        # Add to queue
        self.message_queue.append(message)
        
        return msg_id
    
    def broadcast(self, from_agent: str, content: str):
        """Broadcast to all agents."""
        for to_agent in self.agents:
            if to_agent != from_agent:
                self.send_message(
                    from_agent,
                    to_agent,
                    content,
                    MessageType.BROADCAST,
                )
    
    def get_messages(self, agent_name: str) -> List[AgentMessage]:
        """Get messages for agent."""
        return self.messages.get(agent_name, [])
    
    def get_next_message(self, agent_name: str) -> Optional[AgentMessage]:
        """Get next message."""
        messages = self.messages.get(agent_name, [])
        if messages:
            return messages[0]
        return None
    
    def acknowledge_message(self, agent_name: str, message_id: str):
        """Acknowledge and remove message."""
        if agent_name in self.messages:
            self.messages[agent_name] = [
                m for m in self.messages[agent_name]
                if m.id != message_id
            ]
    
    def list_agents(self) -> Dict[str, str]:
        """List all registered agents."""
        return dict(self.agents)
    
    def get_stats(self) -> Dict:
        """Get bus statistics."""
        total_messages = sum(len(v) for v in self.messages.values())
        
        return {
            "registered_agents": len(self.agents),
            "total_messages": total_messages,
            "queued_messages": len(self.message_queue),
        }


# ============================================================================
# AGENT TEAM
# ============================================================================

class AgentTeam:
    """
    Team of agents working together.
    Like Paperclip - orchestration of multiple agents.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.bus = AgentBus()
        self.tasks: Dict[str, str] = {}  # task_id -> assigned_agent
    
    def add_agent(self, agent_name: str):
        """Add agent to team."""
        self.bus.register(agent_name)
    
    def remove_agent(self, agent_name: str):
        """Remove agent from team."""
        self.bus.unregister(agent_name)
        # Unassign tasks
        for task_id, agent in list(self.tasks.items()):
            if agent == agent_name:
                self.tasks[task_id] = None
    
    def assign_task(self, task_id: str, agent_name: str):
        """Assign task to agent."""
        self.bus.set_status(agent_name, "working")
        self.tasks[task_id] = agent_name
    
    def complete_task(self, task_id: str):
        """Mark task complete."""
        if task_id in self.tasks:
            agent_name = self.tasks[task_id]
            self.bus.set_status(agent_name, "idle")
            del self.tasks[task_id]
    
    def get_agent_tasks(self, agent_name: str) -> List[str]:
        """Get tasks for agent."""
        return [tid for tid, an in self.tasks.items() if an == agent_name]
    
    def delegate(self, from_agent: str, to_agent: str, content: str) -> str:
        """Delegate task to another agent."""
        return self.bus.send_message(
            from_agent,
            to_agent,
            content,
            MessageType.REQUEST,
        )
    
    def get_status(self) -> Dict:
        """Get team status."""
        return {
            "name": self.name,
            "agents": self.bus.list_agents(),
            "active_tasks": len(self.tasks),
        }


# ============================================================================
# EXPORTS
# ============================================================================

agent_bus = AgentBus()
agent_team = AgentTeam("default")

__all__ = [
    "MessageType",
    "AgentMessage",
    "AgentBus",
    "AgentTeam",
    "agent_bus",
    "agent_team",
]