"""
🔒 SECURITY TOOLS

Security scanning and audit tools.
"""

import re
import os
from crewai.tools import tool


@tool("scan_security")
def scan_security(path: str = "workspace") -> str:
    """Scan for security issues."""
    issues = []
    
    patterns = {
        "hardcoded_secret": r'(api_key|password|secret|token)\s*=\s*["\'][^"\']+["\']',
        "sql_injection": r'execute\s*\(\s*f["\']|execute\s*\(\s*["\'][^"\']*\+',
        "xss": r'dangerouslySetInnerHTML',
        "eval": r'eval\s*\(',
    }
    
    for root, dirs, files in os.walk(path):
        if any(skip in root for skip in ["node_modules", ".git", "__pycache__"]):
            continue
        
        for file in files:
            if file.endswith((".js", ".ts", ".py", ".jsx", ".tsx")):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        for issue_type, pattern in patterns.items():
                            if re.search(pattern, content, re.IGNORECASE):
                                issues.append(f"{issue_type} in {filepath}")
                except:
                    pass
    
    return "Issues found:\n" + "\n".join(issues) if issues else "No issues found"


@tool("check_dependencies")
def check_dependencies(path: str = "workspace") -> str:
    """Check for outdated dependencies."""
    package_json = os.path.join(path, "package.json")
    requirements_txt = os.path.join(path, "requirements.txt")
    
    if os.path.exists(package_json):
        import subprocess
        try:
            result = subprocess.run(["npm", "outdated"], capture_output=True, text=True, cwd=path)
            return result.stdout
        except:
            pass
    
    if os.path.exists(requirements_txt):
        import subprocess
        try:
            result = subprocess.run(["pip", "list", "--outdated"], capture_output=True, text=True)
            return result.stdout
        except:
            pass
    
    return "No package manager detected"


@tool("audit_code")
def audit_code(path: str = "workspace") -> str:
    """Run code quality audit."""
    package_json = os.path.join(path, "package.json")
    
    if os.path.exists(package_json):
        import subprocess
        try:
            result = subprocess.run(["npx", "eslint", "src/"], capture_output=True, text=True, cwd=path)
            return result.stdout or "No ESLint issues"
        except:
            pass
    
    return "No linter detected"


__all__ = ["scan_security", "check_dependencies", "audit_code"]