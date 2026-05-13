"""
🎮 CLI INTERFACE

Command-line interface for the AI Software Factory.
Similar to how Manus AI or other agents work.
"""

import sys
import os
import asyncio
from typing import Optional, List
from dataclasses import dataclass


# ============================================================================
# CLI COMMANDS
# ============================================================================

@dataclass
class CLICommand:
    name: str
    description: str
    aliases: List[str]
    action: callable


class CLI:
    """Command-line interface."""
    
    def __init__(self):
        self.commands: List[CLICommand] = []
        self._register_commands()
    
    def _register_commands(self):
        """Register all commands."""
        self.commands = [
            CLICommand(
                name="create",
                description="Create a new project",
                aliases=["new", "init"],
                action=self.cmd_create,
            ),
            CLICommand(
                name="list",
                description="List all projects",
                aliases=["ls", "ll"],
                action=self.cmd_list,
            ),
            CLICommand(
                name="generate",
                description="Generate code for a project",
                aliases=["gen", "build"],
                action=self.cmd_generate,
            ),
            CLICommand(
                name="deploy",
                description="Deploy a project",
                aliases=["d", "ship"],
                action=self.cmd_deploy,
            ),
            CLICommand(
                name="config",
                description="Configure settings",
                aliases=["cfg", "conf"],
                action=self.cmd_config,
            ),
            CLICommand(
                name="models",
                description="List available AI models",
                aliases=["m", "llm"],
                action=self.cmd_models,
            ),
            CLICommand(
                name="agents",
                description="Manage dynamic agents",
                aliases=["agent"],
                action=self.cmd_agents,
            ),
            CLICommand(
                name="skills",
                description="List available skills",
                aliases=["skill"],
                action=self.cmd_skills,
            ),
            CLICommand(
                name="status",
                description="Check system status",
                aliases=["st", "health"],
                action=self.cmd_status,
            ),
            CLICommand(
                name="help",
                description="Show help",
                aliases=["h", "?"],
                action=self.cmd_help,
            ),
        ]
    
    def cmd_create(self, args: List[str]):
        """Create new project."""
        print("🎨 Creating new project...")
        
        # Parse arguments
        name = args[0] if args else None
        if not name:
            name = input("Project name: ").strip()
        
        project_type = "saas"
        for arg in args:
            if arg.startswith("--type="):
                project_type = arg.split("=")[1]
        
        print(f"   Name: {name}")
        print(f"   Type: {project_type}")
        
        # Create project
        from projects import create_project, ProjectType
        project = create_project(name, project_type=ProjectType(project_type))
        
        print(f"\n✅ Project created: {project.id}")
        return project
    
    def cmd_list(self, args: List[str]):
        """List projects."""
        from projects import list_projects
        
        projects = list_projects()
        
        if not projects:
            print("📁 No projects yet. Create one with: factory create")
            return
        
        print(f"\n📁 Your Projects ({len(projects)}):\n")
        print(f"  {'ID':<10} {'Name':<30} {'Type':<12} {'Status':<12}")
        print("  " + "-" * 64)
        
        for p in projects:
            print(f"  {p.id:<10} {p.name:<30} {p.project_type.value:<12} {p.status.value:<12}")
    
    def cmd_generate(self, args: List[str]):
        """Generate code."""
        if not args:
            print("❌ Project ID required. Usage: factory generate <project-id>")
            return
        
        project_id = args[0]
        from projects import get_project
        
        project = get_project(project_id)
        if not project:
            print(f"❌ Project not found: {project_id}")
            return
        
        print(f"🎨 Generating code for: {project.name}...")
        
        # Generate code
        from core.generator import create_saas
        generator = create_saas(
            name=project.name,
            description=project.description,
        )
        paths = generator.save()
        
        print(f"✅ Generated:")
        print(f"   Frontend: {paths['frontend']}")
        print(f"   Backend: {paths['backend']}")
    
    def cmd_deploy(self, args: List[str]):
        """Deploy project."""
        if not args:
            print("❌ Project ID required. Usage: factory deploy <project-id>")
            return
        
        project_id = args[0]
        print(f"🚀 Deploying project: {project_id}...")
        print("   (Deployment coming soon)")
    
    def cmd_config(self, args: List[str]):
        """Configure settings."""
        if not args:
            # Show current config
            from core.llm.providers import manager
            providers = manager.list_providers()
            
            print("\n⚙️ Current Configuration:\n")
            print("  Providers:")
            for p in providers:
                status = "✅" if p["status"] == "configured" else "❌"
                print(f"    {status} {p['provider']}: {p['model']}")
            
            print("\n  Usage:")
            print("    factory config set openai KEY")
            print("    factory config set anthropic KEY")
            print("    factory config models")
            return
        
        # Parse config commands
        action = args[0]
        
        if action == "set":
            if len(args) < 3:
                print("❌ Usage: factory config set <provider> <api-key>")
                return
            
            provider = args[1]
            api_key = args[2]
            
            os.environ[f"{provider.upper()}_API_KEY"] = api_key
            print(f"✅ Set API key for: {provider}")
        
        elif action == "models":
            from core.llm.providers import get_all_models
            models = get_all_models()
            
            print("\n📦 Available Models:\n")
            for provider, provider_models in models.items():
                print(f"  {provider.upper()}:")
                for model_id, info in provider_models.items():
                    print(f"    - {info['name']} ({model_id})")
    
    def cmd_models(self, args: List[str]):
        """List available models."""
        from core.llm.providers import get_all_models, get_models_by_purpose, get_cheapest_models
        
        filter_type = args[0] if args else None
        
        print("\n🤖 Available AI Models:\n")
        
        if filter_type == "--free" or filter_type == "-f":
            print("🆓 FREE Models (no credit card needed!):\n")
            
            print("  📦 Ollama (local):")
            print("    • llama3 - General purpose")
            print("    • qwen2.5-coder - BEST for coding")
            print("    • mixtral - Fast & capable")
            print("    • codellama - Code specialist")
            print("")
            print("  📦 DeepSeek (free API):")
            print("    • deepseek-coder - Excellent for code")
            print("    • deepseek-chat - General chat")
            print("")
            print("  📦 HuggingFace (free tier):")
            print("    • codellama-70b - Big coder model")
            print("    • starcoder2-15b - New coder")
            return
        
        if filter_type == "--fast" or filter_type == "-f":
            models = get_models_by_purpose("fast")
            print("  ⚡ Fast Models:\n")
        elif filter_type == "--cheap" or filter_type == "-c":
            models = get_cheapest_models()
            print("  💰 Cheap Models:\n")
        elif filter_type == "--coding" or filter_type == "-x":
            models = get_models_by_purpose("coding")
            print("  💻 Coding Models:\n")
        else:
            models = []
            all_models = get_all_models()
            for provider, provider_models in all_models.items():
                print(f"  {provider.upper()}:")
                for model_id, info in provider_models.items():
                    purpose = info.get("purpose", "")
                    cost = f"${info.get('cost', 0)}/1k"
                    print(f"    {info['name']:<25} {purpose:<10} {cost}")
                print()
            return
        
        for m in models[:10]:
            print(f"    {m['provider']}/{m['model']:<25} {m.get('name', '')}")
    
    def cmd_agents(self, args: List[str]):
        """Manage dynamic agents."""
        from core.agents.dynamic import agent_factory, list_all_templates
        
        if not args or args[0] == "list":
            print("\n🤖 Dynamic Agents:\n")
            
            print("Available Templates:")
            templates = list_all_templates()
            
            categories = {
                "frontend_dev": "💻 Frontend",
                "backend_dev": "⚙️ Backend",
                "fullstack_dev": "🔄 Full Stack",
                "mobile_dev": "📱 Mobile",
                "devops": "🚀 DevOps",
                "security_eng": "🔒 Security",
                "cloud_architect": "☁️ Cloud",
                "data_engineer": "📊 Data",
                "ml_engineer": "🤖 ML",
                "product_manager": "📋 Product",
                "designer": "🎨 Design",
                "qa_engineer": "🧪 QA",
                "writer": "📝 Writer",
                "researcher": "🔍 Researcher",
                "code_reviewer": "👀 Code Review",
            }
            
            for t in templates:
                cat = categories.get(t["id"], "📦")
                print(f"  {cat} {t['name']:<25} - {t['role'][:40]}")
            
            print("\nUsage: factory agents create <type>")
        
        elif args[0] == "create" and len(args) > 1:
            template = args[1]
            agent = agent_factory.create_from_template(template)
            if agent:
                print(f"✅ Created agent: {agent.name}")
                print(f"   Role: {agent.role}")
                print(f"   Skills: {', '.join(agent.skills)}")
            else:
                print(f"❌ Unknown template: {template}")
    
    def cmd_skills(self, args: List[str]):
        """List available skills."""
        from core.agents.skills import skill_manager, SkillCategory
        
        category = args[0] if args else None
        
        print("\n🛠️ Available Skills:\n")
        
        if category:
            # Filter by category
            try:
                cat = SkillCategory(category)
                skills = skill_manager.by_category(cat)
                print(f"  {category.upper()} ({len(skills)} skills):\n")
                for s in skills:
                    print(f"    • {s.name}: {s.description}")
            except:
                # Search
                skills = skill_manager.search(category)
                print(f"  Search '{category}':\n")
                for s in skills:
                    print(f"    • {s.id}: {s.description}")
        else:
            # List all categories
            categories = {
                SkillCategory.FRONTEND: "💻 Frontend",
                SkillCategory.BACKEND: "⚙️ Backend",
                SkillCategory.MOBILE: "📱 Mobile",
                SkillCategory.DATABASE: "🗄️ Database",
                SkillCategory.DEVOPS: "🚀 DevOps",
                SkillCategory.CLOUD: "☁️ Cloud",
                SkillCategory.SECURITY: "🔒 Security",
                SkillCategory.DATA: "📊 Data",
                SkillCategory.ML: "🤖 ML",
                SkillCategory.TOOLS: "🔧 Tools",
            }
            
            for cat, name in categories.items():
                skills = skill_manager.by_category(cat)
                print(f"  {name:<15} {len(skills)} skills")
    
    def cmd_status(self, args: List[str]):
        """Check system status."""
        print("\n🔍 System Status:\n")
        
        # Check Ollama
        try:
            import urllib.request
            req = urllib.request.Request("http://localhost:11434/api/tags")
            response = urllib.request.urlopen(req, timeout=2)
            print("  ✅ Ollama: Running")
        except:
            print("  ⚠️  Ollama: Not running (optional)")
        
        # Check providers
        from core.llm.providers import manager
        providers = manager.list_providers()
        
        print("  Providers:")
        for p in providers:
            status = "✅" if p["status"] == "configured" else "❌"
            print(f"    {status} {p['provider']}")
        
        # Check projects
        from projects import get_stats
        stats = get_stats()
        print(f"\n  📊 Projects: {stats['total']}")
        print(f"     Ready: {stats['ready']}")
        print(f"     Deployed: {stats['deployed']}")
    
    def cmd_help(self, args: List[str]):
        """Show help."""
        if args:
            # Show specific command help
            cmd_name = args[0]
            for cmd in self.commands:
                if cmd_name in [cmd.name] + cmd.aliases:
                    print(f"\n🔧 {cmd.name}")
                    print(f"   Aliases: {', '.join(cmd.aliases)}")
                    print(f"   {cmd.description}")
                    return
        
        print("""
╔═══════════════════════════════════════════════════════════════════╗
║           🎮 AI SOFTWARE FACTORY CLI                           ║
╠═══════════════════════════════════════════════════════════════════╣
║
║  USAGE:
║    factory <command> [options]
║
║  COMMANDS:
║
║    create [name]        Create a new project
║      --type=saas        Project type (saas, fintech, api)
║
║    list                 List all projects
║
║    generate <id>       Generate code for project
║
║    deploy <id>         Deploy project
║
║    config [options]    Configure settings
║      set <provider> <key>  Set API key
║      models                Show available models
║
║    models [options]    List AI models
║      --fast               Fast models
║      --cheap              Cheap models
║      --coding             Coding models
║
║    status               Check system status
║
║    help [command]      Show this help
║
║  EXAMPLES:
║
║    factory create my-saas --type=saas
║    factory list
║    factory generate abc123
║    factory config set openai sk-xxx
║    factory models --coding
║
╚═══════════════════════════════════════════════════════════════════╝
""")
    
    def run(self, args: List[str]):
        """Run CLI with arguments."""
        if not args:
            self.cmd_help([])
            return
        
        cmd_name = args[0]
        cmd_args = args[1:]
        
        for cmd in self.commands:
            if cmd_name in [cmd.name] + cmd.aliases:
                cmd.action(cmd_args)
                return
        
        print(f"❌ Unknown command: {cmd_name}")
        print("   Run 'factory help' for usage")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main CLI entry point."""
    cli = CLI()
    cli.run(sys.argv[1:])


if __name__ == "__main__":
    main()