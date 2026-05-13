"""
💻 TERMINAL EXECUTION

Execute real terminal commands like Hermes Agent.
"""

import os
import subprocess
import shlex
import time
import shutil
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# TYPES
# ============================================================================

class TerminalStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass
class CommandResult:
    """Result of terminal command."""
    command: str
    stdout: str
    stderr: str
    exit_code: int
    status: TerminalStatus
    duration: float
    timestamp: str


# ============================================================================
# TERMINAL EXECUTOR
# ============================================================================

class TerminalExecutor:
    """Execute terminal commands."""
    
    def __init__(self, workspace: str = None):
        self.workspace = workspace or os.getcwd()
        self.command_history: List[CommandResult] = []
        self.env = os.environ.copy()
    
    def execute(
        self,
        command: str,
        timeout: int = 60,
        cwd: str = None,
        shell: bool = False,
    ) -> CommandResult:
        """Execute terminal command."""
        start_time = time.time()
        if not cwd:
            cwd = self.workspace
        
        if not shell:
            command = shlex.quote(command)
        
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
                env=self.env,
            )
            
            status = TerminalStatus.COMPLETED if result.returncode == 0 else TerminalStatus.ERROR
            
            cmd_result = CommandResult(
                command=command,
                stdout=result.stdout,
                stderr=result.stderr,
                exit_code=result.returncode,
                status=status,
                duration=time.time() - start_time,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            )
            
        except subprocess.TimeoutExpired:
            cmd_result = CommandResult(
                command=command,
                stdout="",
                stderr="Command timed out",
                exit_code=-1,
                status=TerminalStatus.TIMEOUT,
                duration=timeout,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            )
        
        except Exception as e:
            cmd_result = CommandResult(
                command=command,
                stdout="",
                stderr=str(e),
                exit_code=-1,
                status=TerminalStatus.ERROR,
                duration=time.time() - start_time,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            )
        
        self.command_history.append(cmd_result)
        return cmd_result
    
    def run(self, command: str, timeout: int = 60) -> str:
        """Run command and return output."""
        result = self.execute(command, timeout)
        return result.stdout if result.exit_code == 0 else result.stderr
    
    def check_command(self, command: str) -> bool:
        """Check if command exists."""
        result = self.execute(f"which {command}")
        return result.exit_code == 0
    
    def get_system_info(self) -> Dict:
        """Get system information."""
        info = {}
        
        result = self.execute("uname -a")
        info["os"] = result.stdout.strip()
        
        result = self.execute("python3 --version")
        info["python"] = result.stdout.strip()
        
        result = self.execute("node --version")
        info["node"] = result.stdout.strip()
        
        return info
    
    def get_history(self, limit: int = 10) -> List[CommandResult]:
        """Get command history."""
        return self.command_history[-limit:]


# ============================================================================
# SHELL UTILITIES
# ============================================================================

class Shell:
    """Shell utilities."""
    
    @staticmethod
    def cd(path: str):
        os.chdir(path)
    
    @staticmethod
    def pwd() -> str:
        return os.getcwd()
    
    @staticmethod
    def ls(path: str = ".") -> List[str]:
        return os.listdir(path)
    
    @staticmethod
    def mkdir(path: str):
        os.makedirs(path, exist_ok=True)
    
    @staticmethod
    def rm(path: str, recursive: bool = False):
        import shutil
        if os.path.isdir(path):
            if recursive:
                shutil.rmtree(path)
            else:
                os.rmdir(path)
        else:
            os.remove(path)
    
    @staticmethod
    def cp(src: str, dest: str):
        import shutil
        if os.path.isdir(src):
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)
    
    @staticmethod
    def mv(src: str, dest: str):
        import shutil
        shutil.move(src, dest)


# ============================================================================
# EXPORTS
# ============================================================================

terminal = TerminalExecutor()

__all__ = [
    "TerminalStatus",
    "CommandResult",
    "TerminalExecutor",
    "Shell",
    "terminal",
]