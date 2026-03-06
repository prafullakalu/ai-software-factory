import os

schemaFile = "database/schema.sql"

def saveSchema(schema):
    """Save the SQL schema string to a file."""
    os.makedirs(os.path.dirname(schemaFile), exist_ok=True)
    with open(schemaFile, "w", encoding="utf-8") as f:
        f.write(schema)
    return "schema saved"