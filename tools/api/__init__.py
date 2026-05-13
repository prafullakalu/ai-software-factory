"""
🌐 API TOOLS

API documentation and design tools.
"""

import json
import os
from crewai.tools import tool


@tool("generate_openapi")
def generate_openapi(info: dict, endpoints: list, path: str = "workspace/api/openapi.json") -> str:
    """Generate OpenAPI spec."""
    spec = {
        "openapi": "3.0.0",
        "info": info,
        "paths": {},
    }
    
    for ep in endpoints:
        path_item = ep.get("path", "/")
        method = ep.get("method", "get").lower()
        spec["paths"][path_item] = {
            method: {
                "summary": ep.get("summary", ""),
                "responses": {"200": {"description": "OK"}},
            }
        }
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(spec, f, indent=2)
    return f"OpenAPI spec saved: {path}"


@tool("generate_swagger")
def generate_swagger(openapi_path: str, output_path: str = "workspace/api/index.html") -> str:
    """Generate Swagger UI."""
    html = '''<!DOCTYPE html>
<html>
<head>
  <title>API Docs</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css">
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
  <script>
    SwaggerUIBundle({
      url: "./openapi.json",
      dom_id: "#swagger-ui",
    });
  </script>
</body>
</html>
'''
    with open(output_path, "w") as f:
        f.write(html)
    return f"Swagger UI saved: {output_path}"


@tool("generate_postman")
def generate_postman(info: dict, endpoints: list, path: str = "workspace/api/postman.json") -> str:
    """Generate Postman collection."""
    collection = {
        "info": {
            "name": info.get("title", "API"),
            "description": info.get("description", ""),
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "item": [],
    }
    
    for ep in endpoints:
        item = {
            "name": ep.get("summary", ep.get("path")),
            "request": {
                "method": ep.get("method", "GET").upper(),
                "url": {"raw": "{{baseUrl}}" + ep.get("path")},
            },
        }
        collection["item"].append(item)
    
    with open(path, "w") as f:
        json.dump(collection, f, indent=2)
    return f"Postman collection saved: {path}"


__all__ = ["generate_openapi", "generate_swagger", "generate_postman"]