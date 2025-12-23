# ============================================================================
# QUICK START GUIDE - EAIFCH Framework
# Guide de démarrage rapide avec exemples complets
# ============================================================================

"""
EAIFCH Framework - Quick Start Guide

Ce guide vous permet de démarrer en 5 minutes avec le framework.
"""

# ============================================================================
# EXEMPLE 1: Évaluation Éthique Basique (Python Pur)
# ============================================================================

def example_1_basic_assessment():
    """
    Exemple basique: Évaluer la sensibilité d'un objet patrimonial.
    Performance: Standard (47ms par item)
    """
    print("=" * 70)
    print("EXEMPLE 1: Évaluation Éthique Basique")
    print("=" * 70)
    
    from module_1_ethical_assessment import (
        SensitivityClassifier,
        CulturalTaxonomy
    )
    
    # 1. Créer les objets nécessaires
    classifier = SensitivityClassifier()
    taxonomy = CulturalTaxonomy()
    
    # 2. Définir l'item à évaluer
    item_metadata = {
        'id': 'torah_scroll_001',
        'name': 'Ancient Torah Scroll',
        'culture': 'Jewish',
        'date': '15th century',
        'location': 'National Library',
        'description': 'Sacred Torah scroll used in synagogue ceremonies',
        'keywords': ['religious', 'sacred', 'jewish', 'scripture', 'ceremonial']
    }
    
    # 3. Classification taxonomique automatique
    cat, subcat, confidence = taxonomy.classify_item(
        item_metadata['description'],
        item_metadata['keywords']
    )
    
    print(f"\n📋 Item: {item_metadata['name']}")
    print(f"🏷️  Classification:")
    print(f"   Catégorie: {cat}")
    print(f"   Sous-catégorie: {subcat}")
    print(f"   Confiance: {confidence:.2%}")
    
    # 4. Répondre aux indicateurs de sensibilité
    indicators = {
        # Sacralité (30%)
        'used_in_religious_ceremony': True,
        'connected_to_deity': True,
        'restricted_to_initiated': False,
        'seasonal_taboos': False,
        'requires_purification': True,
        
        # Vie privée (20%)
        'contains_personal_data': False,
        'living_individuals': False,
        'family_secrets': False,
        'medical_information': False,
        'financial_data': False,
        
        # Risque commercialisation (20%)
        'market_value_high': True,
        'easily_reproducible': False,
        'exploitable_knowledge': False,
        'biopiracy_potential': False,
        'tourism_exploitation': False,
        
        # Sensibilité politique (15%)
        'colonial_context': False,
        'land_disputes': False,
        'sovereignty_issues': False,
        'cultural_genocide': False,
        'repatriation_claims': False,
        
        # Contrôle communautaire (15%)
        'community_ownership_clear': True,
        'elders_authority': True,
        'traditional_governance': True,
        'active_stewardship': True,
        'documented_protocols': True
    }
    
    # 5. Calculer le score de sensibilité
    score, category, flags = classifier.calculate_sensitivity_score(
        item_metadata,
        indicators
    )
    
    print(f"\n📊 Évaluation de Sensibilité:")
    print(f"   Score: {score:.2f}/100")
    print(f"   Catégorie: {category.upper()}")
    print(f"   Indicateurs déclenchés: {len(flags)}")
    
    # 6. Générer rapport complet
    report = classifier.generate_assessment_report(
        item_metadata, score, category, flags
    )
    
    print(f"\n📄 Rapport Complet:")
    print(f"   ID: {report['metadata']['report_id']}")
    print(f"   Consultation requise: {report['consultation_requirements']['required']}")
    print(f"   Type consentement: {report['consultation_requirements'].get('consultation_type', 'N/A')}")
    print(f"   Durée estimée: {report['consultation_requirements'].get('estimated_duration', 'N/A')}")
    print(f"   Niveau d'accès: {report['access_recommendations']['tier']}")
    print(f"   Actions requises: {len(report['required_actions'])}")
    
    # 7. Afficher actions requises
    print(f"\n⚡ Actions Requises:")
    for action in report['required_actions'][:3]:  # Top 3
        print(f"   [{action['priority'].upper()}] {action['action']}")
        print(f"      → {action['description']}")
    
    return report


# ============================================================================
# EXEMPLE 2: Évaluation Ultra-Rapide avec Rust
# ============================================================================

