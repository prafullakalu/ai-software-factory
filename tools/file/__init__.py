"""
📁 FILE TOOLS

File operations: read, write, copy, move, delete.
"""

import os
import shutil
from crewai.tools import tool


@tool("create_directory")
def create_directory(path: str) -> str:
    """Create a directory and parent directories."""
    os.makedirs(path, exist_ok=True)
    return f"Directory created: {path}"


@tool("write_file")
def write_file(path: str, content: str) -> str:
    """Write content to file. Creates parent dirs if needed."""
    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"File written: {path}"


@tool("read_file")
def read_file(path: str) -> str:
    """Read file content."""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return f"File not found: {path}"


@tool("delete_file")
def delete_file(path: str) -> str:
    """Delete file or directory."""
    if os.path.isfile(path):
        os.remove(path)
        return f"Deleted: {path}"
    elif os.path.isdir(path):
        shutil.rmtree(path)
        return f"Deleted directory: {path}"
    return f"Path not found: {path}"


@tool("copy_file")
def copy_file(source: str, dest: str) -> str:
    """Copy file or directory."""
    if os.path.isfile(source):
        shutil.copy2(source, dest)
    elif os.path.isdir(source):
        shutil.copytree(source, dest, dirs_exist_ok=True)
    return f"Copied {source} to {dest}"


@tool("list_directory")
def list_directory(path: str = ".") -> str:
    """List files in directory."""
    files = []
    for root, dirs, filenames in os.walk(path):
        for f in filenames:
            files.append(os.path.join(root, f))
    return "\n".join(files) if files else "Empty directory"


__all__ = [
    "create_directory",
    "write_file", 
    "read_file",
    "delete_file",
    "copy_file",
    "list_directory",
]