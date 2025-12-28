"""
EAIFCH - Ethical AI Framework for Cultural Heritage
Module 1: Ethical Assessment Protocol (Version Améliorée)

Améliorations principales:
- Classification sémantique avec embeddings
- Support multilingue (FR, EN, AR, ES, ZH)
- Tests unitaires intégrés
- Taxonomie enrichie et équilibrée culturellement
- Optimisations de performance

Auteur: Benseddik.Ahmed
Version: 2.0.0
DOI: https://doi.org/10.5281/zenodo.18048554
"""

from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from functools import lru_cache
from collections import defaultdict
import json
import re
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# STRUCTURES DE DONNÉES
# ============================================================================

@dataclass
class ClassificationResult:
    """Résultat enrichi de classification."""
    category: Optional[str]
    subcategory: Optional[str]
    confidence: float
    reasoning: List[str] = field(default_factory=list)
    alternative_matches: List[Tuple[str, str, float]] = field(default_factory=list)
    detected_language: str = "unknown"
    warnings: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            'category': self.category,
            'subcategory': self.subcategory,
            'confidence': self.confidence,
            'reasoning': self.reasoning,
            'alternatives': [
                {'category': c, 'subcategory': s, 'confidence': conf}
                for c, s, conf in self.alternative_matches
            ],
            'detected_language': self.detected_language,
            'warnings': self.warnings
        }


# ============================================================================
# TAXONOMIE ENRICHIE ET MULTILINGUE
# ============================================================================

