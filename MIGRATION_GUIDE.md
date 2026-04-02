# Guide de migration — EAIFCH repo vers article DSH final (v1.1)

Ce document liste les actions à effectuer dans l'ordre pour mettre
le repository en conformité avec l'article soumis à *Digital Scholarship
in the Humanities*.

---

## 1. Fichiers à REMPLACER (contenu incorrect)

### README.md
Le README actuel référence :
- Journal cible : JOCCH (incorrect → DSH)
- Licence : MIT (incorrect → GPL v3)
- Python : 3.8+ (incorrect → 3.9+)
- Tests : 42 passing (incorrect → 20 passing)
- Badge DOI Zenodo incorrect
- Pas de mention de `GovernanceEscalationError`
- Architecture fictive (core/, rust_engine/, api/, dashboard/)

**Action :** Remplacer intégralement par le fichier `README.md` fourni.

---

## 2. Fichiers à CRÉER (absents du repo)

### eaifch/models.py
`AssessmentRecord` dataclass — absent du repo mais central dans l'article (Section 4.2).
Trois propriétés critiques : immutabilité, dual JSON/PDF, Dublin Core + Schema.org.

### eaifch/module3_consent.py ← remplace consent_risk_modules.py
Le fichier actuel `consent_risk_modules.py` contient `ConsentType.FPIC/ONGOING`
mais est manquant :
- `GovernanceEscalationError` (Section 4.3 — cité explicitement dans l'article)
- `record_ethics_approval()` (exemple de code p.9 de l'article)
- Les 3 voies : PIC / Informed Notification / Attribution (nommage exact de la Section 3.4)
- Les 3 tiers d'accès : Public / Institutional / Community (Section 3.6)
- Les 3 modes GPS : radius_offset / boundary_rounding / full_removal (Section 3.5)

### eaifch/module2_classifier.py ← remplace sensitivity_classifier.py
Vérifier que la formule exacte `S = 100 × Σᵢ [ wᵢ × (ΣIᵢ / nᵢ) ]` est présente
et que les seuils sont corrects : Critical ≥75, High ≥50, Medium ≥25, Low <25.

### validation/synthetic_data_generator.py
Absent mais requis par l'article (Section 4.5) :
- Bootstrap paramétrique
- Vérification des 4 moments (moyenne, variance, skewness, kurtosis) à 5%
- Bruit gaussien σ=5 points

### docs/supplementary_S1.md
Documentation méthodologie Bayésienne complète (Supplementary Materials S1).

---

## 3. Fichiers à SUPPRIMER (confusion)

Ces fichiers créent de la confusion et ne correspondent à aucune structure
citée dans l'article :

```
acm_paper (2).md          ← papier ACM, pas DSH
acm_paper.md              ← idem
conference_presentation (1).md
conference_presentation.md
ameliorations_rapport.md
final_synthesis (1).md
final_synthesis.md
overview_synthesis.md
eaifch_readme (1).md      ← doublon
eaifch_readme.md          ← doublon
project_structure (1).md  ← doublon
contributing_guide (5).md ← numérotation erronée
dockerfile.txt            ← renommer en Dockerfile
makefile.txt              ← renommer en Makefile
rust_readme_build.txt     ← Rust non mentionné dans l'article DSH
rust_core_complete.rs     ← idem
```

---

## 4. Licence à CHANGER

Le fichier `LICENSE` actuel est MIT.
L'article indique GPL v3.0 (mentionné dans la conclusion et le pied de page).

**Action :**
```bash
# Remplacer le contenu de LICENSE par la GPL v3
curl -o LICENSE https://www.gnu.org/licenses/gpl-3.0.txt
```

---

## 5. Structure cible du repo

```
EAIFCH-Ethical-Framework-for-Cultural-Heritage/
├── README.md                          ← REMPLACÉ
├── LICENSE                            ← GPL v3 (pas MIT)
├── requirements.txt                   ← 8 dépendances, 45MB
├── setup.py / pyproject.toml
│
├── eaifch/
│   ├── __init__.py
│   ├── models.py                      ← CRÉER (AssessmentRecord)
│   ├── module1_taxonomy.py            ← renommer module1_core_python.py
│   ├── module2_classifier.py          ← CRÉER / remplacer sensitivity_classifier.py
│   ├── module3_consent.py             ← CRÉER (GovernanceEscalationError)
│   ├── module4_risk.py                ← adapter consent_risk_modules.py (partie risk)
│   ├── module5_validation.py          ← CRÉER
│   └── module6_green.py               ← renommer green_metrics_module.py
│
├── validation/
│   ├── statistical/
│   │   ├── model.stan
│   │   └── permutation_test.py
│   └── synthetic_data_generator.py    ← CRÉER
│
├── tests/
│   └── test_suite.py                  ← 20 tests, 94% coverage
│
├── docs/
│   └── supplementary_S1.md           ← CRÉER
│
└── examples/
    ├── case_study_1_torah.py
    ├── case_study_2_wiradjuri.py
    └── case_study_3_griot.py
```

---

## 6. Commandes Git suggérées

```bash
# 1. Cloner localement si pas déjà fait
git clone https://github.com/benseddikahmed-sudo/EAIFCH-Ethical-Framework-for-Cultural-Heritage.git
cd EAIFCH-Ethical-Framework-for-Cultural-Heritage

# 2. Créer une branche de travail
git checkout -b v1.1-dsh-alignment

# 3. Remplacer le README
cp /chemin/vers/README_nouveau.md README.md

# 4. Créer les sous-dossiers
mkdir -p eaifch validation/statistical tests docs examples

# 5. Déplacer les modules existants
mv module1_core_python.py eaifch/module1_taxonomy.py
mv green_metrics_module.py eaifch/module6_green.py
mv assessment_module.py eaifch/module4_risk.py   # à adapter

# 6. Copier les nouveaux fichiers
cp /chemin/vers/models.py eaifch/models.py
cp /chemin/vers/module2_classifier.py eaifch/module2_classifier.py
cp /chemin/vers/module3_consent.py eaifch/module3_consent.py
cp /chemin/vers/synthetic_data_generator.py validation/synthetic_data_generator.py

# 7. Remplacer la licence
# Télécharger GPL v3 depuis gnu.org et remplacer LICENSE

# 8. Supprimer les fichiers de confusion
git rm acm_paper*.md conference_presentation*.md ameliorations_rapport.md
git rm final_synthesis*.md overview_synthesis.md eaifch_readme*.md
git rm project_structure*.md "contributing_guide (5).md"
git rm dockerfile.txt makefile.txt rust_readme_build.txt rust_core_complete.rs

# 9. Renommer les fichiers txt → fichiers standards
mv dockerfile.txt Dockerfile   # si on garde Docker
mv makefile.txt Makefile

# 10. Commit
git add -A
git commit -m "feat: align repo with DSH final submission (EAIFCH v1.1)

- Replace README: DSH journal, GPL v3, Python 3.9+, 20 tests
- Add GovernanceEscalationError + record_ethics_approval (Module 3)
- Add AssessmentRecord dataclass with Dublin Core + Schema.org mappings
- Add 3-tier differentiated access + 3-mode GPS obfuscation
- Add synthetic_data_generator.py (Section 4.5)
- Restructure flat files into eaifch/ package
- Remove duplicate/outdated documentation files
- Switch licence from MIT to GPL v3"

# 11. Push
git push origin v1.1-dsh-alignment
# Puis créer une Pull Request sur GitHub
```

---

## 7. Points de vérification finale

Avant de merger, vérifier que le repo contient bien :

- [ ] `GovernanceEscalationError` dans module3_consent.py
- [ ] `record_ethics_approval()` dans module3_consent.py
- [ ] Formule `S = 100 × Σᵢ [ wᵢ × (ΣIᵢ / nᵢ) ]` dans module2_classifier.py
- [ ] Seuils : Critical ≥75, High ≥50, Medium ≥25, Low <25
- [ ] 3 tiers : Public / Institutional / Community
- [ ] 3 modes GPS : radius_offset / boundary_rounding / full_removal
- [ ] `AssessmentRecord` dataclass (frozen=True)
- [ ] Dublin Core + Schema.org dans l'export JSON
- [ ] `synthetic_data_generator.py` avec vérification des 4 moments
- [ ] Licence GPL v3
- [ ] Python 3.9+ dans README et requirements
- [ ] Journal cible : Digital Scholarship in the Humanities
- [ ] 20 tests (pas 42)
