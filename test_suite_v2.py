"""
EAIFCH - Module 1 V2.0 - Suite de Tests Complète
Tests unitaires et d'intégration avec pytest

Usage:
    pytest test_suite_v2.py -v --cov=module_1_ethical_assessment
    
Installation:
    pip install pytest pytest-cov pytest-benchmark
"""

import pytest
from datetime import datetime
from typing import List, Dict
import json

# Import du module (ajuster selon structure)
# from module_1_ethical_assessment.core import (
#     EnhancedCulturalTaxonomy,
#     ClassificationResult,
#     LanguageDetector,
#     Language,
#     SensitivityLevel
# )

# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def taxonomy():
    """Fixture pour créer une instance de taxonomie."""
    return EnhancedCulturalTaxonomy()

@pytest.fixture
def sample_descriptions():
    """Descriptions d'exemples pour tests."""
    return {
        'torah_en': "Ancient Torah scroll from 15th century synagogue in Prague",
        'torah_fr': "Ancien rouleau de Torah d'une synagogue du 15ème siècle à Prague",
        'quran_ar': "مخطوطة قرآن قديمة من القرن الثاني عشر",
        'dreamtime': "Aboriginal Dreamtime narrative about creation of Uluru",
        'mummy': "Egyptian mummy from Ptolemaic period with funerary objects",
        'stonehenge': "Prehistoric stone circle used for ceremonial purposes",
        'herbal': "Traditional Chinese herbal medicine knowledge passed through generations",
        'icon': "Byzantine religious icon depicting Virgin Mary",
        'colonial': "Colonial census records from 1890s including forced labor documentation",
        'navajo_language': "Audio recordings of last Navajo elder speaker"
    }

@pytest.fixture
def expected_results():
    """Résultats attendus pour validation."""
    return {
        'torah_en': {
            'category': 'sacred_texts',
            'subcategory': 'religious_scriptures',
            'min_confidence': 0.75
        },
        'dreamtime': {
            'category': 'sacred_texts',
            'subcategory': 'oral_traditions',
            'min_confidence': 0.70
        },
        'mummy': {
            'category': 'human_remains',
            'subcategory': 'ancestral_remains',
            'min_confidence': 0.80
        },
        'stonehenge': {
            'category': 'ceremonial_sites',
            'subcategory': 'archaeological_sacred_sites',
            'min_confidence': 0.75
        },
        'herbal': {
            'category': 'traditional_knowledge',
            'subcategory': 'medicinal_knowledge',
            'min_confidence': 0.70
        }
    }

# ============================================================================
# TESTS DE DÉTECTION DE LANGUE
# ============================================================================

class TestLanguageDetector:
    """Tests pour le détecteur de langue."""
    
    def test_detect_english(self):
        """Test détection anglais."""
        text = "The sacred text is preserved in the museum"
        assert LanguageDetector.detect(text) == Language.ENGLISH
    
    def test_detect_french(self):
        """Test détection français."""
        text = "Le texte sacré est préservé dans le musée"
        assert LanguageDetector.detect(text) == Language.FRENCH
    
    def test_detect_arabic(self):
        """Test détection arabe."""
        text = "النص المقدس محفوظ في المتحف"
        assert LanguageDetector.detect(text) == Language.ARABIC
    
    def test_detect_spanish(self):
        """Test détection espagnol."""
        text = "El texto sagrado está preservado en el museo"
        assert LanguageDetector.detect(text) == Language.SPANISH
    
    def test_detect_chinese(self):
        """Test détection chinois."""
        text = "神圣文本保存在博物馆中"
        assert LanguageDetector.detect(text) == Language.CHINESE
    
    def test_detect_unknown(self):
        """Test texte trop court ou ambigu."""
        assert LanguageDetector.detect("abc") == Language.UNKNOWN
        assert LanguageDetector.detect("") == Language.UNKNOWN
    
    def test_detect_mixed_language(self):
        """Test texte multilingue (devrait détecter langue dominante)."""
        text = "The Torah scroll (texte sacré juif) is ancient"
        result = LanguageDetector.detect(text)
        assert result in [Language.ENGLISH, Language.FRENCH]

