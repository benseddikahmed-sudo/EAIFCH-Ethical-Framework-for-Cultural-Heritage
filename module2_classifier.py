"""
EAIFCH v1.1 — Module 2: Sensitivity Classifier
================================================
Implements the sensitivity score formula from Section 3.3:

    S = 100 × Σᵢ [ wᵢ × (ΣIᵢ / nᵢ) ]

where:
  wᵢ ∈ {0.30, 0.20, 0.20, 0.15, 0.15} is the weight for dimension i
  nᵢ is the number of binary indicators in dimension i
  Iᵢ ∈ {0,1} is indicator j of dimension i

Sensitivity categories (Section 3.3):
  Critical : S ≥ 75
  High     : 50 ≤ S < 75
  Medium   : 25 ≤ S < 50
  Low      : S < 25

Algorithm complexity: O(n) with early-exit conditions.
Green coding: @lru_cache on dimension weights, NumPy vectorisation.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Dict, List, Tuple

import numpy as np


# ---------------------------------------------------------------------------
# Dimension configuration
# ---------------------------------------------------------------------------

DIMENSIONS = {
    "sacredness": {
        "weight": 0.30,
        "indicators": [
            "ceremonial_use",
            "divine_connection",
            "initiation_required",
            "seasonal_restriction",
        ],
    },
    "privacy": {
        "weight": 0.20,
        "indicators": [
            "living_individuals",
            "identifiable_data",
            "family_secrets",
            "medical_info",
        ],
    },
    "commercialization": {
        "weight": 0.20,
        "indicators": [
            "market_demand",
            "digital_marketplace",
            "souvenir_industry",
            "patent_risk",
        ],
    },
    "political": {
        "weight": 0.15,
        "indicators": [
            "contested_ownership",
            "colonial_context",
            "land_dispute",
        ],
    },
    "community_control": {
        "weight": 0.15,
        "indicators": [
            "no_governance_body",
            "diaspora_fragmented",
            "governance_disputed",
        ],
    },
}

# Verify weights sum to 1.0
assert abs(sum(d["weight"] for d in DIMENSIONS.values()) - 1.0) < 1e-9, \
    "Dimension weights must sum to 1.0"


# ---------------------------------------------------------------------------
# Cached helpers (green coding: @lru_cache)
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _get_weight_vector() -> np.ndarray:
    """Returns weight vector [w₁, w₂, w₃, w₄, w₅] as NumPy array."""
    return np.array([d["weight"] for d in DIMENSIONS.values()])


@lru_cache(maxsize=1)
def _get_dimension_sizes() -> np.ndarray:
    """Returns indicator count per dimension as NumPy array."""
    return np.array([len(d["indicators"]) for d in DIMENSIONS.values()])


@lru_cache(maxsize=32)
def _get_dimension_indicators(dimension: str) -> Tuple[str, ...]:
    """Returns tuple of indicator names for a dimension (cached)."""
    return tuple(DIMENSIONS[dimension]["indicators"])


# ---------------------------------------------------------------------------
# Classifier
# ---------------------------------------------------------------------------

class SensitivityClassifier:
    """
    Multi-criteria sensitivity classifier implementing the formula from Section 3.3.

    Produces an explicit reasoning chain auditable by community representatives —
    the key interpretability advantage over logistic regression (Table 4).
    """

    THRESHOLDS = {
        "critical": 75.0,
        "high": 50.0,
        "medium": 25.0,
        "low": 0.0,
    }

    def classify(self,
                 indicators: Dict[str, Dict[str, bool]]) -> Tuple[float, str, List[str], List[str]]:
        """
        Classify a heritage item's sensitivity.

        Args:
            indicators: Dict mapping dimension name → {indicator_name: bool}.
                        Missing indicators default to False (conservative).

        Returns:
            (score, level, flags, reasoning_chain)
        """
        weights = _get_weight_vector()
        sizes = _get_dimension_sizes()

        dim_scores = np.zeros(len(DIMENSIONS))
        flags: List[str] = []
        reasoning: List[str] = []

        for i, (dim_name, dim_cfg) in enumerate(DIMENSIONS.items()):
            dim_indicators = _get_dimension_indicators(dim_name)
            dim_data = indicators.get(dim_name, {})

            # Binary indicator vector — O(nᵢ) per dimension
            triggered = [dim_data.get(ind, False) for ind in dim_indicators]
            count = sum(triggered)

            # Early exit optimisation: if all indicators False, skip division
            if count == 0:
                dim_scores[i] = 0.0
                reasoning.append(f"{dim_name}: 0/{sizes[i]} indicators → 0.00 (weight {dim_cfg['weight']})")
                continue

            # Dimension sub-score: (ΣIᵢ / nᵢ)
            dim_scores[i] = count / sizes[i]

            # Collect flags for triggered indicators
            for j, ind in enumerate(dim_indicators):
                if triggered[j]:
                    flags.append(f"{dim_name}:{ind}")

            reasoning.append(
                f"{dim_name}: {count}/{sizes[i]} indicators "
                f"→ {dim_scores[i]:.3f} × {dim_cfg['weight']} "
                f"= {dim_scores[i] * dim_cfg['weight']:.4f}"
            )

        # S = 100 × Σᵢ [ wᵢ × (ΣIᵢ / nᵢ) ] — NumPy dot product
        score = float(100.0 * np.dot(weights, dim_scores))
        level = self._categorise(score)

        reasoning.append(f"Total S = {score:.2f}/100 → {level.upper()}")
        return score, level, flags, reasoning

    @staticmethod
    def _categorise(score: float) -> str:
        """Apply sensitivity thresholds (Section 3.3)."""
        if score >= 75.0:
            return "critical"
        if score >= 50.0:
            return "high"
        if score >= 25.0:
            return "medium"
        return "low"

    def validate_indicators(self, indicators: Dict[str, Dict[str, bool]]) -> List[str]:
        """Return list of unknown indicator names (for input validation)."""
        unknown = []
        for dim_name, dim_data in indicators.items():
            if dim_name not in DIMENSIONS:
                unknown.append(f"Unknown dimension: {dim_name}")
                continue
            valid = set(_get_dimension_indicators(dim_name))
            for ind in dim_data:
                if ind not in valid:
                    unknown.append(f"Unknown indicator in {dim_name}: {ind}")
        return unknown


# ---------------------------------------------------------------------------
# Standalone demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    clf = SensitivityClassifier()

    # Case 2: Wiradjuri ceremonial site — expected 65.0/100, High
    indicators = {
        "sacredness": {
            "ceremonial_use": True, "divine_connection": True,
            "initiation_required": True, "seasonal_restriction": True,
        },
        "privacy": {
            "living_individuals": False, "identifiable_data": True,
            "family_secrets": False, "medical_info": False,
        },
        "commercialization": {
            "market_demand": False, "digital_marketplace": False,
            "souvenir_industry": False, "patent_risk": False,
        },
        "political": {
            "contested_ownership": True, "colonial_context": True,
            "land_dispute": False,
        },
        "community_control": {
            "no_governance_body": False, "diaspora_fragmented": False,
            "governance_disputed": False,
        },
    }

    score, level, flags, reasoning = clf.classify(indicators)
    print(f"Score: {score:.1f}/100 → {level.upper()}")
    print(f"Flags ({len(flags)}): {flags}")
    print("Reasoning chain:")
    for line in reasoning:
        print(f"  {line}")
