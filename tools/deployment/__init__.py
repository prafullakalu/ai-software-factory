"""
🚀 DEPLOYMENT TOOLS

Deployment and DevOps:
- Docker generation
- Kubernetes configs
- CI/CD pipelines
- Cloud deployment
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass


# ============================================================================
# DOCKER GENERATOR
# ============================================================================

class DockerGenerator:
    """Generate Docker configurations."""
    
    def __init__(self, name: str):
        self.name = name
        self.base_image = "python:3.11-slim"
        self.port = 8000
        self.workdir = "/app"
        self.dependencies: List[str] = []
        self.commands: List[str] = []
        self.env_vars: Dict[str, str] = {}
        self.volumes: List[str] = []
    
    def set_base_image(self, image: str) -> "DockerGenerator":
        self.base_image = image
        return self
    
    def set_port(self, port: int) -> "DockerGenerator":
        self.port = port
        return self
    
    def add_dependency(self, dep: str) -> "DockerGenerator":
        self.dependencies.append(dep)
        return self
    
    def add_command(self, cmd: str) -> "DockerGenerator":
        self.commands.append(cmd)
        return self
    
    def add_env(self, key: str, value: str) -> "DockerGenerator":
        self.env_vars[key] = value
        return self
    
    def add_volume(self, volume: str) -> "DockerGenerator":
        self.volumes.append(volume)
        return self
    
    def generate_dockerfile(self) -> str:
        """Generate Dockerfile."""
        lines = [
            f"FROM {self.base_image}",
            "",
            f"WORKDIR {self.workdir}",
            "",
        ]
        
        # Environment variables
        for key, value in self.env_vars.items():
            lines.append(f'ENV {key}="{value}"')
        
        if self.dependencies:
            lines.append("")
            # For Python
            if "python" in self.base_image.lower():
                lines.append("COPY requirements.txt .")
                lines.append("RUN pip install --no-cache-dir -r requirements.txt")
        
        lines.append("")
        lines.append("COPY . .")
        
        if self.commands:
            lines.append("")
            for cmd in self.commands:
                lines.append(f"RUN {cmd}")
        
        lines.append("")
        lines.append(f"EXPOSE {self.port}")
        lines.append("")
        lines.append(f'CMD ["python", "main.py"]')
        
        return "\n".join(lines)
    
    def generate_docker_compose(self, services: Dict = None) -> str:
        """Generate docker-compose.yml."""
        lines = [
            "version: '3.8'",
            "",
            "services:",
            f"  {self.name}:",
            f"    build: .",
            f"    ports:",
            f'      - "{self.port}:{self.port}"',
        ]
        
        if self.env_vars:
            lines.append("    environment:")
            for key, value in self.env_vars.items():
                lines.append(f'      - {key}={value}')
        
        if self.volumes:
            lines.append("    volumes:")
            for vol in self.volumes:
                lines.append(f'      - {vol}')
        
        lines.append("    restart: unless-stopped")
        
        if services:
            for svc_name, svc_config in services.items():
                lines.append("")
                lines.append(f"  {svc_name}:")
                for key, value in svc_config.items():
                    lines.append(f"    {key}: {value}")
        
        return "\n".join(lines)


# ============================================================================
# KUBERNETES GENERATOR
# ============================================================================

class K8sGenerator:
    """Generate Kubernetes manifests."""
    
    def __init__(self, name: str):
        self.name = name
        self.namespace = "default"
        self.replicas = 1
        self.port = 8000
        self.image = f"{name}:latest"
        self.resources: Dict = {}
        self.env_vars: Dict[str, str] = {}
    
    def set_namespace(self, ns: str) -> "K8sGenerator":
        self.namespace = ns
        return self
    
    def set_replicas(self, replicas: int) -> "K8sGenerator":
        self.replicas = replicas
        return self
    
    def set_image(self, image: str) -> "K8sGenerator":
        self.image = image
        return self
    
    def add_resource(self, resource_type: str, limits: Dict) -> "K8sGenerator":
        self.resources[resource_type] = limits
        return self
    
    def add_env(self, key: str, value: str) -> "K8sGenerator":
        self.env_vars[key] = value
        return self
    
    def generate_deployment(self) -> str:
        """Generate Deployment manifest."""
        lines = [
            "apiVersion: apps/v1",
            "kind: Deployment",
            "metadata:",
            f"  name: {self.name}",
            f"  namespace: {self.namespace}",
            "spec:",
            f"  replicas: {self.replicas}",
            "  selector:",
            "    matchLabels:",
            f"      app: {self.name}",
            "  template:",
            "    metadata:",
            "      labels:",
            f"        app: {self.name}",
            "    spec:",
            "      containers:",
            f"      - name: {self.name}",
            f"        image: {self.image}",
            f"        ports:",
            f"        - containerPort: {self.port}",
        ]
        
        if self.resources:
            lines.append("        resources:")
            if "cpu" in self.resources or "memory" in self.resources:
                lines.append("          requests:")
                if "cpu" in self.resources:
                    lines.append(f"            cpu: {self.resources['cpu'].get('request', '100m')}")
                if "memory" in self.resources:
                    lines.append(f"            memory: {self.resources['memory'].get('request', '128Mi')}")
                lines.append("          limits:")
                if "cpu" in self.resources:
                    lines.append(f"            cpu: {self.resources['cpu'].get('limit', '500m')}")
                if "memory" in self.resources:
                    lines.append(f"            memory: {self.resources['memory'].get('limit', '256Mi')}")
        
        if self.env_vars:
            lines.append("        env:")
            for key, value in self.env_vars.items():
                lines.append(f"        - name: {key}")
                lines.append(f"          value: \"{value}\"")
        
        return "\n".join(lines)
    
    def generate_service(self) -> str:
        """Generate Service manifest."""
        return f"""apiVersion: v1