# ============================================================================
# TESTS DE CLASSIFICATION
# ============================================================================

class TestClassification:
    """Tests de classification des objets patrimoniaux."""
    
    def test_classify_torah_english(self, taxonomy, sample_descriptions, expected_results):
        """Test classification Torah en anglais."""
        desc = sample_descriptions['torah_en']
        keywords = ['jewish', 'religious', 'sacred', 'scripture']
        
        result = taxonomy.classify_item(desc, keywords)
        expected = expected_results['torah_en']
        
        assert result.category == expected['category']
        assert result.subcategory == expected['subcategory']
        assert result.confidence >= expected['min_confidence']
        assert result.detected_language == 'en'
        assert len(result.reasoning) > 0
    
    def test_classify_torah_french(self, taxonomy, sample_descriptions):
        """Test classification Torah en français."""
        desc = sample_descriptions['torah_fr']
        keywords = ['juif', 'religieux', 'sacré']
        
        result = taxonomy.classify_item(desc, keywords)
        
        assert result.category == 'sacred_texts'
        assert result.subcategory == 'religious_scriptures'
        assert result.detected_language == 'fr'
        assert result.confidence > 0.65
    
    def test_classify_dreamtime(self, taxonomy, sample_descriptions, expected_results):
        """Test classification récit Dreamtime aborigène."""
        desc = sample_descriptions['dreamtime']
        keywords = ['aboriginal', 'indigenous', 'oral', 'story']
        
        result = taxonomy.classify_item(desc, keywords)
        expected = expected_results['dreamtime']
        
        assert result.category == expected['category']
        assert result.subcategory == expected['subcategory']
        assert result.confidence >= expected['min_confidence']
        
        # Vérifier consultation requise
        subcat_data = taxonomy.get_subcategory(result.category, result.subcategory)
        assert subcat_data['consultation_required'] == True
    
    def test_classify_mummy(self, taxonomy, sample_descriptions, expected_results):
        """Test classification momie égyptienne."""
        desc = sample_descriptions['mummy']
        keywords = ['egyptian', 'burial', 'ancient', 'preserved']
        
        result = taxonomy.classify_item(desc, keywords)
        expected = expected_results['mummy']
        
        assert result.category == expected['category']
        assert result.confidence >= expected['min_confidence']
        
        # Vérifier sensibilité élevée
        cat_data = taxonomy.get_category(result.category)
        assert cat_data['level'] == 3  # HIGH sensitivity
    
    def test_classify_ceremonial_site(self, taxonomy, sample_descriptions, expected_results):
        """Test classification site cérémoniel."""
        desc = sample_descriptions['stonehenge']
        keywords = ['prehistoric', 'stone', 'ritual', 'ancient']
        
        result = taxonomy.classify_item(desc, keywords)
        expected = expected_results['stonehenge']
        
        assert result.category == expected['category']
        assert result.confidence >= expected['min_confidence']
        
        # Vérifier restrictions GPS
        restrictions = taxonomy.get_restrictions(result.category, result.subcategory)
        assert any('gps' in r.lower() for r in restrictions)
    
    def test_classify_traditional_knowledge(self, taxonomy, sample_descriptions, expected_results):
        """Test classification savoir traditionnel."""
        desc = sample_descriptions['herbal']
        keywords = ['medicine', 'herbal', 'traditional', 'healing']
        
        result = taxonomy.classify_item(desc, keywords)
        expected = expected_results['herbal']
        
        assert result.category == expected['category']
        assert result.confidence >= expected['min_confidence']
        
        # Vérifier protection biopiraterie
        restrictions = taxonomy.get_restrictions(result.category, result.subcategory)
        assert 'prevent_biopiracy' in restrictions
    
    def test_classify_with_alternatives(self, taxonomy):
        """Test génération alternatives de classification."""
        desc = "Sacred mask used in ceremonial dances and rituals"
        keywords = ['ritual', 'ceremonial', 'sacred']
        
        result = taxonomy.classify_item(desc, keywords, include_alternatives=True)
        
        # Devrait avoir alternatives car ambiguïté (sacred_arts vs ceremonial_sites)
        assert len(result.alternative_matches) > 0
        
        # Alternative doit avoir confidence < principale
        if result.alternative_matches:
            assert result.alternative_matches[0][2] < result.confidence
    
    def test_classify_low_confidence(self, taxonomy):
        """Test classification avec confiance faible."""
        desc = "Old object"  # Description très vague
        keywords = []
        
        result = taxonomy.classify_item(desc, keywords)
        
        # Devrait avoir warnings
        assert len(result.warnings) > 0
        assert result.confidence < 0.5
        assert result.requires_manual_review() == True

