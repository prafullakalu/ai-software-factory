from crewai.tools import tool

@tool("write_file")
def writeFile(filename: str, content: str):
    """
    Writes content to a specific file. 
    Use this to save code, documentation, or configuration files.
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Successfully wrote to {filename}"

@tool("read_file")
def readFile(filename: str):
    """
    Reads the content of a file. 
    Use this to review code or check existing project files.
    """
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()