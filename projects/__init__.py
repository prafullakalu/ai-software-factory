"""
💼 PROJECT MANAGER

Tracks all SaaS/Fintech projects created by the AI Factory.
Similar to Paperclip or similar AI project builders.
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum


# ============================================================================
# PROJECT TYPES
# ============================================================================

class ProjectType(Enum):
    SAAS = "saas"
    FINTECH = "fintech"
    ECOMMERCE = "ecommerce"
    API = "api"
    DASHBOARD = "dashboard"
    MOBILE = "mobile"


class ProjectStatus(Enum):
    DRAFT = "draft"
    GENERATING = "generating"
    READY = "ready"
    DEPLOYED = "deployed"
    FAILED = "failed"


class TechStack(Enum):
    # Frontend
    REACT = "react"
    NEXTJS = "nextjs"
    VUE = "vue"
    TAILWIND = "tailwind"
    SHADCN = "shadcn"
    
    # Backend
    FASTAPI = "fastapi"
    DJANGO = "django"
    EXPRESS = "express"
    NESTJS = "nestjs"
    
    # Database
    POSTGRESQL = "postgresql"
    MONGODB = "mongodb"
    REDIS = "redis"
    SUPABASE = "supabase"


# ============================================================================
# PROJECT MODEL
# ============================================================================

class Project:
    """Represents a created project."""
    
    def __init__(
        self,
        name: str,
        description: str = "",
        project_type: ProjectType = ProjectType.SAAS,
    ):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.description = description
        self.project_type = project_type
        self.status = ProjectStatus.DRAFT
        
        # Tech stack
        self.frontend_stack: List[str] = []
        self.backend_stack: List[str] = []
        self.database: List[str] = []
        
        # Features
        self.features: List[str] = []
        
        # Paths
        self.frontend_path = ""
        self.backend_path = ""
        
        # Metadata
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.generated_by = ""
        self.deployed_url = ""
        
        # Stats
        self.files_created = 0
        self.lines_of_code = 0
        
        # Errors (if any)
        self.errors: List[str] = []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "project_type": self.project_type.value,
            "status": self.status.value,
            "frontend_stack": self.frontend_stack,
            "backend_stack": self.backend_stack,
            "database": self.database,
            "features": self.features,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "generated_by": self.generated_by,
            "deployed_url": self.deployed_url,
            "files_created": self.files_created,
            "lines_of_code": self.lines_of_code,
            "errors": self.errors,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Project":
        p = cls(
            name=data.get("name", ""),
            description=data.get("description", ""),
            project_type=ProjectType(data.get("project_type", "saas")),
        )
        p.id = data.get("id", p.id)
        p.status = ProjectStatus(data.get("status", "draft"))
        p.frontend_stack = data.get("frontend_stack", [])
        p.backend_stack = data.get("backend_stack", [])
        p.database = data.get("database", [])
        p.features = data.get("features", [])
        p.generated_by = data.get("generated_by", "")
        p.deployed_url = data.get("deployed_url", "")
        p.files_created = data.get("files_created", 0)
        p.lines_of_code = data.get("lines_of_code", 0)
        p.errors = data.get("errors", [])
        
        if data.get("created_at"):
            p.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("updated_at"):
            p.updated_at = datetime.fromisoformat(data["updated_at"])
        
        return p


# ============================================================================
# PROJECT STORAGE
# ============================================================================

class ProjectManager:
    """Manages all projects."""
    
    def __init__(self, storage_path: str = "projects/projects.json"):
        self.storage_path = storage_path
        self.projects: Dict[str, Project] = {}
        self.load()
    
    def load(self):
        """Load projects from storage."""
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                data = json.load(f)
                for p_data in data.get("projects", []):
                    project = Project.from_dict(p_data)
                    self.projects[project.id] = project
    
    def save(self):
        """Save projects to storage."""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        data = {
            "projects": [p.to_dict() for p in self.projects.values()],
            "stats": self.get_stats(),
        }
        with open(self.storage_path, "w") as f:
            json.dump(data, f, indent=2)
    
    def create(self, name: str, description: str = "", project_type: ProjectType = ProjectType.SAAS) -> Project:
        """Create new project."""
        project = Project(name=name, description=description, project_type=project_type)
        project.status = ProjectStatus.GENERATING
        self.projects[project.id] = project
        self.save()
        return project
    
    def get(self, project_id: str) -> Optional[Project]:
        """Get project by ID."""
        return self.projects.get(project_id)
    
    def update(self, project_id: str, **kwargs):
        """Update project."""
        if project_id in self.projects:
            project = self.projects[project_id]
            for key, value in kwargs.items():
                setattr(project, key, value)
            project.updated_at = datetime.now()
            self.save()
    
    def complete(self, project_id: str, status: ProjectStatus = ProjectStatus.READY):
        """Mark project as complete."""
        if project_id in self.projects:
            self.projects[project_id].status = status
            self.projects[project_id].updated_at = datetime.now()
            self.save()
    
    def delete(self, project_id: str):
        """Delete project."""
        if project_id in self.projects:
            del self.projects[project_id]
            self.save()
    
    def list_all(self, status: ProjectStatus = None) -> List[Project]:
        """List all projects."""
        projects = list(self.projects.values())
        if status:
            projects = [p for p in projects if p.status == status]
        return sorted(projects, key=lambda p: p.updated_at, reverse=True)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get project statistics."""
        total = len(self.projects)
        ready = len([p for p in self.projects.values() if p.status == ProjectStatus.READY])
        deployed = len([p for p in self.projects.values() if p.status == ProjectStatus.DEPLOYED])
        generating = len([p for p in self.projects.values() if p.status == ProjectStatus.GENERATING])
        failed = len([p for p in self.projects.values() if p.status == ProjectStatus.FAILED])
        
        total_files = sum(p.files_created for p in self.projects.values())
        total_loc = sum(p.lines_of_code for p in self.projects.values())
        
        # By type
        by_type = {}
        for p in self.projects.values():
            t = p.project_type.value
            by_type[t] = by_type.get(t, 0) + 1
        
        return {
            "total": total,
            "ready": ready,
            "deployed": deployed,
            "generating": generating,
            "failed": failed,
            "total_files_created": total_files,
            "total_lines_of_code": total_loc,
            "by_type": by_type,
            "last_updated": datetime.now().isoformat(),
        }


# ============================================================================
# EXPORTS
# ============================================================================

# Global instance
manager = ProjectManager()


def create_project(name: str, description: str = "", project_type: ProjectType = ProjectType.SAAS) -> Project:
    """Create a new project."""
    return manager.create(name, description, project_type)


def list_projects(status: ProjectStatus = None) -> List[Project]:
    """List all projects."""
    return manager.list_all(status)


def get_project(project_id: str) -> Optional[Project]:
    """Get project by ID."""
    return manager.get(project_id)


def get_stats() -> Dict[str, Any]:
    """Get project statistics."""
    return manager.get_stats()


__all__ = [
    "Project",
    "ProjectManager",
    "ProjectType",
    "ProjectStatus",
    "TechStack",
    "create_project",
    "list_projects",
    "get_project",
    "get_stats",
    "manager",
]