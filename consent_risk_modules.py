# ============================================================================
# Fichier: module_1_ethical_assessment/core/consent_framework.py
# ============================================================================

"""
Gestion du consentement communautaire selon CARE Principles et FPIC.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum


class ConsentType(Enum):
    """Types de consentement disponibles."""
    FPIC = "free_prior_informed_consent"  # Consentement préalable, libre et éclairé
    ONGOING = "ongoing_consent"  # Consentement continu
    INFORMED_NOTIFICATION = "informed_notification"  # Notification informée
    COMMUNITY_LED = "community_led_process"  # Processus dirigé par la communauté


class ConsentStatus(Enum):
    """Statuts possibles d'une demande de consentement."""
    PENDING = "pending"
    GRANTED = "granted"
    DENIED = "denied"
    CONDITIONAL = "conditional"
    EXPIRED = "expired"
    WITHDRAWN = "withdrawn"


class CommunityConsentFramework:
    """
    Framework de gestion du consentement communautaire.
    
    Implémente:
    - FPIC (Free, Prior, and Informed Consent)
    - CARE Principles
    - UNESCO ethical standards
    - Ongoing consent monitoring
    """
    
    def __init__(self):
        """Initialiser le framework de consentement."""
        self.consent_types = {
            ConsentType.FPIC: {
                'description': 'Consentement préalable complet avant toute action',
                'required_for': ['critical', 'high'],
                'elements': [
                    'full_disclosure_purposes',
                    'potential_risks_explained',
                    'community_benefits_outlined',
                    'right_to_refuse_clarified',
                    'withdrawal_process_explained'
                ],
                'minimum_duration': timedelta(days=180),  # 6 mois minimum
                'requires_legal_agreement': True
            },
            ConsentType.ONGOING: {
                'description': 'Consentement continu avec droit de retrait',
                'required_for': ['critical'],
                'review_frequency': timedelta(days=365),  # Révision annuelle
                'requires_periodic_renewal': True
            },
            ConsentType.INFORMED_NOTIFICATION: {
                'description': 'Notification détaillée sans veto',
                'required_for': ['medium'],
                'elements': ['purpose_disclosure', 'attribution_commitment'],
                'minimum_duration': timedelta(days=30)
            },
            ConsentType.COMMUNITY_LED: {
                'description': 'Processus entièrement dirigé par la communauté',
                'required_for': ['critical', 'high'],
                'community_control': 'full',
                'timeline': 'community_determined'
            }
        }
    
    def determine_consent_type(self, sensitivity_category: str) -> ConsentType:
        """
        Déterminer le type de consentement requis selon la sensibilité.
        
        Args:
            sensitivity_category: 'low', 'medium', 'high', ou 'critical'
            
        Returns:
            Type de consentement approprié
        """
        if sensitivity_category == 'critical':
            return ConsentType.FPIC
        elif sensitivity_category == 'high':
            return ConsentType.ONGOING
        elif sensitivity_category == 'medium':
            return ConsentType.INFORMED_NOTIFICATION
        else:
            return ConsentType.INFORMED_NOTIFICATION
    
    def generate_consent_request(
        self,
        item_metadata: Dict,
        assessment_report: Dict,
        consent_type: ConsentType
    ) -> Dict:
        """
        Générer une demande de consentement formelle.
        
        Args:
            item_metadata: Métadonnées de l'item
            assessment_report: Rapport d'évaluation éthique
            consent_type: Type de consentement requis
            
        Returns:
            Dictionnaire avec demande de consentement complète
        """
        category = assessment_report['sensitivity_assessment']['category']
        
        consent_request = {
            'request_id': f"CONSENT_{item_metadata['id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'consent_type': consent_type.value,
            'date_issued': datetime.now().isoformat(),
            'expiry_date': (datetime.now() + self.consent_types[consent_type].get('minimum_duration', timedelta(days=180))).isoformat(),
            
            'item_description': {
                'id': item_metadata['id'],
                'name': item_metadata['name'],
                'cultural_significance': item_metadata.get('cultural_significance', 'To be determined'),
                'current_status': item_metadata.get('location', 'Unknown'),
                'category': assessment_report['taxonomic_classification'].get('category'),
                'subcategory': assessment_report['taxonomic_classification'].get('subcategory')
            },
            
            'proposed_actions': {
                'digitization': {
                    'method': 'High-resolution digital scanning',
                    'purpose': 'Preservation, research access, and cultural revitalization',
                    'storage': 'Secure institutional repository with community access',
                    'timeline': 'Within 6 months of approval'
                },
                'access_control': {
                    'tier': assessment_report['access_recommendations']['tier'],
                    'permissions': assessment_report['access_recommendations']['permissions'],
                    'restrictions': assessment_report['access_recommendations']['conditions']
                },
                'research_uses': {
                    'allowed': ['academic_study', 'educational_display', 'cultural_preservation'],
                    'prohibited': ['commercial_exploitation', 'decontextualized_use', 'unauthorized_reproduction']
                },
                'dissemination': {
                    'platforms': ['institutional_repository', 'community_portal'],
                    'formats': ['digital_images', 'metadata', '3d_models'],
                    'restrictions': 'As per community agreement'
                }
            },
            
            'community_benefits': {
                'cultural_revitalization': {
                    'description': 'High-quality digital copies returned to community',
                    'timeline': 'Within 3 months of digitization'
                },
                'educational_access': {
                    'description': 'Materials provided for community schools and cultural centers',
                    'format': 'Educational packages with contextual information'
                },
                'economic_benefits': {
                    'description': 'Revenue sharing if commercial uses authorized',
                    'percentage': '50% of net proceeds',
                    'fund_usage': 'Community-determined'
                },
                'capacity_building': {
                    'description': 'Training in digital preservation techniques',
                    'participants': 'Community members',
                    'duration': '6-month training program'
                },
                'knowledge_sovereignty': {
                    'description': 'Community retains ultimate control and decision-making authority',
                    'mechanisms': ['community_advisory_board', 'veto_power', 'ongoing_consultation']
                }
            },
            
            'potential_risks': {
                'misappropriation': {
                    'description': 'Risk of unauthorized commercial use',
                    'mitigation': 'Legal protections, watermarking, monitoring'
                },
                'decontextualization': {
                    'description': 'Removal from cultural meaning and context',
                    'mitigation': 'Mandatory contextual information, community narratives'
                },
                'commodification': {
                    'description': 'Treatment as mere commodity',
                    'mitigation': 'Ethical use agreements, education programs'
                },
                'spiritual_harm': {
                    'description': 'Violation of sacred protocols',
                    'mitigation': 'Cultural protocols respected, community oversight'
                }
            },
            
            'community_rights': {
                'right_to_refuse': {
                    'description': 'Unconditional right to deny consent',
                    'no_consequences': True
                },
                'right_to_modify': {
                    'description': 'Right to modify conditions at any time',
                    'process': 'Written notification with 30-day implementation'
                },
                'right_to_withdraw': {
                    'description': 'Right to withdraw consent at any time',
                    'process': 'Immediate cessation of all uses upon notification',
                    'data_return': 'All data returned or destroyed within 90 days'
                },
                'right_to_consultation': {
                    'description': 'Ongoing consultation throughout process',
                    'frequency': 'Quarterly updates minimum'
                },
                'data_sovereignty': {
                    'description': 'Community retains ultimate ownership and control',
                    'implementation': 'Community-approved governance structure'
                }
            },
            
            'consultation_process': {
                'stakeholders': assessment_report['consultation_requirements']['stakeholders'],
                'timeline': assessment_report['consultation_requirements']['estimated_duration'],
                'decision_mechanism': 'Community consensus or designated cultural authority',
                'language_support': {
                    'primary': item_metadata.get('community_language', 'English'),
                    'translation': 'Professional interpreters provided',
                    'written_materials': 'Translated versions provided'
                },
                'accessibility': {
                    'locations': 'Multiple community meetings at convenient locations',
                    'formats': 'Oral presentations, written materials, visual aids',
                    'accommodations': 'Disability accommodations, childcare, meals provided'
                }
            },
            
            'legal_framework': {
                'applicable_laws': [
                    'UNDRIP (UN Declaration on Rights of Indigenous Peoples)',
                    'National heritage protection laws',
                    'Data protection regulations (GDPR/equivalent)',
                    'Intellectual property laws'
                ],
                'dispute_resolution': {
                    'mechanism': 'Mediation with community-selected mediator',
                    'jurisdiction': 'Community preference',
                    'costs': 'Borne by institution'
                }
            },
            
            'documentation_requirements': {
                'meeting_minutes': 'Full minutes of all consultation meetings',
                'audio_visual': 'Recordings if permitted by community',
                'written_agreement': 'Signed by all authorized representatives',
                'witness_signatures': 'Independent witnesses present',
                'translation_certification': 'Certified translations of all documents'
            }
        }
        
        return consent_request
    
    def record_consent_decision(
        self,
        consent_request_id: str,
        decision: ConsentStatus,
        decision_makers: List[str],
        decision_date: datetime,
        conditions: Optional[List[str]] = None,
        duration: Optional[timedelta] = None,
        notes: Optional[str] = None
    ) -> Dict:
        """
        Enregistrer une décision de consentement.
        
        Args:
            consent_request_id: ID de la demande
            decision: Décision prise
            decision_makers: Liste des décideurs
            decision_date: Date de la décision
            conditions: Conditions éventuelles
            duration: Durée de validité
            notes: Notes additionnelles
            
        Returns:
            Enregistrement complet de la décision
        """
        consent_record = {
            'record_id': f"RECORD_{consent_request_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'request_id': consent_request_id,
            'decision': decision.value,
            'decision_date': decision_date.isoformat(),
            'decision_makers': decision_makers,
            'decision_process': 'Community consensus meeting',
            
            'conditions': conditions or [],
            'duration': duration.days if duration else None,
            'expiry_date': (decision_date + duration).isoformat() if duration else None,
            'review_required': duration is not None and decision == ConsentStatus.GRANTED,
            'next_review_date': (decision_date + timedelta(days=365)).isoformat() if decision == ConsentStatus.GRANTED else None,
            
            'documentation': {
                'meeting_minutes': 'Attached',
                'audio_recording': 'Available upon request',
                'written_agreement': 'Signed and filed',
                'witness_signatures': 'Verified',
                'legal_review': 'Completed'
            },
            
            'ongoing_obligations': self._determine_obligations(decision, conditions),
            
            'withdrawal_process': {
                'method': 'Written notification to designated contact',
                'response_time': 'Immediate upon receipt',
                'data_handling': 'All data returned or destroyed within 90 days'
            },
            
            'notes': notes or ''
        }
        
        return consent_record
    
    def _determine_obligations(self, decision: ConsentStatus, conditions: Optional[List[str]]) -> Dict:
        """Déterminer les obligations continues selon la décision."""
        if decision == ConsentStatus.GRANTED:
            obligations = {
                'reporting': {
                    'frequency': 'Quarterly',
                    'content': ['usage_statistics', 'research_outcomes', 'community_benefits_realized']
                },
                'community_access': {
                    'type': 'High-quality digital copies',
                    'timeline': 'Within 6 months of digitization',
                    'format': 'Community-preferred formats'
                },
                'attribution': {
                    'required': True,
                    'format': 'As specified in community agreement',
                    'verification': 'Regular monitoring'
                },
                'benefit_sharing': {
                    'type': 'As per agreement',
                    'distribution': 'Community-determined',
                    'reporting': 'Annual financial reports'
                },
                'monitoring': {
                    'usage_tracking': 'Comprehensive logging of all access',
                    'compliance_audits': 'Annual independent audits',
                    'community_oversight': 'Community representative access to all records'
                }
            }
        elif decision == ConsentStatus.CONDITIONAL:
            obligations = {
                'condition_compliance': {
                    'monitoring': 'Continuous',
                    'reporting': 'Monthly until conditions met',
                    'verification': 'Community representative inspection'
                }
            }
        else:
            obligations = {}
        
        return obligations
    
    def check_consent_validity(self, consent_record: Dict) -> Tuple[bool, Optional[str]]:
        """
        Vérifier si un consentement est toujours valide.
        
        Args:
            consent_record: Enregistrement de consentement
            
        Returns:
            Tuple (is_valid, reason_if_invalid)
        """
        decision = ConsentStatus(consent_record['decision'])
        
        # Refus ou retrait
        if decision in [ConsentStatus.DENIED, ConsentStatus.WITHDRAWN]:
            return False, f"Consent was {decision.value}"
        
        # Vérifier expiration
        if consent_record['expiry_date']:
            expiry = datetime.fromisoformat(consent_record['expiry_date'])
            if datetime.now() > expiry:
                return False, "Consent has expired"
        
        # Vérifier besoin de révision
        if consent_record['review_required'] and consent_record['next_review_date']:
            review_date = datetime.fromisoformat(consent_record['next_review_date'])
            if datetime.now() > review_date:
                return False, "Consent requires review"
        
        return True, None


