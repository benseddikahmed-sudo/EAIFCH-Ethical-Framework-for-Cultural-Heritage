# EAIFCH Project Structure

Complete overview of the project's file organization and architecture.

```
EAIFCH-Ethical-Framework-for-Cultural-Heritage/
│
├── 📁 eaifch/                          # Main Python package
│   ├── __init__.py                     # Package initialization, exports
│   │
│   ├── 📁 core/                        # Core framework modules
│   │   ├── __init__.py
│   │   ├── taxonomy.py                 # 24 ethical principles, 8 categories
│   │   ├── framework.py                # Main EthicalFramework class
│   │   ├── risk_assessor.py           # Risk identification and scoring
│   │   ├── compliance_checker.py      # Regulatory compliance (GDPR, EU AI Act, UNESCO)
│   │   └── assessment.py               # Assessment results and reporting
│   │
│   ├── 📁 api/                         # REST API
│   │   ├── __init__.py
│   │   ├── main.py                     # FastAPI application
│   │   ├── routes/                     # API endpoints
│   │   │   ├── assess.py               # Assessment endpoints
│   │   │   ├── projects.py             # Project management
│   │   │   ├── taxonomy.py             # Taxonomy info
│   │   │   └── reports.py              # Report generation
│   │   ├── models.py                   # Pydantic models
│   │   ├── dependencies.py             # Dependency injection
│   │   └── middleware.py               # Authentication, rate limiting
│   │
│   ├── 📁 utils/                       # Utility functions
│   │   ├── __init__.py
│   │   ├── validators.py               # Data validation
│   │   ├── exporters.py                # Report exporters (PDF, HTML)
│   │   ├── cache.py                    # Caching utilities
│   │   └── logger.py                   # Logging configuration
│   │
│   ├── 📁 db/                          # Database models and migrations
│   │   ├── __init__.py
│   │   ├── models.py                   # SQLAlchemy models
│   │   ├── session.py                  # Database session management
│   │   └── migrations/                 # Alembic migrations
│   │
│   ├── cli.py                          # Command-line interface
│   └── config.py                       # Configuration management
│
├── 📁 rust_engine/                     # High-performance Rust engine (optional)
│   ├── Cargo.toml                      # Rust dependencies
│   ├── Cargo.lock
│   └── src/
│       ├── lib.rs                      # Rust library entry point
│       ├── assessment.rs               # Fast assessment algorithms
│       └── scoring.rs                  # Optimized scoring functions
│
├── 📁 dashboard/                       # React dashboard (optional)
│   ├── package.json
│   ├── public/
│   ├── src/
│   │   ├── App.js                      # Main React component
│   │   ├── components/                 # React components
│   │   │   ├── AssessmentCard.js
│   │   │   ├── CategoryChart.js
│   │   │   └── RiskMatrix.js
│   │   ├── pages/                      # Dashboard pages
│   │   └── api/                        # API client
│   └── build/                          # Production build
│
├── 📁 tests/                           # Test suite (42+ tests)
│   ├── __init__.py
│   ├── conftest.py                     # Pytest configuration
│   ├── test_taxonomy.py                # Taxonomy tests
│   ├── test_framework.py               # Framework tests
│   ├── test_risk_assessor.py          # Risk assessment tests
│   ├── test_compliance.py              # Compliance checker tests
│   ├── test_api.py                     # API endpoint tests
│   ├── 📁 integration/                 # Integration tests
│   │   ├── test_full_assessment.py
│   │   └── test_batch_processing.py
│   └── 📁 fixtures/                    # Test data
│       ├── sample_projects.json
│       └── test_taxonomy.json
│
├── 📁 docs/                            # Documentation (MkDocs)
│   ├── mkdocs.yml                      # MkDocs configuration
│   ├── index.md                        # Documentation home
│   ├── getting-started.md
│   ├── installation.md
│   ├── 📁 framework/                   # Framework documentation
│   │   ├── introduction.md
│   │   ├── principles.md               # The 24 principles
│   │   └── categories/                 # Category-specific docs
│   │       ├── privacy-security.md
│   │       ├── fairness-bias.md
│   │       └── ...
│   ├── 📁 api/                         # API documentation
│   │   ├── overview.md
│   │   ├── rest-api.md
│   │   └── python-sdk.md
│   ├── 📁 use-cases/                   # Real-world examples
│   └── 📁 research/                    # Academic resources
│
├── 📁 examples/                        # Usage examples
│   ├── README.md                       # Examples guide
│   ├── 01_basic_assessment.py          # Basic usage
│   ├── 02_api_usage.py                 # API examples
│   ├── 03_advanced_custom_principles.py # Custom principles
│   └── example_project.json            # Sample project data
│
├── 📁 scripts/                         # Utility scripts
│   ├── quick_start.py                  # Interactive quick start
│   ├── generate_report.py              # Report generator
│   ├── batch_assess.py                 # Batch processing
│   └── export_taxonomy.py              # Export taxonomy to JSON
│
├── 📁 data/                            # Data files
│   ├── taxonomy/                       # Taxonomy definitions
│   │   └── standard_taxonomy.json
│   ├── examples/                       # Example datasets
│   └── schemas/                        # JSON schemas
│
├── 📁 .github/                         # GitHub configuration
│   ├── workflows/                      # GitHub Actions
│   │   ├── ci.yml                      # CI/CD pipeline
│   │   ├── tests.yml                   # Test workflow
│   │   └── deploy.yml                  # Deployment workflow
│   ├── ISSUE_TEMPLATE/                 # Issue templates
│   └── PULL_REQUEST_TEMPLATE.md        # PR template
│
├── 📁 monitoring/                      # Monitoring configuration
│   ├── prometheus.yml                  # Prometheus config
│   └── grafana/
│       ├── dashboards/                 # Grafana dashboards
│       └── datasources/                # Data source configs
│
├── 📁 nginx/                           # Nginx configuration
│   ├── nginx.conf
│   └── ssl/                            # SSL certificates
│
├── 📁 logs/                            # Application logs
│   ├── eaifch.log
│   ├── api.log
│   └── error.log
│
├── 📄 Configuration Files
├── .env.example                        # Environment variables template
├── .gitignore                          # Git ignore rules
├── .dockerignore                       # Docker ignore rules
├── pyproject.toml                      # Python project config (modern)
├── setup.py                            # Python setup (legacy support)
├── requirements.txt                    # Python dependencies
├── Dockerfile                          # Docker image definition
├── docker-compose.yml                  # Multi-container setup
├── Makefile                            # Development commands
│
├── 📄 Documentation Files
├── README.md                           # Main project README
├── CHANGELOG.md                        # Version history
├── CONTRIBUTING.md                     # Contribution guidelines
├── LICENSE                             # MIT License
├── ROADMAP.md                          # Future plans
├── INSTALL.md                          # Installation guide
├── PROJECT_STRUCTURE.md                # This file
│
└── 📄 CI/CD & Quality
    ├── .pre-commit-config.yaml         # Pre-commit hooks
    ├── pytest.ini                      # Pytest configuration
    ├── .coveragerc                     # Coverage settings
    └── .flake8                         # Flake8 linting rules
```

