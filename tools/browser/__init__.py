"""
🌐 BROWSER AUTOMATION

Browser automation using requests (no external deps).
For real Playwright/Selenium, add playwright package.
"""

import os
import json
import time
import base64
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# BROWSER TYPES
# ============================================================================

class BrowserDriver(Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"
    SAFARI = "safari"
    PLAYWRIGHT = "playwright"
    REQUESTS = "requests"


@dataclass
class BrowserElement:
    """Browser element."""
    tag: str
    text: str
    attributes: Dict = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}


@dataclass
class BrowserResult:
    """Browser operation result."""
    success: bool
    content: str = ""
    elements: List[BrowserElement] = None
    error: str = ""
    screenshot: Optional[str] = None
    
    def __post_init__(self):
        if self.elements is None:
            self.elements = []


# ============================================================================
# BROWSER CONTROLLER
# ============================================================================

class BrowserController:
    """
    Browser automation controller.
    Uses requests for simple HTTP operations.
    For full browser automation, install playwright.
    """
    
    def __init__(self, driver: BrowserDriver = BrowserDriver.REQUESTS):
        self.driver = driver
        self.session = None
        self.current_url = ""
        self.history: List[str] = []
    
    def init_session(self, headless: bool = True):
        """Initialize browser session."""
        try:
            import requests
            self.session = requests.Session()
            return True
        except ImportError:
            return False
    
    def get(self, url: str, timeout: int = 30) -> BrowserResult:
        """Navigate to URL."""
        if not self.session:
            self.init_session()
        
        try:
            resp = self.session.get(url, timeout=timeout)
            self.current_url = url
            self.history.append(url)
            
            return BrowserResult(
                success=resp.status_code == 200,
                content=resp.text,
            )
        except Exception as e:
            return BrowserResult(success=False, error=str(e))
    
    def post(self, url: str, data: Dict = None, json_data: Dict = None) -> BrowserResult:
        """POST to URL."""
        if not self.session:
            self.init_session()
        
        try:
            resp = self.session.post(url, data=data, json=json_data)
            return BrowserResult(
                success=resp.status_code in [200, 201],
                content=resp.text,
            )
        except Exception as e:
            return BrowserResult(success=False, error=str(e))
    
    def click(self, selector: str) -> BrowserResult:
        """Click element (requires full browser)."""
        return BrowserResult(
            success=False,
            error="Full browser required. Install: pip install playwright && playwright install"
        )
    
    def type(self, selector: str, text: str) -> BrowserResult:
        """Type text (requires full browser)."""
        return BrowserResult(
            success=False,
            error="Full browser required"
        )
    
    def screenshot(self) -> Optional[str]:
        """Take screenshot (requires full browser)."""
        return None
    
    def evaluate(self, js: str) -> str:
        """Execute JavaScript (requires full browser)."""
        return ""
    
    def get_elements(self, selector: str) -> List[BrowserElement]:
        """Get elements (requires full browser)."""
        return []
    
    def wait_for(self, selector: str, timeout: int = 10) -> bool:
        """Wait for element (requires full browser)."""
        return False
    
    def close(self):
        """Close browser."""
        if self.session:
            self.session.close()
            self.session = None


# ============================================================================
# FULL BROWSER (with playwright)
# ============================================================================

class FullBrowser:
    """Full browser automation when playwright is available."""
    
    def __init__(self):
        self.browser = None
        self.page = None
        self.context = None
        self._playwright_available = self._check_playwright()
    
    def _check_playwright(self) -> bool:
        try:
            from playwright.sync_api import sync_playwright
            return True
        except ImportError:
            return False
    
    def launch(self, headless: bool = True) -> bool:
        """Launch browser."""
        if not self._playwright_available:
            return False
        
        try:
            from playwright.sync_api import sync_playwright
            pw = sync_playwright().start()
            self.browser = pw.chromium.launch(headless=headless)
            self.context = self.browser.new_context()
            self.page = self.context.new_page()
            return True
        except:
            return False
    
    def navigate(self, url: str) -> bool:
        """Navigate to URL."""
        if self.page:
            self.page.goto(url)
            return True
        return False
    
    def click(self, selector: str) -> bool:
        """Click element."""
        if self.page:
            self.page.click(selector)
            return True
        return False
    
    def type(self, selector: str, text: str) -> bool:
        """Type text."""
        if self.page:
            self.page.type(selector, text)
            return True
        return False
    
    def fill(self, selector: str, text: str) -> bool:
        """Fill input."""
        if self.page:
            self.page.fill(selector, text)
            return True
        return False
    
    def click(self, selector: str) -> bool:
        """Click element."""
        if self.page:
            self.page.click(selector)
            return True
        return False
    
    def get_text(self, selector: str) -> str:
        """Get text content."""
        if self.page:
            return self.page.text_content(selector) or ""
        return ""
    
    def get_html(self) -> str:
        """Get page HTML."""
        if self.page:
            return self.page.content()
        return ""
    
    def screenshot(self, path: str = None) -> Optional[bytes]:
        """Take screenshot."""
        if self.page:
            return self.page.screenshot(path=path)
        return None
    
    def close(self):
        """Close browser."""
        if self.browser:
            self.browser.close()


# ============================================================================
# EXPORTS
# ============================================================================

browser = BrowserController()
full_browser = FullBrowser()

__all__ = [
    "BrowserDriver",
    "BrowserElement", 
    "BrowserResult",
    "BrowserController",
    "FullBrowser",
    "browser",
    "full_browser",
]