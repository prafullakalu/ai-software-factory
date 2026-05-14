"""
🏭 AI Software Factory Test Suite
"""

import pytest
import tempfile
from pathlib import Path


# Test CLI commands
def test_help_command():
    """Test help command parses."""
    from factory import CommandParser
    parser = CommandParser()
    result = parser.execute("help")
    assert "project" in result.lower()


def test_project_new():
    """Test project new."""
    from factory import CommandParser
    parser = CommandParser()
    with tempfile.TemporaryDirectory() as tmp:
        # Would need to mock workspace
        result = parser.execute("project new TestApp")
        assert "TestApp" in result


def test_unknown_command():
    """Test unknown command handling."""
    from factory import CommandParser
    parser = CommandParser()
    result = parser.execute("xyzzy frobble")
    assert "unknown" in result.lower() or "?" in result


def test_analyze_command():
    """Test analyze command."""
    from factory import CommandParser
    parser = CommandParser()
    with tempfile.TemporaryDirectory() as tmp:
        # Create a simple Python file
        p = Path(tmp) / "test.py"
        p.write_text("def hello(): pass")
        
        # Run analyze on it
        result = parser.execute(f"analyze {tmp}")
        assert "Python" in result


# Test agents
def test_list_agents():
    """Test agent listing."""
    from core.agents.real import list_agents
    agents = list_agents()
    assert len(agents) > 0
    assert any(a.get("type") == "developer" for a in agents)


def test_run_agent():
    """Test agent execution."""
    from core.agents.real import run_agent
    result = run_agent("developer", "hello world")
    assert result is not None


# Test analyzer
def test_codebase_analyzer():
    """Test codebase analyzer."""
    from core.analyzer.codebase import CodebaseAnalyzer
    
    with tempfile.TemporaryDirectory() as tmp:
        # Create a test file
        p = Path(tmp) / "main.py"
        p.write_text("import fastapi\n\ndef main():\n    pass\n")
        
        analyzer = CodebaseAnalyzer()
        report = analyzer.analyze(tmp)
        
        assert report.total_files > 0
        assert "Python" in report.languages


def test_detect_frameworks():
    """Test framework detection."""
    from core.analyzer.codebase import CodebaseAnalyzer
    
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "main.py"
        p.write_text("from fastapi import FastAPI\napp = FastAPI()\n")
        
        analyzer = CodebaseAnalyzer()
        report = analyzer.analyze(tmp)
        
        assert "FastAPI" in report.frameworks_detected


# Test memory
def test_memory_remember_recall():
    """Test memory store."""
    from core.memory.persistent import PersistentMemory, Memory
    
    with tempfile.TemporaryDirectory() as tmp:
        from core.memory import persistent
        persistent.MEMORY_FILE = Path(tmp) / "memory.json"
        
        memory = PersistentMemory(Path(tmp) / "memory.json")
        memory.remember("Test fact", "global")
        
        results = memory.recall("test")
        assert any("Test fact" in m.content for m in results)


# Test LLM client
def test_llm_client():
    """Test LLM client initialization."""
    from core.llm.client import LLMClient
    client = LLMClient()
    # Should return some provider
    assert client.config.provider in ["anthropic", "openai", "deepseek", "ollama", "stub"]


# Test code generator
def test_fullstack_generator():
    """Test fullstack code generation."""
    from tools.fullstack_generator import generate_fullstack
    
    result = generate_fullstack("TestApp")
    
    assert "frontend" in result
    assert "backend" in result
    assert len(result["frontend"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])