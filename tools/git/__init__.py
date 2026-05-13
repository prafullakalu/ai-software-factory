"""
🐙 GIT OPERATIONS

Full Git integration like Hermes Agent.
"""

import os
import subprocess
import shutil
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# GIT TYPES
# ============================================================================

class GitStatus(Enum):
    CLEAN = "clean"
    MODIFIED = "modified"
    UNTRACKED = "untracked"
    CONFLICT = "conflict"


@dataclass
class GitCommit:
    """Git commit info."""
    hash: str
    message: str
    author: str
    date: str
    files: List[str]


@dataclass
class GitBranch:
    """Git branch info."""
    name: str
    is_current: bool
    is_remote: bool


# ============================================================================
# GIT OPERATIONS
# ============================================================================

class Git:
    """
    Full Git operations.
    Like Hermes Agent - real Git operations.
    """
    
    def __init__(self, repo_path: str = None):
        self.repo_path = repo_path or os.getcwd()
    
    def _run(self, *args, capture_output=True):
        """Run git command."""
        cmd = ["git", "-C", self.repo_path] + list(args)
        result = subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
        )
        return result
    
    # ============================================================================
    # BASIC OPERATIONS
    # ============================================================================
    
    def init(self, path: str = None) -> bool:
        """Initialize new repository."""
        repo_path = path or self.repo_path
        result = subprocess.run(
            ["git", "init"],
            cwd=repo_path,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            self.repo_path = repo_path
            return True
        return False
    
    def clone(self, url: str, path: str) -> bool:
        """Clone repository."""
        result = subprocess.run(
            ["git", "clone", url, path],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            self.repo_path = path
            return True
        return False
    
    def status(self) -> GitStatus:
        """Get repository status."""
        result = self._run("status", "--porcelain")
        if not result.stdout.strip():
            return GitStatus.CLEAN
        elif "UU" in result.stdout or "AA" in result.stdout:
            return GitStatus.CONFLICT
        return GitStatus.MODIFIED
    
    # ============================================================================
    # BRANCH OPERATIONS
    # ============================================================================
    
    def branch(self, name: str = None, create: bool = False) -> List[GitBranch]:
        """List or create branches."""
        if create:
            self._run("checkout", "-b", name)
        
        result = self._run("branch", "-a")
        branches = []
        
        for line in result.stdout.strip().split("\n"):
            if line:
                is_current = line.startswith("*")
                name = line.replace("*", "").strip()
                is_remote = name.startswith("remotes/")
                branches.append(GitBranch(
                    name=name,
                    is_current=is_current,
                    is_remote=is_remote,
                ))
        
        return branches
    
    def checkout(self, branch: str, create: bool = False) -> bool:
        """Checkout branch."""
        if create:
            result = self._run("checkout", "-b", branch)
        else:
            result = self._run("checkout", branch)
        return result.returncode == 0
    
    def current_branch(self) -> str:
        """Get current branch name."""
        result = self._run("branch", "--show-current")
        return result.stdout.strip()
    
    # ============================================================================
    # STAGING & COMMIT
    # ============================================================================
    
    def add(self, *paths) -> bool:
        """Stage files."""
        result = self._run("add", *paths)
        return result.returncode == 0
    
    def add_all(self) -> bool:
        """Stage all files."""
        result = self._run("add", "-A")
        return result.returncode == 0
    
    def commit(self, message: str, author: str = None) -> bool:
        """Commit changes."""
        cmd = ["commit", "-m", message]
        if author:
            cmd = ["git", "-C", self.repo_path, "commit", "--author", author, "-m", message]
            result = subprocess.run(cmd, capture_output=True, text=True)
        else:
            result = self._run(*cmd)
        return result.returncode == 0
    
    def log(self, limit: int = 10) -> List[GitCommit]:
        """Get commit history."""
        result = self._run(
            "log",
            f"-{limit}",
            "--pretty=format:%H|%s|%an|%ad",
            "--date=short"
        )
        
        commits = []
        for line in result.stdout.strip().split("\n"):
            if line:
                parts = line.split("|")
                if len(parts) >= 4:
                    commits.append(GitCommit(
                        hash=parts[0],
                        message=parts[1],
                        author=parts[2],
                        date=parts[3],
                        files=[],
                    ))
        
        return commits
    
    # ============================================================================
    # REMOTE OPERATIONS
    # ============================================================================
    
    def remote(self, action: str = "list", name: str = None, url: str = None) -> List[str]:
        """Manage remotes."""
        if action == "add" and name and url:
            self._run("remote", "add", name, url)
        
        result = self._run("remote", "-v")
        return result.stdout.strip().split("\n")
    
    def push(self, remote: str = "origin", branch: str = None, force: bool = False) -> bool:
        """Push to remote."""
        cmd = ["push"]
        if force:
            cmd.append("--force")
        cmd.append(remote)
        if branch:
            cmd.append(branch)
        
        result = self._run(*cmd)
        return result.returncode == 0
    
    def pull(self, remote: str = "origin", branch: str = None) -> bool:
        """Pull from remote."""
        cmd = ["pull"]
        if remote:
            cmd.append(remote)
        if branch:
            cmd.append(branch)
        
        result = self._run(*cmd)
        return result.returncode == 0
    
    def fetch(self, remote: str = None) -> bool:
        """Fetch from remote."""
        cmd = ["fetch"]
        if remote:
            cmd.append(remote)
        
        result = self._run(*cmd)
        return result.returncode == 0
    
    # ============================================================================
    # DIFF & MERGE
    # ============================================================================
    
    def diff(self, file: str = None, staged: bool = False) -> str:
        """Get diff."""
        cmd = ["diff"]
        if staged:
            cmd.append("--staged")
        if file:
            cmd.append(file)
        
        result = self._run(*cmd)
        return result.stdout
    
    def merge(self, branch: str, no_ff: bool = False) -> bool:
        """Merge branch."""
        cmd = ["merge"]
        if no_ff:
            cmd.append("--no-ff")
        cmd.append(branch)
        
        result = self._run(*cmd)
        return result.returncode == 0
    
    def rebase(self, branch: str) -> bool:
        """Rebase onto branch."""
        result = self._run("rebase", branch)
        return result.returncode == 0
    
    # ============================================================================
    # STASH
    # ============================================================================
    
    def stash(self, message: str = None) -> bool:
        """Stash changes."""
        cmd = ["stash"]
        if message:
            cmd.extend(["-m", message])
        
        result = self._run(*cmd)
        return result.returncode == 0
    
    def stash_pop(self) -> bool:
        """Pop stash."""
        result = self._run("stash", "pop")
        return result.returncode == 0
    
    def stash_list(self) -> List[str]:
        """List stashes."""
        result = self._run("stash", "list")
        return result.stdout.strip().split("\n")
    
    # ============================================================================
    # UTILITIES
    # ============================================================================
    
    def is_repo(self) -> bool:
        """Check if directory is git repository."""
        git_dir = os.path.join(self.repo_path, ".git")
        return os.path.isdir(git_dir)
    
    def get_remote_url(self, remote: str = "origin") -> str:
        """Get remote URL."""
        result = self._run("config", "--get", f"remote.{remote}.url")
        return result.stdout.strip()
    
    def set_remote_url(self, remote: str, url: str):
        """Set remote URL."""
        self._run("remote", "set-url", remote, url)
    
    def get_config(self, key: str) -> str:
        """Get git config."""
        result = self._run("config", "--get", key)
        return result.stdout.strip()
    
    def set_config(self, key: str, value: str):
        """Set git config."""
        self._run("config", key, value)


# ============================================================================
# EXPORTS
# ============================================================================

git = Git()

__all__ = [
    "GitStatus",
    "GitCommit", 
    "GitBranch",
    "Git",
    "git",
]