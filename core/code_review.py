"""
🤖 AI CODE REVIEWER

Automated code analysis and review.
Features:
- Security vulnerability detection
- Code quality scoring
- Best practices enforcement
- Performance suggestions
- Readability analysis
"""

import os
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# REVIEW TYPES
# ============================================================================

class IssueSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class IssueType(Enum):
    SECURITY = "security"
    PERFORMANCE = "performance"
    BEST_PRACTICE = "best_practice"
    READABILITY = "readability"
    BUG_RISK = "bug_risk"


@dataclass
class CodeIssue:
    """Code issue found."""
    severity: IssueSeverity
    issue_type: IssueType
    message: str
    line: int
    file: str
    suggestion: str


@dataclass
class CodeReview:
    """Complete code review result."""
    file: str
    issues: List[CodeIssue]
    score: float
    summary: str


# ============================================================================
# PATTERNS
# ============================================================================

SECURITY_PATTERNS = {
    "hardcoded_secret": {
        "pattern": r'(api_key|password|secret|token|key)\s*=\s*["\'][^"\']{8,}["\']',
        "severity": IssueSeverity.CRITICAL,
        "suggestion": "Use environment variables instead of hardcoded secrets",
    },
    "sql_injection": {
        "pattern": r'execute\s*\(\s*f["\']|execute\s*\(\s*["\'][^"\']*%s|execute\s*\(\s*["\']*\+',
        "severity": IssueSeverity.CRITICAL,
        "suggestion": "Use parameterized queries to prevent SQL injection",
    },
    "eval_usage": {
        "pattern": r'\beval\s*\(',
        "severity": IssueSeverity.HIGH,
        "suggestion": "Avoid using eval() as it can execute arbitrary code",
    },
    "pickle_usage": {
        "pattern": r'\bpickle\.loads?\(',
        "severity": IssueSeverity.HIGH,
        "suggestion": "Use JSON or safer serialization methods",
    },
    "command_injection": {
        "pattern": r'os\.system\s*\(|subprocess.*shell\s*=\s*True',
        "severity": IssueSeverity.HIGH,
        "suggestion": "Avoid shell=True to prevent command injection",
    },
    "xss_dangerous": {
        "pattern": r'dangerouslySetInnerHTML|dangerouslySetInnerHTML\s*\(',
        "severity": IssueSeverity.HIGH,
        "suggestion": "Sanitize HTML before using dangerouslySetInnerHTML",
    },
    "weak_crypto": {
        "pattern": r'md5\(|hashlib\.md5\(|sha1\(',
        "severity": IssueSeverity.MEDIUM,
        "suggestion": "Use stronger hashing like bcrypt or argon2",
    },
}

BEST_PRACTICE_PATTERNS = {
    "console_log": {
        "pattern": r'console\.log\(|print\(',
        "severity": IssueSeverity.LOW,
        "suggestion": "Remove debug statements in production code",
    },
    "unused_import": {
        "pattern": r'^import\s+\w+\s*$',
        "severity": IssueSeverity.LOW,
        "suggestion": "Remove unused imports",
    },
    "todo_comment": {
        "pattern": r'#\s*TODO|#\s*FIXME|#\s*HACK',
        "severity": IssueSeverity.INFO,
        "suggestion": "Address TODO comments before production",
    },
    "broad_exception": {
        "pattern": r'except\s*:\s*$',
        "severity": IssueSeverity.MEDIUM,
        "suggestion": "Catch specific exceptions instead of broad except",
    },
    "nested_callbacks": {
        "pattern": r'\.then\(.+\.then\(|\.then\(.+\.catch\(',
        "severity": IssueSeverity.MEDIUM,
        "suggestion": "Use async/await instead of nested callbacks",
    },
}

PERFORMANCE_PATTERNS = {
    "n_plus_one": {
        "pattern": r'for\s+\w+\s+in\s+\w+:\s*\n\s+\w+\.query\(',
        "severity": IssueSeverity.MEDIUM,
        "suggestion": "Use eager loading to avoid N+1 queries",
    },
    "memory_leak": {
        "pattern": r'addEventListener.*removeEventListener',
        "severity": IssueSeverity.MEDIUM,
        "suggestion": "Ensure event listeners are properly removed",
    },
    "sync_blocking": {
        "pattern": r'time\.sleep\(|Thread\.sleep\(',
        "severity": IssueSeverity.LOW,
        "suggestion": "Use async/await for non-blocking delays",
    },
}


# ============================================================================
# CODE REVIEWER
# ============================================================================