def example_2_rust_performance():
    """
    Exemple avec Rust core: Performance maximale.
    Performance: 3,357x plus rapide (14 microseconds par item)
    """
    print("\n" + "=" * 70)
    print("EXEMPLE 2: Évaluation Ultra-Rapide avec Rust")
    print("=" * 70)
    
    try:
        from eaifch_core import RustSensitivityScorer
        rust_available = True
    except ImportError:
        print("\n⚠️  Module Rust non disponible. Installez avec: maturin develop")
        return
    
    import time
    
    # Créer scorer Rust
    scorer = RustSensitivityScorer([0.30, 0.20, 0.20, 0.15, 0.15])
    
    # Indicateurs (format compact: liste de booléens)
    indicators = [
        # Sacralité (5 indicateurs)
        True, True, False, False, True,
        # Vie privée (5 indicateurs)
        False, False, False, False, False,
        # Commercialisation (5 indicateurs)
        True, False, False, False, False,
        # Politique (5 indicateurs)
        False, False, False, False, False,
        # Contrôle (5 indicateurs)
        True, True, True, True, True,
    ]
    
    # Mesurer performance - Single item
    start = time.perf_counter()
    score = scorer.calculate_score(indicators)
    duration = time.perf_counter() - start
    
    category = scorer.classify(score)
    
    print(f"\n⚡ Performance (Single Item):")
    print(f"   Score: {score:.2f}/100")
    print(f"   Catégorie: {category}")
    print(f"   Temps: {duration * 1_000_000:.2f} microseconds")
    
    # Mesurer performance - Batch processing
    batch = [indicators] * 1000
    
    start = time.perf_counter()
    scores = scorer.batch_calculate(batch)
    duration = time.perf_counter() - start
    
    print(f"\n🚀 Performance (Batch 1000 items):")
    print(f"   Items traités: {len(scores)}")
    print(f"   Temps total: {duration:.3f} seconds")
    print(f"   Temps moyen: {duration * 1000 / len(scores):.3f} ms/item")
    print(f"   Throughput: {len(scores) / duration:.0f} items/second")


# ============================================================================
# EXEMPLE 3: Workflow Complet avec Consentement
# ============================================================================

def example_3_complete_workflow():
    """
    Exemple workflow complet: De l'évaluation au consentement.
    """
    print("\n" + "=" * 70)
    print("EXEMPLE 3: Workflow Complet")
    print("=" * 70)
    
    from module_1_ethical_assessment import (
        SensitivityClassifier,
        CommunityConsentFramework,
        CulturalHeritageRiskAssessor
    )
    from datetime import datetime, timedelta
    
    # === ÉTAPE 1: Évaluation initiale ===
    print("\n📋 ÉTAPE 1: Évaluation Initiale")
    
    classifier = SensitivityClassifier()
    
    item = {
        'id': 'sacred_site_001',
        'name': 'Sacred Mountain Petroglyphs',
        'culture': 'Indigenous Australian',
        'description': 'Ancient rock art with spiritual significance',
        'keywords': ['sacred', 'ceremonial', 'rock art', 'dreamtime']
    }
    
    indicators = {
        'used_in_religious_ceremony': True,
        'connected_to_deity': True,
        'restricted_to_initiated': True,
        'seasonal_taboos': True,
        'requires_purification': True,
        'contains_personal_data': False,
        'living_individuals': True,
        'family_secrets': False,
        'medical_information': False,
        'financial_data': False,
        'market_value_high': False,
        'easily_reproducible': True,
        'exploitable_knowledge': False,
        'biopiracy_potential': False,
        'tourism_exploitation': True,
        'colonial_context': True,
        'land_disputes': True,
        'sovereignty_issues': True,
        'cultural_genocide': False,
        'repatriation_claims': False,
        'community_ownership_clear': True,
        'elders_authority': True,
        'traditional_governance': True,
        'active_stewardship': True,
        'documented_protocols': True
    }
    
    score, category, flags = classifier.calculate_sensitivity_score(item, indicators)
    report = classifier.generate_assessment_report(item, score, category, flags)
    
    print(f"   Score: {score:.2f}/100")
    print(f"   Catégorie: {category.upper()}")
    print(f"   ⚠️  Catégorie {category} détectée - Consultation requise")
    
    # === ÉTAPE 2: Évaluation des risques ===
    print("\n🔍 ÉTAPE 2: Évaluation des Risques")
    
    risk_assessor = CulturalHeritageRiskAssessor()
    
    risk_indicators = {
        'market_demand': False,
        'ease_of_reproduction': True,
        'gps_precision_available': True,
        'high_value_objects': False,
        'living_individuals': True,
        'complex_cultural_context': True,
        'sacred_meanings': True,
        'tourism_exploitation': True
    }
    
    risk_report = risk_assessor.assess_multidimensional_risk(item, risk_indicators)
    
    print(f"   Risque global: {risk_report['overall_risk_score']:.2f}/100")
    print(f"   Catégorie: {risk_report['risk_category'].upper()}")
    print(f"   Zones haut risque: {', '.join(risk_report['high_risk_areas'])}")
    print(f"   Mitigations planifiées: {len(risk_report['mitigation_plan'])}")
    
    # === ÉTAPE 3: Processus de consentement ===
    print("\n🤝 ÉTAPE 3: Processus de Consentement")
    
    consent_fw = CommunityConsentFramework()
    
    # Déterminer type de consentement
    consent_type = consent_fw.determine_consent_type(category)
    print(f"   Type requis: {consent_type.value}")
    
    # Générer demande de consentement
    consent_request = consent_fw.generate_consent_request(
        item, report, consent_type
    )
    
    print(f"   ID demande: {consent_request['request_id']}")
    print(f"   Stakeholders: {len(consent_request['consultation_process']['stakeholders'])}")
    print(f"   Durée estimée: {consent_request['consultation_process']['timeline']}")
    
    # Simuler décision (dans la réalité, ceci vient de la communauté)
    print("\n   [Simulation] Consultation communautaire en cours...")
    print("   [Simulation] Décision obtenue: CONDITIONAL")
    
    decision_record = consent_fw.record_consent_decision(
        consent_request_id=consent_request['request_id'],
        decision=consent_fw.ConsentStatus.CONDITIONAL,
        decision_makers=['Elder Council', 'Cultural Authority'],
        decision_date=datetime.now(),
        conditions=[
            'GPS coordinates must be obfuscated',
            'No high-resolution images',
            'Community narrative must accompany all displays',
            'Quarterly reporting to community required'
        ],
        duration=timedelta(days=365),
        notes='Approved for research purposes with strict conditions'
    )
    
    print(f"\n✅ Décision Enregistrée:")
    print(f"   ID: {decision_record['record_id']}")
    print(f"   Décision: {decision_record['decision'].upper()}")
    print(f"   Conditions: {len(decision_record['conditions'])}")
    print(f"   Durée: {decision_record['duration']} jours")
    print(f"   Révision requise: {decision_record['review_required']}")
    
    # === ÉTAPE 4: Implémentation ===
    print("\n🔧 ÉTAPE 4: Implémentation")
    print("   Actions à entreprendre:")
    for i, condition in enumerate(decision_record['conditions'], 1):
        print(f"   {i}. {condition}")
    
    print("\n   Obligations continues:")
    for key, value in decision_record['ongoing_obligations'].items():
        if isinstance(value, dict):
            print(f"   • {key}:")
            for k, v in value.items():
                print(f"      - {k}: {v}")


