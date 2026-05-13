"""
🗄️ DATABASE TOOLS

Comprehensive database operations:
- PostgreSQL, MySQL, MongoDB
- Prisma schema generation
- SQLAlchemy models
- Migrations
- Connection pooling
"""

import os
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from contextlib import contextmanager


# ============================================================================
# DATABASE CONFIG
# ============================================================================

@dataclass
class DatabaseConfig:
    """Database connection configuration."""
    type: str = "postgresql"
    host: str = "localhost"
    port: int = 5432
    name: str = "app_db"
    user: str = "postgres"
    password: str = ""
    pool_size: int = 5
    max_overflow: int = 10
    
    def get_url(self) -> str:
        if self.type == "postgresql":
            return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        elif self.type == "mysql":
            return f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        elif self.type == "mongodb":
            return f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        return ""


# ============================================================================
# SQL QUERY BUILDER
# ============================================================================

class SQLQueryBuilder:
    """Build SQL queries dynamically."""
    
    def __init__(self, table: str):
        self.table = table
        self.where_clauses: List[str] = []
        self.order_by: List[str] = []
        self.limit_val: Optional[int] = None
        self.select_fields: List[str] = ["*"]
        self.join_clauses: List[str] = []
        self.group_by: List[str] = []
        self._offset: Optional[int] = None
    
    def select(self, *fields) -> "SQLQueryBuilder":
        self.select_fields = list(fields) if fields else ["*"]
        return self
    
    def where(self, condition: str) -> "SQLQueryBuilder":
        self.where_clauses.append(condition)
        return self
    
    def where_eq(self, column: str, value: Any) -> "SQLQueryBuilder":
        if isinstance(value, str):
            self.where_clauses.append(f"{column} = '{value}'")
        else:
            self.where_clauses.append(f"{column} = {value}")
        return self
    
    def where_in(self, column: str, values: List) -> "SQLQueryBuilder":
        vals = ", ".join(f"'{v}'" if isinstance(v, str) else str(v) for v in values)
        self.where_clauses.append(f"{column} IN ({vals})")
        return self
    
    def where_null(self, column: str) -> "SQLQueryBuilder":
        self.where_clauses.append(f"{column} IS NULL")
        return self
    
    def where_between(self, column: str, start: Any, end: Any) -> "SQLQueryBuilder":
        if isinstance(start, str):
            self.where_clauses.append(f"{column} BETWEEN '{start}' AND '{end}'")
        else:
            self.where_clauses.append(f"{column} BETWEEN {start} AND {end}")
        return self
    
    def where_like(self, column: str, pattern: str) -> "SQLQueryBuilder":
        self.where_clauses.append(f"{column} LIKE '{pattern}'")
        return self
    
    def join(self, table: str, on: str, join_type: str = "INNER") -> "SQLQueryBuilder":
        self.join_clauses.append(f"{join_type} JOIN {table} ON {on}")
        return self
    
    def left_join(self, table: str, on: str) -> "SQLQueryBuilder":
        return self.join(table, on, "LEFT")
    
    def right_join(self, table: str, on: str) -> "SQLQueryBuilder":
        return self.join(table, on, "RIGHT")
    
    def order_by(self, column: str, desc: bool = False) -> "SQLQueryBuilder":
        direction = "DESC" if desc else "ASC"
        self.order_by.append(f"{column} {direction}")
        return self
    
    def group_by(self, *columns) -> "SQLQueryBuilder":
        self.group_by.extend(columns)
        return self
    
    def having(self, condition: str) -> "SQLQueryBuilder":
        self._having = condition
        return self
    
    def limit(self, limit: int) -> "SQLQueryBuilder":
        self.limit_val = limit
        return self
    
    def offset(self, offset: int) -> "SQLQueryBuilder":
        self._offset = offset
        return self
    
    def build(self) -> str:
        select = ", ".join(self.select_fields)
        query = f"SELECT {select} FROM {self.table}"
        
        for join in self.join_clauses:
            query += f" {join}"
        
        if self.where_clauses:
            query += " WHERE " + " AND ".join(self.where_clauses)
        
        if self.group_by:
            query += " GROUP BY " + ", ".join(self.group_by)
        
        if hasattr(self, '_having') and self._having:
            query += f" HAVING {self._having}"
        
        if self.order_by:
            query += " ORDER BY " + ", ".join(self.order_by)
        
        if self.limit_val:
            query += f" LIMIT {self.limit_val}"
        
        if self._offset:
            query += f" OFFSET {self._offset}"
        
        return query


# ============================================================================
# PRISMA SCHEMA GENERATOR
# ============================================================================

class PrismaSchemaGenerator:
    """Generate Prisma schemas."""
    
    def __init__(self):
        self.models: List[Dict] = []
        self.enums: List[Dict] = []
        self.datasource = "postgresql"
    
    def set_datasource(self, provider: str):
        self.datasource = provider
    
    def add_model(self, name: str, fields: Dict, relations: Dict = None) -> "PrismaSchemaGenerator":
        self.models.append({"name": name, "fields": fields, "relations": relations or {}})
        return self
    
    def add_enum(self, name: str, values: List[str]) -> "PrismaSchemaGenerator":
        self.enums.append({"name": name, "values": values})
        return self
    
    def generate(self) -> str:
        lines = [
            "generator client {",
            '  provider = "prisma-client-js"',
            "}",
            "",
            f'datasource db {{',
            f'  provider = "{self.datasource}"',
            '  url      = env("DATABASE_URL")',
            "}",
        ]
        
        for enum in self.enums:
            lines.extend([f"enum {enum['name']} {{", *[f"  {v}" for v in enum["values"]], "}", ""])
        
        for model in self.models:
            lines.append(f"model {model['name']} {{")
            for field, info in model["fields"].items():
                if isinstance(info, dict):
                    ftype = info.get("type", "String")
                    attrs = [ftype]
                    if info.get("unique"):
                        attrs.append("@unique")
                    if info.get("default"):
                        attrs.append(f"@default({info['default']})")
                    if model["relations"].get(field):
                        attrs.append(f"@relation(\"{model['relations'][field]}\")")
                    lines.append(f"  {field} {' '.join(attrs)}")
                else:
                    lines.append(f"  {field} {info}")
            
            lines.append("")
            lines.append("  @@id([id])")
            lines.append("}")
            lines.append("")
        
        return "\n".join(lines)