---

## 📦 Package Organization

### Core Package (`eaifch/`)

The main Python package containing all framework functionality:

- **`core/`**: Core ethical framework logic
  - Taxonomy management (24 principles, 8 categories)
  - Risk assessment algorithms
  - Compliance checking
  - Assessment report generation

- **`api/`**: REST API for remote assessments
  - FastAPI-based endpoints
  - Authentication and rate limiting
  - Batch processing support

- **`utils/`**: Helper utilities
  - Data validators
  - Report exporters (PDF, HTML, JSON)
  - Caching and logging

- **`db/`**: Database layer
  - SQLAlchemy models
  - Alembic migrations

---

## 🔧 Development Files

### Configuration Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Modern Python project configuration |
| `setup.py` | Legacy Python setup (backward compatibility) |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment variables template |
| `Makefile` | Development task automation |

### Docker Files

| File | Purpose |
|------|---------|
| `Dockerfile` | Container image definition |
| `docker-compose.yml` | Multi-container orchestration |
| `.dockerignore` | Files to exclude from Docker build |

### CI/CD Files

| File | Purpose |
|------|---------|
| `.github/workflows/ci.yml` | Main CI/CD pipeline |
| `.pre-commit-config.yaml` | Git pre-commit hooks |
| `pytest.ini` | Test configuration |

---

## 📊 Data Flow