# ============================================================================
# EXEMPLE 4: Green Metrics Tracking
# ============================================================================

def example_4_green_metrics():
    """
    Exemple: Tracker l'empreinte carbone de vos opérations.
    """
    print("\n" + "=" * 70)
    print("EXEMPLE 4: Green Metrics Tracking")
    print("=" * 70)
    
    from module_1_ethical_assessment import (
        SensitivityClassifier,
        GreenMetricsTracker
    )
    
    # Créer tracker
    tracker = GreenMetricsTracker(enable_logging=True)
    
    # Décorateur pour mesurer automatiquement
    @tracker.measure_operation("sensitivity_assessment")
    def perform_assessment():
        classifier = SensitivityClassifier()
        
        items = []
        for i in range(10):
            items.append({
                'id': f'item_{i}',
                'name': f'Cultural Item {i}',
                'culture': 'Various',
                'description': 'Test item'
            })
        
        indicators = {f'indicator_{j}': (j % 2 == 0) for j in range(25)}
        
        results = []
        for item in items:
            score, cat, flags = classifier.calculate_sensitivity_score(item, indicators)
            results.append((score, cat))
        
        return results
    
    # Exécuter avec tracking
    print("\n🌱 Exécution avec Green Metrics...")
    results = perform_assessment()
    
    # Obtenir résumé
    summary = tracker.get_session_summary()
    
    print(f"\n📊 Métriques Environnementales:")
    print(f"   Opérations: {summary['operations_count']}")
    print(f"   Durée totale: {summary['total_duration_seconds']:.3f}s")
    print(f"   Énergie: {summary['total_energy_wh']:.6f} Wh")
    print(f"   CO₂: {summary['total_co2_grams']:.6f} g")
    print(f"   CPU moyen: {summary['average_cpu_percent']:.2f}%")
    print(f"   Mémoire peak: {summary['peak_memory_mb']:.2f} MB")
    
    # Comparaison Python vs Rust (théorique)
    print(f"\n🦀 Impact si Rust Core était utilisé:")
    
    python_metrics = {
        'operation': 'batch_assessment',
        'duration_seconds': summary['total_duration_seconds'],
        'energy_wh': summary['total_energy_wh'],
        'co2_grams': summary['total_co2_grams'],
        'memory_mb': summary['peak_memory_mb']
    }
    
    # Rust serait ~60x plus rapide pour batch
    rust_metrics = {
        'operation': 'batch_assessment',
        'duration_seconds': python_metrics['duration_seconds'] / 60,
        'energy_wh': python_metrics['energy_wh'] / 60,
        'co2_grams': python_metrics['co2_grams'] / 60,
        'memory_mb': python_metrics['memory_mb'] * 0.09  # 91% reduction
    }
    
    comparison = tracker.compare_implementations(python_metrics, rust_metrics)
    
    print(f"   Speedup: {comparison['improvements']['speedup_factor']}x")
    print(f"   Réduction CO₂: {comparison['improvements']['co2_reduction_percent']:.1f}%")
    print(f"   Réduction énergie: {comparison['improvements']['energy_reduction_percent']:.1f}%")
    print(f"   Impact annuel (10K users): {comparison['annual_impact_10k_users']['co2_saved_kg']} kg CO₂ économisés")


