"""
📋 TASK MANAGEMENT

Goal and task tracking like Hermes Agent.
Goals with subtasks and progress tracking.
"""

import uuid
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum


# ============================================================================
# TASK TYPES
# ============================================================================

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 5
    HIGH = 10
    URGENT = 20


# ============================================================================
# TASK MODEL
# ============================================================================

@dataclass
class Task:
    """Individual task."""
    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    subtasks: List[str]  # subtask IDs
    parent_id: Optional[str]
    created_at: str
    updated_at: str
    completed_at: Optional[str]
    tags: List[str]
    metadata: Dict
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data["status"] = self.status.value
        data["priority"] = self.priority.value
        return data


# ============================================================================
# GOAL MODEL  
# ============================================================================

@dataclass
class Goal:
    """Goal with tasks."""
    id: str
    title: str
    description: str
    tasks: List[str]  # task IDs
    status: TaskStatus
    progress: int  # 0-100
    created_at: str
    updated_at: str
    completed_at: Optional[str]
    metadata: Dict
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data["status"] = self.status.value
        return data


# ============================================================================
# TASK MANAGER
# ============================================================================

class TaskManager:
    """
    Task management like Hermes Agent.
    Goals with subtasks and progress tracking.
    """
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.goals: Dict[str, Goal] = {}
    
    # =========================================================================
    # TASK OPERATIONS
    # =========================================================================
    
    def create_task(
        self,
        title: str,
        description: str = "",
        priority: TaskPriority = TaskPriority.MEDIUM,
        parent_id: str = None,
        tags: List[str] = None,
    ) -> str:
        """Create new task."""
        task_id = str(uuid.uuid4())[:8]
        
        task = Task(
            id=task_id,
            title=title,
            description=description,
            status=TaskStatus.PENDING,
            priority=priority,
            subtasks=[],
            parent_id=parent_id,
            created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=time.strftime("%Y-%m-%d %H:%M:%S"),
            completed_at=None,
            tags=tags or [],
            metadata={},
        )
        
        self.tasks[task_id] = task
        
        # Add to parent task
        if parent_id and parent_id in self.tasks:
            self.tasks[parent_id].subtasks.append(task_id)
        
        return task_id
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID."""
        return self.tasks.get(task_id)
    
    def update_task(
        self,
        task_id: str,
        title: str = None,
        description: str = None,
        status: TaskStatus = None,
        priority: TaskPriority = None,
    ) -> bool:
        """Update task."""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        
        if title:
            task.title = title
        if description:
            task.description = description
        if status:
            task.status = status
            if status == TaskStatus.COMPLETED:
                task.completed_at = time.strftime("%Y-%m-%d %H:%M:%S")
        if priority:
            task.priority = priority
        
        task.updated_at = time.strftime("%Y-%m-%d %H:%M:%S")
        
        return True
    
    def complete_task(self, task_id: str) -> bool:
        """Mark task as completed."""
        return self.update_task(task_id, status=TaskStatus.COMPLETED)
    
    def fail_task(self, task_id: str) -> bool:
        """Mark task as failed."""
        return self.update_task(task_id, status=TaskStatus.FAILED)
    
    def delete_task(self, task_id: str) -> bool:
        """Delete task."""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False
    
    def list_tasks(
        self,
        status: TaskStatus = None,
        priority: TaskPriority = None,
        parent_id: str = None,
    ) -> List[Task]:
        """List tasks with filters."""
        tasks = list(self.tasks.values())
        
        if status:
            tasks = [t for t in tasks if t.status == status]
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
        if parent_id:
            tasks = [t for t in tasks if t.parent_id == parent_id]
        
        return sorted(tasks, key=lambda t: t.priority.value, reverse=True)
    
    # =========================================================================
    # GOAL OPERATIONS
    # =========================================================================
    
    def create_goal(
        self,
        title: str,
        description: str = "",
    ) -> str:
        """Create new goal."""
        goal_id = str(uuid.uuid4())[:8]
        
        goal = Goal(
            id=goal_id,
            title=title,
            description=description,
            tasks=[],
            status=TaskStatus.PENDING,
            progress=0,
            created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=time.strftime("%Y-%m-%d %H:%M:%S"),
            completed_at=None,
            metadata={},
        )
        
        self.goals[goal_id] = goal
        return goal_id
    
    def add_task_to_goal(self, goal_id: str, task_id: str) -> bool:
        """Add task to goal."""
        if goal_id not in self.goals or task_id not in self.tasks:
            return False
        
        self.goals[goal_id].tasks.append(task_id)
        self.tasks[task_id].parent_id = goal_id
        self._update_goal_progress(goal_id)
        
        return True
    
    def get_goal(self, goal_id: str) -> Optional[Goal]:
        """Get goal by ID."""
        return self.goals.get(goal_id)
    
    def complete_goal(self, goal_id: str) -> bool:
        """Mark goal as completed."""
        if goal_id not in self.goals:
            return False
        
        goal = self.goals[goal_id]
        goal.status = TaskStatus.COMPLETED
        goal.progress = 100
        goal.completed_at = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Complete all tasks
        for task_id in goal.tasks:
            self.complete_task(task_id)
        
        return True
    
    def get_goal_progress(self, goal_id: str) -> int:
        """Calculate goal progress."""
        if goal_id not in self.goals:
            return 0
        
        goal = self.goals[goal_id]
        
        if not goal.tasks:
            return 0
        
        completed = sum(
            1 for t in goal.tasks 
            if t in self.tasks and self.tasks[t].status == TaskStatus.COMPLETED
        )
        
        return int((completed / len(goal.tasks)) * 100)
    
    def _update_goal_progress(self, goal_id: str):
        """Update goal progress."""
        if goal_id in self.goals:
            self.goals[goal_id].progress = self.get_goal_progress(goal_id)
            self.goals[goal_id].updated_at = time.strftime("%Y-%m-%d %H:%M:%S")
    
    def list_goals(self, status: TaskStatus = None) -> List[Goal]:
        """List goals."""
        goals = list(self.goals.values())
        
        if status:
            goals = [g for g in goals if g.status == status]
        
        return sorted(goals, key=lambda g: g.created_at, reverse=True)
    
    # =========================================================================
    # WORKFLOW
    # =========================================================================
    
    def create_goal_with_tasks(
        self,
        goal_title: str,
        goal_description: str,
        task_titles: List[str],
    ) -> str:
        """Create goal with multiple tasks."""
        # Create goal
        goal_id = self.create_goal(goal_title, goal_description)
        
        # Create tasks
        for title in task_titles:
            task_id = self.create_task(title, parent_id=goal_id)
            self.add_task_to_goal(goal_id, task_id)
        
        return goal_id
    
    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks."""
        return self.list_tasks(status=TaskStatus.PENDING)
    
    def get_in_progress_tasks(self) -> List[Task]:
        """Get in-progress tasks."""
        return self.list_tasks(status=TaskStatus.IN_PROGRESS)
    
    def get_next_task(self) -> Optional[Task]:
        """Get highest priority pending task."""
        pending = self.get_pending_tasks()
        if pending:
            return pending[0]
        return None
    
    # =========================================================================
    # STATS
    # =========================================================================
    
    def get_stats(self) -> Dict:
        """Get task statistics."""
        tasks = list(self.tasks.values())
        
        return {
            "total_tasks": len(tasks),
            "completed": sum(1 for t in tasks if t.status == TaskStatus.COMPLETED),
            "pending": sum(1 for t in tasks if t.status == TaskStatus.PENDING),
            "in_progress": sum(1 for t in tasks if t.status == TaskStatus.IN_PROGRESS),
            "failed": sum(1 for t in tasks if t.status == TaskStatus.FAILED),
            "total_goals": len(self.goals),
            "goals_completed": sum(1 for g in self.goals.values() if g.status == TaskStatus.COMPLETED),
        }


# ============================================================================
# EXPORTS
# ============================================================================

task_manager = TaskManager()

__all__ = [
    "TaskStatus",
    "TaskPriority", 
    "Task",
    "Goal",
    "TaskManager",
    "task_manager",
]