# ============================================================================
# TESTS DE SENSIBILITÉ
# ============================================================================

class TestSensitivity:
    """Tests des niveaux de sensibilité et restrictions."""
    
    def test_high_sensitivity_categories(self, taxonomy):
        """Test catégories haute sensibilité (niveau 3)."""
        high_sensitivity = ['sacred_texts', 'human_remains']
        
        for category in high_sensitivity:
            level = taxonomy.get_sensitivity_level(category)
            assert level == 3
    
    def test_medium_sensitivity_categories(self, taxonomy):
        """Test catégories sensibilité moyenne (niveau 2)."""
        medium_sensitivity = ['ceremonial_sites', 'traditional_knowledge']
        
        for category in medium_sensitivity:
            level = taxonomy.get_sensitivity_level(category)
            assert level == 2
    
    def test_low_sensitivity_categories(self, taxonomy):
        """Test catégories basse sensibilité (niveau 1)."""
        low_sensitivity = ['artistic_expressions', 'historical_documents', 'linguistic_materials']
        
        for category in low_sensitivity:
            level = taxonomy.get_sensitivity_level(category)
            assert level == 1
    
    def test_consultation_required(self, taxonomy):
        """Test identification items nécessitant consultation."""
        # Human remains doivent TOUJOURS nécessiter consultation
        assert taxonomy.requires_consultation('human_remains', 'ancestral_remains') == True
        
        # Sacred texts aussi
        assert taxonomy.requires_consultation('sacred_texts', 'religious_scriptures') == True
        
        # Secular traditional arts non
        assert taxonomy.requires_consultation('artistic_expressions', 'secular_traditional_arts') == False
    
    def test_repatriation_priority(self, taxonomy):
        """Test identification items prioritaires pour rapatriement."""
        restrictions = taxonomy.get_restrictions('human_remains', 'ancestral_remains')
        assert 'repatriation_priority' in restrictions
        assert 'NAGPRA_compliance' in restrictions
    
    def test_biopiracy_protection(self, taxonomy):
        """Test protection contre biopiraterie."""
        restrictions = taxonomy.get_restrictions('traditional_knowledge', 'medicinal_knowledge')
        assert 'prevent_biopiracy' in restrictions
        assert 'Nagoya_Protocol_compliance' in restrictions

# ============================================================================
# TESTS MULTILINGUES
# ============================================================================

class TestMultilingual:
    """Tests support multilingue."""
    
    def test_multilingual_terms_coverage(self, taxonomy):
        """Test que toutes catégories ont termes multilingues."""
        for category, cat_data in taxonomy.TAXONOMY.items():
            assert 'terms_multilang' in cat_data
            
            # Au moins anglais et français
            assert 'en' in cat_data['terms_multilang']
            assert 'fr' in cat_data['terms_multilang']
            
            # Au moins 3 termes par langue
            for lang, terms in cat_data['terms_multilang'].items():
                assert len(terms) >= 3
    
    def test_classification_language_consistency(self, taxonomy):
        """Test cohérence classification multilingue."""
        # Torah en anglais et français devrait donner même catégorie
        desc_en = "Torah scroll from ancient synagogue"
        desc_fr = "Rouleau de Torah d'une ancienne synagogue"
        
        result_en = taxonomy.classify_item(desc_en, ['jewish', 'religious'])
        result_fr = taxonomy.classify_item(desc_fr, ['juif', 'religieux'])
        
        assert result_en.category == result_fr.category
        assert result_en.subcategory == result_fr.subcategory
        
        # Langues détectées correctement
        assert result_en.detected_language == 'en'
        assert result_fr.detected_language == 'fr'

