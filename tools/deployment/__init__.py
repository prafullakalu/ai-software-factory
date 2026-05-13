"""
🚀 DEPLOYMENT TOOLS

Docker, Kubernetes, Vercel, Netlify deployment.
"""

import os
import yaml
import json
from crewai.tools import tool


@tool("save_dockerfile")
def save_dockerfile(dockerfile_type: str = "nextjs", path: str = "workspace/Dockerfile") -> str:
    """Generate Dockerfile."""
    dockerfiles = {
        "nextjs": """FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
""",
        "fastapi": """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
""",
        "nodejs": """FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
EXPOSE 3000
CMD ["node", "index.js"]
""",
    }
    
    content = dockerfiles.get(dockerfile_type, dockerfiles["nodejs"])
    with open(path, "w") as f:
        f.write(content)
    return f"Dockerfile saved: {path}"


@tool("save_docker_compose")
def save_docker_compose(services: list, path: str = "workspace/docker-compose.yml") -> str:
    """Generate docker-compose.yml."""
    compose = {"version": "3.8", "services": {}}
    
    for service in services:
        name = service.get("name", "service")
        compose["services"][name] = {
            "build": service.get("build", "."),
            "ports": service.get("ports", []),
            "environment": service.get("environment", {}),
        }
    
    with open(path, "w") as f:
        yaml.dump(compose, f, default_flow_style=False)
    return f"docker-compose saved: {path}"


@tool("save_k8s_manifests")
def save_k8s_manifests(app_name: str, image: str, port: int = 3000, path: str = "workspace/infrastructure/k8s") -> str:
    """Generate Kubernetes manifests."""
    os.makedirs(path, exist_ok=True)
    
    deployment = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {app_name}
spec:
  replicas: 2
  selector:
    matchLabels:
      app: {app_name}
  template:
    metadata:
      labels:
        app: {app_name}
    spec:
      containers:
      - name: {app_name}
        image: {image}
        ports:
        - containerPort: {port}
"""
    
    service = f"""apiVersion: v1
kind: Service
metadata:
  name: {app_name}
spec:
  selector:
    app: {app_name}
  ports:
  - port: 80
    targetPort: {port}
  type: ClusterIP
"""
    
    with open(f"{path}/deployment.yaml", "w") as f:
        f.write(deployment)
    with open(f"{path}/service.yaml", "w") as f:
        f.write(service)
    
    return f"K8s manifests saved: {path}"


@tool("save_vercel_config")
def save_vercel_config(path: str = "workspace/vercel.json") -> str:
    """Generate Vercel config."""
    config = {
        "buildCommand": "npm run build",
        "outputDirectory": ".next",
        "installCommand": "npm install",
        "framework": "nextjs",
    }
    with open(path, "w") as f:
        json.dump(config, f, indent=2)
    return f"Vercel config saved: {path}"


__all__ = ["save_dockerfile", "save_docker_compose", "save_k8s_manifests", "save_vercel_config"]