```
User Input (Project Data)
    ↓
EthicalFramework.assess()
    ↓
┌─────────────────────────────────┐
│ 1. Taxonomy Validation          │
│    - Check all 24 principles    │
│    - Apply validation rules     │
└──────────────┬──────────────────┘
               ↓
┌─────────────────────────────────┐
│ 2. Category Scoring             │
│    - Calculate 8 category scores│
│    - Apply weights              │
└──────────────┬──────────────────┘
               ↓
┌─────────────────────────────────┐
│ 3. Risk Assessment              │
│    - Identify ethical risks     │
│    - Prioritize by severity     │
└──────────────┬──────────────────┘
               ↓
┌─────────────────────────────────┐
│ 4. Compliance Check             │
│    - GDPR, EU AI Act, UNESCO    │
│    - WCAG, ICOM, UNDRIP         │
└──────────────┬──────────────────┘
               ↓
┌─────────────────────────────────┐
│ 5. Generate Report              │
│    - Overall score              │
│    - Violations list            │
│    - Recommendations            │
└──────────────┬──────────────────┘
               ↓
Assessment Object
    ↓
User Output (Report, Dashboard, API Response)
```

---

## 🏗️ Architecture Layers

```
┌─────────────────────────────────────────────────┐
│          Presentation Layer                      │
│  • CLI (eaifch commands)                        │
│  • REST API (FastAPI)                           │
│  • Dashboard (React)                            │
└────────────────┬────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────┐
│          Application Layer                       │
│  • EthicalFramework                             │
│  • CulturalHeritageProject                      │
│  • Assessment workflow                          │
└────────────────┬────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────┐
│          Business Logic Layer                    │
│  • EthicalTaxonomy                              │
│  • RiskAssessor                                 │
│  • ComplianceChecker                            │
└────────────────┬────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────┐
│          Data Layer                              │
│  • SQLAlchemy models                            │
│  • Redis cache                                  │
│  • File storage                                 │
└─────────────────────────────────────────────────┘
```

---

## 🚀 Deployment Structure

### Development
```
Local Machine
├── Python virtual environment
├── SQLite database
├── Local file storage
└── Development server
```

### Production (Docker Compose)
```
Docker Network
├── EAIFCH API (container)
├── PostgreSQL (container)
├── Redis (container)
├── Dashboard (container)
├── Nginx (container)
├── Prometheus (container)
└── Grafana (container)
```

### Cloud Deployment
```
Cloud Platform (AWS/Azure/GCP)
├── Container Orchestration (ECS/AKS/GKE)
├── Managed Database (RDS/Azure SQL/Cloud SQL)
├── Cache (ElastiCache/Azure Cache/Memorystore)
├── Load Balancer
└── CDN for Dashboard
```

---

## 📝 Key Files Reference

### Must Read First
1. `README.md` - Project overview
2. `INSTALL.md` - Installation instructions
3. `examples/README.md` - Usage examples

### For Users
- `examples/01_basic_assessment.py` - Start here
- `eaifch/cli.py` - CLI commands reference
- `docs/` - Complete documentation

### For Developers
- `CONTRIBUTING.md` - How to contribute
- `eaifch/core/taxonomy.py` - Core framework
- `tests/` - Test suite

### For Researchers
- `ROADMAP.md` - Future plans
- Research paper (link in README)
- `docs/research/` - Methodology

---

## 🔍 Finding What You Need

| I want to... | Look here |
|--------------|-----------|
| Install EAIFCH | `INSTALL.md`, `README.md` |
| Run my first assessment | `examples/01_basic_assessment.py` |
| Use the CLI | `eaifch/cli.py`, run `eaifch --help` |
| Understand the 24 principles | `docs/framework/principles.md` |
| Use the API | `examples/02_api_usage.py`, `docs/api/` |
| Add custom principles | `examples/03_advanced_custom_principles.py` |
| Run tests | `make test` or `pytest tests/` |
| Build documentation | `make docs` or `cd docs && mkdocs build` |
| Deploy with Docker | `docker-compose.yml`, `Dockerfile` |
| Contribute | `CONTRIBUTING.md` |
| Report a bug | `.github/ISSUE_TEMPLATE/` |
| See the roadmap | `ROADMAP.md` |

---

This structure ensures:
- ✅ Clear separation of concerns
- ✅ Easy navigation for newcomers
- ✅ Scalability for future features
- ✅ Best practices for Python packages
- ✅ Professional project organization
