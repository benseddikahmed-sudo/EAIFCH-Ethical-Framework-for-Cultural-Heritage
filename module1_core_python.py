# ============================================================================
# MODULE 1: ETHICAL ASSESSMENT PROTOCOL
# Fichier: module_1_ethical_assessment/__init__.py
# ============================================================================

"""
EAIFCH - Ethical AI Framework for Cultural Heritage
Module 1: Ethical Assessment Protocol

Ce module fournit les outils pour évaluer éthiquement les objets du patrimoine
culturel avant leur numérisation et diffusion.
"""

__version__ = "1.0.0"
__author__ = "Benseddik"

from .core.cultural_taxonomy import CulturalTaxonomy
from .core.sensitivity_classifier import SensitivityClassifier
from .core.consent_framework import CommunityConsentFramework
from .core.risk_assessor import CulturalHeritageRiskAssessor
from .core.green_metrics import GreenMetricsTracker

__all__ = [
    "CulturalTaxonomy",
    "SensitivityClassifier",
    "CommunityConsentFramework",
    "CulturalHeritageRiskAssessor",
    "GreenMetricsTracker",
]


# ============================================================================
# Fichier: module_1_ethical_assessment/core/__init__.py
# ============================================================================

"""Core components for ethical assessment."""

from .cultural_taxonomy import CulturalTaxonomy
from .sensitivity_classifier import SensitivityClassifier
from .consent_framework import CommunityConsentFramework
from .risk_assessor import CulturalHeritageRiskAssessor
from .green_metrics import GreenMetricsTracker

__all__ = [
    "CulturalTaxonomy",
    "SensitivityClassifier",
    "CommunityConsentFramework",
    "CulturalHeritageRiskAssessor",
    "GreenMetricsTracker",
]


# ============================================================================
# Fichier: module_1_ethical_assessment/core/cultural_taxonomy.py
# ============================================================================

"""
Classification taxonomique hiérarchique pour objets patrimoniaux.
Inspiré des standards UNESCO + CARE Principles.
"""

from typing import Dict, List, Optional, Tuple
from functools import lru_cache
import json


