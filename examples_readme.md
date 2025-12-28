# EAIFCH Examples

This directory contains practical examples demonstrating how to use the EAIFCH framework for ethical assessment of AI in cultural heritage projects.

## 📁 Files Overview

### Python Examples

1. **`01_basic_assessment.py`** - Basic Ethical Assessment
   - Simple project assessment workflow
   - Using the core framework
   - Displaying results with Rich formatting
   - **Run**: `python examples/01_basic_assessment.py`

2. **`02_api_usage.py`** - REST API Usage
   - Interacting with the EAIFCH API
   - Batch assessments
   - Real-time streaming
   - Report generation and export
   - **Run**: `python examples/02_api_usage.py` (requires API server running)

3. **`03_advanced_custom_principles.py`** - Advanced Usage with Custom Principles
   - Extending the framework with custom principles
   - Sacred site protection
   - Oral tradition ethics
   - Digital repatriation support
   - Custom validators
   - **Run**: `python examples/03_advanced_custom_principles.py`

### JSON Examples

4. **`example_project.json`** - Example Project Data
   - Complete project template
   - All required and optional fields
   - Ready to use with CLI or API
   - **Use**: `eaifch assess examples/example_project.json`

## 🚀 Quick Start

### 1. Install EAIFCH

```bash
pip install -e .
```

### 2. Run Basic Example

```bash
python examples/01_basic_assessment.py
```

### 3. Try CLI Assessment

```bash
# Generate a template
eaifch template my_project.json

# Edit my_project.json with your data

# Run assessment
eaifch assess my_project.json -o report.txt
```

### 4. Start API Server (for API examples)

```bash
# Terminal 1: Start API
eaifch serve

# Terminal 2: Run API example
python examples/02_api_usage.py
```

## 📚 Example Scenarios

### Scenario 1: Museum AI Guide

**Use Case**: Virtual tour with AI recommendations

**File**: `example_project.json`

**Assessment Focus**:
- Bias in recommendations
- Accessibility for all visitors
- GDPR compliance for user data
- Cultural representation fairness

**Expected Issues**:
- ⚠️ No bias testing
- ⚠️ Dataset diversity not assessed
- ⚠️ Model not explainable

### Scenario 2: Sacred Site Digitization

**Use Case**: 3D scanning of sacred indigenous sites

**Example**: `03_advanced_custom_principles.py` → `example_sacred_site_assessment()`

**Assessment Focus**:
- Indigenous consultation (UNDRIP)
- Sacred content protection
- Access restrictions
- Religious authority approval

**Expected Issues**:
- 🔴 Critical if no indigenous consultation
- 🔴 Critical if sacred content unprotected

### Scenario 3: Archaeological AI Analysis

**Use Case**: AI classification of archaeological artifacts

**Assessment Focus**:
- Provenance tracking
- Bias in classification
- Cultural expert review
- IP rights for artifact images

### Scenario 4: Oral History Transcription

**Use Case**: AI transcription of indigenous oral traditions

**Example**: `03_advanced_custom_principles.py` → `example_oral_tradition_project()`

**Assessment Focus**:
- Speaker consent
- Cultural context preservation
- Sacred knowledge filtering
- Commercial use restrictions

## 🔧 Customizing Examples

### Modify a Project

Edit `example_project.json`:

```json
{
  "name": "Your Project Name",
  "ai_techniques": ["your_techniques"],
  "bias_testing": true,  // Change to true
  "model_explainability": true  // Change to true
}
```

Run assessment:
```bash
eaifch assess example_project.json
```

### Create Custom Principles

```python
from eaifch.core.taxonomy import EthicalPrinciple, ValidationRule

my_principle = EthicalPrinciple(
    id="custom_001",
    name="My Custom Principle",
    description="Description here",
    category="cultural_sensitivity",
    severity="high",
    validation_rules=[
        ValidationRule(
            field="my_field",
            operator="equals",
            value=True,
            error_message="Must comply with my principle"
        )
    ]
)

framework.add_custom_principle(my_principle)
```

## 📊 Expected Outputs

### Console Output Example

```
EAIFCH - Basic Ethical Assessment Example

Step 1: Initializing EAIFCH framework...
✓ Framework initialized with 24 principles

Step 2: Defining the AI project...
✓ Project defined: Virtual Museum Tour with AI Guide

Step 3: Running ethical assessment...
✓ Assessment complete!

╭─────────────────────────────────────────────╮
│   Overall Ethical Compliance Score          │
│              78.5/100                        │
╰─────────────────────────────────────────────╯

Category Breakdown:

┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Category                 ┃    Score ┃ Status        ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ Privacy Security         │    85.0  │ Excellent     │
│ Fairness Bias            │    62.5  │ Needs Work    │
│ Cultural Sensitivity     │    91.7  │ Excellent     │
│ Transparency             │    58.3  │ Needs Work    │
...
```

### JSON Report Example

```json
{
  "project_name": "Louvre Virtual Museum Guide",
  "overall_score": 78.5,
  "category_scores": {
    "privacy_security": 85.0,
    "fairness_bias": 62.5,
    ...
  },
  "violations": [
    {
      "principle_id": "fairness_002",
      "severity": "high",
      "description": "AI models must be tested for bias"
    }
  ],
  "summary": {
    "total_violations": 5,
    "critical_violations": 0,
    "status": "good"
  }
}
```

## 🎯 Learning Path

1. **Beginner**: Start with `01_basic_assessment.py`
   - Understand the assessment flow
   - Learn about the 24 principles
   - Interpret results

2. **Intermediate**: Use CLI and `example_project.json`
   - Command-line workflow
   - Batch assessments
   - Report generation

3. **Advanced**: Explore `03_advanced_custom_principles.py`
   - Custom principles
   - Institution-specific requirements
   - Complex validation logic

4. **Expert**: API integration (`02_api_usage.py`)
   - Integrate EAIFCH into your systems
   - Automated assessments
   - Real-time monitoring

## 🐛 Troubleshooting

### Import Errors

```bash
# Make sure EAIFCH is installed
pip install -e .

# Or install from PyPI
pip install eaifch
```

### Missing Dependencies

```bash
# For examples with Rich formatting
pip install rich

# For API examples
pip install httpx requests

# Install all example dependencies
pip install -e ".[dev]"
```

### API Connection Errors

```bash
# Start the API server first
eaifch serve

# Then run API examples in another terminal
```

## 📖 Further Reading

- **Main Documentation**: [https://eaifch.readthedocs.io](https://eaifch.readthedocs.io)
- **API Reference**: See `docs/api/`
- **Research Paper**: See `research/paper.md`
- **Contributing**: See `CONTRIBUTING.md`

## 💡 Tips

- Use `--verbose` flag for detailed output: `eaifch assess project.json -v`
- Generate reports in different formats: `-f html`, `-f markdown`, `-f json`
- Compare projects: `eaifch compare project1.json project2.json`
- List all principles: `eaifch principles`

## 🆘 Getting Help

- **GitHub Issues**: [Report bugs or request features](https://github.com/benseddikahmed-sudo/EAIFCH-Ethical-Framework-for-Cultural-Heritage/issues)
- **Discussions**: [Ask questions](https://github.com/benseddikahmed-sudo/EAIFCH-Ethical-Framework-for-Cultural-Heritage/discussions)
- **Email**: your-email@institution.fr

---

**Happy Assessing! 🏛️🤖**
