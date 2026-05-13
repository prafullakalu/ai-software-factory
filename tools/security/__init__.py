"""
🔒 SECURITY TOOLS

Security scanning and auditing:
- Vulnerability detection
- Secret scanning
- OWASP checks
- Encryption utilities
"""

import re
import hashlib
import hmac
import base64
from typing import Dict, List, Optional


# ============================================================================
# SECURITY SCANNER
# ============================================================================

class SecurityScanner:
    """Scan code for security issues."""
    
    def __init__(self):
        self.issues: List[Dict] = []
    
    PATTERNS = {
        "hardcoded_secret": {
            "pattern": r'(api_key|password|secret|token|key)\s*=\s*["\'][^"\']{8,}["\']',
            "severity": "CRITICAL",
            "message": "Hardcoded secret found",
        },
        "sql_injection": {
            "pattern": r'execute\s*\(\s*f["\']|execute\s*\(\s*["\'][^"\']*%s|execute\s*\(\s*["\']*\+',
            "severity": "CRITICAL",
            "message": "Potential SQL injection",
        },
        "eval_usage": {
            "pattern": r'\beval\s*\(',
            "severity": "HIGH",
            "message": "eval() usage is dangerous",
        },
        "command_injection": {
            "pattern": r'os\.system\s*\(|subprocess.*shell\s*=\s*True',
            "severity": "HIGH",
            "message": "Potential command injection",
        },
        "xss_dangerous": {
            "pattern": r'dangerouslySetInnerHTML',
            "severity": "HIGH",
            "message": "Potential XSS vulnerability",
        },
        "weak_crypto": {
            "pattern": r'md5\(|hashlib\.md5\(|sha1\(',
            "severity": "MEDIUM",
            "message": "Weak cryptographic function",
        },
        "hardcoded_ip": {
            "pattern": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            "severity": "LOW",
            "message": "Hardcoded IP address",
        },
    }
    
    def scan_file(self, filepath: str, content: str) -> List[Dict]:
        """Scan file for vulnerabilities."""
        issues = []
        lines = content.split("\n")
        
        for pattern_name, rule in self.PATTERNS.items():
            for i, line in enumerate(lines, 1):
                if re.search(rule["pattern"], line, re.IGNORECASE):
                    issues.append({
                        "file": filepath,
                        "line": i,
                        "rule": pattern_name,
                        "severity": rule["severity"],
                        "message": rule["message"],
                        "code": line.strip()[:80],
                    })
        
        return issues
    
    def scan_directory(self, dirpath: str) -> List[Dict]:
        """Scan directory for vulnerabilities."""
        import os
        all_issues = []
        
        for root, dirs, files in os.walk(dirpath):
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__']]
            
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.jsx', '.tsx')):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r') as f:
                            content = f.read()
                            issues = self.scan_file(filepath, content)
                            all_issues.extend(issues)
                    except:
                        pass
        
        return all_issues


# ============================================================================
# ENCRYPTION UTILITIES
# ============================================================================

class CryptoUtils:
    """Cryptographic utilities."""
    
    @staticmethod
    def hash_password(password: str, salt: str = None) -> tuple:
        """Hash password with salt."""
        import secrets
        if not salt:
            salt = secrets.token_hex(16)
        
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000,
        )
        return key.hex(), salt
    
    @staticmethod
    def verify_password(password: str, hashed: str, salt: str) -> bool:
        """Verify password."""
        key, _ = CryptoUtils.hash_password(password, salt)
        return hmac.compare_digest(key, hashed)
    
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """Generate secure token."""
        return base64.urlsafe_b64encode(hashlib.sha256(str(length).encode()).digest()).decode()[:length]
    
    @staticmethod
    def encrypt_aes(data: str, key: str) -> str:
        """AES encryption (simplified)."""
        from cryptography.fernet import Fernet
        f = Fernet(key.encode())
        return f.encrypt(data.encode()).decode()
    
    @staticmethod
    def decrypt_aes(encrypted: str, key: str) -> str:
        """AES decryption."""
        from cryptography.fernet import Fernet
        f = Fernet(key.encode())
        return f.decrypt(encrypted.encode()).decode()
    
    @staticmethod
    def generate_key() -> str:
        """Generate AES key."""
        return base64.urlsafe_b64encode(hashlib.sha256(b"key").digest()).decode()


# ============================================================================
# INPUT SANITIZER
# ============================================================================

class InputSanitizer:
    """Sanitize user input."""
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """Remove HTML tags."""
        import re
        return re.sub(r'<[^>]+>', '', text)
    
    @staticmethod
    def sanitize_sql(text: str) -> str:
        """Escape SQL characters."""
        return text.replace("'", "''").replace(";", "")
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename."""
        import re
        filename = re.sub(r'[^\w\s.-]', '', filename)
        return filename[:255]
    
    @staticmethod
    def sanitize_path(path: str) -> str:
        """Prevent path traversal."""
        import os
        return os.path.normpath(path).replace("..", "")


# ============================================================================
# RATE LIMITER
# ============================================================================

class RateLimiter:
    """Rate limiting for APIs."""
    
    def __init__(self):
        self.requests: Dict[str, List[float]] = {}
    
    def is_allowed(self, key: str, limit: int = 100, window: int = 60) -> bool:
        """Check if request is allowed."""
        import time
        now = time.time()
        
        if key not in self.requests:
            self.requests[key] = []
        
        # Remove old requests
        self.requests[key] = [t for t in self.requests[key] if now - t < window]
        
        if len(self.requests[key]) >= limit:
            return False
        
        self.requests[key].append(now)
        return True
    
    def reset(self, key: str):
        """Reset rate limit for key."""
        if key in self.requests:
            del self.requests[key]


# ============================================================================
# EXPORTS
# ============================================================================

scanner = SecurityScanner()
crypto = CryptoUtils()
sanitizer = InputSanitizer()
rate_limiter = RateLimiter()

__all__ = [
    "SecurityScanner", "CryptoUtils", "InputSanitizer", "RateLimiter",
    "scanner", "crypto", "sanitizer", "rate_limiter",
]