"""
💾 PERSISTENT MEMORY SYSTEM

Persists to disk, supports namespaces, keyword search.
"""

import json
import hashlib
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional


MEMORY_DIR = Path.home() / ".aifactory"
MEMORY_FILE = MEMORY_DIR / "memory.json"


@dataclass
class Memory:
    id: str
    content: str
    namespace: str
    created_at: str
    tags: List[str] = field(default_factory=list)


class PersistentMemory:
    """Persistent memory that survives restarts."""
    
    def __init__(self, path: Optional[Path] = None):
        self.path = path or MEMORY_FILE
        self._memories: List[Memory] = []
        self._load()
    
    def _load(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            try:
                data = json.loads(self.path.read_text())
                self._memories = [Memory(**m) for m in data.get("memories", [])]
            except:
                self._memories = []
    
    def _save(self):
        data = {"memories": [asdict(m) for m in self._memories]}
        self.path.write_text(json.dumps(data, indent=2))
    
    def remember(self, content: str, namespace: str = "global", tags: List[str] = None) -> Memory:
        m = Memory(
            id=hashlib.md5(content.encode()).hexdigest()[:8],
            content=content,
            namespace=namespace,
            created_at=datetime.now().isoformat(),
            tags=tags or [],
        )
        if not any(x.id == m.id for x in self._memories):
            self._memories.append(m)
            self._save()
        return m
    
    def recall(self, query: str, namespace: str = None, top_k: int = 5) -> List[Memory]:
        candidates = self._memories
        if namespace:
            candidates = [m for m in candidates if m.namespace == namespace]
        q = query.lower()
        scored = [(m, sum(1 for w in q.split() if w in m.content.lower())) for m in candidates]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [m for m, s in scored[:top_k]]
    
    def get_stats(self) -> dict:
        namespaces = {}
        for m in self._memories:
            namespaces[m.namespace] = namespaces.get(m.namespace, 0) + 1
        return {"total": len(self._memories), "namespaces": namespaces}
    
    def clear(self, namespace: str = None):
        if namespace:
            self._memories = [m for m in self._memories if m.namespace != namespace]
        else:
            self._memories = []
        self._save()


memory = PersistentMemory()


def remember_cmd(content: str, namespace: str = "global") -> str:
    m = memory.remember(content, namespace)
    return f"Remembered [{m.id}]: {content[:50]}..."


def recall_cmd(query: str, namespace: str = None) -> List[Memory]:
    return memory.recall(query, namespace)

def memory_stats() -> dict:
    return memory.get_stats()


# Export aliases for CLI compatibility
def remember(content: str, namespace: str = "global") -> str:
    """Remember a fact."""
    return remember_cmd(content, namespace)


def recall(query: str, namespace: str = None):
    """Recall memories."""
    return recall_cmd(query, namespace)


__all__ = ["PersistentMemory", "Memory", "memory", "remember", "recall", "memory_stats"]