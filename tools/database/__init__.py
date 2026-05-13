"""
🗄️ DATABASE TOOLS

Database operations and ORM tools.
"""

import os
from crewai.tools import tool


@tool("save_schema")
def save_schema(schema: str, path: str = "workspace/database/schema.sql") -> str:
    """Save SQL schema to file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(schema)
    return f"Schema saved: {path}"


@tool("generate_prisma")
def generate_prisma(models: list) -> str:
    """Generate Prisma schema from models."""
    lines = ['generator client {', '  provider = "prisma-client-js"', "}", ""]
    lines.append('datasource db {')
    lines.append('  provider = "postgresql"')
    lines.append('  url      = env("DATABASE_URL")')
    lines.append("}")
    lines.append("")
    
    for model in models:
        lines.append(f"model {model.get('name', 'Model')} {{")
        for field in model.get("fields", []):
            fname = field.get("name")
            ftype = field.get("type", "String")
            optional = "?" if field.get("optional") else ""
            default = f" @default({field.get('default')})" if field.get("default") else ""
            lines.append(f"  {fname} {ftype}{optional}{default}")
        lines.append("}")
        lines.append("")
    
    return "\n".join(lines)


@tool("generate_sqlalchemy")
def generate_sqlalchemy(models: list) -> str:
    """Generate SQLAlchemy models."""
    code = [
        "from sqlalchemy import Column, Integer, String, DateTime",
        "from sqlalchemy.ext.declarative import declarative_base",
        "from datetime import datetime",
        "",
        "Base = declarative_base()",
    ]
    
    for model in models:
        code.append(f"class {model.get('name', 'Model')}(Base):")
        code.append(f"    __tablename__ = '{model.get('table', 'models').lower()}s'")
        code.append("")
        
        for field in model.get("fields", []):
            fname = field.get("name")
            ftype = field.get("type", "String")
            if ftype == "Integer":
                col_type = "Integer"
            elif ftype == "String":
                col_type = f"String({field.get('length', 255)})"
            else:
                col_type = "String(255)"
            code.append(f"    {fname} = Column({col_type})")
        code.append("")
    
    return "\n".join(code)


@tool("generate_migration")
def generate_migration(name: str, direction: str = "up") -> str:
    """Generate migration file."""
    filename = f"workspace/database/migrations/{name}_{direction}.sql"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(f"-- Migration: {name}\n-- Direction: {direction}\n\n")
    return f"Migration created: {filename}"


__all__ = ["save_schema", "generate_prisma", "generate_sqlalchemy", "generate_migration"]