kind: Service
metadata:
  name: {self.name}
  namespace: {self.namespace}
spec:
  selector:
    app: {self.name}
  ports:
  - port: 80
    targetPort: {self.port}
  type: ClusterIP
"""
    
    def generate_ingress(self, host: str = None) -> str:
        """Generate Ingress manifest."""
        lines = [
            "apiVersion: networking.k8s.io/v1",
            "kind: Ingress",
            "metadata:",
            f"  name: {self.name}",
            f"  namespace: {self.namespace}",
            "spec:",
            "  rules:",
        ]
        
        if host:
            lines.append(f"  - host: {host}")
            lines.append("    http:")
            lines.append("      paths:")
            lines.append(f"      - path: /")
            lines.append("        pathType: Prefix")
            lines.append("        backend:")
            lines.append("          service:")
            lines.append(f"            name: {self.name}")
            lines.append("            port:")
            lines.append("              number: 80")
        
        return "\n".join(lines)


# ============================================================================
# CI/CD PIPELINE GENERATOR
# ============================================================================

class CIPipelineGenerator:
    """Generate CI/CD pipelines."""
    
    def __init__(self, name: str):
        self.name = name
        self.steps: List[Dict] = []
    
    def add_step(self, name: str, run: str, env: Dict = None) -> "CIPipelineGenerator":
        self.steps.append({"name": name, "run": run, "env": env or {}})
        return self
    
    def generate_github_actions(self) -> str:
        """Generate GitHub Actions workflow."""
        lines = [
            f"name: {self.name}",
            "",
            "on:",
            "  push:",
            "    branches: [ main ]",
            "  pull_request:",
            "    branches: [ main ]",
            "",
            "jobs:",
            "  build:",
            "    runs-on: ubuntu-latest",
            "    steps:",
        ]
        
        for step in self.steps:
            lines.append(f"      - name: {step['name']}")
            lines.append(f"        run: |")
            for line in step['run'].split('\n'):
                lines.append(f"          {line}")
            
            if step.get('env'):
                lines.append("        env:")
                for key, value in step['env'].items():
                    lines.append(f"          {key}: {value}")
        
        return "\n".join(lines)
    
    def generate_gitlab_ci(self) -> str:
        """Generate GitLab CI pipeline."""
        lines = [
            f"image: python:3.11",
            "",
            "stages:",
            "  - build",
            "  - test",
            "  - deploy",
            "",
        ]
        
        for step in self.steps:
            lines.append(f"{step['name'].lower().replace(' ', '-')}:")
            lines.append(f"  stage: {'build' if 'build' in step['name'].lower() else 'test'}")
            lines.append("  script:")
            for line in step['run'].split('\n'):
                lines.append(f"    - {line}")
            lines.append("")
        
        return "\n".join(lines)


# ============================================================================
# EXPORTS
# ============================================================================

docker_gen = DockerGenerator("app")
k8s_gen = K8sGenerator("app")
ci_gen = CIPipelineGenerator("app")

__all__ = [
    "DockerGenerator",
    "K8sGenerator",
    "CIPipelineGenerator",
    "docker_gen",
    "k8s_gen",
    "ci_gen",
]