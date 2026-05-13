"""
🏖️ SANDBOX CODE EXECUTION

Safe code execution environment like E2B.
Execute code securely in isolated sandbox.
"""

import os
import subprocess
import tempfile
import shutil
import uuid
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# SANDBOX CONFIG
# ============================================================================

class Language(Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    BASH = "bash"
    GO = "go"
    RUST = "rust"


class SandboxStatus(Enum):
    READY = "ready"
    RUNNING = "running"
    TIMEOUT = "timeout"
    ERROR = "error"
    STOPPED = "stopped"


@dataclass
class ExecutionResult:
    """Result of code execution."""
    success: bool
    output: str
    error: str
    exit_code: int
    execution_time: float
    logs: List[str]


# ============================================================================
# SANDBOX EXECUTOR
# ============================================================================

class SandboxExecutor:
    """
    Secure code execution sandbox.
    Like E2B - runs code in isolated environment.
    """
    
    def __init__(self, workspace: str = None):
        self.workspace = workspace or "/tmp/sandbox"
        os.makedirs(self.workspace, exist_ok=True)
        self.active_sessions: Dict[str, Dict] = {}
    
    def create_session(self, language: Language = Language.PYTHON) -> str:
        """Create new sandbox session."""
        session_id = str(uuid.uuid4())[:8]
        session_path = os.path.join(self.workspace, session_id)
        os.makedirs(session_path, exist_ok=True)
        
        self.active_sessions[session_id] = {
            "id": session_id,
            "language": language,
            "path": session_path,
            "status": SandboxStatus.READY,
            "created": time.time(),
        }
        
        return session_id
    
    def execute(
        self,
        code: str,
        language: Language = Language.PYTHON,
        timeout: int = 30,
        session_id: str = None,
    ) -> ExecutionResult:
        """Execute code in sandbox."""
        start_time = time.time()
        
        # Use existing session or create new one
        if not session_id:
            session_id = self.create_session(language)
        
        session = self.active_sessions.get(session_id)
        if not session:
            return ExecutionResult(
                success=False,
                output="",
                error="Invalid session",
                exit_code=-1,
                execution_time=0,
                logs=[],
            )
        
        session["status"] = SandboxStatus.RUNNING
        
        # Write code to file
        extensions = {
            Language.PYTHON: ".py",
            Language.JAVASCRIPT: ".js",
            Language.TYPESCRIPT: ".ts",
            Language.BASH: ".sh",
            Language.GO: ".go",
            Language.RUST: ".rs",
        }
        
        ext = extensions.get(language, ".txt")
        filename = f"main{ext}"
        filepath = os.path.join(session["path"], filename)
        
        with open(filepath, "w") as f:
            f.write(code)
        
        # Execute based on language
        try:
            if language == Language.PYTHON:
                result = self._run_python(filepath, timeout)
            elif language == Language.JAVASCRIPT:
                result = self._run_javascript(filepath, timeout)
            elif language == Language.TYPESCRIPT:
                result = self._run_typescript(filepath, timeout)
            elif language == Language.BASH:
                result = self._run_bash(code, timeout)
            elif language == Language.GO:
                result = self._run_go(filepath, timeout)
            elif language == Language.RUST:
                result = self._run_rust(filepath, timeout)
            else:
                result = ExecutionResult(
                    success=False,
                    output="",
                    error=f"Unsupported language: {language}",
                    exit_code=-1,
                    execution_time=time.time() - start_time,
                    logs=[],
                )
        except Exception as e:
            result = ExecutionResult(
                success=False,
                output="",
                error=str(e),
                exit_code=-1,
                execution_time=time.time() - start_time,
                logs=[],
            )
        
        session["status"] = SandboxStatus.READY
        return result
    
    def _run_python(self, filepath: str, timeout: int) -> ExecutionResult:
        """Run Python code."""
        try:
            result = subprocess.run(
                ["python3", filepath],
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            return ExecutionResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr,
                exit_code=result.returncode,
                execution_time=0,
                logs=[],
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                output="",
                error="Execution timeout",
                exit_code=-1,
                execution_time=timeout,
                logs=[],
            )
    
    def _run_javascript(self, filepath: str, timeout: int) -> ExecutionResult:
        """Run JavaScript code."""
        try:
            result = subprocess.run(
                ["node", filepath],
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            return ExecutionResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr,
                exit_code=result.returncode,
                execution_time=0,
                logs=[],
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                output="",
                error="Execution timeout",
                exit_code=-1,
                execution_time=timeout,
                logs=[],
            )
    
    def _run_typescript(self, filepath: str, timeout: int) -> ExecutionResult:
        """Run TypeScript code (compile first)."""
        # For simplicity, treat as JS
        return self._run_javascript(filepath, timeout)
    
    def _run_bash(self, code: str, timeout: int) -> ExecutionResult:
        """Run bash script."""
        try:
            result = subprocess.run(
                ["bash", "-c", code],
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            return ExecutionResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr,
                exit_code=result.returncode,
                execution_time=0,
                logs=[],
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                output="",
                error="Execution timeout",
                exit_code=-1,
                execution_time=timeout,
                logs=[],
            )
    
    def _run_go(self, filepath: str, timeout: int) -> ExecutionResult:
        """Run Go code."""
        # Compile first
        exe_path = filepath.replace(".go", "")
        
        compile_result = subprocess.run(
            ["go", "build", "-o", exe_path, filepath],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        
        if compile_result.returncode != 0:
            return ExecutionResult(
                success=False,
                output="",
                error=compile_result.stderr,
                exit_code=compile_result.returncode,
                execution_time=0,
                logs=[],
            )
        
        # Run
        try:
            result = subprocess.run(
                [exe_path],
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            return ExecutionResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr,
                exit_code=result.returncode,
                execution_time=0,
                logs=[],
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                output="",
                error="Execution timeout",
                exit_code=-1,
                execution_time=timeout,
                logs=[],
            )
    
    def _run_rust(self, filepath: str, timeout: int) -> ExecutionResult:
        """Run Rust code."""
        return ExecutionResult(
            success=False,
            output="",
            error="Rust execution requires cargo project",
            exit_code=-1,
            execution_time=0,
            logs=[],
        )
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session info."""
        return self.active_sessions.get(session_id)
    
    def stop_session(self, session_id: str) -> bool:
        """Stop and cleanup session."""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            session["status"] = SandboxStatus.STOPPED
            
            # Cleanup files
            if os.path.exists(session["path"]):
                shutil.rmtree(session["path"])
            
            del self.active_sessions[session_id]
            return True
        return False
    
    def list_sessions(self) -> List[Dict]:
        """List all active sessions."""
        return list(self.active_sessions.values())


# ============================================================================
# QUICK EXECUTE FUNCTIONS
# ============================================================================

executor = SandboxExecutor()


def run_python(code: str, timeout: int = 30) -> ExecutionResult:
    """Quick execute Python code."""
    return executor.execute(code, Language.PYTHON, timeout)


def run_javascript(code: str, timeout: int = 30) -> ExecutionResult:
    """Quick execute JavaScript code."""
    return executor.execute(code, Language.JAVASCRIPT, timeout)


def run_bash(code: str, timeout: int = 30) -> ExecutionResult:
    """Quick execute bash code."""
    return executor.execute(code, Language.BASH, timeout)


__all__ = [
    "Language",
    "SandboxStatus",
    "ExecutionResult",
    "SandboxExecutor",
    "executor",
    "run_python",
    "run_javascript",
    "run_bash",
]