class AICodeReviewer:
    """AI-powered code reviewer."""
    
    def __init__(self):
        self.patterns = {
            **SECURITY_PATTERNS,
            **BEST_PRACTICE_PATTERNS,
            **PERFORMANCE_PATTERNS,
        }
    
    def review_file(self, filepath: str) -> CodeReview:
        """Review a single file."""
        issues = []
        
        if not os.path.exists(filepath):
            return CodeReview(
                file=filepath,
                issues=[],
                score=100,
                summary="File not found",
            )
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")
        except:
            return CodeReview(
                file=filepath,
                issues=[],
                score=100,
                summary="Could not read file",
            )
        
        # Check patterns
        for line_num, line in enumerate(lines, 1):
            for pattern_name, pattern_info in self.patterns.items():
                if re.search(pattern_info["pattern"], line, re.IGNORECASE):
                    issues.append(CodeIssue(
                        severity=pattern_info["severity"],
                        issue_type=IssueType.SECURITY if pattern_name in SECURITY_PATTERNS 
                                   else IssueType.BEST_PRACTICE if pattern_name in BEST_PRACTICE_PATTERNS
                                   else IssueType.PERFORMANCE,
                        message=f"Found: {pattern_name}",
                        line=line_num,
                        file=filepath,
                        suggestion=pattern_info["suggestion"],
                    ))
        
        # Calculate score
        score = self._calculate_score(issues)
        
        # Generate summary
        summary = self._generate_summary(issues)
        
        return CodeReview(
            file=filepath,
            issues=issues,
            score=score,
            summary=summary,
        )
    
    def review_directory(self, dirpath: str) -> List[CodeReview]:
        """Review all files in a directory."""
        reviews = []
        
        for root, dirs, files in os.walk(dirpath):
            # Skip common non-code directories
            dirs[:] = [d for d in dirs if d not in 
                      ['node_modules', '.git', '__pycache__', 'venv', '.venv', 'dist', 'build']]
            
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.tsx', '.jsx', '.go', '.rs', '.java')):
                    filepath = os.path.join(root, file)
                    review = self.review_file(filepath)
                    if review.issues:  # Only include files with issues
                        reviews.append(review)
        
        return reviews
    
    def _calculate_score(self, issues: List[CodeIssue]) -> float:
        """Calculate code score (0-100)."""
        if not issues:
            return 100
        
        # Deduct points based on severity
        deductions = {
            IssueSeverity.CRITICAL: 15,
            IssueSeverity.HIGH: 10,
            IssueSeverity.MEDIUM: 5,
            IssueSeverity.LOW: 2,
            IssueSeverity.INFO: 1,
        }
        
        score = 100
        for issue in issues:
            score -= deductions.get(issue.severity, 0)
        
        return max(0, score)
    
    def _generate_summary(self, issues: List[CodeIssue]) -> str:
        """Generate review summary."""
        if not issues:
            return "✅ No issues found! Great code!"
        
        # Count by severity
        critical = sum(1 for i in issues if i.severity == IssueSeverity.CRITICAL)
        high = sum(1 for i in issues if i.severity == IssueSeverity.HIGH)
        medium = sum(1 for i in issues if i.severity == IssueSeverity.MEDIUM)
        low = sum(1 for i in issues if i.severity == IssueSeverity.LOW)
        
        parts = []
        if critical > 0:
            parts.append(f"{critical} critical")
        if high > 0:
            parts.append(f"{high} high")
        if medium > 0:
            parts.append(f"{medium} medium")
        if low > 0:
            parts.append(f"{low} low")
        
        return f"Found {', '.join(parts)} issues"
    
    def format_report(self, reviews: List[CodeReview]) -> str:
        """Format complete review report."""
        lines = [
            "\n" + "="*60,
            "🤖 AI CODE REVIEW REPORT",
            "="*60 + "\n",
        ]
        
        total_issues = sum(len(r.issues) for r in reviews)
        avg_score = sum(r.score for r in reviews) / max(len(reviews), 1)
        
        lines.append(f"📊 Files reviewed: {len(reviews)}")
        lines.append(f"⚠️  Total issues: {total_issues}")
        lines.append(f"📈 Average score: {avg_score:.1f}/100\n")
        
        # Group by severity
        severity_counts = {}
        for review in reviews:
            for issue in review.issues:
                sev = issue.severity.value
                severity_counts[sev] = severity_counts.get(sev, 0) + 1
        
        if severity_counts:
            lines.append("📋 Issues by severity:")
            for sev in ["critical", "high", "medium", "low", "info"]:
                if sev in severity_counts:
                    emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵", "info": "ℹ️"}[sev]
                    lines.append(f"  {emoji} {sev.upper()}: {severity_counts[sev]}")
        
        lines.append("\n" + "-"*60)
        
        # Show issues
        for review in reviews:
            if not review.issues:
                continue
            
            lines.append(f"\n📁 {review.file}")
            lines.append(f"   Score: {review.score}/100")
            
            for issue in review.issues:
                emoji = {
                    IssueSeverity.CRITICAL: "🔴",
                    IssueSeverity.HIGH: "🟠",
                    IssueSeverity.MEDIUM: "🟡",
                    IssueSeverity.LOW: "🔵",
                    IssueSeverity.INFO: "ℹ️",
                }.get(issue.severity, "•")
                
                lines.append(f"  {emoji} Line {issue.line}: {issue.message}")
                lines.append(f"     💡 {issue.suggestion}")
        
        lines.append("\n" + "="*60)
        
        return "\n".join(lines)


# ============================================================================
# EXPORTS
# ============================================================================

reviewer = AICodeReviewer()


__all__ = [
    "AICodeReviewer",
    "CodeIssue",
    "CodeReview",
    "IssueSeverity",
    "IssueType",
    "reviewer",
]