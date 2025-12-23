# ============================================================================
# Fichier: module_1_ethical_assessment/core/sensitivity_classifier.py
# ============================================================================

"""
Classification et scoring de sensibilité culturelle.
Approche multi-critères avec pondération bayésienne.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from .cultural_taxonomy import CulturalTaxonomy


class SensitivityClassifier:
    """
    Classificateur de sensibilité pour objets du patrimoine culturel.
    
    Évalue 5 critères principaux:
    1. Sacralité (30%)
    2. Vie privée (20%)
    3. Risque commercialisation (20%)
    4. Sensibilité politique (15%)
    5. Contrôle communautaire (15%)
    
    Score final: 0-100
    Catégories: low (0-25), medium (25-50), high (50-75), critical (75-100)
    """
    
    def __init__(self):
        """Initialiser le classificateur avec critères d'évaluation."""
        self.taxonomy = CulturalTaxonomy()
        
        # Critères d'évaluation avec pondération
        self.evaluation_criteria = {
            'sacredness': {
                'weight': 0.30,
                'indicators': [
                    'used_in_religious_ceremony',
                    'connected_to_deity',
                    'restricted_to_initiated',
                    'seasonal_taboos',
                    'requires_purification'
                ],
                'description': 'Degré de sacralité et importance religieuse'
            },
            'privacy': {
                'weight': 0.20,
                'indicators': [
                    'contains_personal_data',
                    'living_individuals',
                    'family_secrets',
                    'medical_information',
                    'financial_data'
                ],
                'description': 'Protection des données personnelles'
            },
            'commercialization_risk': {
                'weight': 0.20,
                'indicators': [
                    'market_value_high',
                    'easily_reproducible',
                    'exploitable_knowledge',
                    'biopiracy_potential',
                    'tourism_exploitation'
                ],
                'description': 'Risque d\'exploitation commerciale'
            },
            'political_sensitivity': {
                'weight': 0.15,
                'indicators': [
                    'colonial_context',
                    'land_disputes',
                    'sovereignty_issues',
                    'cultural_genocide',
                    'repatriation_claims'
                ],
                'description': 'Implications politiques et historiques'
            },
            'community_control': {
                'weight': 0.15,
                'indicators': [
                    'community_ownership_clear',
                    'elders_authority',
                    'traditional_governance',
                    'active_stewardship',
                    'documented_protocols'
                ],
                'description': 'Niveau de contrôle communautaire'
            }
        }
    
    def calculate_sensitivity_score(
        self,
        item_metadata: Dict,
        indicator_responses: Dict[str, bool]
    ) -> Tuple[float, str, List[str]]:
        """
        Calculer le score de sensibilité (0-100).
        
        Args:
            item_metadata: Métadonnées de l'item (id, nom, culture, date, etc.)
            indicator_responses: Réponses booléennes pour chaque indicateur
            
        Returns:
            Tuple (score, category, triggered_flags)
            - score: float 0-100
            - category: 'low' | 'medium' | 'high' | 'critical'
            - triggered_flags: liste des indicateurs déclenchés
        """
        total_score = 0.0
        triggered_flags = []
        criterion_scores = {}
        
        for criterion, details in self.evaluation_criteria.items():
            criterion_score = 0
            criterion_flags = []
            
            for indicator in details['indicators']:
                full_indicator = f"{criterion}:{indicator}"
                if indicator_responses.get(indicator, False):
                    criterion_score += 1
                    criterion_flags.append(full_indicator)
            
            # Normalisation 0-1
            normalized = criterion_score / len(details['indicators'])
            
            # Application pondération
            weighted_score = normalized * details['weight']
            total_score += weighted_score
            
            criterion_scores[criterion] = {
                'raw_score': criterion_score,
                'normalized': normalized,
                'weighted': weighted_score,
                'percentage': normalized * 100
            }
            
            triggered_flags.extend(criterion_flags)
        
        # Conversion score final 0-100
        final_score = total_score * 100
        
        # Catégorisation
        category = self._categorize_score(final_score)
        
        return final_score, category, triggered_flags
    
    def _categorize_score(self, score: float) -> str:
        """
        Catégoriser un score de sensibilité.
        
        Args:
            score: Score 0-100
            
        Returns:
            Catégorie: 'low' | 'medium' | 'high' | 'critical'
        """
        if score >= 75:
            return 'critical'
        elif score >= 50:
            return 'high'
        elif score >= 25:
            return 'medium'
        else:
            return 'low'
    
    def generate_assessment_report(
        self,
        item_metadata: Dict,
        sensitivity_score: float,
        category: str,
        flags: List[str]
    ) -> Dict:
        """
        Générer un rapport d'évaluation éthique complet.
        
        Args:
            item_metadata: Métadonnées de l'item
            sensitivity_score: Score calculé
            category: Catégorie de sensibilité
            flags: Indicateurs déclenchés
            
        Returns:
            Dictionnaire avec rapport complet
        """
        # Classification taxonomique automatique
        description = item_metadata.get('description', '')
        keywords = item_metadata.get('keywords', [])
        tax_category, tax_subcategory, confidence = self.taxonomy.classify_item(
            description, keywords
        )
        
        report = {
            'metadata': {
                'report_id': f"ASSESS_{item_metadata.get('id', 'UNKNOWN')}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'generated_at': datetime.now().isoformat(),
                'framework_version': '1.0.0'
            },
            
            'item_identification': {
                'id': item_metadata.get('id'),
                'name': item_metadata.get('name'),
                'culture': item_metadata.get('culture'),
                'date': item_metadata.get('date'),
                'current_location': item_metadata.get('location'),
                'description': description
            },
            
            'taxonomic_classification': {
                'category': tax_category,
                'subcategory': tax_subcategory,
                'confidence': confidence,
                'sensitivity_level': self.taxonomy.get_sensitivity_level(tax_category) if tax_category else None
            },
            
            'sensitivity_assessment': {
                'score': round(sensitivity_score, 2),
                'category': category,
                'triggered_concerns': flags,
                'total_flags': len(flags)
            },
            
            'required_actions': self._determine_required_actions(category, flags),
            
            'consultation_requirements': self._determine_consultations(
                category, item_metadata, tax_category, tax_subcategory
            ),
            
            'access_recommendations': self._recommend_access_tier(category, flags),
            
            'timeline_estimate': self._estimate_timeline(category),
            
            'ethical_review_status': 'pending_consultation' if category in ['high', 'critical'] else 'preliminary_approval',
            
            'next_steps': self._generate_next_steps(category, tax_category, tax_subcategory)
        }
        
        return report
    
    def _determine_required_actions(self, category: str, flags: List[str]) -> List[Dict]:
        """Déterminer les actions requises selon niveau de sensibilité."""
        actions = []
        
        if category == 'critical':
            actions.extend([
                {
                    'action': 'halt_digitization',
                    'priority': 'immediate',
                    'description': 'Arrêt immédiat de toute numérisation en attente de consultation',
                    'responsible': 'Project Manager'
                },
                {
                    'action': 'identify_stakeholders',
                    'priority': 'immediate',
                    'description': 'Identification des communautés sources et autorités culturelles',
                    'responsible': 'Cultural Liaison Officer'
                },
                {
                    'action': 'legal_review',
                    'priority': 'high',
                    'description': 'Vérification conformité UNDRIP, NAGPRA, législations nationales',
                    'responsible': 'Legal Team'
                }
            ])
        
        if category in ['high', 'critical']:
            actions.append({
                'action': 'community_consultation',
                'priority': 'high',
                'description': 'Consultation formelle des communautés sources requise',
                'responsible': 'Cultural Liaison Officer'
            })
        
        # Actions spécifiques selon flags
        flag_prefixes = [f.split(':')[0] for f in flags]
        
        if 'commercialization_risk' in flag_prefixes:
            actions.append({
                'action': 'intellectual_property_assessment',
                'priority': 'medium',
                'description': 'Évaluation droits de propriété intellectuelle et risque biopiraterie',
                'responsible': 'IP Specialist'
            })
        
        if 'privacy' in flag_prefixes:
            actions.append({
                'action': 'gdpr_compliance_check',
                'priority': 'high',
                'description': 'Vérification conformité RGPD et lois protection données',
                'responsible': 'Data Protection Officer'
            })
        
        if 'political_sensitivity' in flag_prefixes:
            actions.append({
                'action': 'historical_context_research',
                'priority': 'medium',
                'description': 'Recherche approfondie du contexte historique et politique',
                'responsible': 'Historian/Researcher'
            })
        
        return actions
    
    def _determine_consultations(
        self,
        category: str,
        metadata: Dict,
        tax_category: Optional[str],
        tax_subcategory: Optional[str]
    ) -> Dict:
        """Déterminer les protocoles de consultation requis."""
        consultations = {
            'required': category in ['high', 'critical'],
            'stakeholders': [],
            'protocol': None,
            'estimated_duration': None,
            'consultation_type': None
        }
        
        if consultations['required']:
            culture = metadata.get('culture', 'Unknown')
            
            # Identifier stakeholders
            stakeholders = [
                f"{culture} community elders",
                f"{culture} cultural authority",
                "National heritage commission"
            ]
            
            if category == 'critical':
                stakeholders.extend([
                    "Indigenous rights organization",
                    "Ethics review board",
                    "Legal representatives"
                ])
            
            consultations['stakeholders'] = stakeholders
            
            # Protocole selon catégorie
            if category == 'critical':
                consultations['protocol'] = 'full_consensus_required'
                consultations['consultation_type'] = 'free_prior_informed_consent'
                consultations['estimated_duration'] = '6-12 months'
            else:
                consultations['protocol'] = 'informed_consultation'
                consultations['consultation_type'] = 'community_engagement'
                consultations['estimated_duration'] = '3-6 months'
            
            # Ajouter protocoles taxonomiques
            if tax_category and tax_subcategory:
                if self.taxonomy.requires_consultation(tax_category, tax_subcategory):
                    restrictions = self.taxonomy.get_restrictions(tax_category, tax_subcategory)
                    consultations['additional_requirements'] = restrictions
        
        return consultations
    
    def _recommend_access_tier(self, category: str, flags: List[str]) -> Dict:
        """Recommander le niveau d'accès approprié."""
        if category == 'critical':
            return {
                'tier': 'tier_3_restricted',
                'permissions': 'metadata_only',
                'conditions': [
                    'community_approval_required',
                    'ceremonial_context_only',
                    'no_digital_reproduction'
                ],
                'rationale': 'Sensibilité extrême requiert restrictions maximales'
            }
        
        elif category == 'high':
            return {
                'tier': 'tier_2_community',
                'permissions': 'authenticated_research_only',
                'conditions': [
                    'attribution_required',
                    'non_commercial',
                    'contextual_information_mandatory'
                ],
                'rationale': 'Haute sensibilité nécessite contrôle accès'
            }
        
        elif category == 'medium':
            return {
                'tier': 'tier_1_authenticated',
                'permissions': 'research_with_attribution',
                'conditions': [
                    'proper_citation',
                    'context_preservation',
                    'educational_use_preferred'
                ],
                'rationale': 'Sensibilité modérée permet accès contrôlé'
            }
        
        else:
            return {
                'tier': 'tier_0_public',
                'permissions': 'open_access',
                'conditions': [
                    'attribution_recommended',
                    'responsible_use'
                ],
                'rationale': 'Faible sensibilité permet accès ouvert'
            }
    
    def _estimate_timeline(self, category: str) -> Dict:
        """Estimer le calendrier pour le processus d'évaluation."""
        timelines = {
            'critical': {
                'initial_assessment': '1-2 weeks',
                'stakeholder_identification': '2-3 weeks',
                'consultation_process': '6-12 months',
                'decision_implementation': '1-2 months',
                'total_estimated': '8-15 months'
            },
            'high': {
                'initial_assessment': '1 week',
                'stakeholder_identification': '1-2 weeks',
                'consultation_process': '3-6 months',
                'decision_implementation': '2-4 weeks',
                'total_estimated': '4-8 months'
            },
            'medium': {
                'initial_assessment': '3-5 days',
                'stakeholder_identification': '1 week',
                'consultation_process': '1-3 months',
                'decision_implementation': '1-2 weeks',
                'total_estimated': '2-4 months'
            },
            'low': {
                'initial_assessment': '1-2 days',
                'stakeholder_identification': 'Not required',
                'consultation_process': 'Optional',
                'decision_implementation': '3-7 days',
                'total_estimated': '1-2 weeks'
            }
        }
        
        return timelines.get(category, timelines['medium'])
    
    def _generate_next_steps(
        self,
        category: str,
        tax_category: Optional[str],
        tax_subcategory: Optional[str]
    ) -> List[str]:
        """Générer liste des prochaines étapes recommandées."""
        steps = []
        
        if category in ['high', 'critical']:
            steps.extend([
                "1. Suspendre toute activité de numérisation",
                "2. Contacter les représentants de la communauté source",
                "3. Préparer documentation complète de l'item"
            ])
        
        if tax_category and tax_subcategory:
            restrictions = self.taxonomy.get_restrictions(tax_category, tax_subcategory)
            if restrictions:
                steps.append(f"4. Respecter les restrictions: {', '.join(restrictions)}")
        
        steps.extend([
            f"{'5' if len(steps) == 4 else '4'}. Soumettre à comité d'éthique pour validation",
            f"{'6' if len(steps) == 5 else '5'}. Documenter tout le processus de décision"
        ])
        
        return steps
    
    def batch_assess(
        self,
        items: List[Dict],
        indicators_list: List[Dict]
    ) -> List[Dict]:
        """
        Évaluer un lot d'items en batch.
        
        Args:
            items: Liste de métadonnées d'items
            indicators_list: Liste de réponses d'indicateurs correspondantes
            
        Returns:
            Liste de rapports d'évaluation
        """
        reports = []
        
        for item, indicators in zip(items, indicators_list):
            score, category, flags = self.calculate_sensitivity_score(item, indicators)
            report = self.generate_assessment_report(item, score, category, flags)
            reports.append(report)
        
        return reports


