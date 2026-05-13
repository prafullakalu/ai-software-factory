"""
🚀 AI SOFTWARE FACTORY v3.0 - Complete

A powerful system for building SaaS/Fintech applications.
Supports multiple LLM providers and generates full-stack code.

Usage:
    python main.py "Build a payment gateway"          # Quick start
    python cli.py create my-saas --type=saas          # CLI
    python -m ui.server                              # Run UI
"""

import os
import sys


def main():
    """Main entry point."""
    args = sys.argv[1:]
    
    if not args:
        show_banner()
        return
    
    # Check if running CLI
    if args[0] in ["create", "list", "generate", "deploy", "config", "models", "status", "help"]:
        from cli import main as cli_main
        cli_main()
        return
    
    # Otherwise, run with goal
    goal = " ".join(args)
    
    show_banner(goal)
    
    # Run the system
    from orchestrator import create_fullstack_orchestrator
    import asyncio
    
    async def run():
        orchestrator = create_fullstack_orchestrator(
            project_name="generated-project",
            description="AI generated SaaS application",
        )
        result = await orchestrator.execute(goal)
        
        if result.get("success"):
            print("\n✅ Project generated successfully!")
        else:
            print(f"\n❌ Error: {result.get('error')}")
    
    asyncio.run(run())


def show_banner(goal: str = None):
    """Show welcome banner."""
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
║  ├── Azure OpenAI                                                   ║
║  ├── Ollama (Local - Free!)                                         ║
║  └── AWS Bedrock                                                    ║
║                                                                      ║
║  Can Build:                                                        ║
║  ├── SaaS Applications                                              ║
║  ├── Fintech (Payments, Wallets, Banking)                          ║
║  ├── E-commerce Platforms                                           ║
║  ├── REST APIs                                                      ║
║  └── Dashboards                                                     ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════════╝
""")
    
    if goal:
        print(f"\n🎯 Goal: {goal}\n")
        print("🚀 Starting generation...\n")


if __name__ == "__main__":
    main()
    designerAgent,     # UI/UX Designer
