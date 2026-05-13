"""
👁️ LIVE PREVIEW SYSTEM

Real-time preview of generated applications.
Features:
- Browser-based preview
- Hot reload on code changes
- Mobile/tablet/desktop viewport
- Interactive console
- Network requests viewer
"""

import os
import json
import time
import threading
import http.server
import socketserver
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# PREVIEW TYPES
# ============================================================================

class PreviewDevice(Enum):
    MOBILE = "mobile"
    TABLET = "tablet"
    DESKTOP = "desktop"


class PreviewStatus(Enum):
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    ERROR = "error"


# ============================================================================
# PREVIEW CONFIG
# ============================================================================

@dataclass
class PreviewConfig:
    """Configuration for preview."""
    project_path: str
    port: int = 3000
    device: PreviewDevice = PreviewDevice.DESKTOP
    theme: str = "dark"
    show_console: bool = True
    show_network: bool = True
    hot_reload: bool = True


class LivePreview:
    """Live preview server for generated apps."""
    
    def __init__(self, config: PreviewConfig = None):
        self.config = config or PreviewConfig(project_path=".")
        self.status = PreviewStatus.STOPPED
        self.server = None
        self.thread = None
        self.start_time = None
        self.requests: List[Dict] = []
        self.console_logs: List[Dict] = []
        self.callbacks: Dict[str, List[Callable]] = {
            "on_start": [],
            "on_stop": [],
            "on_request": [],
            "on_error": [],
        }
    
    def on(self, event: str, callback: Callable):
        """Register event callback."""
        if event in self.callbacks:
            self.callbacks[event].append(callback)
    
    def _trigger(self, event: str, *args):
        """Trigger callbacks."""
        for callback in self.callbacks.get(event, []):
            try:
                callback(*args)
            except:
                pass
    
    def start(self) -> Dict[str, Any]:
        """Start the preview server."""
        if self.status == PreviewStatus.RUNNING:
            return {"status": "already_running", "port": self.config.port}
        
        self.status = PreviewStatus.STARTING
        
        try:
            # Start server in background thread
            self.thread = threading.Thread(target=self._run_server)
            self.thread.daemon = True
            self.thread.start()
            
            # Wait for server to start
            time.sleep(1)
            
            self.status = PreviewStatus.RUNNING
            self.start_time = time.time()
            
            self._trigger("on_start", self.config.port)
            
            return {
                "status": "success",
                "port": self.config.port,
                "url": f"http://localhost:{self.config.port}",
            }
        except Exception as e:
            self.status = PreviewStatus.ERROR
            self._trigger("on_error", str(e))
            return {"status": "error", "error": str(e)}
    
    def _run_server(self):
        """Run the preview server."""
        try:
            handler = self._create_handler()
            
            # Allow port reuse
            socketserver.TCPServer.allow_reuse_address = True
            
            self.server = socketserver.TCPServer(("", self.config.port), handler)
            self.server.serve_forever()
        except Exception as e:
            self.status = PreviewStatus.ERROR
            self._trigger("on_error", str(e))
    
    def _create_handler(self):
        """Create custom request handler."""
        project_path = self.config.project_path
        
        class PreviewHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=project_path, **kwargs)
            
            def log_message(self, format, *args):
                # Log requests
                self.server.instance.log_request({
                    "method": self.command,
                    "path": self.path,
                    "status": self.log_request_code,
                    "time": time.time(),
                })
        
        return PreviewHandler
    
    def stop(self):
        """Stop the preview server."""
        if self.server:
            self.server.shutdown()
            self.server = None
        
        self.status = PreviewStatus.STOPPED
        self._trigger("on_stop")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current preview status."""
        uptime = 0
        if self.start_time:
            uptime = time.time() - self.start_time
        
        return {
            "status": self.status.value,
            "port": self.config.port,
            "url": f"http://localhost:{self.config.port}",
            "uptime": uptime,
            "device": self.config.device.value,
            "requests_count": len(self.requests),
            "logs_count": len(self.console_logs),
        }
    
    def get_logs(self, limit: int = 50) -> List[Dict]:
        """Get console logs."""
        return self.console_logs[-limit:]
    
    def get_requests(self, limit: int = 50) -> List[Dict]:
        """Get network requests."""
        return self.requests[-limit:]
    
    def clear_logs(self):
        """Clear console logs."""
        self.console_logs.clear()
    
    def clear_requests(self):
        """Clear network requests."""
        self.requests.clear()


# ============================================================================
# PREVIEW MANAGER
# ============================================================================

class PreviewManager:
    """Manages multiple preview instances."""
    
    def __init__(self):
        self.previews: Dict[str, LivePreview] = {}
        self.default_port = 3000
    
    def create(self, project_id: str, project_path: str, port: int = None) -> LivePreview:
        """Create a new preview."""
        if port is None:
            port = self.default_port + len(self.previews)
        
        config = PreviewConfig(
            project_path=project_path,
            port=port,
        )
        
        preview = LivePreview(config)
        self.previews[project_id] = preview
        
        return preview
    
    def get(self, project_id: str) -> Optional[LivePreview]:
        """Get preview by project ID."""
        return self.previews.get(project_id)
    
    def start(self, project_id: str) -> Dict[str, Any]:
        """Start preview."""
        preview = self.get(project_id)
        if not preview:
            return {"status": "error", "error": "Project not found"}
        return preview.start()
    
    def stop(self, project_id: str) -> bool:
        """Stop preview."""
        preview = self.get(project_id)
        if preview:
            preview.stop()
            return True
        return False
    
    def delete(self, project_id: str) -> bool:
        """Delete preview."""
        if project_id in self.previews:
            self.previews[project_id].stop()
            del self.previews[project_id]
            return True
        return False
    
    def list_all(self) -> List[Dict]:
        """List all previews."""
        return [
            {"project_id": pid, **preview.get_status()}
            for pid, preview in self.previews.items()
        ]


# ============================================================================
# PREVIEW INJECTOR
# ============================================================================

def inject_preview_script(html_content: str, preview_url: str = None) -> str:
    """Inject preview functionality into HTML."""
    
    script = f"""
    <!-- AI Factory Live Preview -->
    <script>
    (function() {{
        const PREVIEW_URL = '{preview_url or ""}';
        const isPreview = window.__AI_FACTORY_PREVIEW__ = true;
        
        // Console capture
        const originalConsole = {{}};
        ['log', 'warn', 'error', 'info'].forEach(method => {{
            originalConsole[method] = console[method];
            console[method] = function(...args) {{
                parent.postMessage({{
                    type: 'console',
                    method: method,
                    args: args.map(a => 
                        typeof a === 'object' ? JSON.stringify(a) : String(a)
                    ),
                    timestamp: Date.now()
                }}, '*');
                originalConsole[method].apply(console, args);
            }};
        }});
        
        // Network capture
        const originalFetch = window.fetch;
        window.fetch = function(...args) {{
            const start = Date.now();
            return originalFetch.apply(this, args).then(response => {{
                parent.postMessage({{
                    type: 'network',
                    method: args[0] || 'fetch',
                    url: args[1]?.url || args[0],
                    status: response.status,
                    duration: Date.now() - start
                }}, '*');
                return response;
            }});
        }};
        
        // Report ready
        window.addEventListener('load', () => {{
            parent.postMessage({{ type: 'ready' }}, '*');
        }});
    }})();
    </script>
    """
    
    # Inject before </body>
    if "</body>" in html_content:
        return html_content.replace("</body>", script + "</body>")
    return html_content + script


def generate_viewport_html(device: PreviewDevice = PreviewDevice.DESKTOP) -> str:
    """Generate viewport wrapper HTML."""
    
    widths = {
        PreviewDevice.MOBILE: "375px",
        PreviewDevice.TABLET: "768px",
        PreviewDevice.DESKTOP: "100%",
    }
    
    return f"""
    <style>
    .preview-viewport {{
        width: {widths[device]};
        height: 100vh;
        margin: 0 auto;
        border: none;
        box-shadow: 0 0 20px rgba(0,0,0,0.3);
    }}
    </style>
    """


# ============================================================================
# EXPORTS
# ============================================================================

preview_manager = PreviewManager()


__all__ = [
    "LivePreview",
    "PreviewManager",
    "PreviewConfig",
    "PreviewDevice",
    "PreviewStatus",
    "inject_preview_script",
    "generate_viewport_html",
    "preview_manager",
]