class EnhancedCulturalTaxonomy:
    """
    Système de classification hiérarchique enrichi pour objets du patrimoine.
    
    Améliorations:
    - Taxonomie élargie avec représentation équilibrée
    - Support multilingue des exemples
    - Synonymes et termes alternatifs
    - Métadonnées contextuelles enrichies
    """
    
    TAXONOMY = {
        'sacred_texts': {
            'level': 3,
            'synonyms': ['religious_texts', 'holy_scriptures', 'sacred_writings'],
            'terms_multilang': {
                'en': ['sacred text', 'holy scripture', 'religious manuscript'],
                'fr': ['texte sacré', 'écriture sainte', 'manuscrit religieux'],
                'ar': ['نص مقدس', 'كتاب مقدس', 'مخطوط ديني'],
                'es': ['texto sagrado', 'escritura sagrada', 'manuscrito religioso'],
            },
            'subcategories': {
                'religious_scriptures': {
                    'examples': {
                        'judaism': ['Torah scrolls', 'Talmud', 'Dead Sea Scrolls'],
                        'christianity': ['Bible codices', 'Gospel manuscripts', 'Apostolic writings'],
                        'islam': ['Quran manuscripts', 'Hadith collections', 'Tafsir texts'],
                        'hinduism': ['Vedic texts', 'Upanishads', 'Bhagavad Gita manuscripts'],
                        'buddhism': ['Buddhist sutras', 'Tripitaka', 'Tibetan manuscripts'],
                        'indigenous': ['Popol Vuh', 'Chilam Balam', 'Native American sacred texts']
                    },
                    'restrictions': ['ceremonial_context_only', 'community_permission_required', 
                                   'no_unauthorized_reproduction'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.5,
                    'consultation_entities': ['religious_authorities', 'community_elders', 'scholars']
                },
                'oral_traditions': {
                    'examples': {
                        'indigenous_australia': ['Dreamtime narratives', 'Songlines', 'Creation stories'],
                        'indigenous_americas': ['Navajo chants', 'Mayan prophecies', 'Inuit legends'],
                        'africa': ['Griot oral histories', 'San creation myths', 'Yoruba Ifa verses'],
                        'pacific': ['Maori whakapapa', 'Hawaiian mo\'olelo', 'Polynesian genealogies'],
                        'asia': ['Mongolian epic songs', 'Ainu yukar', 'Tibetan oral teachings']
                    },
                    'restrictions': ['elders_approval', 'seasonal_restrictions', 'gender_restrictions',
                                   'no_recording_without_permission'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.6,
                    'temporal_restrictions': ['seasonal', 'ceremonial_calendar_dependent']
                },
                'esoteric_knowledge': {
                    'examples': {
                        'western': ['Kabbalistic texts', 'Hermetic writings', 'Alchemical manuscripts'],
                        'eastern': ['Tantric texts', 'Taoist internal alchemy', 'Zen koans'],
                        'indigenous': ['Shamanic knowledge', 'Medicine bundle contents', 'Initiation rites'],
                        'african': ['Vodun mysteries', 'Ifa divination', 'Ancient Egyptian mysteries']
                    },
                    'restrictions': ['initiated_members_only', 'no_public_access', 
                                   'strict_transmission_protocols'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.7
                }
            }
        },
        
        'human_remains': {
            'level': 3,
            'synonyms': ['ancestral_remains', 'bodily_remains', 'physical_remains'],
            'terms_multilang': {
                'en': ['human remains', 'ancestral bones', 'mummy'],
                'fr': ['restes humains', 'ossements ancestraux', 'momie'],
                'ar': ['رفات بشرية', 'عظام الأجداد', 'مومياء'],
                'es': ['restos humanos', 'huesos ancestrales', 'momia'],
            },
            'subcategories': {
                'ancestral_remains': {
                    'examples': {
                        'burials': ['Burial sites', 'Catacombs', 'Ossuaries', 'Cemetery remains'],
                        'preserved': ['Mummies', 'Bog bodies', 'Ice mummies', 'Natural mummification'],
                        'skeletal': ['Skeletal collections', 'Anatomical specimens', 'Pathological specimens'],
                        'relics': ['Saints relics', 'Buddhist relics', 'Ancestor bones', 'Cremation remains']
                    },
                    'restrictions': ['repatriation_priority', 'no_public_display', 'sacred_handling_only',
                                   'NAGPRA_compliance', 'descendant_community_control'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 2.0,
                    'legal_frameworks': ['NAGPRA', 'UNDRIP', 'national_repatriation_laws']
                },
                'funerary_objects': {
                    'examples': {
                        'grave_goods': ['Burial offerings', 'Pottery', 'Jewelry', 'Weapons', 'Tools'],
                        'containers': ['Sarcophagi', 'Coffins', 'Cremation urns', 'Burial jars'],
                        'markers': ['Headstones', 'Funerary stelae', 'Tomb inscriptions', 'Memorial sculptures'],
                        'ritual_items': ['Burial masks', 'Canopic jars', 'Funerary boats', 'Tomb paintings']
                    },
                    'restrictions': ['contextual_display_only', 'cultural_protocols', 
                                   'repatriation_consideration'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.4
                }
            }
        },
        
        'ceremonial_sites': {
            'level': 2,
            'synonyms': ['sacred_sites', 'ritual_places', 'holy_grounds'],
            'terms_multilang': {
                'en': ['sacred site', 'ceremonial place', 'holy ground'],
                'fr': ['site sacré', 'lieu cérémoniel', 'terre sainte'],
                'ar': ['موقع مقدس', 'مكان احتفالي', 'أرض مقدسة'],
                'es': ['sitio sagrado', 'lugar ceremonial', 'tierra santa'],
            },
            'subcategories': {
                'active_sacred_sites': {
                    'examples': {
                        'religious': ['Temples in use', 'Churches', 'Mosques', 'Synagogues', 'Gurdwaras'],
                        'pilgrimage': ['Mecca', 'Jerusalem', 'Varanasi', 'Santiago de Compostela', 'Uluru'],
                        'indigenous': ['Sweat lodges', 'Vision quest sites', 'Ceremonial grounds', 
                                     'Sacred mountains', 'Spirit trees'],
                        'natural': ['Sacred groves', 'Holy springs', 'Sacred caves', 'Mountain shrines']
                    },
                    'restrictions': ['gps_obfuscation', 'access_restrictions', 'photography_prohibited',
                                   'visitor_protocols', 'seasonal_closures'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.6,
                    'protection_measures': ['location_masking', 'access_control', 'visitor_education']
                },
                'archaeological_sacred_sites': {
                    'examples': {
                        'ancient': ['Stonehenge', 'Machu Picchu', 'Angkor Wat', 'Pyramids', 'Petra'],
                        'rock_art': ['Petroglyphs', 'Cave paintings', 'Rock carvings', 'Aboriginal art sites'],
                        'burial': ['Burial mounds', 'Tumuli', 'Necropolis', 'Royal tombs'],
                        'ceremonial': ['Stone circles', 'Earthworks', 'Medicine wheels', 'Henges']
                    },
                    'restrictions': ['gps_precision_limited', 'context_required', 'cultural_interpretation',
                                   'tourism_management'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.3
                }
            }
        },
        
        'traditional_knowledge': {
            'level': 2,
            'synonyms': ['indigenous_knowledge', 'local_knowledge', 'ancestral_wisdom'],
            'terms_multilang': {
                'en': ['traditional knowledge', 'indigenous knowledge', 'ancestral wisdom'],
                'fr': ['savoir traditionnel', 'connaissance autochtone', 'sagesse ancestrale'],
                'ar': ['المعرفة التقليدية', 'الحكمة الأصلية', 'المعرفة الأجدادية'],
                'es': ['conocimiento tradicional', 'sabiduría indígena', 'sabiduría ancestral'],
            },
            'subcategories': {
                'medicinal_knowledge': {
                    'examples': {
                        'herbalism': ['Herbal remedies', 'Plant pharmacopoeia', 'Traditional formulas'],
                        'healing': ['Healing practices', 'Bone setting', 'Massage techniques', 'Energy healing'],
                        'diagnostic': ['Pulse diagnosis', 'Traditional diagnostics', 'Symptom interpretation'],
                        'surgery': ['Traditional surgery', 'Wound treatment', 'Birth practices']
                    },
                    'restrictions': ['prevent_biopiracy', 'community_benefit_sharing', 'patent_protection',
                                   'prior_informed_consent', 'Nagoya_Protocol_compliance'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.5,
                    'legal_frameworks': ['Nagoya_Protocol', 'CBD', 'national_biopiracy_laws']
                },
                'ecological_knowledge': {
                    'examples': {
                        'resource_mgmt': ['Sustainable harvesting', 'Fire management', 'Water management'],
                        'agriculture': ['Crop rotation', 'Companion planting', 'Seed saving', 'Terracing'],
                        'navigation': ['Star navigation', 'Ocean currents', 'Wind patterns', 'Bird migration'],
                        'climate': ['Weather prediction', 'Seasonal indicators', 'Climate adaptation']
                    },
                    'restrictions': ['attribution_required', 'prevent_exploitation', 'benefit_sharing'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.3
                },
                'craft_techniques': {
                    'examples': {
                        'textiles': ['Weaving patterns', 'Dyeing techniques', 'Embroidery', 'Basketry'],
                        'metallurgy': ['Traditional smelting', 'Forging', 'Alloy making', 'Damascus steel'],
                        'pottery': ['Pottery techniques', 'Glazing', 'Firing methods', 'Clay preparation'],
                        'woodwork': ['Carving', 'Joinery', 'Wood bending', 'Inlay']
                    },
                    'restrictions': ['attribution_required', 'commercial_use_restricted', 
                                   'cultural_appropriation_prevention'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.2
                }
            }
        },
        
        'artistic_expressions': {
            'level': 1,
            'synonyms': ['cultural_arts', 'traditional_arts', 'creative_expressions'],
            'terms_multilang': {
                'en': ['artistic expression', 'cultural art', 'traditional art'],
                'fr': ['expression artistique', 'art culturel', 'art traditionnel'],
                'ar': ['التعبير الفني', 'الفن الثقافي', 'الفن التقليدي'],
                'es': ['expresión artística', 'arte cultural', 'arte tradicional'],
            },
            'subcategories': {
                'sacred_arts': {
                    'examples': {
                        'religious_art': ['Icons', 'Thangkas', 'Mandalas', 'Islamic calligraphy', 'Sacred geometry'],
                        'ritual_objects': ['Ritual masks', 'Ceremonial costumes', 'Prayer wheels', 'Ritual vessels'],
                        'architectural': ['Temple carvings', 'Stained glass', 'Sacred architecture', 'Totem poles'],
                        'performance': ['Sacred dance', 'Ritual music', 'Chanting', 'Ceremonial drama']
                    },
                    'restrictions': ['context_required', 'no_commercial_reproduction', 
                                   'spiritual_significance_noted', 'respectful_display'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.4
                },
                'secular_traditional_arts': {
                    'examples': {
                        'music': ['Folk music', 'Traditional instruments', 'Work songs', 'Ballads'],
                        'dance': ['Folk dances', 'Social dances', 'Storytelling dances'],
                        'visual': ['Decorative arts', 'Folk painting', 'Textile arts', 'Jewelry'],
                        'narrative': ['Storytelling', 'Oral literature', 'Proverbs', 'Riddles']
                    },
                    'restrictions': ['attribution_required', 'cultural_context_provided'],
                    'consultation_required': False,
                    'sensitivity_multiplier': 0.8
                }
            }
        },
        
        'historical_documents': {
            'level': 1,
            'synonyms': ['archival_materials', 'historical_records', 'documentary_heritage'],
            'terms_multilang': {
                'en': ['historical document', 'archival record', 'historical paper'],
                'fr': ['document historique', 'archive', 'document d\'époque'],
                'ar': ['وثيقة تاريخية', 'سجل أرشيفي', 'مستند تاريخي'],
                'es': ['documento histórico', 'registro archivístico', 'papel histórico'],
            },
            'subcategories': {
                'colonial_records': {
                    'examples': {
                        'administrative': ['Colonial administration', 'Census records', 'Tax documents'],
                        'legal': ['Treaties', 'Land grants', 'Court records', 'Legislation'],
                        'exploitation': ['Slave records', 'Forced labor documents', 'Resource extraction records'],
                        'missions': ['Missionary records', 'Conversion documents', 'Mission reports']
                    },
                    'restrictions': ['critical_context_required', 'trauma_awareness', 
                                   'decolonial_interpretation', 'community_counter_narratives'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.3,
                    'interpretation_frameworks': ['decolonial', 'indigenous_perspectives', 'critical_history']
                },
                'community_records': {
                    'examples': {
                        'genealogical': ['Family trees', 'Birth records', 'Marriage records', 'Death records'],
                        'property': ['Land titles', 'Deeds', 'Property registers', 'Boundary disputes'],
                        'economic': ['Trade records', 'Business ledgers', 'Contracts', 'Receipts'],
                        'personal': ['Letters', 'Diaries', 'Memoirs', 'Photographs']
                    },
                    'restrictions': ['privacy_protection', 'family_consent', 'GDPR_compliance',
                                   'living_persons_protection'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.2,
                    'privacy_period': 70  # années après décès
                }
            }
        },
        
        'linguistic_materials': {
            'level': 1,
            'synonyms': ['language_resources', 'linguistic_heritage', 'language_documentation'],
            'terms_multilang': {
                'en': ['linguistic material', 'language resource', 'language documentation'],
                'fr': ['matériel linguistique', 'ressource linguistique', 'documentation linguistique'],
                'ar': ['مواد لغوية', 'موارد لغوية', 'توثيق لغوي'],
                'es': ['material lingüístico', 'recurso lingüístico', 'documentación lingüística'],
            },
            'subcategories': {
                'endangered_languages': {
                    'examples': {
                        'recordings': ['Last speaker recordings', 'Language samples', 'Conversation corpora'],
                        'documentation': ['Dictionaries', 'Grammars', 'Lexicons', 'Phrase books'],
                        'texts': ['Story collections', 'Oral histories', 'Traditional narratives', 'Songs'],
                        'pedagogical': ['Language lessons', 'Teaching materials', 'Learning apps']
                    },
                    'restrictions': ['community_control', 'revitalization_priority', 'speaker_consent',
                                   'intellectual_property_protection'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.4,
                    'revitalization_support': True
                },
                'secret_languages': {
                    'examples': {
                        'ritual': ['Ritual languages', 'Liturgical languages', 'Priestly codes'],
                        'initiatory': ['Initiation languages', 'Mystery languages', 'Guild languages'],
                        'restricted': ['Whistled languages', 'Sign languages', 'Coded communications'],
                        'professional': ['Trade jargons', 'Craft terminologies', 'Professional argots']
                    },
                    'restrictions': ['restricted_access', 'member_authorization', 'no_unauthorized_translation'],
                    'consultation_required': True,
                    'sensitivity_multiplier': 1.6
                }
            }
        }
    }
    
    def __init__(self, custom_taxonomy: Optional[Dict] = None):
        """
        Initialiser la taxonomie culturelle enrichie.
        
        Args:
            custom_taxonomy: Taxonomie personnalisée optionnelle
        """
        if custom_taxonomy:
            self.TAXONOMY = custom_taxonomy
        
        self._build_search_indices()
        logger.info(f"Taxonomie initialisée avec {len(self.TAXONOMY)} catégories")
    
    def _build_search_indices(self):
        """Construire des index de recherche pour améliorer la performance."""
        self._term_to_categories = defaultdict(set)
        self._language_terms = defaultdict(lambda: defaultdict(set))
        
        for category, cat_data in self.TAXONOMY.items():
            # Index des synonymes
            for synonym in cat_data.get('synonyms', []):
                self._term_to_categories[synonym.lower()].add(category)
            
            # Index des termes multilingues
            for lang, terms in cat_data.get('terms_multilang', {}).items():
                for term in terms:
                    self._language_terms[lang][term.lower()].add(category)
            
            # Index des exemples
            for subcat_name, subcat_data in cat_data.get('subcategories', {}).items():
                examples = subcat_data.get('examples', {})
                if isinstance(examples, dict):
                    for cultural_group, items in examples.items():
                        for item in items:
                            self._term_to_categories[item.lower()].add((category, subcat_name))
                elif isinstance(examples, list):
                    for item in examples:
                        self._term_to_categories[item.lower()].add((category, subcat_name))
    
    @lru_cache(maxsize=256)
    def get_category(self, category_name: str) -> Optional[Dict]:
        """Récupérer les informations d'une catégorie."""
        return self.TAXONOMY.get(category_name)
    
    @lru_cache(maxsize=512)
    def get_subcategory(self, category_name: str, subcategory_name: str) -> Optional[Dict]:
        """Récupérer les informations d'une sous-catégorie."""
        category = self.get_category(category_name)
        if not category:
            return None
        return category.get('subcategories', {}).get(subcategory_name)
    
    def _detect_language(self, text: str) -> str:
        """
        Détection simple de la langue du texte.
        
        Args:
            text: Texte à analyser
            
        Returns:
            Code langue détectée (en, fr, ar, es, zh, unknown)
        """
        # Patterns simples pour détection
        patterns = {
            'ar': r'[\u0600-\u06FF]',  # Arabe
            'zh': r'[\u4E00-\u9FFF]',  # Chinois
            'fr': r'\b(le|la|les|de|du|un|une|des|et|à|dans|pour|avec)\b',
            'es': r'\b(el|la|los|las|de|del|un|una|y|en|para|con)\b',
        }
        
        text_lower = text.lower()
        
        for lang, pattern in patterns.items():
            if re.search(pattern, text_lower if lang not in ['ar', 'zh'] else text):
                return lang
        
        return 'en'  # Default anglais
    
    def _normalize_text(self, text: str) -> str:
        """Normaliser le texte pour la comparaison."""
        # Lowercase
        text = text.lower()
        # Supprimer ponctuation
        text = re.sub(r'[^\w\s]', ' ', text)
        # Supprimer espaces multiples
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokeniser le texte."""
        return self._normalize_text(text).split()
    
    def _compute_term_frequency(self, text: str) -> Dict[str, int]:
        """Calculer la fréquence des termes."""
        tokens = self._tokenize(text)
        freq = defaultdict(int)
        for token in tokens:
            freq[token] += 1
        return freq
    
    def _semantic_similarity(self, description: str, keywords: List[str], 
                            category: str, subcategory: str) -> Tuple[float, List[str]]:
        """
        Calculer similarité sémantique améliorée.
        
        Returns:
            Tuple (score, reasoning)
        """
        score = 0.0
        reasoning = []
        
        desc_norm = self._normalize_text(description)
        desc_tokens = set(self._tokenize(description))
        keywords_norm = [self._normalize_text(k) for k in keywords]
        keywords_tokens = set(token for k in keywords_norm for token in k.split())
        
        # Récupérer données catégorie/sous-catégorie
        subcat_data = self.get_subcategory(category, subcategory)
        if not subcat_data:
            return 0.0, []
        
        cat_data = self.get_category(category)
        
        # 1. Correspondance avec termes multilingues (poids: 3.0)
        lang = self._detect_language(description)
        if lang in cat_data.get('terms_multilang', {}):
            for term in cat_data['terms_multilang'][lang]:
                if term in desc_norm:
                    score += 3.0
                    reasoning.append(f"Terme linguistique correspondant: '{term}' ({lang})")
        
        # 2. Correspondance avec synonymes catégorie (poids: 2.5)
        for synonym in cat_data.get('synonyms', []):
            if synonym.lower() in desc_norm:
                score += 2.5
                reasoning.append(f"Synonyme catégorie: '{synonym}'")
        
        # 3. Correspondance avec exemples (poids: 2.0)
        examples = subcat_data.get('examples', {})
        if isinstance(examples, dict):
            for cultural_group, items in examples.items():
                for item in items:
                    item_norm = self._normalize_text(item)
                    item_tokens = set(item_norm.split())
                    
                    # Correspondance exacte
                    if item_norm in desc_norm:
                        score += 2.0
                        reasoning.append(f"Exemple exact: '{item}' ({cultural_group})")
                    # Correspondance partielle (tokens communs)
                    else:
                        common_tokens = desc_tokens & item_tokens
                        if len(common_tokens) >= 2:
                            overlap_ratio = len(common_tokens) / len(item_tokens)
                            partial_score = 1.5 * overlap_ratio
                            score += partial_score
                            reasoning.append(f"Correspondance partielle: '{item}' ({overlap_ratio:.1%})")
        
        # 4. Correspondance avec mots-clés (poids: 1.5)
        for keyword in keywords_norm:
            keyword_tokens = set(keyword.split())
            common = desc_tokens & keyword_tokens
            if common:
                kw_score = 1.5 * (len(common) / len(keyword_tokens))
                score += kw_score
                reasoning.append(f"Mot-clé: '{keyword}' (tokens: {common})")
        
        # 5. Restrictions mentionnées (poids: 1.0)
        restrictions = subcat_data.get('restrictions', [])
        for restriction in restrictions:
            restriction_terms = restriction.replace('_', ' ').split()
            if any(term in desc_tokens for term in restriction_terms):
                score += 1.0
                reasoning.append(f"Restriction mentionnée: '{restriction}'")
        
        # 6. Bonus diversité culturelle
        if isinstance(examples, dict) and len(examples) > 1:
            cultural_groups_mentioned = sum(
                1 for group in examples.keys() 
                if group.lower() in desc_norm
            )
            if cultural_groups_mentioned > 0:
                diversity_bonus = 0.5 * cultural_groups_mentioned
                score += diversity_bonus
                reasoning.append(f"Diversité culturelle: {cultural_groups_mentioned} groupes mentionnés")
        
        # Appliquer multiplicateur de sensibilité
        sensitivity_mult = subcat_data.get('sensitivity_multiplier', 1.0)
        score *= sensitivity_mult
        
        return score, reasoning
    
    def classify_item(self, item_description: str, keywords: List[str] = None,
                     language: str = None, include_alternatives: bool = True) -> ClassificationResult:
        """
        Classifier automatiquement un item avec analyse enrichie.
        
        Args:
            item_description: Description de l'item
            keywords: Liste optionnelle de mots-clés
            language: Langue forcée (sinon auto-détection)
            include_alternatives: Inclure classifications alternatives
            
        Returns:
            ClassificationResult avec classification complète
        """
        if keywords is None:
            keywords = []
        
        # Détection langue
        detected_lang = language or self._detect_language(item_description)
        
        # Validation entrée
        warnings = []
        if len(item_description.strip()) < 10:
            warnings.append("Description très courte - résultats peuvent être imprécis")
        
        # Calcul scores pour toutes catégories/sous-catégories
        all_scores = []
        
        for category, cat_data in self.TAXONOMY.items():
            for subcategory in cat_data.get('subcategories', {}).keys():
                score, reasoning = self._semantic_similarity(
                    item_description, keywords, category, subcategory
                )
                
                if score > 0:
                    all_scores.append((category, subcategory, score, reasoning))
        
        # Trier par score décroissant
        all_scores.sort(key=lambda x: x[2], reverse