# ============================================================================
# Exemple d'utilisation
# ============================================================================

if __name__ == "__main__":
    # Créer classifier
    classifier = SensitivityClassifier()
    
    # Métadonnées d'un item
    item_metadata = {
        'id': 'torah_001',
        'name': 'Ancient Torah Scroll',
        'culture': 'Jewish',
        'date': '15th century',
        'location': 'National Library',
        'description': 'Torah scroll used in synagogue ceremonies',
        'keywords': ['religious', 'sacred', 'jewish', 'scripture']
    }
    
    # Réponses aux indicateurs
    indicators = {
        # Sacredness
        'used_in_religious_ceremony': True,
        'connected_to_deity': True,
        'restricted_to_initiated': False,
        'seasonal_taboos': False,
        'requires_purification': True,
        
        # Privacy
        'contains_personal_data': False,
        'living_individuals': False,
        'family_secrets': False,
        'medical_information': False,
        'financial_data': False,
        
        # Commercialization risk
        'market_value_high': True,
        'easily_reproducible': False,
        'exploitable_knowledge': False,
        'biopiracy_potential': False,
        'tourism_exploitation': False,
        
        # Political sensitivity
        'colonial_context': False,
        'land_disputes': False,
        'sovereignty_issues': False,
        'cultural_genocide': False,
        'repatriation_claims': False,
        
        # Community control
        'community_ownership_clear': True,
        'elders_authority': True,
        'traditional_governance': True,
        'active_stewardship': True,
        'documented_protocols': True
    }
    
    # Calcul score
    score, category, flags = classifier.calculate_sensitivity_score(
        item_metadata, indicators
    )
    
    print(f"📊 Évaluation de Sensibilité:")
    print(f"  Score: {score:.2f}/100")
    print(f"  Catégorie: {category}")
    print(f"  Indicateurs déclenchés: {len(flags)}")
    
    # Rapport complet
    report = classifier.generate_assessment_report(
        item_metadata, score, category, flags
    )
    
    print(f"\n📋 Rapport Complet:")
    print(f"  ID Rapport: {report['metadata']['report_id']}")
    print(f"  Classification: {report['taxonomic_classification']['category']} / {report['taxonomic_classification']['subcategory']}")
    print(f"  Consultation requise: {report['consultation_requirements']['required']}")
    print(f"  Niveau d'accès: {report['access_recommendations']['tier']}")
    print(f"  Durée estimée: {report['timeline_estimate']['total_estimated']}")