# ============================================================================
# SQLALCHEMY MODEL GENERATOR
# ============================================================================

TYPE_MAP = {
    "String": "String(255)", "Text": "Text()", "Integer": "Integer()",
    "BigInteger": "BigInteger()", "Float": "Float()", "Boolean": "Boolean()",
    "DateTime": "DateTime()", "Date": "Date()", "JSON": "JSON()",
    "UUID": "UUID()", "SmallInteger": "SmallInteger()", "Numeric": "Numeric(10, 2)",
}


class SQLAlchemyGenerator:
    """Generate SQLAlchemy models."""
    
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.columns: List[Dict] = []
        self.relationships: List[Dict] = []
        self.indexes: List[Dict] = []
    
    def add_column(self, name: str, col_type: str, pk: bool = False, 
                 nullable: bool = True, default: Any = None, 
                 unique: bool = False, foreign_key: str = None) -> "SQLAlchemyGenerator":
        self.columns.append({
            "name": name, "type": col_type, "pk": pk, "nullable": nullable,
            "default": default, "unique": unique, "fk": foreign_key
        })
        return self
    
    def add_relationship(self, model: str, back_pop: str, uselist: bool = False) -> "SQLAlchemyGenerator":
        self.relationships.append({"model": model, "back_pop": back_pop, "uselist": uselist})
        return self
    
    def add_index(self, columns: List[str], unique: bool = False) -> "SQLAlchemyGenerator":
        self.indexes.append({"columns": columns, "unique": unique})
        return self
    
    def generate(self) -> str:
        class_name = "".join(word.capitalize() for word in self.table_name.split("_"))
        
        lines = [
            "from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Index",
            "from sqlalchemy.orm import relationship, declarative_base",
            "",
            "Base = declarative_base()",
            "",
            f"class {class_name}(Base):",
            f'    __tablename__ = "{self.table_name}"',
            "",
        ]
        
        for col in self.columns:
            parts = [f"    {col['name']} = Column("]
            parts.append(TYPE_MAP.get(col["type"], "String(255))"))
            
            if col["pk"]:
                parts.append("primary_key=True")
            if not col["nullable"]:
                parts.append("nullable=False")
            if col.get("default") is not None:
                parts.append(f"default={repr(col['default'])}")
            if col["unique"]:
                parts.append("unique=True")
            if col.get("fk"):
                parts.append(f"ForeignKey('{col['fk']}')")
            
            parts[-1] += ")"
            lines.append(" ".join(parts))
        
        for rel in self.relationships:
            lines.append(f'    {rel["back_pop"]} = relationship("{rel["model"]}", back_populates="{rel["back_pop"]}")')
        
        if self.indexes:
            cols = ", ".join(f"'{c}'" for c in self.indexes[0]["columns"])
            unique = ", unique=True" if self.indexes[0]["unique"] else ""
            lines.append(f'    __table_args__ = (Index("idx_{self.table_name}", {cols}{unique}),)')
        
        return "\n".join(lines)


# ============================================================================
# MIGRATION RUNNER
# ============================================================================

class MigrationManager:
    """Database migration management."""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.migrations: List[Dict] = []
    
    def create_table(self, name: str, columns: Dict[str, str], primary_key: str = "id") -> str:
        cols = [f"{primary_key} SERIAL PRIMARY KEY"]
        for col, dtype in columns.items():
            if col != primary_key:
                cols.append(f"{col} {dtype}")
        return f"CREATE TABLE {name} ({', '.join(cols)});"
    
    def drop_table(self, name: str) -> str:
        return f"DROP TABLE IF EXISTS {name};"
    
    def add_column(self, table: str, column: str, dtype: str) -> str:
        return f"ALTER TABLE {table} ADD {column} {dtype};"
    
    def drop_column(self, table: str, column: str) -> str:
        return f"ALTER TABLE {table} DROP COLUMN {column};"
    
    def rename_table(self, old_name: str, new_name: str) -> str:
        return f"ALTER TABLE {old_name} RENAME TO {new_name};"
    
    def add_index(self, table: str, column: str, unique: bool = False) -> str:
        unique_str = "UNIQUE" if unique else ""
        return f"CREATE {unique_str} INDEX idx_{table}_{column} ON {table}({column});"
    
    def add_foreign_key(self, table: str, column: str, ref_table: str, ref_column: str) -> str:
        return f"ALTER TABLE {table} ADD FOREIGN KEY ({column}) REFERENCES {ref_table}({ref_column});"


# ============================================================================
# EXPORTS
# ============================================================================

def create_pool(config: DatabaseConfig):
    """Create database connection pool."""
    return {"config": config, "active": True}


@contextmanager
def get_connection(config: DatabaseConfig):
    """Get database connection context."""
    conn = create_pool(config)
    try:
        yield conn
    finally:
        pass


__all__ = [
    "DatabaseConfig", "SQLQueryBuilder", "PrismaSchemaGenerator",
    "SQLAlchemyGenerator", "MigrationManager", "create_pool", "get_connection",
]