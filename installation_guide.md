# Installation Guide

Complete installation instructions for EAIFCH (Ethical AI Framework for Cultural Heritage).

## 📋 Requirements

### System Requirements
- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.8 or higher
- **Memory**: 2GB RAM minimum, 4GB recommended
- **Storage**: 500MB free space

### Optional Requirements
- **Rust**: 1.70+ (for high-performance engine)
- **Node.js**: 16+ (for dashboard)
- **Docker**: 20.10+ (for containerized deployment)

---

## 🚀 Quick Installation

### Option 1: Install from PyPI (Recommended for Users)

```bash
pip install eaifch
```

### Option 2: Install from Source (Recommended for Developers)

```bash
# Clone the repository
git clone https://github.com/benseddikahmed-sudo/EAIFCH-Ethical-Framework-for-Cultural-Heritage.git
cd EAIFCH-Ethical-Framework-for-Cultural-Heritage

# Install in development mode
pip install -e .

# Or with all optional dependencies
pip install -e ".[dev,docs,ml,viz]"
```

### Option 3: Docker (Recommended for Production)

```bash
# Pull the image
docker pull yourusername/eaifch:latest

# Or build locally
docker build -t eaifch:latest .

# Run
docker run -p 8000:8000 eaifch:latest
```

---

## 📦 Detailed Installation Steps

### Step 1: Prepare Your Environment

#### Create a Virtual Environment (Recommended)

**On Linux/macOS:**
```bash
python3 -m venv eaifch_env
source eaifch_env/bin/activate
```

**On Windows:**
```bash
python -m venv eaifch_env
eaifch_env\Scripts\activate
```

#### Upgrade pip
```bash
pip install --upgrade pip setuptools wheel
```

### Step 2: Install EAIFCH

#### Basic Installation
```bash
pip install eaifch
```

#### Development Installation
```bash
# Clone repository
git clone https://github.com/benseddikahmed-sudo/EAIFCH-Ethical-Framework-for-Cultural-Heritage.git
cd EAIFCH-Ethical-Framework-for-Cultural-Heritage

# Install with development dependencies
pip install -e ".[dev]"

# Set up pre-commit hooks
pre-commit install
```

#### Custom Installation with Optional Dependencies

```bash
# For machine learning features
pip install eaifch[ml]

# For visualization features
pip install eaifch[viz]

# For documentation building
pip install eaifch[docs]

# Install everything
pip install eaifch[all]
```

### Step 3: Verify Installation

```bash
# Check version
eaifch --version

# Run quick test
python -c "import eaifch; print(eaifch.get_info())"

# Run examples
python examples/01_basic_assessment.py
```

---

## 🔧 Component Installation

### 1. Python Core (Required)

Already installed with basic installation above.

**Test:**
```bash
python -c "from eaifch import EthicalFramework; print('Core installed ✓')"
```

### 2. Rust Engine (Optional, for Performance)

**Install Rust:**
```bash
# On Linux/macOS
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# On Windows, download from: https://rustup.rs/
```

**Build Rust Engine:**
```bash
cd rust_engine
cargo build --release

# Copy library to system path
sudo cp target/release/libeaifch_engine.so /usr/local/lib/
# On macOS: libeaifch_engine.dylib
# On Windows: eaifch_engine.dll
```

**Test:**
```bash
cd rust_engine
cargo test
```

### 3. API Server (Optional)

**Install API dependencies:**
```bash
pip install fastapi uvicorn[standard]
```

**Start server:**
```bash
eaifch serve
# Or manually:
uvicorn eaifch.api:app --reload
```

**Test:**
```bash
curl http://localhost:8000/health
```

### 4. Dashboard (Optional)

**Install Node.js dependencies:**
```bash
cd dashboard
npm install
```

**Start development server:**
```bash
npm start
# Access at: http://localhost:3000
```

**Build for production:**
```bash
npm run build
```

### 5. Documentation (Optional)

**Install documentation dependencies:**
```bash
pip install eaifch[docs]
```

**Build documentation:**
```bash
cd docs
mkdocs build
```

**Serve locally:**
```bash
mkdocs serve
# Access at: http://localhost:8000
```

---

## 🐳 Docker Installation

### Using Docker Compose (Full Stack)

**1. Start all services:**
```bash
docker-compose up -d
```

This starts:
- EAIFCH API (port 8000)
- PostgreSQL database
- Redis cache
- Dashboard (port 3000)
- Nginx reverse proxy (port 80)
- Prometheus monitoring (port 9090)
- Grafana (port 3001)

**2. Verify services:**
```bash
docker-compose ps
```