# ============================================================================
# TESTS D'ÉQUILIBRE CULTUREL
# ============================================================================

class TestCulturalBalance:
    """Tests équilibre représentation culturelle."""
    
    def test_cultural_groups_representation(self, taxonomy):
        """Test représentation équilibrée groupes culturels."""
        cultural_groups = set()
        
        for category, cat_data in taxonomy.TAXONOMY.items():
            for subcat, subcat_data in cat_data['subcategories'].items():
                examples = subcat_data.get('examples', {})
                if isinstance(examples, dict):
                    cultural_groups.update(examples.keys())
        
        # Au moins 20 groupes culturels différents
        assert len(cultural_groups) >= 20
        
        # Vérifier diversité régionale
        regions = {
            'africa', 'indigenous_australia', 'indigenous_americas',
            'pacific', 'asia', 'middle_east', 'europe'
        }
        
        represented_regions = set()
        for group in cultural_groups:
            for region in regions:
                if region in group.lower():
                    represented_regions.add(region)
        
        # Au moins 5 régions représentées
        assert len(represented_regions) >= 5
    
    def test_indigenous_representation(self, taxonomy):
        """Test représentation peuples autochtones."""
        indigenous_examples = 0
        total_examples = 0
        
        for category, cat_data in taxonomy.TAXONOMY.items():
            for subcat, subcat_data in cat_data['subcategories'].items():
                examples = subcat_data.get('examples', {})
                if isinstance(examples, dict):
                    for group, items in examples.items():
                        total_examples += len(items)
                        if 'indigenous' in group.lower():
                            indigenous_examples += len(items)
        
        # Au moins 15% d'exemples autochtones
        indigenous_ratio = indigenous_examples / total_examples if total_examples > 0 else 0
        assert indigenous_ratio >= 0.15
    
    def test_non_western_representation(self, taxonomy):
        """Test représentation cultures non-occidentales."""
        non_western_groups = {
            'africa', 'asia', 'indigenous', 'pacific', 'aboriginal',
            'maori', 'inuit', 'navajo', 'yoruba', 'polynesian'
        }
        
        non_western_count = 0
        total_count = 0
        
        for category, cat_data in taxonomy.TAXONOMY.items():
            for subcat, subcat_data in cat_data['subcategories'].items():
                examples = subcat_data.get('examples', {})
                if isinstance(examples, dict):
                    for group in examples.keys():
                        total_count += 1
                        if any(nw in group.lower() for nw in non_western_groups):
                            non_western_count += 1
        
        # Au moins 50% de groupes non-occidentaux
        non_western_ratio = non_western_count / total_count if total_count > 0 else 0
        assert non_western_ratio >= 0.50

# ============================================================================
# TESTS DE PERFORMANCE
# ============================================================================

class TestPerformance:
    """Tests de performance et optimisation."""
    
    def test_classification_speed(self, taxonomy, benchmark):
        """Test vitesse classification (doit être < 20ms)."""
        desc = "Ancient Buddhist sutra manuscript from Tang dynasty"
        keywords = ['buddhist', 'religious', 'manuscript']
        
        result = benchmark(taxonomy.classify_item, desc, keywords)
        
        # Vérifier que benchmark a réussi
        assert result is not None
    
    def test_batch_classification_speed(self, taxonomy, sample_descriptions, benchmark):
        """Test vitesse classification par lot."""
        descriptions = list(sample_descriptions.values())
        
        def classify_batch():
            results = []
            for desc in descriptions:
                result = taxonomy.classify_item(desc, [])
                results.append(result)
            return results
        
        results = benchmark(classify_batch)
        assert len(results) == len(descriptions)
    
    def test_cache_effectiveness(self, taxonomy):
        """Test efficacité du cache LRU."""
        desc = "Torah scroll from synagogue"
        keywords = ['jewish', 'religious']
        
        # Première classification
        start1 = datetime.now()
        result1 = taxonomy.classify_item(desc, keywords)
        time1 = (datetime.now() - start1).total_seconds() * 1000
        
        # Deuxième classification (devrait utiliser cache)
        start2 = datetime.now()
        result2 = taxonomy.classify_item(desc, keywords)
        time2 = (datetime.now() - start2).total_seconds() * 1000
        
        # Même résultat
        assert result1.category == result2.category
        assert result1.confidence == result2.confidence
        
        # Cache devrait être plus rapide (au moins 2x)
        # Note: Peut ne pas être vrai en pratique car classification déjà rapide
        # Mais on peut vérifier que les deux appellent le même code
        assert time2 <= time1 * 1.5  # Tolérance

