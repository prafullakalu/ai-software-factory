# 📁 AI Software Factory v2.0

## Folder Structure

```
ai-software-factory/
├── core/                    # Core AI system
│   ├── agents/             # 12 specialized AI agents
│   ├── tasks/             # Task definitions
│   ├── orchestration/    # Crew coordination
│   ├── memory/           # Shared memory
│   └── llm/             # LLM configuration
│
├── tools/                  # Building tools
│   ├── file/             # File operations
│   ├── database/         # DB & ORM tools
│   ├── git/             # Version control
│   ├── terminal/         # Shell commands
│   ├── deployment/      # Docker, K8s, Vercel
│   ├── testing/          # Pytest, Jest, Playwright
│   ├── security/        # Security scanning
│   └── api/             # OpenAPI docs
│
├── config/                 # Configuration
├── tests/                 # Test suites
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/                   # Documentation
├── src/                    # Generated code
│   ├── frontend/
│   └── backend/
├── infrastructure/         # Deployment configs
│   ├── docker/
│   ├── k8s/
│   └── ci/
├── lib/                    # Utilities
├── types/                  # TypeScript types
├── workspace/              # Working directory
├── main.py                 # Entry point
├── config.py              # Legacy config
├── orchestrator.py         # Legacy orchestrator
├── requirements.txt
└── README.md
```

## Key Components

### 🤖 Core Agents
- `ProductManager` - Sprint planning
- `SystemArchitect` - Architecture design
- `FrontendDeveloper` - React/Next.js
- `BackendDeveloper` - FastAPI/APIs
- `DatabaseEngineer` - Schema design
- `UIDesigner` - UI/UX design
- `QAEngineer` - Testing
- `SecurityEngineer` - Security audit
- `DevOpsEngineer` - Deployment
- `APIDesigner` - API design
- `PerformanceEngineer` - Optimization
- `DocsEngineer` - Documentation

### 🛠️ Tools
- File operations
- Database (Prisma, SQLAlchemy)
- Git operations
- Terminal commands
- Deployment (Docker, K8s, Vercel)
- Testing (Pytest, Jest, Playwright)
- Security scanning
- API docs (OpenAPI, Swagger)

## Usage

```bash
# Run the system
python main.py "Build a sneaker e-commerce site"

# With orchestrator mode
python main.py "Build SaaS" orchestrator
```

## Configuration

Edit `config/` for:
- Environment variables
- Model selection (Ollama, OpenAI, Anthropic)
- Project settings