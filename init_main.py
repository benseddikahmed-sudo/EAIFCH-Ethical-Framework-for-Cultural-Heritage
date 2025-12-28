"""
EAIFCH - Ethical AI Framework for Cultural Heritage

A comprehensive framework for ensuring ethical AI deployment in cultural heritage
management, preservation, and valorization.

Author: Ahmed Ben Seddik
License: MIT
"""

__version__ = "1.1.0"
__author__ = "Ahmed Ben Seddik"
__email__ = "your-email@institution.fr"
__license__ = "MIT"

from eaifch.core.taxonomy import (
    EthicalPrinciple,
    EthicalCategory,
    EthicalTaxonomy,
)

from eaifch.core.framework import (
    EthicalFramework,
    CulturalHeritageProject,
)

from eaifch.core.risk_assessor import (
    RiskAssessor,
    RiskLevel,
    Risk,
)

from eaifch.core.compliance_checker import (
    ComplianceChecker,
    ComplianceStatus,
)

from eaifch.core.assessment import (
    Assessment,
    AssessmentReport,
)

__all__ = [
    # Version
    "__version__",
    "__author__",
    
    # Core classes
    "EthicalFramework",
    "CulturalHeritageProject",
    "EthicalTaxonomy",
    "EthicalPrinciple",
    "EthicalCategory",
    
    # Risk assessment
    "RiskAssessor",
    "RiskLevel",
    "Risk",
    
    # Compliance
    "ComplianceChecker",
    "ComplianceStatus",
    
    # Assessment
    "Assessment",
    "AssessmentReport",
]

# Package metadata
PACKAGE_INFO = {
    "name": "eaifch",
    "version": __version__,
    "description": "Ethical AI Framework for Cultural Heritage",
    "author": __author__,
    "email": __email__,
    "license": __license__,
    "url": "https://github.com/benseddikahmed-sudo/EAIFCH-Ethical-Framework-for-Cultural-Heritage",
    "documentation": "https://eaifch.readthedocs.io",
    "principles_count": 24,
    "categories_count": 8,
}


def get_version() -> str:
    """Get the current version of EAIFCH."""
    return __version__


def get_info() -> dict:
    """Get package information."""
    return PACKAGE_INFO.copy()


# Quick start function
def quick_assess(project_data: dict) -> dict:
    """
    Quick ethical assessment of a cultural heritage AI project.
    
    Args:
        project_data: Dictionary containing project details
        
    Returns:
        Dictionary with assessment results
        
    Example:
        >>> result = quick_assess({
        ...     "name": "Museum AI Guide",
        ...     "ai_techniques": ["nlp", "recommendation"],
        ...     "data_encryption": True,
        ...     "bias_testing": False
        ... })
        >>> print(f"Score: {result['overall_score']}/100")
    """
    framework = EthicalFramework()
    project = CulturalHeritageProject(**project_data)
    assessment = framework.assess(project)
    
    return {
        "overall_score": assessment.overall_score,
        "category_scores": assessment.category_scores,
        "violations_count": len(assessment.violations),
        "high_priority_risks": len(assessment.high_priority_risks),
        "recommendations": assessment.get_top_recommendations(5),
    }