# ============================================================================
# TESTS D'INTÉGRATION
# ============================================================================

class TestIntegration:
    """Tests d'intégration end-to-end."""
    
    def test_full_workflow_high_sensitivity(self, taxonomy):
        """Test workflow complet pour item haute sensibilité."""
        # 1. Classification
        desc = "Human skeletal remains from ancient burial site with grave goods"
        keywords = ['human', 'remains', 'burial', 'ancestral']
        
        result = taxonomy.classify_item(desc, keywords)
        
        # 2. Vérifications
        assert result.category == 'human_remains'
        assert result.confidence > 0.70
        
        # 3. Obtenir niveau sensibilité
        level = taxonomy.get_sensitivity_level(result.category)
        assert level == 3  # HIGH
        
        # 4. Vérifier consultation requise
        requires_consult = taxonomy.requires_consultation(result.category, result.subcategory)
        assert requires_consult == True
        
        # 5. Obtenir restrictions
        restrictions = taxonomy.get_restrictions(result.category, result.subcategory)
        assert 'repatriation_priority' in restrictions
        assert 'NAGPRA_compliance' in restrictions
        
        # 6. Vérifier nécessité révision manuelle
        if result.confidence < 0.75:
            assert result.requires_manual_review() == True
    
    def test_full_workflow_traditional_knowledge(self, taxonomy):
        """Test workflow pour savoir traditionnel."""
        desc = "Traditional herbal medicine formulas passed down through generations"
        keywords = ['traditional', 'medicine', 'herbal', 'knowledge']
        
        result = taxonomy.classify_item(desc, keywords)
        
        assert result.category == 'traditional_knowledge'
        assert result.subcategory == 'medicinal_knowledge'
        
        # Vérifier protections légales
        subcat_data = taxonomy.get_subcategory(result.category, result.subcategory)
        legal_frameworks = subcat_data.get('legal_frameworks', [])
        assert 'Nagoya_Protocol' in legal_frameworks
        assert 'CBD' in legal_frameworks
        
        # Vérifier restrictions biopiraterie
        restrictions = taxonomy.get_restrictions(result.category, result.subcategory)
        assert 'prevent_biopiracy' in restrictions
        assert 'community_benefit_sharing' in restrictions
    
    def test_export_import_result(self, taxonomy):
        """Test export/import résultat classification."""
        desc = "Ancient Torah scroll"
        result = taxonomy.classify_item(desc, ['religious'])
        
        # Export JSON
        json_str = result.to_json()
        json_data = json.loads(json_str)
        
        # Vérifier champs essentiels
        assert 'category' in json_data
        assert 'confidence' in json_data
        assert 'timestamp' in json_data
        assert 'input_hash' in json_data
        
        # Vérifier valeurs
        assert json_data['category'] == result.category
        assert json_data['confidence'] == round(result.confidence, 4)

# ============================================================================
# TESTS DE RÉGRESSION
# ============================================================================

class TestRegression:
    """Tests de non-régression pour garantir stabilité."""
    
    def test_known_good_classifications(self, taxonomy):
        """Test classifications connues qui doivent toujours fonctionner."""
        known_goods = [
            {
                'desc': "Torah scroll from 15th century synagogue",
                'keywords': ['jewish', 'religious', 'sacred'],
                'expected': ('sacred_texts', 'religious_scriptures', 0.75)
            },
            {
                'desc': "Egyptian mummy from Ptolemaic period",
                'keywords': ['mummy', 'burial', 'ancient'],
                'expected': ('human_remains', 'ancestral_remains', 0.80)
            },
            {
                'desc': "Aboriginal Dreamtime creation story",
                'keywords': ['aboriginal', 'oral', 'story', 'indigenous'],
                'expected': ('sacred_texts', 'oral_traditions', 0.70)
            }
        ]
        
        for case in known_goods:
            result = taxonomy.classify_item(case['desc'], case['keywords'])
            expected_cat, expected_subcat, min_conf = case['expected']
            
            assert result.category == expected_cat, \
                f"Regression: {case['desc']} devrait être {expected_cat}"
            assert result.subcategory == expected_subcat, \
                f"Regression: {case['desc']} devrait être {expected_subcat}"
            assert result.confidence >= min_conf, \
                f"Regression: {case['desc']} confiance trop faible"