class CulturalTaxonomy:
    """
    Système de classification hiérarchique pour objets du patrimoine culturel.
    
    Catégories principales (7):
    - sacred_texts (niveau 3 - très haute sensibilité)
    - human_remains (niveau 3)
    - ceremonial_sites (niveau 2)
    - traditional_knowledge (niveau 2)
    - artistic_expressions (niveau 1)
    - historical_documents (niveau 1)
    - linguistic_materials (niveau 1)
    """
    
    TAXONOMY = {
        'sacred_texts': {
            'level': 3,
            'subcategories': {
                'religious_scriptures': {
                    'examples': ['Torah scrolls', 'Quran manuscripts', 'Vedic texts', 
                                'Bible codices', 'Buddhist sutras'],
                    'restrictions': ['ceremonial_context_only', 'community_permission_required'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.5
                },
                'oral_traditions': {
                    'examples': ['Creation stories', 'Initiation rites', 'Sacred songs',
                                'Dreamtime narratives', 'Prophecies'],
                    'restrictions': ['elders_approval', 'seasonal_restrictions', 'gender_restrictions'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.4
                },
                'esoteric_knowledge': {
                    'examples': ['Kabbalistic texts', 'Mystery traditions', 'Secret societies',
                                'Alchemical manuscripts', 'Shamanic knowledge'],
                    'restrictions': ['initiated_members_only', 'no_public_access'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.6
                }
            }
        },
        
        'human_remains': {
            'level': 3,
            'subcategories': {
                'ancestral_remains': {
                    'examples': ['Burial sites', 'Mummies', 'Skeletal collections',
                                'Cremation urns', 'Relics'],
                    'restrictions': ['repatriation_priority', 'no_public_display', 
                                   'sacred_handling_only'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 2.0
                },
                'funerary_objects': {
                    'examples': ['Grave goods', 'Burial masks', 'Sarcophagi',
                                'Funerary statues', 'Tomb paintings'],
                    'restrictions': ['contextual_display_only', 'cultural_protocols'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.3
                }
            }
        },
        
        'ceremonial_sites': {
            'level': 2,
            'subcategories': {
                'active_sacred_sites': {
                    'examples': ['Temples in use', 'Pilgrimage routes', 'Prayer grounds',
                                'Sweat lodges', 'Sacred mountains'],
                    'restrictions': ['gps_obfuscation', 'access_restrictions', 
                                   'photography_prohibited'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.5
                },
                'archaeological_sacred_sites': {
                    'examples': ['Ancient temples', 'Stone circles', 'Petroglyphs',
                                'Pyramids', 'Burial mounds'],
                    'restrictions': ['gps_obfuscation_optional', 'context_required',
                                   'cultural_interpretation'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.2
                }
            }
        },
        
        'traditional_knowledge': {
            'level': 2,
            'subcategories': {
                'medicinal_knowledge': {
                    'examples': ['Herbal remedies', 'Healing practices', 'Traditional surgery',
                                'Pharmacopoeia', 'Diagnostic methods'],
                    'restrictions': ['prevent_biopiracy', 'community_benefit_sharing',
                                   'patent_protection'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.4
                },
                'ecological_knowledge': {
                    'examples': ['Resource management', 'Climate predictions', 
                                'Agricultural techniques', 'Navigation methods'],
                    'restrictions': ['attribution_required', 'prevent_exploitation'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.2
                },
                'craft_techniques': {
                    'examples': ['Weaving patterns', 'Metallurgy', 'Pottery',
                                'Woodcarving', 'Textile dyeing'],
                    'restrictions': ['attribution_required', 'commercial_use_restricted'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.1
                }
            }
        },
        
        'artistic_expressions': {
            'level': 1,
            'subcategories': {
                'sacred_arts': {
                    'examples': ['Icons', 'Mandalas', 'Ritual masks', 'Totem poles',
                                'Sacred dance regalia'],
                    'restrictions': ['context_required', 'no_commercial_reproduction',
                                   'spiritual_significance_noted'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.3
                },
                'secular_traditional_arts': {
                    'examples': ['Folk music', 'Dances', 'Decorative arts', 'Storytelling'],
                    'restrictions': ['attribution_required'],
                    'consultation_required': False,
                    'sensitivity_multiplier': 0.8
                }
            }
        },
        
        'historical_documents': {
            'level': 1,
            'subcategories': {
                'colonial_records': {
                    'examples': ['Administrative docs', 'Treaties', 'Surveys',
                                'Slave records', 'Land appropriation documents'],
                    'restrictions': ['critical_context_required', 'trauma_awareness'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.2
                },
                'community_records': {
                    'examples': ['Genealogies', 'Land titles', 'Trade records',
                                'Correspondence', 'Personal diaries'],
                    'restrictions': ['privacy_protection', 'family_consent'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.1
                }
            }
        },
        
        'linguistic_materials': {
            'level': 1,
            'subcategories': {
                'endangered_languages': {
                    'examples': ['Last speaker recordings', 'Dictionaries', 'Grammars',
                                'Story collections', 'Language lessons'],
                    'restrictions': ['community_control', 'revitalization_priority',
                                   'speaker_consent'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.3
                },
                'secret_languages': {
                    'examples': ['Ritual languages', 'Coded communications',
                                'Initiatory languages', 'Trade jargons'],
                    'restrictions': ['restricted_access', 'member_authorization'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.5
                }
            }
        }
    }
    
    def __init__(self):
        """Initialiser la taxonomie culturelle."""
        self._cache = {}
    
    @lru_cache(maxsize=128)
    def get_category(self, category_name: str) -> Optional[Dict]:
        """
        Récupérer les informations d'une catégorie.
        
        Args:
            category_name: Nom de la catégorie
            
        Returns:
            Dictionnaire avec infos catégorie ou None
        """
        return self.TAXONOMY.get(category_name)
    
    @lru_cache(maxsize=256)
    def get_subcategory(self, category_name: str, subcategory_name: str) -> Optional[Dict]:
        """
        Récupérer les informations d'une sous-catégorie.
        
        Args:
            category_name: Nom de la catégorie principale
            subcategory_name: Nom de la sous-catégorie
            
        Returns:
            Dictionnaire avec infos sous-catégorie ou None
        """
        category = self.get_category(category_name)
        if not category:
            return None
        
        return category.get('subcategories', {}).get(subcategory_name)
    
    def classify_item(self, item_description: str, keywords: List[str]) -> Tuple[Optional[str], Optional[str], float]:
        """
        Classifier automatiquement un item basé sur description et mots-clés.
        
        Args:
            item_description: Description de l'item
            keywords: Liste de mots-clés associés
            
        Returns:
            Tuple (category, subcategory, confidence_score)
        """
        description_lower = item_description.lower()
        keywords_lower = [k.lower() for k in keywords]
        
        best_match = (None, None, 0.0)
        
        for cat_name, cat_data in self.TAXONOMY.items():
            for subcat_name, subcat_data in cat_data['subcategories'].items():
                score = 0.0
                examples = [ex.lower() for ex in subcat_data['examples']]
                
                # Correspondance avec exemples
                for example in examples:
                    if example in description_lower:
                        score += 2.0
                    for keyword in keywords_lower:
                        if keyword in example or example in keyword:
                            score += 1.0
                
                # Pondération par niveau sensibilité
                score *= subcat_data.get('sensitivity_multiplier', 1.0)
                
                if score > best_match[2]:
                    best_match = (cat_name, subcat_name, score)
        
        # Normaliser score confiance (0-1)
        if best_match[2] > 0:
            confidence = min(best_match[2] / 10.0, 1.0)
            return (best_match[0], best_match[1], confidence)
        
        return (None, None, 0.0)
    
    def get_restrictions(self, category: str, subcategory: str) -> List[str]:
        """
        Obtenir les restrictions pour une catégorie/sous-catégorie.
        
        Args:
            category: Nom de la catégorie
            subcategory: Nom de la sous-catégorie
            
        Returns:
            Liste des restrictions applicables
        """
        subcat_data = self.get_subcategory(category, subcategory)
        if subcat_data:
            return subcat_data.get('restrictions', [])
        return []
    
    def requires_consultation(self, category: str, subcategory: str) -> bool:
        """
        Vérifier si consultation communautaire est requise.
        
        Args:
            category: Nom de la catégorie
            subcategory: Nom de la sous-catégorie
            
        Returns:
            True si consultation requise, False sinon
        """
        subcat_data = self.get_subcategory(category, subcategory)
        if subcat_data:
            return subcat_data.get('consultation_required', False)
        return False
    
    def get_sensitivity_level(self, category: str) -> int:
        """
        Obtenir le niveau de sensibilité d'une catégorie (1-3).
        
        Args:
            category: Nom de la catégorie
            
        Returns:
            Niveau de sensibilité (1=low, 2=medium, 3=high)
        """
        cat_data = self.get_category(category)
        if cat_data:
            return cat_data.get('level', 1)
        return 1
    
    def export_taxonomy(self, filepath: str):
        """
        Exporter la taxonomie vers un fichier JSON.
        
        Args:
            filepath: Chemin du fichier de sortie
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.TAXONOMY, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_taxonomy(cls, filepath: str):
        """
        Charger une taxonomie depuis un fichier JSON.
        
        Args:
            filepath: Chemin du fichier JSON
            
        Returns:
            Instance CulturalTaxonomy avec taxonomie chargée
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            taxonomy_data = json.load(f)
        
        instance = cls()
        instance.TAXONOMY = taxonomy_data
        return instance
    
    def get_all_categories(self) -> List[str]:
        """Obtenir la liste de toutes les catégories principales."""
        return list(self.TAXONOMY.keys())
    
    def get_all_subcategories(self, category: str) -> List[str]:
        """
        Obtenir toutes les sous-catégories d'une catégorie.
        
        Args:
            category: Nom de la catégorie
            
        Returns:
            Liste des noms de sous-catégories
        """
        cat_data = self.get_category(category)
        if cat_data:
            return list(cat_data.get('subcategories', {}).keys())
        return []
    
    def get_statistics(self) -> Dict:
        """
        Obtenir des statistiques sur la taxonomie.
        
        Returns:
            Dictionnaire avec statistiques
        """
        total_categories = len(self.TAXONOMY)
        total_subcategories = sum(
            len(cat['subcategories']) 
            for cat in self.TAXONOMY.values()
        )
        total_examples = sum(
            len(subcat['examples'])
            for cat in self.TAXONOMY.values()
            for subcat in cat['subcategories'].values()
        )
        
        return {
            'total_categories': total_categories,
            'total_subcategories': total_subcategories,
            'total_examples': total_examples,
            'categories_by_level': {
                level: sum(1 for cat in self.TAXONOMY.values() if cat['level'] == level)
                for level in [1, 2, 3]
            }
        }


# ============================================================================
# Exemple d'utilisation
# ============================================================================

if __name__ == "__main__":
    # Créer taxonomie
    taxonomy = CulturalTaxonomy()
    
    # Statistiques
    stats = taxonomy.get_statistics()
    print(f"📊 Statistiques Taxonomie:")
    print(f"  Catégories: {stats['total_categories']}")
    print(f"  Sous-catégories: {stats['total_subcategories']}")
    print(f"  Exemples: {stats['total_examples']}")
    
    # Classification automatique
    description = "Ancient Torah scroll from 15th century used in synagogue ceremonies"
    keywords = ["religious", "jewish", "sacred", "scripture"]
    
    category, subcategory, confidence = taxonomy.classify_item(description, keywords)
    print(f"\n🔍 Classification:")
    print(f"  Catégorie: {category}")
    print(f"  Sous-catégorie: {subcategory}")
    print(f"  Confiance: {confidence:.2%}")
    
    # Restrictions
    if category and subcategory:
        restrictions = taxonomy.get_restrictions(category, subcategory)
        print(f"\n⚠️  Restrictions: {', '.join(restrictions)}")
        
        requires_consult = taxonomy.requires_consultation(category, subcategory)
        print(f"  Consultation requise: {'Oui' if requires_consult else 'Non'}")
