from crewai.tools import tool
import subprocess

@tool("run_terminal_command")
def runCommand(command: str):
    """
    Executes a command in the terminal. 
    Use this to install packages (npm install) or run tests.
    """
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)