# ============================================================================
# Fichier: module_1_ethical_assessment/core/risk_assessor.py
# ============================================================================

"""
Évaluation des risques multidimensionnels pour objets patrimoniaux.
"""

import numpy as np
from typing import Dict, List, Tuple


class CulturalHeritageRiskAssessor:
    """
    Évaluateur de risques multi-dimensionnels pour patrimoine culturel.
    
    5 dimensions évaluées:
    1. Appropriation Risk (x2.0)
    2. Misrepresentation Risk (x1.5)
    3. Security Risk (x2.5)
    4. Privacy Risk (x2.0)
    5. Commodification Risk (x1.5)
    """
    
    def __init__(self):
        """Initialiser l'évaluateur de risques."""
        self.risk_dimensions = {
            'appropriation_risk': {
                'factors': [
                    'market_demand',
                    'ease_of_reproduction',
                    'lack_of_legal_protection',
                    'historical_exploitation',
                    'commercial_interest'
                ],
                'severity_multiplier': 2.0,
                'description': 'Risque d\'appropriation culturelle et exploitation'
            },
            
            'misrepresentation_risk': {
                'factors': [
                    'complex_cultural_context',
                    'sacred_meanings',
                    'easy_to_decontextualize',
                    'stereotype_potential',
                    'simplified_narratives'
                ],
                'severity_multiplier': 1.5,
                'description': 'Risque de décontextualisation et mauvaise représentation'
            },
            
            'security_risk': {
                'factors': [
                    'site_vulnerability_to_looting',
                    'gps_precision_available',
                    'high_value_objects',
                    'conflict_zone',
                    'inadequate_protection'
                ],
                'severity_multiplier': 2.5,
                'description': 'Risques de sécurité physique et pillage'
            },
            
            'privacy_risk': {
                'factors': [
                    'living_individuals',
                    'identifiable_data',
                    'sensitive_personal_info',
                    'family_secrets',
                    'medical_records'
                ],
                'severity_multiplier': 2.0,
                'description': 'Risques de violation de vie privée'
            },
            
            'commodification_risk': {
                'factors': [
                    'commercial_interest_high',
                    'tourism_impact_potential',
                    'souvenir_industry',
                    'digital_marketplace',
                    'intellectual_property_value'
                ],
                'severity_multiplier': 1.5,
                'description': 'Risque de marchandisation culturelle'
            }
        }
    
    def assess_multidimensional_risk(
        self,
        item_metadata: Dict,
        risk_indicators: Dict[str, bool]
    ) -> Dict:
        """
        Évaluer les risques selon toutes les dimensions.
        
        Args:
            item_metadata: Métadonnées de l'item
            risk_indicators: Indicateurs de risque booléens
            
        Returns:
            Rapport d'évaluation des risques complet
        """
        risk_scores = {}
        overall_risk = 0.0
        high_risk_areas = []
        critical_factors = []
        
        for dimension, details in self.risk_dimensions.items():
            dimension_score = 0
            triggered_factors = []
            
            for factor in details['factors']:
                indicator_key = f"{dimension}:{factor}"
                if risk_indicators.get(factor, False):
                    dimension_score += 1
                    triggered_factors.append(factor)
            
            # Normalisation 0-1
            normalized = dimension_score / len(details['factors'])
            
            # Application multiplicateur de sévérité
            weighted = normalized * details['severity_multiplier']
            
            risk_scores[dimension] = {
                'raw_score': dimension_score,
                'normalized': normalized,
                'weighted': weighted,
                'percentage': normalized * 100,
                'triggered_factors': triggered_factors,
                'severity_multiplier': details['severity_multiplier']
            }
            
            overall_risk += weighted
            
            # Identifier zones à haut risque
            if normalized >= 0.6:
                high_risk_areas.append(dimension)
                
            if normalized >= 0.8:
                critical_factors.extend(triggered_factors)
        
        # Normalisation score global
        max_possible = sum(d['severity_multiplier'] for d in self.risk_dimensions.values())
        overall_risk_normalized = (overall_risk / max_possible) * 100
        
        return {
            'assessment_id': f"RISK_{item_metadata.get('id', 'UNKNOWN')}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'item_id': item_metadata.get('id'),
            'assessment_date': datetime.now().isoformat(),
            
            'overall_risk_score': round(overall_risk_normalized, 2),
            'risk_category': self._categorize_risk(overall_risk_normalized),
            
            'dimensional_scores': risk_scores,
            'high_risk_areas': high_risk_areas,
            'critical_factors': critical_factors,
            
            'mitigation_plan': self._generate_mitigation_plan(risk_scores, high_risk_areas),
            
            'monitoring_requirements': self._determine_monitoring(overall_risk_normalized),
            
            'recommendations': self._generate_recommendations(
                overall_risk_normalized,
                high_risk_areas,
                critical_factors
            )
        }
    
    def _categorize_risk(self, score: float) -> str:
        """Catégoriser le risque global."""
        if score >= 70:
            return 'critical'
        elif score >= 50:
            return 'high'
        elif score >= 30:
            return 'moderate'
        else:
            return 'low'
    
    def _generate_mitigation_plan(
        self,
        risk_scores: Dict,
        high_risk_areas: List[str]
    ) -> List[Dict]:
        """Générer un plan de mitigation des risques."""
        mitigations = []
        
        mitigation_strategies = {
            'appropriation_risk': [
                {'action': 'Register trademark/copyright protection', 'priority': 'high', 'timeline': '1 month'},
                {'action': 'Implement digital watermarking', 'priority': 'high', 'timeline': '2 weeks'},
                {'action': 'Restrict high-resolution access', 'priority': 'medium', 'timeline': '1 week'},
                {'action': 'Monitor commercial marketplaces', 'priority': 'ongoing', 'timeline': 'continuous'}
            ],
            'misrepresentation_risk': [
                {'action': 'Require contextual information display', 'priority': 'high', 'timeline': '1 week'},
                {'action': 'Commission community-authored descriptions', 'priority': 'high', 'timeline': '1 month'},
                {'action': 'Bundle with educational materials', 'priority': 'medium', 'timeline': '2 weeks'},
                {'action': 'Prohibit decontextualized use in license', 'priority': 'high', 'timeline': '1 week'}
            ],
            'security_risk': [
                {'action': 'Implement GPS obfuscation', 'priority': 'critical', 'timeline': 'immediate'},
                {'action': 'Enable comprehensive access logging', 'priority': 'high', 'timeline': '1 week'},
                {'action': 'Apply geographic access restrictions', 'priority': 'high', 'timeline': '1 week'},
                {'action': 'Enhance on-site surveillance', 'priority': 'medium', 'timeline': '1 month'}
            ],
            'privacy_risk': [
                {'action': 'Apply anonymization protocols', 'priority': 'critical', 'timeline': 'immediate'},
                {'action': 'Collect individual consents', 'priority': 'high', 'timeline': '2 months'},
                {'action': 'Implement time-delayed release', 'priority': 'medium', 'timeline': '1 week'},
                {'action': 'Create restricted access tiers', 'priority': 'high', 'timeline': '1 week'}
            ],
            'commodification_risk': [
                {'action': 'Apply non-commercial license', 'priority': 'high', 'timeline': '1 week'},
                {'action': 'Negotiate benefit-sharing agreement', 'priority': 'high', 'timeline': '2 months'},
                {'action': 'Prohibit commercial derivatives', 'priority': 'high', 'timeline': '1 week'},
                {'action': 'Conduct tourism impact assessment', 'priority': 'medium', 'timeline': '1 month'}
            ]
        }
        
        for dimension in high_risk_areas:
            strategies = mitigation_strategies.get(dimension, [])
            for strategy in strategies:
                strategy['dimension'] = dimension
                strategy['status'] = 'planned'
                mitigations.append(strategy)
        
        # Trier par priorité
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'ongoing': 3}
        mitigations.sort(key=lambda x: priority_order.get(x['priority'], 99))
        
        return mitigations
    
    def _determine_monitoring(self, risk_score: float) -> Dict:
        """Déterminer les exigences de monitoring."""
        if risk_score >= 70:
            return {
                'frequency': 'daily',
                'metrics': ['access_logs', 'usage_patterns', 'anomaly_detection', 'security_alerts'],
                'reporting': 'weekly',
                'escalation': 'immediate_for_violations'
            }
        elif risk_score >= 50:
            return {
                'frequency': 'weekly',
                'metrics': ['access_logs', 'usage_patterns', 'security_alerts'],
                'reporting': 'monthly',
                'escalation': '24h_for_violations'
            }
        elif risk_score >= 30:
            return {
                'frequency': 'monthly',
                'metrics': ['access_logs', 'usage_patterns'],
                'reporting': 'quarterly',
                'escalation': '72h_for_violations'
            }
        else:
            return {
                'frequency': 'quarterly',
                'metrics': ['basic_analytics'],
                'reporting': 'annual',
                'escalation': 'standard_process'
            }
    
    def _generate_recommendations(
        self,
        overall_risk: float,
        high_risk_areas: List[str],
        critical_factors: List[str]
    ) -> List[str]:
        """Générer des recommandations basées sur l'évaluation."""
        recommendations = []
        
        if overall_risk >= 70:
            recommendations.append("⚠️ RISQUE CRITIQUE: Consultation immédiate avec experts sécurité et communauté")
            recommendations.append("Envisager de reporter la numérisation jusqu'à mise en place protections adéquates")
        
        if 'security_risk' in high_risk_areas:
            recommendations.append("🔒 Implémenter obfuscation GPS et restrictions géographiques immédiatement")
        
        if 'appropriation_risk' in high_risk_areas:
            recommendations.append("© Enregistrer protections légales avant toute publication")
        
        if 'privacy_risk' in high_risk_areas:
            recommendations.append("🔐 Obtenir consentements individuels avant numérisation")
        
        if len(critical_factors) > 0:
            recommendations.append(f"⚡ Facteurs critiques à traiter en priorité: {', '.join(critical_factors)}")
        
        recommendations.append("📋 Documenter toutes les décisions et mesures prises")
        recommendations.append("🤝 Maintenir communication régulière avec les parties prenantes")
        
        return recommendations


# ============================================================================
# Tests et exemples
# ============================================================================

if __name__ == "__main__":
    print("🛡️ Test Consent Framework & Risk Assessor")
    print("=" * 60)
    
    # Test Consent Framework
    consent_fw = CommunityConsentFramework()
    consent_type = consent_fw.determine_consent_type('critical')
    print(f"\n✅ Consent type pour 'critical': {consent_type.value}")
    
    # Test Risk Assessor
    risk_assessor = CulturalHeritageRiskAssessor()
    
    item = {'id': 'sacred_site_001', 'name': 'Sacred Mountain Site'}
    indicators = {
        'market_demand': True,
        'ease_of_reproduction': False,
        'gps_precision_available': True,
        'high_value_objects': True,
        'living_individuals': True
    }
    
    risk_report = risk_assessor.assess_multidimensional_risk(item, indicators)
    print(f"\n📊 Risk Assessment:")
    print(f"  Overall Risk: {risk_report['overall_risk_score']:.2f}/100")
    print(f"  Category: {risk_report['risk_category']}")
    print(f"  High Risk Areas: {', '.join(risk_report['high_risk_areas'])}")
    print(f"  Mitigations: {len(risk_report['mitigation_plan'])} actions recommended")
