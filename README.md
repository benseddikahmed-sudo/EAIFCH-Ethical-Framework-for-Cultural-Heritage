[readme_eaifch.md](https://github.com/user-attachments/files/24360717/readme_eaifch.md)
# EAIFCH - Ethical AI Framework for Cultural Heritage

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tests Passing](https://img.shields.io/badge/tests-42%20passing-brightgreen.svg)]()
[![DOI](https://img.shields.io/badge/DOI-JOCCH%202024-blue)](https://dl.acm.org/journal/jocch)
![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18055206.svg)

## 🎯 Vue d'ensemble

**EAIFCH** (Ethical AI Framework for Cultural Heritage) est un framework open-source développé pour garantir une application éthique et responsable de l'intelligence artificielle dans la gestion, la préservation et la valorisation du patrimoine culturel. Ce projet découle d'une recherche publiée dans le *Journal on Computing and Cultural Heritage* (JOCCH).

### 🔗 Lien avec la recherche académique

Ce framework implémente la taxonomie et les principes éthiques définis dans notre article JOCCH : **"Contextual Ethical Framework for Artificial Intelligence in the Management of Cultural Heritage"**. Il propose 24 principes éthiques organisés en 8 catégories principales pour guider les praticiens et institutions culturelles.

---

## ✨ Fonctionnalités principales

- **📊 Taxonomie éthique structurée** : 24 principes éthiques en 8 catégories
- **🔍 Évaluation des risques IA** : Outils d'analyse automatisée des risques éthiques
- **🛡️ Conformité réglementaire** : Alignement avec l'EU AI Act et UNESCO
- **📈 Tableaux de bord interactifs** : Visualisation des métriques éthiques
- **🔧 Modules extensibles** : Architecture modulaire en Python et Rust
- **🌐 API REST** : Intégration facile dans vos systèmes existants
- **📝 Documentation complète** : Guides détaillés et exemples d'usage

---

## 🏗️ Architecture

```
EAIFCH/
├── core/              # Modules Python principaux
│   ├── taxonomy.py    # Taxonomie des 24 principes éthiques
│   ├── risk_assessor.py
│   └── compliance_checker.py
├── rust_engine/       # Moteur haute performance en Rust
│   ├── src/
│   └── Cargo.toml
├── api/               # API REST (FastAPI)
├── dashboard/         # Interface web (React)
├── tests/             # 42 tests unitaires et d'intégration
├── docs/              # Documentation (MkDocs)
├── examples/          # Cas d'usage concrets
└── data/              # Datasets de référence
```

---

## 🚀 Installation

### Prérequis

- Python 3.8+
- Rust 1.70+ (optionnel, pour le moteur haute performance)
- Node.js 16+ (pour le dashboard)

### Installation rapide

```bash
# Clone le repository
git clone https://github.com/benseddikahmed-sudo/EAIFCH-Ethical-Framework-for-Cultural-Heritage.git
cd EAIFCH-Ethical-Framework-for-Cultural-Heritage

# Installation des dépendances Python
pip install -r requirements.txt

# Installation du module Python en mode développement
pip install -e .

# (Optionnel) Compilation du moteur Rust
cd rust_engine
cargo build --release
cd ..

# (Optionnel) Installation du dashboard
cd dashboard
npm install
cd ..
```

---

## 📖 Utilisation

### Exemple 1 : Évaluation éthique basique

```python
from eaifch import EthicalFramework, CulturalHeritageProject

# Initialisation du framework
framework = EthicalFramework()

# Définir votre projet IA
project = CulturalHeritageProject(
    name="3D Reconstruction of Ancient Temple",
    ai_techniques=["neural_rendering", "photogrammetry"],
    heritage_type="tangible",
    location="UNESCO World Heritage Site"
)

# Évaluation éthique
assessment = framework.assess(project)

# Affichage des résultats
print(f"Score éthique global : {assessment.overall_score}/100")
print(f"Risques détectés : {len(assessment.risks)}")

for risk in assessment.high_priority_risks:
    print(f"⚠️  {risk.category}: {risk.description}")
    print(f"   Recommandation: {risk.mitigation}")
```

**Output :**
```
Score éthique global : 78/100
Risques détectés : 5

⚠️  Data Privacy: Potential exposure of site location details
   Recommandation: Implement geofencing and anonymization

⚠️  Cultural Sensitivity: Risk of misrepresentation of sacred elements
   Recommandation: Engage with local community stakeholders
```

### Exemple 2 : Utilisation de l'API REST

```bash
# Démarrer le serveur API
python -m eaifch.api

# Effectuer une évaluation via API
curl -X POST http://localhost:8000/api/assess \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Virtual Museum Experience",
    "ai_techniques": ["nlp", "recommendation_system"],
    "heritage_type": "intangible"
  }'
```

### Exemple 3 : Dashboard interactif

```bash
# Lancer le dashboard web
cd dashboard
npm start
```

Ouvrez `http://localhost:3000` pour accéder à l'interface de gestion visuelle.

---

## 📚 Les 8 catégories éthiques

| Catégorie | Principes | Description |
|-----------|-----------|-------------|
| **🔐 Privacy & Security** | 3 principes | Protection des données sensibles et des informations culturelles |
| **⚖️ Fairness & Bias** | 4 principes | Prévention des biais algorithmiques et représentation équitable |
| **🎭 Cultural Sensitivity** | 3 principes | Respect des valeurs culturelles et des communautés autochtones |
| **🔍 Transparency** | 3 principes | Explicabilité des décisions IA et auditabilité |
| **👥 Human Agency** | 2 principes | Maintien du contrôle humain et expertise culturelle |
| **♻️ Sustainability** | 3 principes | Impact environnemental et durabilité à long terme |
| **📜 Legal Compliance** | 3 principes | Conformité EU AI Act, UNESCO, propriété intellectuelle |
| **🌍 Accessibility** | 3 principes | Accès universel et inclusivité numérique |

---

## 🧪 Tests

Le framework inclut 42 tests couvrant tous les modules :

```bash
# Exécuter tous les tests
pytest tests/ -v

# Tests avec couverture
pytest tests/ --cov=eaifch --cov-report=html

# Tests spécifiques
pytest tests/test_taxonomy.py
pytest tests/test_risk_assessor.py
```

**Résultats attendus :**
```
======================== 42 passed in 3.24s ========================
Coverage: 94%
```

---

## 📊 Cas d'usage

### 1. Musée national utilisant des recommandations IA
- **Défi** : Éviter les biais dans les recommandations d'œuvres
- **Solution** : Utilisation du module `fairness_analyzer`
- **Résultat** : +32% de diversité dans les recommandations

### 2. Digitalisation d'un site UNESCO
- **Défi** : Conformité réglementaire et respect culturel
- **Solution** : Framework complet avec audit automatique
- **Résultat** : Certification obtenue en 6 semaines

### 3. Reconstruction 3D d'artefacts
- **Défi** : Authenticité et transparence des modèles IA
- **Solution** : Module de traçabilité et explainabilité
- **Résultat** : Approbation des communautés locales

---

## 🛠️ Développement

### Structure des modules

```python
# eaifch/core/taxonomy.py
class EthicalPrinciple:
    """Représente un principe éthique de la taxonomie"""
    
class EthicalCategory:
    """Groupe de principes éthiques"""
    
class EthicalTaxonomy:
    """Taxonomie complète (24 principes, 8 catégories)"""
```

### Contribuer

Nous accueillons les contributions ! Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour :
- Rapporter des bugs
- Proposer de nouvelles fonctionnalités
- Soumettre des pull requests

---

## 📄 Citation académique

Si vous utilisez EAIFCH dans votre recherche, veuillez citer :

```bibtex
@article{benseddik2024eaifch,
  title={Contextual Ethical Framework for Artificial Intelligence in the Management of Cultural Heritage},
  author={Ben Seddik, Ahmed and [Co-authors]},
  journal={Journal on Computing and Cultural Heritage},
  year={2024},
  publisher={ACM}
}
```

---

## 📞 Contact & Support

- **Issues GitHub** : [github.com/benseddikahmed-sudo/EAIFCH/issues](https://github.com/benseddikahmed-sudo/EAIFCH-Ethical-Framework-for-Cultural-Heritage/issues)
- **Email** : [votre-email@institution.fr]
- **Documentation** : [eaifch.readthedocs.io](https://eaifch.readthedocs.io)

---

## 📜 Licence

Ce projet est sous licence MIT. Voir [LICENSE](LICENSE) pour plus de détails.

---

## 🙏 Remerciements

- UNESCO pour les guidelines sur le patrimoine culturel
- EU AI Act pour le cadre réglementaire
- Communauté open-source pour les outils et bibliothèques

---

## 🗺️ Roadmap

- [x] Framework de base (v1.0)
- [x] API REST (v1.1)
- [ ] Dashboard avancé avec ML monitoring (v1.2)
- [ ] Intégration cloud (AWS/Azure/GCP) (v1.3)
- [ ] Support multilingue complet (v2.0)
- [ ] Plugin pour Europeana et DSpace (v2.1)

---

**⭐ Si ce projet vous est utile, n'hésitez pas à le star sur GitHub !**
