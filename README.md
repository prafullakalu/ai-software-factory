# 🤖 AI Software Factory

A powerful **AI-powered platform** for building complete SaaS/Fintech applications. Build any web application with the power of AI - completely FREE!

---

## ✨ Features

### 🧠 Multiple LLM Providers (Including FREE!)

| Provider | Models | Cost |
|----------|--------|------|
| **Ollama** | Llama 3, Mixtral, Qwen Coder | **FREE** |
| **DeepSeek** | Coder, Chat | **FREE** |
| **HuggingFace** | 100+ Models | **FREE** |
| **Cohere** | Command R | **FREE Tier** |
| **Google** | Gemini 1.5 Flash | **FREE Tier** |
| **OpenAI** | GPT-4, GPT-4o | Paid |
| **Anthropic** | Claude 3 Sonnet | Paid |
| **Azure** | GPT-4 | Paid |
| **AWS** | Claude on Bedrock | Paid |

### 💼 Project Management

- Track all generated projects
- Multiple project types: SaaS, Fintech, E-commerce, API
- Status tracking: Draft → Generating → Ready → Deployed
- Full statistics dashboard

### ⚡ Complete SaaS Generator

- **Frontend**: Next.js 14 with React, Tailwind CSS, shadcn/ui
- **Backend**: FastAPI with Python, JWT auth, users API
- **Database**: PostgreSQL, Redis (or Supabase/Neon free tier)
- **Features**: Authentication, Dashboard components, API routes

### 💻 Beautiful UI

- Modern dark theme (Paperclip-inspired)
- Dashboard with project stats
- 3-step project creation wizard
- Sidebar navigation

### 🏖️ Code Sandbox

- Test generated code
- Install dependencies
- Run dev servers
- Build projects

### 👁️ Live Preview System

- Browser-based app preview
- Mobile/tablet/desktop viewport
- Hot reload support
- Console & network logging

### 🏪 Template Marketplace

- 6 built-in templates:
  - SaaS Starter Kit
  - Payment Gateway (Fintech)
  - E-commerce Store
  - REST API Boilerplate
  - Admin Dashboard
  - Blog CMS
- Search & filter
- Rating & download tracking

### 💰 Cost Calculator

- Hosting estimates (Vercel, Railway, AWS)
- Database pricing (all FREE tier options!)
- LLM API cost tracking
- **Optimization tips to run 100% FREE**

### 🤖 AI Code Reviewer

- Security vulnerability detection
- Performance issue scanning
- Best practices enforcement
- Code scoring (0-100)
- Fix suggestions

### 🎮 CLI Interface

```bash
# Quick start
python main.py "Build a payment gateway"

# CLI commands
python cli.py create my-saas --type=saas
python cli.py list
python cli.py generate abc123
python cli.py models --free
python cli.py status
```

---

## 🎯 Can Build

- **SaaS Applications** - Auth, billing, dashboard, multi-tenant
- **Fintech** - Payments, wallets, banking API
- **E-commerce** - Products, cart, checkout
- **REST APIs** - Full documentation
- **Dashboards** - Charts, analytics
- **Blogs** - CMS with markdown

---

## 📁 Project Structure

```
ai-software-factory/
├── core/                      # AI System
│   ├── agents/               # 12 specialized AI agents
│   ├── tasks/              # Task definitions
│   ├── llm/                # LLM providers (10+)
│   │   ├── providers.py    # Multi-provider system
│   │   └── free_models.py  # FREE models guide
│   ├── generator.py         # SaaS code generator
│   ├── code_review.py       # AI code reviewer
│   ├── cost_calculator.py   # Cost estimator
│   └── orchestration/
│
├── projects/                 # Project manager
├── templates/                # Templates
│   ├── saas/
│   ├── fintech/
│   └── marketplace.py       # Template marketplace
│
├── sandbox/                 # Code sandbox
│   ├── __init__.py
│   └── preview.py           # Live preview
│
├── ui/                      # React UI
│   ├── components/
│   ├── pages/
│   └── styles/
│
├── tools/                   # Building tools
│   ├── file/
│   ├── database/
│   ├── deployment/
│   ├── testing/
│   ├── security/
│   └── api/
│
├── cli.py                   # CLI interface
├── main.py                  # Entry point
├── .env.example            # API keys template
└── README.md
```

---

## ⚙️ Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure (Optional - Works FREE with Ollama!)

```bash
# Copy the example env file
cp .env.example .env

# Option A: Use Ollama (FREE - runs locally!)
# Install: https://ollama.ai
# Then just run the project!

# Option B: Add API keys for paid providers
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
DEEPSEEK_API_KEY=xxx
```

### 3. Run!

```bash
# Build any web application!
python main.py "Build a SaaS for subscription management"

# Or use CLI
python cli.py create my-saas
python cli.py list
python cli.py status
```

---

## 📊 Statistics

| Metric | Count |
|--------|-------|
| **Total Python Lines** | 5,700+ |
| **AI Agents** | 12+ |
| **LLM Providers** | 10+ |
| **Templates** | 6+ |
| **Tools** | 50+ |

---

## 🏆 Why This Beats Other Tools

| Feature | AI Factory | Paperclip AI | Others |
|---------|-----------|--------------|--------|
| **LLM Providers** | 10+ (many FREE) | Limited | Paid only |
| **Templates** | 6+ built-in | Basic | Extra cost |
| **Cost Calculator** | ✅ Built-in | ❌ | ❌ |
| **Code Review** | ✅ Built-in | ❌ | ❌ |
| **Live Preview** | ✅ Built-in | Limited | ❌ |
| **Price** | **100% FREE** | $$$ | $$$ |

---

## 📖 Documentation

- [Folder Structure](docs/FOLDER_STRUCTURE.md)
- [Free Models Guide](core/llm/free_models.py)
- [CLI Commands](cli.py)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📜 License

MIT License

---

## 🙏 Credits

Built with:
- [CrewAI](https://crewai.com) - Multi-agent framework
- [Ollama](https://ollama.ai) - Local AI models
- [OpenAI](https://openai.com) - AI models
- [Anthropic](https://anthropic.com) - Claude
- [DeepSeek](https://deepseek.com) - Open source AI
- [HuggingFace](https://huggingface.co) - AI models

---

<p align="center">
  <strong>🚀 Build anything. Run for FREE. No credit card required!</strong>
</p>