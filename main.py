#!/usr/bin/env python3
"""
🤖 AI SOFTWARE FACTORY - Main Entry Point

Usage:
    python main.py "Build a payment gateway"
    python main.py --help
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """Main entry point."""
    # Show banner
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║     ███████╗ ██████╗ ██████╗  ██████╗  █████╗ ███╗   ███╗███████╗██╗  ║
║     ██╔════╝██╔═══██╗██╔══██╗██╔═══██╗██╔══██╗████╗ ████║██╔════╝██║  ║
║     ███████╗██║   ██║██████╔╝██║   ██║███████║██╔████╔██║█████╗  ██║  ║
║     ╚════██║██║   ██║██╔══██╗██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  ╚═╝  ║
║     ███████║╚██████╔╝██║  ██║╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗██╗  ║
║     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ║
║                                                                      ║
║              🤖 AI SaaS/Fintech Factory v3.0                         ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  Supported LLM Providers:                                            ║
║  ├── OpenAI (GPT-4, GPT-4o, GPT-3.5)                             ║
║  ├── Anthropic (Claude 3 Opus, Sonnet, Haiku)                     ║
║  ├── Google (Gemini Pro, Ultra, 1.5)                               ║
║  ├── Ollama (Local - Free!)                                         ║
║  └── DeepSeek (Free!)                                             ║
║                                                                      ║
║  Commands (CLI):                                                  ║
║  ├── run <project>      - Run a new project                          ║
║  ├── python <code>    - Execute Python code                           ║
║  ├── remember <fact>  - Remember a fact                           ║
║  ├── agents        - List all agents                               ║
║  └── exit         - Exit the CLI                                 ║
║                                                                      ║
║  Usage:                                                          ║
║  ├── python factory.py        - Start interactive CLI                  ║
║  ├── python main.py <goal>  - Run a goal directly                      ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════════╝
""")

    # Get goal from command line
    goal = None
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--help', '-h', 'help']:
            print("Usage: python main.py \"Build a payment gateway\"")
            print("       python factory.py    # Interactive CLI")
            sys.exit(0)
        
        goal = ' '.join(sys.argv[1:])
    
    if not goal:
        print("❌ No goal provided!")
        print("Usage: python main.py \"Build a payment gateway\"")
        print("       python factory.py    # Interactive CLI")
        sys.exit(1)
    
    # Run the project
    print(f"🎯 Goal: {goal}")
    print("🚀 Starting generation...\n")
    
    try:
        from orchestrator import runner
        
        ctx = runner.run(goal, goal)
        
        print(f"\n✅ Status: {ctx.status}")
        print(f"📊 Progress: {ctx.progress}%")
        
        if ctx.results:
            print("\n📦 Generated:")
            for key, value in ctx.results.items():
                print(f"   - {key}: {value.get('status', 'done')}")
        
        print("\n🎉 Project generated!")
        print("\n📁 Files saved to: workspace/")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()