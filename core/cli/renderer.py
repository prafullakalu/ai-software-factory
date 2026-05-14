"""
🎨 Rich CLI Renderer for AI Software Factory

Provides streaming terminal UI with Rich library.
"""

import sys
import time
from typing import Generator, Optional, List, Dict
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.syntax import Syntax
from rich.live import Live
from rich.table import Table
from rich.text import Text


console = Console()


class FactoryRenderer:
    """Rich-based terminal UI renderer."""
    
    def __init__(self):
        self.console = Console()
    
    def stream_agent_response(
        self,
        agent_name: str,
        role: str,
        token_generator: Generator[str, None, None]
    ) -> str:
        """Stream agent response with panel."""
        emoji = self._get_agent_emoji(agent_name)
        header = f"{emoji} {agent_name} ({role})"
        
        response = ""
        with Live(Panel(Text("Thinking...", style="cyan"), console=self.console, refresh_per_second=10) as live:
            try:
                for token in token_generator:
                    response += token
                    live.update(Panel(Text(response[-500:], style="white"), title=header))
            except:
                pass
        
        self.console.print(Panel(
            Text(response[:1000] + ("..." if len(response) > 1000 else "")),
            title=f"✅ {header}",
            style="green",
        ))
        return response
    
    def show_file_write(self, filepath: str, content: str) -> None:
        """Show file being written with syntax highlighting."""
        language = self._detect_language(filepath)
        syntax = Syntax(
            content[:2000] + ("..." if len(content) > 2000 else ""),
            language, theme="monokai", line_numbers=True,
        )
        self.console.print(Panel(syntax, title=f"📄 Writing: {filepath}", border_style="blue"))
    
    def show_agent_status_bar(self, agents: List[Dict]) -> None:
        """Show agent status bar."""
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Agent")
        table.add_column("Status")
        
        colors = {"working": "green", "idle": "dim", "error": "red"}
        
        for agent in agents:
            status = agent.get("status", "idle")
            table.add_row(
                f"{agent.get('emoji', '🤖')} {agent.get('name', agent.get('type', 'unknown'))}",
                f"[{colors.get(status, 'dim')}]{status}[/]",
            )
        self.console.print(table)
    
    def show_progress(self, step: str, percent: int) -> None:
        """Show progress bar."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console,
        ) as progress:
            task = progress.add_task(step, total=100)
            progress.update(task, completed=percent)
    
    def show_project_created(self, name: str, files: List[str]) -> None:
        """Show project creation summary."""
        table = Table(title=f"✅ Project: {name}")
        table.add_column("Type", style="cyan")
        table.add_column("Files", style="white")
        frontend_count = len([f for f in files if 'frontend' in f])
        backend_count = len([f for f in files if 'backend' in f])
        table.add_row("Frontend", f"{frontend_count} files")
        table.add_row("Backend", f"{backend_count} files")
        self.console.print(table)
    
    def show_analysis_report(self, report: str) -> None:
        """Show codebase analysis report."""
        self.console.print(Panel(Text(report), title="📊 Codebase Analysis", border_style="yellow"))
    
    def show_error(self, message: str) -> None:
        """Show error message."""
        self.console.print(Panel(Text(message, style="red bold"), title="❌ Error", border_style="red"))
    
    def show_success(self, message: str) -> None:
        """Show success message."""
        self.console.print(Panel(Text(message, style="green"), title="✅ Success", border_style="green"))
    
    def _get_agent_emoji(self, agent_type: str) -> str:
        emojis = {"cto": "🧠", "developer": "💻", "qa": "🔍", "designer": "🎨", "devops": "🚀", "pm": "📋"}
        return emojis.get(agent_type, "🤖")
    
    def _detect_language(self, filepath: str) -> str:
        ext = filepath.split(".")[-1].lower() if "." in filepath else ""
        languages = {"py": "python", "jsx": "javascript", "js": "javascript", "ts": "typescript", "tsx": "typescript", "go": "go", "rs": "rust", "html": "html", "css": "css", "json": "json", "yaml": "yaml", "md": "markdown"}
        return languages.get(ext, "text")


renderer = FactoryRenderer()

def get_renderer() -> FactoryRenderer:
    return renderer

__all__ = ["FactoryRenderer", "renderer", "get_renderer", "console"]