**3. View logs:**
```bash
docker-compose logs -f eaifch-api
```

**4. Stop services:**
```bash
docker-compose down
```

### Using Docker Only

**Build image:**
```bash
docker build -t eaifch:latest .
```

**Run container:**
```bash
docker run -d \
  --name eaifch \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  eaifch:latest
```

**Check logs:**
```bash
docker logs -f eaifch
```

---

## 🔍 Troubleshooting

### Common Issues

#### 1. Import Error: "No module named 'eaifch'"

**Solution:**
```bash
# Make sure you're in the right virtual environment
which python

# Reinstall
pip uninstall eaifch
pip install -e .
```

#### 2. Permission Denied on Linux/macOS

**Solution:**
```bash
# Use --user flag
pip install --user eaifch

# Or use sudo (not recommended)
sudo pip install eaifch
```

#### 3. SSL Certificate Error

**Solution:**
```bash
# Use trusted host
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org eaifch
```

#### 4. Rust Build Fails

**Solution:**
```bash
# Update Rust
rustup update

# Install required build tools
# On Ubuntu/Debian:
sudo apt-get install build-essential pkg-config libssl-dev

# On macOS:
xcode-select --install

# On Windows:
# Install Visual Studio Build Tools
```

#### 5. Database Connection Error

**Solution:**
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Reset database
docker-compose down -v
docker-compose up -d
```

#### 6. Port Already in Use

**Solution:**
```bash
# Check what's using the port
lsof -i :8000  # On Linux/macOS
netstat -ano | findstr :8000  # On Windows

# Kill the process or use a different port
eaifch serve --port 8080
```

### Getting Help

If you encounter issues not listed here:

1. **Check GitHub Issues**: [Search existing issues](https://github.com/benseddikahmed-sudo/EAIFCH-Ethical-Framework-for-Cultural-Heritage/issues)
2. **Enable Verbose Mode**: Run with `-v` or `--verbose` flag
3. **Check Logs**: `tail -f logs/eaifch.log`
4. **Ask for Help**: [Open a new issue](https://github.com/benseddikahmed-sudo/EAIFCH-Ethical-Framework-for-Cultural-Heritage/issues/new)

---

## ✅ Post-Installation

### Verify Everything Works

Run the complete test suite:

```bash
# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/ -v -m unit
pytest tests/ -v -m integration

# Check code coverage
pytest tests/ --cov=eaifch --cov-report=html
```

### Run Quick Start

```bash
# Interactive quick start
python scripts/quick_start.py

# Or use CLI
eaifch template my_first_project.json
eaifch assess my_first_project.json
```

### Explore Examples

```bash
# Basic assessment
python examples/01_basic_assessment.py

# API usage (requires server running)
eaifch serve &
python examples/02_api_usage.py

# Advanced custom principles
python examples/03_advanced_custom_principles.py
```

---

## 🔄 Updating EAIFCH

### Update from PyPI

```bash
pip install --upgrade eaifch
```

### Update from Source

```bash
cd EAIFCH-Ethical-Framework-for-Cultural-Heritage
git pull origin main
pip install -e . --upgrade
```

### Update Docker Image

```bash
docker pull yourusername/eaifch:latest
docker-compose down
docker-compose up -d
```

---

## 🗑️ Uninstallation

### Remove Python Package

```bash
pip uninstall eaifch
```

### Remove Docker Containers

```bash
docker-compose down -v
docker rmi eaifch:latest
```

### Remove All Files

```bash
# Remove virtual environment
rm -rf eaifch_env

# Remove repository
rm -rf EAIFCH-Ethical-Framework-for-Cultural-Heritage

# Remove configuration files
rm -rf ~/.eaifch
```

---

## 📚 Next Steps

After installation:

1. **Read the Documentation**: [docs/](docs/)
2. **Try Examples**: [examples/README.md](examples/README.md)
3. **Read the Paper**: See research publication for methodology
4. **Join Community**: [GitHub Discussions](https://github.com/benseddikahmed-sudo/EAIFCH-Ethical-Framework-for-Cultural-Heritage/discussions)
5. **Contribute**: See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🆘 Support

Need help?

- **Documentation**: [https://eaifch.readthedocs.io](https://eaifch.readthedocs.io)
- **GitHub Issues**: [Report bugs](https://github.com/benseddikahmed-sudo/EAIFCH-Ethical-Framework-for-Cultural-Heritage/issues)
- **Email**: your-email@institution.fr
- **Community**: [Discussions](https://github.com/benseddikahmed-sudo/EAIFCH-Ethical-Framework-for-Cultural-Heritage/discussions)

---

**Installation successful? Star us on GitHub! ⭐**