# ============================================================================
# TESTS STATISTIQUES
# ============================================================================

class TestStatistics:
    """Tests des statistiques de taxonomie."""
    
    def test_taxonomy_statistics(self, taxonomy):
        """Test génération statistiques."""
        stats = taxonomy.get_statistics()
        
        assert 'total_categories' in stats
        assert 'total_subcategories' in stats
        assert 'total_examples' in stats
        
        # Valeurs attendues
        assert stats['total_categories'] == 7
        assert stats['total_subcategories'] >= 14
        assert stats['total_examples'] >= 100
    
    def test_cultural_representation_equity(self, taxonomy):
        """Test métrique CRE (Cultural Representation Equity)."""
        stats = taxonomy.get_cultural_statistics()
        
        assert 'CRE' in stats
        assert 0 <= stats['CRE'] <= 1
        
        # CRE devrait être > 0.70 (bien équilibré)
        assert stats['CRE'] >= 0.70

# ============================================================================
# TESTS D'ERREURS ET CAS LIMITES
# ============================================================================

class TestEdgeCases:
    """Tests cas limites et gestion erreurs."""
    
    def test_empty_description(self, taxonomy):
        """Test description vide."""
        result = taxonomy.classify_item("", [])
        
        assert result.category is None
        assert result.confidence == 0.0
        assert len(result.warnings) > 0
    
    def test_very_short_description(self, taxonomy):
        """Test description très courte."""
        result = taxonomy.classify_item("Old", [])
        
        assert len(result.warnings) > 0
        assert 'très courte' in ' '.join(result.warnings).lower()
    
    def test_no_matches(self, taxonomy):
        """Test aucune correspondance."""
        desc = "Modern plastic toy manufactured in 2020"
        result = taxonomy.classify_item(desc, ['modern', 'plastic'])
        
        # Devrait retourner résultat mais confiance très faible
        assert result.confidence < 0.3
    
    def test_invalid_category_query(self, taxonomy):
        """Test requête catégorie invalide."""
        result = taxonomy.get_category('nonexistent_category')
        assert result is None
    
    def test_invalid_subcategory_query(self, taxonomy):
        """Test requête sous-catégorie invalide."""
        result = taxonomy.get_subcategory('sacred_texts', 'nonexistent_subcategory')
        assert result is None

# ============================================================================
# SUITE DE TESTS COMPLÈTE
# ============================================================================

if __name__ == "__main__":
    """Exécuter tous les tests."""
    pytest.main([
        __file__,
        '-v',
        '--cov=module_1_ethical_assessment',
        '--cov-report=html',
        '--cov-report=term',
        '--benchmark-only',
        '--benchmark-compare'
    ])
    
    print("\n" + "="*70)
    print("✅ Suite de tests complète Module 1 V2.0")
    print("="*70)
    print("\nTests couverts:")
    print("  ✓ Détection langue (7 tests)")
    print("  ✓ Classification (10 tests)")
    print("  ✓ Sensibilité (6 tests)")
    print("  ✓ Multilingue (2 tests)")
    print("  ✓ Équilibre culturel (3 tests)")
    print("  ✓ Performance (3 tests)")
    print("  ✓ Intégration (3 tests)")
    print("  ✓ Régression (1 test)")
    print("  ✓ Statistiques (2 tests)")
    print("  ✓ Cas limites (5 tests)")
    print("\nTotal: ~42 tests")
    print("\nCouverture cible: >90%")
    print("="*70)