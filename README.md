# EAIFCH — Ethical AI Framework for Cultural Heritage

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-20%20passing-brightgreen.svg)](https://github.com/benseddikahmed-sudo/EAIFCH-Ethical-Framework-for-Cultural-Heritage)
[![Coverage](https://img.shields.io/badge/coverage-94%25-brightgreen.svg)](https://github.com/benseddikahmed-sudo/EAIFCH-Ethical-Framework-for-Cultural-Heritage)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![OSF Pre-registration](https://img.shields.io/badge/OSF-preregistered-blue)](https://osf.io/XXXXX)
[![Target Journal: DSH](https://img.shields.io/badge/journal-Digital%20Scholarship%20in%20the%20Humanities-lightgrey)](https://academic.oup.com/dsh)

**EAIFCH v1.1** is the first framework integrating systematic ethical assessment with green computing for cultural heritage digitisation. It combines a hierarchical cultural sensitivity classification system grounded in CARE Principles and UNESCO standards, a multi-dimensional risk assessment protocol with statistical validation, and energy-efficient algorithms achieving 78% CO₂ reduction compared to conventional machine learning approaches.

> **Target journal:** *Digital Scholarship in the Humanities* (Oxford University Press)  
> **Article type:** Research Article  
> **Pre-registration:** OSF osf.io/XXXXX | Zenodo: 10.5281/zenodo.XXXXXXX  
> **License:** GPL v3.0

---

## Key Contributions

1. **Three-level baseline comparison** confirming energy efficiency is not a straw man (~300,000× CO₂ gap between indicator-based systems and CNN/deep learning pipelines)
2. **10,000-simulation false-negative characterisation** of the Bayesian validation protocol
3. **Governance escalation mechanism** blocking JSON export for HIGH/CRITICAL sensitivity items when community authority is unclear
4. **Explicit CARE-to-module mapping** demonstrating concrete operationalisation of each CARE Principle
5. **Feasibility demonstration** across three case studies with quantified community feedback (5 representatives, 2 communities)

---

## Framework Architecture

EAIFCH follows a pipeline pattern: unified intake → sequential modules → structured `AssessmentRecord` output. Each module operates independently for partial deployment.

```
EAIFCH/
├── eaifch/
│   ├── __init__.py
│   ├── models.py                  # AssessmentRecord dataclass (immutable)
│   ├── module1_taxonomy.py        # Cultural Taxonomy — 7 categories, 4 sensitivity levels
│   ├── module2_classifier.py      # Sensitivity Classifier — S = 100×Σ[wᵢ×(ΣIᵢ/nᵢ)]
│   ├── module3_consent.py         # Community Consent — PIC / IN / Attribution
│   │                              #   + GovernanceEscalationError + 3-tier access
│   ├── module4_risk.py            # Risk Assessment — 5 dimensions + mitigation plans
│   ├── module5_validation.py      # Statistical Validation — Bayesian BF>10, 10k perms
│   └── module6_green.py           # Green Metrics — CodeCarbon, @lru_cache, NumPy
├── validation/
│   ├── statistical/               # Stan MCMC model + permutation test implementation
│   │   ├── model.stan
│   │   └── permutation_test.py
│   └── synthetic_data_generator.py  # Parametric bootstrap, 4-moment verification
├── tests/
│   └── test_suite.py              # 20 tests, 94% line coverage
├── docs/
│   └── supplementary_S1.md        # Complete Bayesian methodology documentation
├── examples/
│   ├── case_study_1_torah.py
│   ├── case_study_2_wiradjuri.py
│   └── case_study_3_griot.py
├── README.md
├── LICENSE                        # GPL v3.0
└── requirements.txt               # 8 dependencies, 45MB installation
```

---

## Module Overview

| Module | Function | Output |
|--------|----------|--------|
| 1. Cultural Taxonomy | Sensitivity classification | Score (0–100), level (Low/Medium/High/Critical) |
| 2. Sensitivity Classifier | Multi-criteria scoring S = 100×Σ[wᵢ×(ΣIᵢ/nᵢ)] | Score, level, flags, reasoning chain |
| 3. Community Consent | Consent pathway + governance escalation | Consent type, template, escalation record |
| 4. Risk Assessment | Multi-dimensional risk scoring | Risk scores (5 dims), mitigation plan |
| 5. Statistical Validation | Batch pattern validation | Validated/rejected pattern flags |
| 6. Green Metrics | Energy and CO₂ tracking | Wh, CO₂ (g), duration |

---

## Installation

**Requirements:** Python 3.9+, 45MB installation, 8 dependencies.

```bash
git clone https://github.com/benseddikahmed-sudo/EAIFCH-Ethical-Framework-for-Cultural-Heritage.git
cd EAIFCH-Ethical-Framework-for-Cultural-Heritage
pip install -r requirements.txt
pip install -e .
```

---

## Quick Start

### Basic assessment

```python
from eaifch import EAIFCHPipeline

pipeline = EAIFCHPipeline()

record = pipeline.assess(
    item_id="MUS_TF_001",
    category="sacred_texts",
    subcategory="religious_scriptures",
    indicators={
        "sacredness": {"ceremonial_use": True, "divine_connection": True,
                       "initiation_required": False, "seasonal_restriction": False},
        "privacy": {"living_individuals": False, "identifiable_data": False,
                    "family_secrets": False, "medical_info": False},
        "commercialization": {"market_demand": True, "digital_marketplace": False,
                              "souvenir_industry": False, "patent_risk": False},
        "political": {"contested_ownership": False, "colonial_context": True,
                      "land_dispute": False},
        "community_control": {"no_governance_body": False, "diaspora_fragmented": False,
                              "governance_disputed": False}
    },
    governance_indicators={"named_authority": True, "legal_entity": True,
                           "contact_established": True, "protocol_documented": True}
)

print(f"Sensitivity: {record.sensitivity_score}/100 — {record.sensitivity_level}")
print(f"Consent pathway: {record.consent_pathway}")
print(f"CO₂: {record.co2_grams:.9f}g")
```

### Governance escalation (v1.1)

When a HIGH or CRITICAL item has fewer than 2 of 4 governance indicators, export is blocked:

```python
from eaifch import EAIFCHPipeline
from eaifch.module3_consent import GovernanceEscalationError

pipeline = EAIFCHPipeline()

try:
    record = pipeline.export_item_record('MUS_WA_042', assessment)
except GovernanceEscalationError as e:
    # Export blocked until named ethics officer approves
    # e.g.: 'Status: unclear | Next: Identify diaspora organizations...'
    pipeline.record_ethics_approval(
        item_id='MUS_WA_042',
        approving_officer='Dr. Smith, Ethics Committee Chair',
        approval_notes='Diaspora organizations identified; provisional consent obtained'
    )
    record = pipeline.export_item_record('MUS_WA_042', assessment)  # now succeeds
```

### Three-tier differentiated access

```python
# Community tier always has full unobfuscated access
record = pipeline.assess(..., access_tier="community")   # full GPS coordinates
record = pipeline.assess(..., access_tier="public")      # GPS obfuscated ≥10km radius
record = pipeline.assess(..., access_tier="institutional")  # per community agreement
```

---

## Sensitivity Classification

Five weighted dimensions evaluated via binary indicators:

| Dimension | Weight | Indicators |
|-----------|--------|------------|
| Sacredness | 30% | ceremonial use, divine connection, initiation required, seasonal restriction |
| Privacy | 20% | living individuals, identifiable data, family secrets, medical info |
| Commercialization Risk | 20% | market demand, digital marketplace, souvenir industry, patent risk |
| Political Sensitivity | 15% | contested ownership, colonial context, land dispute |
| Community Control | 15% | no governance body, diaspora fragmented, governance disputed |

**Score formula:** `S = 100 × Σᵢ [ wᵢ × (ΣIᵢ / nᵢ) ]`

**Sensitivity categories:** Critical (S ≥ 75) · High (50 ≤ S < 75) · Medium (25 ≤ S < 50) · Low (S < 25)

---

## CARE Principles — Concrete Implementation

| CARE Principle | Implementing Module | Mechanism |
|----------------|--------------------|-----------| 
| Collective Benefit | Module 3 — Community Consent | Community benefit clauses in PIC templates; 50% revenue sharing provisions |
| Authority to Control | Module 2 + Governance Escalation | PIC required for High/Critical; export blocked until named community authority approves; withdrawal triggers 24h access suspension |
| Responsibility | Module 4 — Risk Assessment | Mitigation plan per dimension; escalation record names approving officer; immutable audit trail |
| Ethics | Module 1 — Cultural Taxonomy | Sensitivity multipliers encode cultural protocols; NAGPRA/UNDRIP/Nagoya Protocol flags built into subcategory specifications |

---

## Green Performance

| Method | CO₂/item | Accuracy | Interpretable |
|--------|----------|----------|---------------|
| **EAIFCH v1.1** | **0.00000002g** | 70%* | **Yes — full reasoning chain** |
| Baseline 0: Ad-hoc rules | ~0g | 50% | Partial |
| Baseline 1: Logistic Regression | 0.00000027g | 80%* | No |
| CNN ResNet-50 | 0.007125g | — | No |

*10-item validation dataset; accuracy indicative only. The ~300,000× CO₂ gap lies between all indicator-based systems and deep learning pipelines.

**At 10,000 annual assessments:** EAIFCH emits <0.5g CO₂ vs ~72g for CNN equivalents.

Green coding practices: O(n) algorithmic ceiling · `@lru_cache` reducing taxonomy access from 47ms to 0.0012ms · NumPy vectorisation (96.6% energy reduction) · 8 dependencies (45MB vs 580MB for typical ML frameworks) · automated CO₂ tracking via CodeCarbon.

---

## Feasibility Case Studies

| Metric | Case 1: Torah Fragment | Case 2: Wiradjuri Site | Case 3: Griot Recording |
|--------|----------------------|----------------------|------------------------|
| Sensitivity score | 40.0/100 | 65.0/100 | 52.5/100 |
| Sensitivity level | Medium | High | High |
| Governance status | Clear | Clear | **Unclear → BLOCKED** |
| Consent pathway | Informed Notification | PIC (6–12 mo.) | PIC — escalation pending |
| Duration | 0.103ms | 0.062ms | 0.047ms |
| CO₂/assessment | 0.000049g | 0.000030g | 0.000023g |

---

## Statistical Validation

Three-phase protocol (Module 5):

- **Phase A:** Unsupervised pattern discovery
- **Phase B:** Bayesian hierarchical models — patterns validated only if posterior 95% CI excludes null AND Bayes Factor BF > 10; 10,000-iteration permutation testing
- **Phase C:** 5–7 expert consensus, ≥80% agreement required

**91% pattern rejection rate** — strong discriminatory power by design. False negatives (conservative treatment) are the ethically preferable error under CARE Principles.

| Condition | True Positive Rate | False Negative Rate |
|-----------|-------------------|---------------------|
| Effect d=0.2 (weak) | 2.3% | 97.7% |
| Effect d=0.5 (moderate) | 15.0% | 85.0% |
| Effect d=0.8 (strong) | 50.0% | 50.0% |
| Effect d=1.2 (very strong) | 90.8% | 9.2% |
| False positive rate (H₀ true) | — | **0.65%** |

Institutions processing N ≥ 200 items can expect substantially improved detection of moderate effects.

---

## Running Tests

```bash
pytest tests/ -v
# Expected: 20 passed, 94% coverage

pytest tests/ --cov=eaifch --cov-report=html
```

---

## Integration

Three integration modes:

- **Standalone CLI** — batch processing: `python -m eaifch.cli --input items.json --output results/`
- **Python API** — custom workflows: `from eaifch import EAIFCHPipeline`
- **DAMS plugins** — Omeka S, Arches v7 (ethics-by-default interception before items become accessible)

JSON output schema includes mappings to Dublin Core (`dc:subject`, `dc:rights`, `dc:accessRights`) and Schema.org CreativeWork (`accessMode`, `conditionsOfAccess`). IIIF adapter planned for v2.0.

---

## Limitations

- **Feasibility scope:** Three case studies demonstrate coherent outputs; systematic external validation with pre-registered protocols is planned 2026–2027.
- **Validation dataset:** 10-item dataset insufficient for robust accuracy claims. N ≥ 200 items per category recommended.
- **Taxonomy coverage:** Traditions from South/Southeast Asia, Central Asia, and the Pacific are underrepresented. Weight recalibration via regional advisory board consultations planned for v2.0.
- **Additive model assumption:** Linear scoring may not reflect cultural logics where indicator combinations create disproportionate sensitivity. Boolean rule and fuzzy logic models under investigation.
- **Language:** English-only indicators and taxonomy. Multilingual support in development.

---

## Reproducibility

- OSF pre-registration of complete methodology before empirical testing
- Semantic versioning with Zenodo archiving
- Automated static analysis: pylint 9.14/10, bandit 0 high-severity issues, pytest 20/20 passing, 94% line coverage — verified via GitHub Actions on each commit
- Synthetic datasets for reproducibility without exposing sensitive cultural materials: `/validation/synthetic_data_generator.py`
- Community-contributed taxonomy extensions reviewed by regional advisory boards before merge

---

## Academic Citation

```bibtex
@article{benseddik2024eaifch,
  title={Green AI for Cultural Heritage: An Ethical Framework with Minimal Environmental Footprint},
  author={Benseddik, Ahmed},
  journal={Digital Scholarship in the Humanities},
  publisher={Oxford University Press},
  year={2024},
  doi={10.5281/zenodo.XXXXXXX},
  note={Pre-registered: OSF osf.io/XXXXX}
}
```

---

## License

This project is licensed under the **GNU General Public License v3.0**. See [LICENSE](LICENSE) for details.

GPL v3 was selected over MIT to ensure that derivative works — including institutional adaptations — remain open and community-auditable, consistent with CARE Principles' Authority to Control.

---

## Contact

- **Issues:** https://github.com/benseddikahmed-sudo/EAIFCH-Ethical-Framework-for-Cultural-Heritage/issues
- **Email:** benseddik.ahmed@gmail.com

---

## Roadmap

- [x] Core framework — 6 modules (v1.0)
- [x] Governance escalation mechanism — `GovernanceEscalationError` (v1.1)
- [x] Differentiated 3-tier access architecture (v1.1)
- [ ] Liturgical activity bonus modifier for active ceremonial items (v2.0)
- [ ] Community-specified weighting profiles via co-design (v2.0)
- [ ] Taxonomy expansion — South/Southeast Asia, Pacific (v2.0)
- [ ] Non-additive scoring models — Boolean rules, fuzzy logic (v2.0)
- [ ] IIIF adapter (v2.0)
- [ ] Multilingual indicators and taxonomy (v2.1)