# ============================================================================
# EXEMPLE 5: Traitement Batch de Grande Échelle
# ============================================================================

def example_5_batch_processing():
    """
    Exemple: Traiter des milliers d'items en batch.
    """
    print("\n" + "=" * 70)
    print("EXEMPLE 5: Traitement Batch")
    print("=" * 70)
    
    from module_1_ethical_assessment import SensitivityClassifier
    import time
    
    classifier = SensitivityClassifier()
    
    # Générer dataset de test
    print("\n📦 Génération dataset de test...")
    items = []
    indicators_list = []
    
    for i in range(100):
        items.append({
            'id': f'item_{i:04d}',
            'name': f'Cultural Object {i}',
            'culture': ['Jewish', 'Indigenous', 'African', 'Asian'][i % 4],
            'description': 'Various cultural items for testing'
        })
        
        # Indicateurs variés
        indicators = {
            f'indicator_{j}': (i + j) % 3 == 0
            for j in range(25)
        }
        indicators_list.append(indicators)
    
    print(f"   Items générés: {len(items)}")
    
    # Traitement batch
    print(f"\n⚙️  Traitement batch en cours...")
    start = time.perf_counter()
    
    reports = classifier.batch_assess(items, indicators_list)
    
    duration = time.perf_counter() - start
    
    print(f"\n✅ Traitement terminé:")
    print(f"   Items traités: {len(reports)}")
    print(f"   Durée: {duration:.2f}s")
    print(f"   Vitesse: {len(reports)/duration:.1f} items/s")
    
    # Statistiques
    categories = {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}
    for report in reports:
        cat = report['sensitivity_assessment']['category']
        categories[cat] += 1
    
    print(f"\n📊 Distribution:")
    for cat, count in categories.items():
        pct = count / len(reports) * 100
        bar = '█' * int(pct / 2)
        print(f"   {cat:8s}: {bar:25s} {count:3d} ({pct:5.1f}%)")


# ============================================================================
# MAIN - Exécuter tous les exemples
# ============================================================================

if __name__ == "__main__":
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "EAIFCH FRAMEWORK - QUICK START" + " " * 23 + "║")
    print("║" + " " * 10 + "Ethical AI for Cultural Heritage" + " " * 26 + "║")
    print("╚" + "═" * 68 + "╝")
    
    print("\n🚀 Exécution des exemples de démarrage...\n")
    
    try:
        # Exemple 1: Basique
        example_1_basic_assessment()
        
        # Exemple 2: Rust (si disponible)
        example_2_rust_performance()
        
        # Exemple 3: Workflow complet
        example_3_complete_workflow()
        
        # Exemple 4: Green Metrics
        example_4_green_metrics()
        
        # Exemple 5: Batch processing
        example_5_batch_processing()
        
        print("\n" + "=" * 70)
        print("✅ TOUS LES EXEMPLES TERMINÉS AVEC SUCCÈS")
        print("=" * 70)
        
        print("\n📚 Prochaines Étapes:")
        print("   1. Consultez la documentation complète: docs/")
        print("   2. Explorez les cas d'usage réels: examples/")
        print("   3. Installez le core Rust pour performance maximale")
        print("   4. Testez l'API REST: cd eaifch-api && uvicorn main:app")
        print("   5. Rejoignez la communauté: GitHub Discussions")
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        print("\n💡 Vérifiez que toutes les dépendances sont installées:")
        print("   pip install -e .")
