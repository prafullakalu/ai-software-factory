from crewai import LLM

# CHANGE THIS: Use 'llama3' instead of 'llama3.3'
planningModel = LLM(
    model="ollama/llama3", 
    base_url="http://localhost:11434"
)

codingModel = LLM(
    model="ollama/qwen2.5-coder:7b", 
    base_url="http://localhost:11434"
)