"""
📊 CODEBASE ANALYZER

Analyzes any codebase and produces detailed reports.
"""

import os
import re
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class FileAnalysis:
    """Analysis of a single file."""
    path: str
    language: str
    lines: int
    functions: List[str] = field(default_factory=list)
    classes: List[str] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    complexity_score: int = 1
    issues: List[str] = field(default_factory=list)


@dataclass
class CodebaseReport:
    """Complete codebase analysis report."""
    root_path: str
    total_files: int
    total_lines: int
    languages: Dict[str, int] = field(default_factory=dict)
    file_analyses: List[FileAnalysis] = field(default_factory=list)
    dependency_graph: Dict[str, List[str]] = field(default_factory=dict)
    entry_points: List[str] = field(default_factory=list)
    frameworks_detected: List[str] = field(default_factory=list)
    architecture_pattern: str = "unknown"
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    complexity_score: int = 1


class CodebaseAnalyzer:
    """Analyze any codebase."""
    
    LANGUAGE_EXTENSIONS = {
        ".py": "Python", ".ts": "TypeScript", ".tsx": "TypeScript",
        ".js": "JavaScript", ".jsx": "JavaScript", ".go": "Go",
        ".rs": "Rust", ".java": "Java", ".cpp": "C++", ".cs": "C#",
        ".html": "HTML", ".css": "CSS", ".json": "JSON", ".md": "Markdown"
    }
    
    IGNORE_DIRS = {".git", "node_modules", "__pycache__", ".venv", "dist", "build", ".next", "venv", ".tox"}
    
    def analyze(self, path: str) -> CodebaseReport:
        """Analyze a directory."""
        root = Path(path)
        if not root.exists():
            return CodebaseReport(root_path=str(root), total_files=0, total_lines=0)
        
        files = self._collect_files(root)
        analyses = [self._analyze_file(f) for f in files if f.is_file()]
        
        return CodebaseReport(
            root_path=str(root),
            total_files=len(files),
            total_lines=sum(a.lines for a in analyses),
            languages=self._count_languages(analyses),
            file_analyses=analyses,
            dependency_graph=self._build_dep_graph(analyses),
            entry_points=self._find_entry_points(files),
            frameworks_detected=self._detect_frameworks(root),
            architecture_pattern=self._detect_architecture(analyses),
            issues=self._find_global_issues(analyses),
            suggestions=self._generate_suggestions(analyses),
            complexity_score=self._overall_complexity(analyses)
        )
    
    def _collect_files(self, root: Path) -> List[Path]:
        """Collect all code files."""
        files = []
        for item in root.rglob("*"):
            if item.is_file():
                if any(ignored in item.parts for ignored in self.IGNORE_DIRS):
                    continue
                if item.suffix in self.LANGUAGE_EXTENSIONS:
                    files.append(item)
        return files
    
    def _analyze_file(self, path: Path) -> FileAnalysis:
        """Analyze a single file."""
        try:
            content = path.read_text()
        except:
            return FileAnalysis(str(path), "unknown", 0)
        
        lines = len(content.splitlines())
        language = self.LANGUAGE_EXTENSIONS.get(path.suffix, "unknown")
        
        imports = []
        if language == "Python":
            imports = re.findall(r'^(?:from|import)\s+([\w.]+)', content, re.MULTILINE)
        elif language in ("JavaScript", "TypeScript"):
            imports = re.findall(r"^import\s+.*?from\s+['\"](.+?)['\"]", content, re.MULTILINE)
        
        classes = []
        if language == "Python":
            classes = re.findall(r'^class\s+(\w+)', content, re.MULTILINE)
        
        functions = []
        if language == "Python":
            functions = re.findall(r'^def\s+(\w+)', content, re.MULTILINE)
        
        complexity_score = min(10, 1 + len(functions) // 5 + len(imports) // 3)
        
        issues = []
        if "password" in content.lower() and "hash" not in content.lower():
            issues.append("Possible plaintext password")
        if "TODO" in content or "FIXME" in content:
            issues.append("Contains TODOs or FIXMEs")
        
        return FileAnalysis(
            path=str(path),
            language=language,
            lines=lines,
            functions=functions,
            classes=classes,
            imports=imports[:20],
            complexity_score=complexity_score,
            issues=issues
        )
    
    def _count_languages(self, analyses: List[FileAnalysis]) -> Dict[str, int]:
        counts = {}
        for a in analyses:
            counts[a.language] = counts.get(a.language, 0) + 1
        return counts
    
    def _build_dep_graph(self, analyses: List[FileAnalysis]) -> Dict[str, List[str]]:
        return {a.path: a.imports[:10] for a in analyses}
    
    def _find_entry_points(self, files: List[Path]) -> List[str]:
        entry_names = {"main", "index", "app", "server", "api", "setup"}
        return [str(f) for f in files if f.stem.lower() in entry_names][:10]
    
    def _detect_frameworks(self, root: Path) -> List[str]:
        frameworks = []
        pkg = root / "package.json"
        if pkg.exists():
            try:
                data = json.loads(pkg.read_text())
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                if "react" in deps: frameworks.append("React")
                if "next" in deps: frameworks.append("Next.js")
                if "express" in deps: frameworks.append("Express")
            except: pass
        
        for py in root.rglob("*.py"):
            try:
                content = py.read_text()
                if "fastapi" in content: frameworks.append("FastAPI")
                if "flask" in content: frameworks.append("Flask")
                if "sqlalchemy" in content: frameworks.append("SQLAlchemy")
            except: pass
        
        return list(set(frameworks))[:5]
    
    def _detect_architecture(self, analyses: List[FileAnalysis]) -> str:
        has_api = any("api" in a.path.lower() or "route" in a.path.lower() for a in analyses)
        has_models = any("model" in a.path.lower() for a in analyses)
        if has_api and has_models:
            return "MVC"
        elif any("component" in a.path.lower() for a in analyses):
            return "Component-based"
        return "Monolith"
    
    def _find_global_issues(self, analyses: List[FileAnalysis]) -> List[str]:
        issues = []
        large = [a for a in analyses if a.lines > 500]
        if large:
            issues.append(f"{len(large)} large files may need splitting")
        return issues[:10]
    
    def _generate_suggestions(self, analyses: List[FileAnalysis]) -> List[str]:
        suggestions = []
        no_tests = not any("test" in a.path.lower() for a in analyses)
        if no_tests and len(analyses) > 5:
            suggestions.append("No test files found - add tests")
        return suggestions[:5]
    
    def _overall_complexity(self, analyses: List[FileAnalysis]) -> int:
        if not analyses:
            return 1
        return min(100, int((sum(a.complexity_score for a in analyses) / len(analyses)) * 10))
    
    def analyze_and_report(self, path: str = ".") -> str:
        """Format as text report."""
        r = self.analyze(path)
        lines = [
            f"📊 Codebase Analysis: {r.root_path}",
            "=" * 50,
            f"📁 Files: {r.total_files} | 📝 Lines: {r.total_lines}",
            "",
            "🗣️ Languages:",
        ]
        for lang, count in sorted(r.languages.items(), key=lambda x: -x[1]):
            lines.append(f"  {lang}: {count}")
        if r.frameworks_detected:
            lines.append(f"\n🛠️ Frameworks: {', '.join(r.frameworks_detected)}")
        lines.append(f"\n🏗️ Architecture: {r.architecture_pattern}")
        lines.append(f"⚡ Complexity: {r.complexity_score}/100")
        if r.issues:
            lines.append("\n⚠️ Issues:")
            for i in r.issues[:5]:
                lines.append(f"  - {i}")
        return "\n".join(lines)
    
    def analyze_for_llm(self, path: str = ".") -> str:
        r = self.analyze(path)
        return f"""CODEBASE: {r.total_files} files, {r.total_lines} lines
Languages: {r.languages}
Frameworks: {r.frameworks_detected}
Architecture: {r.architecture_pattern}"""


analyzer = CodebaseAnalyzer()

# Wrapper functions
def analyze_and_report(path: str = ".") -> str:
    """Run analysis and format as text report."""
    return analyzer.analyze_and_report(path)

def analyze_for_llm(path: str = ".") -> str:
    """Compact summary for LLM."""
    return analyzer.analyze_for_llm(path)


__all__ = ["CodebaseAnalyzer", "CodebaseReport", "FileAnalysis", "analyzer", "analyze_and_report", "analyze_for_llm"]