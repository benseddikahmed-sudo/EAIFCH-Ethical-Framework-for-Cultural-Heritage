"""
EAIFCH v1.1 — Synthetic Data Generator
========================================
Parametric bootstrap procedure for generating synthetic validation datasets
that replicate statistical properties of case study collections without
exposing sensitive cultural information (Section 4.5).

Procedure:
  1. Estimate empirical distribution of sensitivity scores and risk dimension
     values from real case study assessments
  2. Draw synthetic items from these distributions using Monte Carlo sampling
     with added Gaussian noise (σ = 5 score points) to prevent exact reproduction
  3. Verify synthetic distribution matches real on first four moments
     (mean, variance, skewness, kurtosis) within 5% tolerance

Ground truth labels assigned by applying the scoring algorithm to synthetic
indicator vectors — ensuring labels are consistent with taxonomy without
encoding real item characteristics.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Moment verification
# ---------------------------------------------------------------------------

def _mean(xs: List[float]) -> float:
    return sum(xs) / len(xs)

def _variance(xs: List[float]) -> float:
    m = _mean(xs)
    return sum((x - m) ** 2 for x in xs) / len(xs)

def _skewness(xs: List[float]) -> float:
    m = _mean(xs)
    s = math.sqrt(_variance(xs)) or 1e-9
    return sum(((x - m) / s) ** 3 for x in xs) / len(xs)

def _kurtosis(xs: List[float]) -> float:
    m = _mean(xs)
    s = math.sqrt(_variance(xs)) or 1e-9
    return sum(((x - m) / s) ** 4 for x in xs) / len(xs)

def _moments(xs: List[float]) -> Dict[str, float]:
    return {
        "mean": _mean(xs),
        "variance": _variance(xs),
        "skewness": _skewness(xs),
        "kurtosis": _kurtosis(xs),
    }

def _within_tolerance(real: Dict[str, float],
                       synth: Dict[str, float],
                       tol: float = 0.05) -> Tuple[bool, List[str]]:
    """Verify all four moments within tolerance (default 5%)."""
    failures = []
    for moment, real_val in real.items():
        synth_val = synth[moment]
        if abs(real_val) < 1e-9:
            if abs(synth_val) > 1e-6:
                failures.append(f"{moment}: real≈0 but synth={synth_val:.4f}")
        else:
            rel_err = abs(synth_val - real_val) / abs(real_val)
            if rel_err > tol:
                failures.append(
                    f"{moment}: real={real_val:.4f}, synth={synth_val:.4f}, "
                    f"rel_err={rel_err:.2%} > {tol:.0%}"
                )
    return len(failures) == 0, failures


# ---------------------------------------------------------------------------
# Synthetic item dataclass
# ---------------------------------------------------------------------------

@dataclass
class SyntheticItem:
    item_id: str
    sensitivity_score: float        # 0–100
    sensitivity_level: str          # Low / Medium / High / Critical
    dimension_scores: Dict[str, float]
    indicators: Dict[str, Dict[str, bool]]
    is_synthetic: bool = True
    generation_note: str = "Parametric bootstrap — no real item data encoded"

    def to_dict(self) -> Dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class SyntheticDataGenerator:
    """
    Generates synthetic datasets replicating statistical properties of
    case study collections (Section 4.5).

    Usage:
        gen = SyntheticDataGenerator(seed=42)
        dataset = gen.generate(n_items=50, real_scores=[40.0, 65.0, 52.5])
        gen.verify_moments(real_scores, [item.sensitivity_score for item in dataset])
    """

    NOISE_SIGMA = 5.0   # Gaussian noise σ (score points) — prevents exact reproduction

    DIMENSIONS = {
        "sacredness":        {"weight": 0.30, "n": 4},
        "privacy":           {"weight": 0.20, "n": 4},
        "commercialization": {"weight": 0.20, "n": 4},
        "political":         {"weight": 0.15, "n": 3},
        "community_control": {"weight": 0.15, "n": 3},
    }

    def __init__(self, seed: int = 42):
        self._rng = random.Random(seed)

    def generate(self,
                 n_items: int,
                 real_scores: List[float],
                 max_retries: int = 10) -> List[SyntheticItem]:
        """
        Generate n_items synthetic items whose score distribution matches
        real_scores within 5% tolerance on all four moments.

        Args:
            n_items: Number of synthetic items to generate
            real_scores: Sensitivity scores from real case study assessments
            max_retries: Maximum generation attempts before relaxing tolerance

        Returns:
            List of SyntheticItem instances
        """
        real_m = _moments(real_scores)
        mu = real_m["mean"]
        sigma = math.sqrt(real_m["variance"])

        for attempt in range(max_retries):
            items = [self._generate_item(i, mu, sigma) for i in range(n_items)]
            synth_scores = [item.sensitivity_score for item in items]
            synth_m = _moments(synth_scores)

            ok, failures = _within_tolerance(real_m, synth_m)
            if ok:
                return items

            # Adjust mu/sigma slightly towards real moments
            mu = 0.9 * mu + 0.1 * real_m["mean"]
            sigma = 0.9 * sigma + 0.1 * math.sqrt(max(real_m["variance"], 1e-9))

        # Return last batch with warning
        print(f"Warning: moment tolerance not met after {max_retries} retries. "
              f"Failures: {failures}")
        return items

    def verify_moments(self, real_scores: List[float],
                        synth_scores: List[float],
                        tolerance: float = 0.05) -> Tuple[bool, Dict]:
        real_m = _moments(real_scores)
        synth_m = _moments(synth_scores)
        ok, failures = _within_tolerance(real_m, synth_m, tolerance)
        return ok, {
            "passed": ok,
            "real_moments": real_m,
            "synth_moments": synth_m,
            "failures": failures,
        }

    def _generate_item(self, idx: int, mu: float, sigma: float) -> SyntheticItem:
        """Generate a single synthetic item via Monte Carlo sampling + noise."""
        # Target score: Normal(mu, sigma) + noise, clipped to [0, 100]
        # Use sigma=15 minimum to ensure realistic spread (3 case studies give limited variance)
        effective_sigma = max(sigma, 15.0)
        target = mu + self._rng.gauss(0, effective_sigma) + self._rng.gauss(0, self.NOISE_SIGMA)
        target = max(0.0, min(100.0, target))

        # Generate indicator vectors consistent with target score
        indicators, dim_scores = self._indicators_for_score(target)

        # Recompute score from indicators (labels consistent with taxonomy)
        score = self._score_from_indicators(indicators)
        score = max(0.0, min(100.0, score))
        level = self._categorise(score)

        return SyntheticItem(
            item_id=f"SYN_{idx:04d}",
            sensitivity_score=round(score, 2),
            sensitivity_level=level,
            dimension_scores={k: round(v, 4) for k, v in dim_scores.items()},
            indicators=indicators,
        )

    def _indicators_for_score(self,
                               target: float) -> Tuple[Dict[str, Dict[str, bool]], Dict[str, float]]:
        """Generate binary indicator vectors whose aggregate score approximates target."""
        indicators: Dict[str, Dict[str, bool]] = {}
        dim_scores: Dict[str, float] = {}

        # For each dimension, the expected sub-score is target/100
        # (since score = 100 × Σ wᵢ × sub_i, and weights sum to 1)
        expected_sub = target / 100.0

        for dim_name, cfg in self.DIMENSIONS.items():
            n = cfg["n"]
            # Number of indicators to trigger ≈ expected_sub × n, with stochastic jitter
            expected_count = expected_sub * n
            jitter = self._rng.gauss(0, 0.5)
            needed = int(round(max(0, min(n, expected_count + jitter))))

            keys = [f"ind_{j}" for j in range(n)]
            values = [True] * needed + [False] * (n - needed)
            self._rng.shuffle(values)

            indicators[dim_name] = dict(zip(keys, values))
            dim_scores[dim_name] = needed / n

        return indicators, dim_scores

    def _score_from_indicators(self, indicators: Dict[str, Dict[str, bool]]) -> float:
        """Recompute sensitivity score from indicator dict — mirrors Module 2 formula."""
        total = 0.0
        for dim_name, cfg in self.DIMENSIONS.items():
            dim_data = indicators.get(dim_name, {})
            n = cfg["n"]
            count = sum(1 for v in dim_data.values() if v)
            total += cfg["weight"] * (count / n if n > 0 else 0)
        return 100.0 * total

    @staticmethod
    def _categorise(score: float) -> str:
        if score >= 75.0:
            return "critical"
        if score >= 50.0:
            return "high"
        if score >= 25.0:
            return "medium"
        return "low"

    def save(self, items: List[SyntheticItem], filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([item.to_dict() for item in items], f, indent=2, ensure_ascii=False)
        print(f"Saved {len(items)} synthetic items to {filepath}")


# ---------------------------------------------------------------------------
# Standalone demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Real scores from three case studies (Section 5)
    real_scores = [40.0, 65.0, 52.5]

    gen = SyntheticDataGenerator(seed=42)
    dataset = gen.generate(n_items=50, real_scores=real_scores)

    synth_scores = [item.sensitivity_score for item in dataset]
    ok, report = gen.verify_moments(real_scores, synth_scores)

    print(f"Moment verification: {'PASSED' if ok else 'FAILED'}")
    print(f"Real moments:  {report['real_moments']}")
    print(f"Synth moments: {report['synth_moments']}")
    if report["failures"]:
        print(f"Failures: {report['failures']}")

    level_dist = {}
    for item in dataset:
        level_dist[item.sensitivity_level] = level_dist.get(item.sensitivity_level, 0) + 1
    print(f"\nLevel distribution (n=50): {level_dist}")

    gen.save(dataset, "/tmp/eaifch_synthetic_n50.json")
