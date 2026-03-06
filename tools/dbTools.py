import os
from crewai.tools import tool

schemaFile = "database/schema.sql"

@tool("save_database_schema")
def saveSchema(schema: str):
    """
    Saves a SQL database schema string to a local file. 
    Use this when the System Architect finishes the DB design.
    """
    os.makedirs(os.path.dirname(schemaFile), exist_ok=True)
    with open(schemaFile, "w", encoding="utf-8") as f:
        f.write(schema)
    return f"Schema successfully saved to {schemaFile}"