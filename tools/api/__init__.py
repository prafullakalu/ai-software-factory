"""
🔌 API TOOLS

API development and documentation:
- REST API builder
- OpenAPI/Swagger generation
- GraphQL schema
- Request/response validation
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass


# ============================================================================
# API CONFIG
# ============================================================================

@dataclass
class APIEndpoint:
    """API endpoint definition."""
    path: str
    method: str
    handler: str
    description: str = ""
    params: List[Dict] = None
    body: Dict = None
    responses: Dict = None
    
    def __post_init__(self):
        if self.params is None:
            self.params = []
        if self.responses is None:
            self.responses = {}


# ============================================================================
# REST API BUILDER
# ============================================================================

class RESTAPIGenerator:
    """Generate REST API code."""
    
    def __init__(self, name: str):
        self.name = name
        self.endpoints: List[APIEndpoint] = []
        self.middleware: List[str] = []
        self.models: Dict = {}
    
    def add_endpoint(
        self,
        path: str,
        method: str,
        handler: str,
        description: str = "",
    ) -> "RESTAPIGenerator":
        endpoint = APIEndpoint(
            path=path,
            method=method,
            handler=handler,
            description=description,
        )
        self.endpoints.append(endpoint)
        return self
    
    def add_model(self, name: str, fields: Dict) -> "RESTAPIGenerator":
        self.models[name] = fields
        return self
    
    def add_middleware(self, middleware: str) -> "RESTAPIGenerator":
        self.middleware.append(middleware)
        return self
    
    def generate_fastapi(self) -> str:
        """Generate FastAPI code."""
        lines = [
            '"""',
            f"Auto-generated {self.name} API",
            '"""',
            "",
            "from fastapi import FastAPI, HTTPException, Depends",
            "from pydantic import BaseModel, Field",
            "from typing import Optional, List",
            "from datetime import datetime",
            "",
            "app = FastAPI(",
            f'    title="{self.name} API",',
            '    version="1.0.0",',
            ")",
            "",
        ]
        
        # Models
        for name, fields in self.models.items():
            lines.append(f"class {name}(BaseModel):")
            for field, ftype in fields.items():
                if ftype == "str":
                    lines.append(f"    {field}: str")
                elif ftype == "int":
                    lines.append(f"    {field}: int")
                elif ftype == "bool":
                    lines.append(f"    {field}: bool")
                elif "datetime" in ftype:
                    lines.append(f"    {field}: datetime")
            lines.append("")
        
        # Endpoints
        for ep in self.endpoints:
            method = ep.method.upper()
            lines.append(f'@app.{method.lower()}("{ep.path}")')
            
            if ep.body:
                lines.append(f"def {ep.handler}(item: {list(ep.body.keys())[0]}):")
            else:
                lines.append(f"def {ep.handler}():")
            
            lines.append(f'    """{ep.description}"""')
            lines.append("    pass")
            lines.append("")
        
        return "\n".join(lines)
    
    def generate_express(self) -> str:
        """Generate Express.js code."""
        lines = [
            '"""',
            f"Auto-generated {self.name} API",
            '"""',
            "",
            "const express = require('express');",
            "const app = express();",
            "",
            "app.use(express.json());",
            "",
        ]
        
        for ep in self.endpoints:
            method = ep.method.lower()
            lines.append(f'app.{method}("{ep.path}", async (req, res) => {{')
            lines.append(f"    // {ep.description}")
            lines.append("    res.json({ message: 'OK' });")
            lines.append("});")
            lines.append("")
        
        lines.append("app.listen(3000, () => console.log('Server running'));")
        return "\n".join(lines)


# ============================================================================
# OPENAPI GENERATOR
# ============================================================================

class OpenAPIGenerator:
    """Generate OpenAPI/Swagger documentation."""
    
    def __init__(self, title: str, version: str = "1.0.0"):
        self.title = title
        self.version = version
        self.endpoints: List[Dict] = []
        self.models: Dict = {}
    
    def add_endpoint(
        self,
        path: str,
        method: str,
        summary: str,
        params: List[Dict] = None,
        request_body: Dict = None,
        responses: Dict = None,
    ) -> "OpenAPIGenerator":
        self.endpoints.append({
            "path": path,
            "method": method,
            "summary": summary,
            "parameters": params or [],
            "requestBody": request_body,
            "responses": responses or {},
        })
        return self
    
    def add_model(self, name: str, properties: Dict) -> "OpenAPIGenerator":
        self.models[name] = {
            "type": "object",
            "properties": properties,
        }
        return self
    
    def generate(self) -> Dict:
        """Generate OpenAPI spec."""
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": self.title,
                "version": self.version,
            },
            "paths": {},
            "components": {
                "schemas": self.models,
            },
        }
        
        for ep in self.endpoints:
            path = ep["path"]
            method = ep["method"].lower()
            
            spec["paths"][path] = {
                method: {
                    "summary": ep["summary"],
                    "parameters": ep["parameters"],
                    "responses": ep["responses"],
                }
            }
            
            if ep.get("requestBody"):
                spec["paths"][path][method]["requestBody"] = ep["requestBody"]
        
        return spec
    
    def to_yaml(self) -> str:
        """Convert to YAML."""
        import yaml
        return yaml.dump(self.generate(), default_flow_style=False)


# ============================================================================
# GRAPHQL SCHEMA GENERATOR
# ============================================================================

class GraphQLSchemaGenerator:
    """Generate GraphQL schemas."""
    
    def __init__(self):
        self.types: Dict = {}
        self.queries: List[Dict] = []
        self.mutations: List[Dict] = []
    
    def add_type(self, name: str, fields: Dict) -> "GraphQLSchemaGenerator":
        self.types[name] = fields
        return self
    
    def add_query(self, name: str, return_type: str, resolver: str) -> "GraphQLSchemaGenerator":
        self.queries.append({"name": name, "return_type": return_type, "resolver": resolver})
        return self
    
    def add_mutation(self, name: str, input_type: str, return_type: str) -> "GraphQLSchemaGenerator":
        self.mutations.append({"name": name, "input_type": input_type, "return_type": return_type})
        return self
    
    def generate(self) -> str:
        """Generate GraphQL schema."""
        lines = ["type Query {"]
        
        for q in self.queries:
            lines.append(f"    {q['name']}: {q['return_type']}")
        
        lines.append("}")
        lines.append("")
        
        if self.mutations:
            lines.append("type Mutation {")
            for m in self.mutations:
                lines.append(f"    {m['name']}(input: {m['input_type']}): {m['return_type']}")
            lines.append("}")
            lines.append("")
        
        for name, fields in self.types.items():
            lines.append(f"type {name} {{")
            for field, ftype in fields.items():
                lines.append(f"    {field}: {ftype}")
            lines.append("}")
            lines.append("")
        
        return "\n".join(lines)


# ============================================================================
# REQUEST VALIDATOR
# ============================================================================

class RequestValidator:
    """Validate API requests."""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_url(url: str) -> bool:
        import re
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, url))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        import re
        pattern = r'^\+?1?\d{9,15}$'
        return re.match(pattern, phone.replace("-", "").replace(" ", ""))
    
    @staticmethod
    def validate_required(data: Dict, required: List[str]) -> List[str]:
        """Check required fields."""
        missing = []
        for field in required:
            if field not in data or not data[field]:
                missing.append(field)
        return missing


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    "APIEndpoint",
    "RESTAPIGenerator",
    "OpenAPIGenerator",
    "GraphQLSchemaGenerator",
    "RequestValidator",
]