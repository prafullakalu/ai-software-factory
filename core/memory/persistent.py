"""
💾 PERSISTENT MEMORY SYSTEM

Persistent memory that remembers everything across sessions.
Like Hermes Agent - stores in ~/.hermes/
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


# ============================================================================
# MEMORY CONFIG
# ============================================================================

class MemoryConfig:
    """Memory storage configuration."""
    def __init__(self, storage_path: str = None):
        if storage_path:
            self.storage_path = storage_path
        else:
            # Default: ~/.hermes/
            home = os.path.expanduser("~")
            self.storage_path = os.path.join(home, ".hermes", "memory")
        
        self.conversations_file = os.path.join(self.storage_path, "conversations.json")
        self.facts_file = os.path.join(self.storage_path, "facts.json")
        self.skills_file = os.path.join(self.storage_path, "skills.json")
        self.projects_file = os.path.join(self.storage_path, "projects.json")
        
        os.makedirs(self.storage_path, exist_ok=True)


# ============================================================================
# MEMORY TYPES
# ============================================================================

@dataclass
class MemoryItem:
    """Single memory item."""
    id: str
    content: str
    category: str  # conversation, fact, skill, project
    timestamp: str
    importance: int  # 1-10
    tags: List[str]
    metadata: Dict
    
    def to_dict(self) -> Dict:
        return asdict(self)


class PersistentMemory:
    """
    Persistent memory system like Hermes Agent.
    Stores everything in local filesystem.
    """
    
    def __init__(self, config: MemoryConfig = None):
        self.config = config or MemoryConfig()
        self.conversations: Dict[str, List[MemoryItem]] = {}
        self.facts: Dict[str, MemoryItem] = {}
        self.skills: Dict[str, Dict] = {}
        self.projects: Dict[str, Dict] = {}
        
        # Load existing memory
        self._load_all()
    
    def _load_all(self):
        """Load all memory from disk."""
        # Load conversations
        if os.path.exists(self.config.conversations_file):
            with open(self.config.conversations_file, "r") as f:
                data = json.load(f)
                self.conversations = {
                    k: [MemoryItem(**item) for item in v] 
                    for k, v in data.items()
                }
        
        # Load facts
        if os.path.exists(self.config.facts_file):
            with open(self.config.facts_file, "r") as f:
                data = json.load(f)
                self.facts = {k: MemoryItem(**v) for k, v in data.items()}
        
        # Load skills
        if os.path.exists(self.config.skills_file):
            with open(self.config.skills_file, "r") as f:
                self.skills = json.load(f)
        
        # Load projects
        if os.path.exists(self.config.projects_file):
            with open(self.config.projects_file, "r") as f:
                self.projects = json.load(f)
    
    def _save_all(self):
        """Save all memory to disk."""
        # Save conversations
        with open(self.config.conversations_file, "w") as f:
            data = {
                k: [item.to_dict() for item in v] 
                for k, v in self.conversations.items()
            }
            json.dump(data, f, indent=2)
        
        # Save facts
        with open(self.config.facts_file, "w") as f:
            data = {k: v.to_dict() for k, v in self.facts.items()}
            json.dump(data, f, indent=2)
        
        # Save skills
        with open(self.config.skills_file, "w") as f:
            json.dump(self.skills, f, indent=2)
        
        # Save projects
        with open(self.config.projects_file, "w") as f:
            json.dump(self.projects, f, indent=2)
    
    # ============================================================================
    # CORE OPERATIONS
    # ============================================================================
    
    def add_memory(
        self,
        content: str,
        category: str,
        importance: int = 5,
        tags: List[str] = None,
        metadata: Dict = None,
    ) -> str:
        """Add a new memory."""
        # Generate ID
        content_hash = hashlib.md5(content.encode()).hexdigest()[:12]
        timestamp = datetime.now().isoformat()
        
        memory = MemoryItem(
            id=content_hash,
            content=content,
            category=category,
            timestamp=timestamp,
            importance=importance,
            tags=tags or [],
            metadata=metadata or {},
        )
        
        # Store based on category
        if category == "conversation":
            session_id = metadata.get("session_id", "default") if metadata else "default"
            if session_id not in self.conversations:
                self.conversations[session_id] = []
            self.conversations[session_id].append(memory)
        
        elif category == "fact":
            self.facts[content_hash] = memory
        
        self._save_all()
        return content_hash
    
    def recall(self, query: str, category: str = None, limit: int = 10) -> List[MemoryItem]:
        """Recall memories matching query."""
        results = []
        query_lower = query.lower()
        
        # Search facts
        for memory in self.facts.values():
            if category and memory.category != category:
                continue
            if query_lower in memory.content.lower():
                results.append(memory)
        
        # Search conversations
        for session_memories in self.conversations.values():
            for memory in session_memories:
                if category and memory.category != category:
                    continue
                if query_lower in memory.content.lower():
                    results.append(memory)
        
        # Sort by importance and return
        results.sort(key=lambda x: x.importance, reverse=True)
        return results[:limit]
    
    def learn_fact(self, fact: str, tags: List[str] = None) -> str:
        """Learn a new fact."""
        return self.add_memory(
            content=fact,
            category="fact",
            importance=8,
            tags=tags or [],
        )
    
    def remember_project(self, project_name: str, details: Dict) -> str:
        """Remember project details."""
        self.projects[project_name] = {
            "details": details,
            "updated": datetime.now().isoformat(),
        }
        self._save_all()
        return project_name
    
    def get_project_context(self, project_name: str) -> Optional[Dict]:
        """Get all context about a project."""
        return self.projects.get(project_name)
    
    # ============================================================================
    # SKILL MANAGEMENT (like Hermes Agent)
    # ============================================================================
    
    def create_skill(
        self,
        name: str,
        description: str,
        code: str,
        triggers: List[str],
    ) -> str:
        """Create a new skill that the agent can use."""
        skill_id = hashlib.md5(name.encode()).hexdigest()[:8]
        
        self.skills[skill_id] = {
            "id": skill_id,
            "name": name,
            "description": description,
            "code": code,
            "triggers": triggers,
            "created": datetime.now().isoformat(),
            "usage_count": 0,
        }
        
        self._save_all()
        return skill_id
    
    def find_skill(self, query: str) -> List[Dict]:
        """Find skills matching query."""
        results = []
        query_lower = query.lower()
        
        for skill in self.skills.values():
            if (query_lower in skill["name"].lower() or
                query_lower in skill["description"].lower() or
                any(query_lower in t.lower() for t in skill.get("triggers", []))):
                results.append(skill)
        
        return results
    
    def use_skill(self, skill_id: str) -> bool:
        """Increment skill usage count."""
        if skill_id in self.skills:
            self.skills[skill_id]["usage_count"] += 1
            self._save_all()
            return True
        return False
    
    # ============================================================================
    # SESSION MANAGEMENT
    # ============================================================================
    
    def start_session(self, session_id: str = None) -> str:
        """Start a new conversation session."""
        if not session_id:
            session_id = hashlib.md5(
                datetime.now().isoformat().encode()
            ).hexdigest()[:12]
        
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        return session_id
    
    def add_to_session(self, session_id: str, message: str, role: str = "user"):
        """Add message to session."""
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        self.add_memory(
            content=message,
            category="conversation",
            importance=5,
            metadata={"session_id": session_id, "role": role},
        )
    
    def get_session_history(self, session_id: str, limit: int = 50) -> List[MemoryItem]:
        """Get conversation history for session."""
        if session_id not in self.conversations:
            return []
        
        memories = self.conversations[session_id]
        return memories[-limit:]
    
    # ============================================================================
    # CONTEXT BUILDING
    # ============================================================================
    
    def build_context(self, query: str = None) -> str:
        """Build context string for AI."""
        context_parts = []
        
        # Get relevant memories
        if query:
            memories = self.recall(query, limit=5)
            if memories:
                context_parts.append("## Relevant Memories")
                for m in memories:
                    context_parts.append(f"- {m.content}")
        
        # Get recent conversations
        all_sessions = list(self.conversations.values())
        if all_sessions:
            recent = all_sessions[-1][-3:] if all_sessions[-1] else []
            if recent:
                context_parts.append("\n## Recent Conversation")
                for m in recent:
                    context_parts.append(f"- {m.content}")
        
        # Get project context
        if self.projects:
            context_parts.append("\n## Known Projects")
            for name, proj in self.projects.items():
                context_parts.append(f"- {name}")
        
        return "\n".join(context_parts) if context_parts else ""
    
    # ============================================================================
    # UTILITIES
    # ============================================================================
    
    def get_stats(self) -> Dict:
        """Get memory statistics."""
        total_conversations = sum(len(v) for v in self.conversations.values())
        
        return {
            "total_conversations": total_conversations,
            "total_facts": len(self.facts),
            "total_skills": len(self.skills),
            "total_projects": len(self.projects),
            "storage_path": self.config.storage_path,
        }
    
    def clear_old_sessions(self, keep_recent: int = 5):
        """Clear old conversation sessions."""
        sessions = sorted(
            self.conversations.keys(),
            key=lambda x: self.conversations[x][-1].timestamp if self.conversations[x] else "",
            reverse=True
        )
        
        for session_id in sessions[keep_recent:]:
            del self.conversations[session_id]
        
        self._save_all()


# ============================================================================
# EXPORTS
# ============================================================================

# Global memory instance
memory = PersistentMemory()


def remember(query: str, importance: int = 5):
    """Quick remember function."""
    return memory.add_memory(query, "fact", importance)


def recall(query: str, limit: int = 5):
    """Quick recall function."""
    return memory.recall(query, limit=limit)


__all__ = [
    "MemoryConfig",
    "MemoryItem",
    "PersistentMemory",
    "memory",
    "remember",
    "recall",
]