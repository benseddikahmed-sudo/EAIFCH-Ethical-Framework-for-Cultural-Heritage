# Contributing to EAIFCH

First off, thank you for considering contributing to EAIFCH! 🎉

The Ethical AI Framework for Cultural Heritage (EAIFCH) is an open-source project that aims to ensure responsible AI use in cultural heritage management. We welcome contributions from researchers, developers, cultural heritage professionals, and anyone passionate about ethical AI.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Process](#development-process)
- [Style Guidelines](#style-guidelines)
- [Testing Requirements](#testing-requirements)
- [Documentation](#documentation)
- [Community](#community)

---

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [your-email@institution.fr].

### Our Pledge

We are committed to making participation in this project a harassment-free experience for everyone, regardless of:
- Age, body size, disability, ethnicity, gender identity and expression
- Level of experience, nationality, personal appearance, race, religion
- Sexual identity and orientation

---

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the problem
- **Expected vs. actual behavior**
- **Screenshots** (if applicable)
- **Environment details**: OS, Python version, package versions

**Bug Report Template:**
```markdown
**Description**: Brief description of the bug

**Steps to Reproduce**:
1. Step one
2. Step two
3. ...

**Expected Behavior**: What should happen

**Actual Behavior**: What actually happened

**Environment**:
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.10.5]
- EAIFCH version: [e.g., 1.1.0]

**Additional Context**: Any other relevant information
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the proposed functionality
- **Explain why this enhancement would be useful** to most EAIFCH users
- **List examples** of how this feature would be used

### Contributing Code

1. **Fork** the repository
2. **Create a branch** from `develop` for your feature or bugfix
3. **Make your changes** following our style guidelines
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Submit a pull request**

#### Branch Naming Convention

- `feature/descriptive-name` - for new features
- `bugfix/issue-number-description` - for bug fixes
- `docs/what-is-updated` - for documentation updates
- `test/what-is-tested` - for test additions

Example: `feature/add-ml-bias-detector` or `bugfix/42-fix-api-timeout`

---

## Development Process

### Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/EAIFCH-Ethical-Framework-for-Cultural-Heritage.git
cd EAIFCH-Ethical-Framework-for-Cultural-Heritage

# Add upstream remote
git remote add upstream https://github.com/benseddikahmed-sudo/EAIFCH-Ethical-Framework-for-Cultural-Heritage.git

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev,docs]"

# Install pre-commit hooks
pre-commit install
```

### Development Workflow

```bash
# 1. Sync with upstream
git checkout develop
git pull upstream develop

# 2. Create a feature branch
git checkout -b feature/my-new-feature

# 3. Make your changes
# ... edit files ...

# 4. Run tests
pytest tests/ -v --cov=eaifch

# 5. Run linters
black eaifch tests
flake8 eaifch tests
mypy eaifch

# 6. Commit your changes
git add .
git commit -m "feat: add new ethical principle for XYZ"

# 7. Push to your fork
git push origin feature/my-new-feature

# 8. Create a Pull Request on GitHub
```

### Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(taxonomy): add new cultural sensitivity principle

docs(api): update REST API authentication examples

fix(risk-assessor): correct calculation for high-priority risks

test(integration): add tests for UNESCO site digitization
```

---

## Style Guidelines

### Python Code Style

We follow **PEP 8** with some modifications:
- Line length: 100 characters
- Use **Black** for automatic formatting
- Use **type hints** where appropriate

```python
from typing import List, Dict, Optional

def assess_ethical_risk(
    project_data: Dict[str, Any],
    principles: List[EthicalPrinciple],
    threshold: float = 0.7
) -> Optional[RiskAssessment]:
    """
    Assess ethical risks for a cultural heritage AI project.
    
    Args:
        project_data: Dictionary containing project details
        principles: List of ethical principles to check
        threshold: Minimum compliance score (0-1)
    
    Returns:
        RiskAssessment object or None if no risks detected
    
    Example:
        >>> data = {"name": "Museum AI", "bias_testing": False}
        >>> principles = taxonomy.get_principles("fairness_bias")
        >>> assessment = assess_ethical_risk(data, principles)
    """
    # Implementation here
    pass
```

### Rust Code Style

For the Rust engine:
- Follow standard Rust conventions
- Run `cargo fmt` before committing
- Run `cargo clippy` and address warnings

```rust
/// Assesses ethical compliance for a heritage project
pub fn assess_project(config: &ProjectConfig) -> Result<Assessment, EthicalError> {
    // Implementation
}
```

### Documentation Style

- Use **Google-style docstrings** for Python
- Include **examples** in docstrings
- Keep documentation **up-to-date** with code changes
- Use **Markdown** for all documentation files

---

## Testing Requirements

### Unit Tests

All new features must include unit tests:

```python
# tests/test_new_feature.py

def test_new_ethical_principle():
    """Test that new ethical principle is correctly validated."""
    principle = EthicalPrinciple(
        id="new_001",
        name="New Principle",
        category="cultural_sensitivity"
    )
    
    project_data = {"complies_with_new_principle": True}
    violations = principle.validate(project_data)
    
    assert len(violations) == 0
```

### Integration Tests

Mark integration tests with `@pytest.mark.integration`:

```python
@pytest.mark.integration
def test_full_assessment_workflow():
    """Test complete assessment from data input to report generation."""
    # Test implementation
```

### Test Coverage

- Maintain **>90% code coverage**
- Run coverage reports: `pytest --cov=eaifch --cov-report=html`
- All critical paths must be tested

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_taxonomy.py -v

# Tests by marker
pytest -m unit
pytest -m integration
pytest -m "not slow"

# With coverage
pytest --cov=eaifch --cov-report=term-missing
```

---

## Documentation

### Code Documentation

- All public functions/classes must have docstrings
- Use type hints for function signatures
- Include usage examples in docstrings

### User Documentation

When adding features that affect users:
1. Update relevant pages in `docs/`
2. Add examples to `examples/`
3. Update `README.md` if applicable
4. Update `CHANGELOG.md`

### Building Documentation Locally

```bash
cd docs
mkdocs serve
# Open http://localhost:8000
```

---

## Pull Request Process

1. **Ensure all tests pass** and coverage is maintained
2. **Update documentation** for any changed functionality
3. **Add entry to CHANGELOG.md** under "Unreleased"
4. **Link related issues** in the PR description
5. **Request review** from maintainers
6. **Address review comments** promptly

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Related Issues
Closes #123
Related to #456

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing
- [ ] Coverage maintained/improved

## Documentation
- [ ] Code comments updated
- [ ] Docstrings updated
- [ ] User documentation updated
- [ ] CHANGELOG.md updated

## Checklist
- [ ] Code follows style guidelines
- [ ] Commits follow conventional commits
- [ ] No breaking changes (or clearly documented)
- [ ] Ready for review
```

---

## Community

### Getting Help

- **GitHub Discussions**: For questions and discussions
- **GitHub Issues**: For bugs and feature requests
- **Email**: [your-email@institution.fr]

### Recognition

Contributors will be:
- Listed in `CONTRIBUTORS.md`
- Mentioned in release notes
- Acknowledged in academic papers (for significant contributions)

---

## Areas for Contribution

We especially welcome contributions in:

### 🔬 Research & Academia
- New ethical principles based on recent research
- Case studies from real-world implementations
- Validation studies and empirical evaluations

### 💻 Development
- New risk assessment algorithms
- Performance optimizations
- Integration with cultural heritage platforms (Europeana, DSpace)
- Dashboard enhancements

### 📚 Documentation
- Translation to other languages
- Tutorial videos
- Use case documentation
- API examples

### 🧪 Testing
- Additional test cases
- Edge case identification
- Performance benchmarks

### 🌍 Cultural Heritage Expertise
- Domain-specific ethical considerations
- Regional/cultural variations in principles
- Stakeholder requirements

---

## License

By contributing to EAIFCH, you agree that your contributions will be licensed under the MIT License.

---

## Questions?

Don't hesitate to reach out if you have questions or need clarification. We're here to help!

**Thank you for contributing to ethical AI in cultural heritage! 🏛️🤖**
