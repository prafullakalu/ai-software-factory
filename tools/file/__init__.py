"""
📁 FILE TOOLS

Comprehensive file operations:
- Read, write, copy, move files
- Directory operations
- File search
- Content manipulation
"""

import os
import shutil
import hashlib
import json
from typing import List, Optional, Dict, Any
from pathlib import Path


# ============================================================================
# FILE OPERATIONS
# ============================================================================

class FileManager:
    """Manage file operations."""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
    
    def read(self, filepath: str) -> str:
        """Read file content."""
        path = self.base_path / filepath
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    
    def write(self, filepath: str, content: str) -> str:
        """Write content to file."""
        path = self.base_path / filepath
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Written: {filepath}"
    
    def append(self, filepath: str, content: str) -> str:
        """Append content to file."""
        path = self.base_path / filepath
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
        return f"Appended to: {filepath}"
    
    def copy(self, src: str, dest: str) -> str:
        """Copy file or directory."""
        src_path = self.base_path / src
        dest_path = self.base_path / dest
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        if src_path.is_dir():
            shutil.copytree(src_path, dest_path)
        else:
            shutil.copy2(src_path, dest_path)
        return f"Copied: {src} -> {dest}"
    
    def move(self, src: str, dest: str) -> str:
        """Move file or directory."""
        src_path = self.base_path / src
        dest_path = self.base_path / dest
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src_path), str(dest_path))
        return f"Moved: {src} -> {dest}"
    
    def delete(self, filepath: str) -> str:
        """Delete file or directory."""
        path = self.base_path / filepath
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
        return f"Deleted: {filepath}"
    
    def exists(self, filepath: str) -> bool:
        """Check if file exists."""
        return (self.base_path / filepath).exists()
    
    def mkdir(self, dirpath: str) -> str:
        """Create directory."""
        path = self.base_path / dirpath
        path.mkdir(parents=True, exist_ok=True)
        return f"Created: {dirpath}"
    
    def list_files(self, dirpath: str = ".", pattern: str = "*", recursive: bool = False) -> List[str]:
        """List files in directory."""
        path = self.base_path / dirpath
        
        if recursive:
            return [str(p.relative_to(self.base_path)) for p in path.rglob(pattern)]
        else:
            return [str(p.relative_to(self.base_path)) for p in path.glob(pattern)]
    
    def get_size(self, filepath: str) -> int:
        """Get file size in bytes."""
        return (self.base_path / filepath).stat().st_size
    
    def get_hash(self, filepath: str, algorithm: str = "md5") -> str:
        """Get file hash."""
        path = self.base_path / filepath
        hash_obj = hashlib.new(algorithm)
        
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        
        return hash_obj.hexdigest()
    
    def find(self, pattern: str, dirpath: str = ".") -> List[str]:
        """Find files matching pattern."""
        path = self.base_path / dirpath
        return [str(p.relative_to(self.base_path)) for p in path.rglob(f"*{pattern}*")]
    
    def read_json(self, filepath: str) -> Dict:
        """Read JSON file."""
        return json.loads(self.read(filepath))
    
    def write_json(self, filepath: str, data: Dict, indent: int = 2) -> str:
        """Write JSON file."""
        return self.write(filepath, json.dumps(data, indent=indent))
    
    def get_tree(self, dirpath: str = ".", max_depth: int = 3) -> str:
        """Get directory tree."""
        path = self.base_path / dirpath
        lines = []
        
        def _tree(p: Path, prefix: str = "", depth: int = 0):
            if depth > max_depth:
                return
            
            items = sorted(p.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                current = prefix + ("└── " if is_last else "├── ") + item.name
                lines.append(current)
                
                if item.is_dir():
                    _tree(item, prefix + ("    " if is_last else "│   "), depth + 1)
        
        lines.append(path.name)
        _tree(path)
        return "\n".join(lines)


# ============================================================================
# TEMPLATE ENGINE
# ============================================================================

class TemplateEngine:
    """Simple template engine."""
    
    def __init__(self):
        self.variables: Dict[str, Any] = {}
    
    def set(self, key: str, value: Any):
        self.variables[key] = value
    
    def render(self, template: str) -> str:
        """Render template with variables."""
        result = template
        
        for key, value in self.variables.items():
            result = result.replace(f"{{{{{key}}}}}", str(value))
        
        return result
    
    def render_file(self, template_path: str, output_path: str, file_manager: FileManager):
        """Render template file."""
        template = file_manager.read(template_path)
        rendered = self.render(template)
        file_manager.write(output_path, rendered)
        return f"Rendered: {template_path} -> {output_path}"


# ============================================================================
# EXPORTS
# ============================================================================

file_manager = FileManager()

__all__ = ["FileManager", "TemplateEngine", "file_manager"]