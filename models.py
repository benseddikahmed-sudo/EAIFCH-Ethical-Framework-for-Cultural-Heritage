"""
EAIFCH v1.1 — Core Data Structures
====================================
AssessmentRecord is the central immutable dataclass aggregating all module outputs
for a single heritage item.

Three critical properties (Section 4.2):
  1. Immutability after validation — modifications require new assessment with audit trail
  2. Dual JSON/PDF serialisation
  3. Verbatim cultural metadata preservation alongside computed scores

Metadata mappings:
  - Dublin Core: dc:subject, dc:rights, dc:accessRights
  - Schema.org CreativeWork: accessMode, conditionsOfAccess
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class SensitivityResult:
    score: float                    # 0–100
    level: str                      # Low / Medium / High / Critical
    flags: List[str]
    reasoning_chain: List[str]      # Explicit, community-auditable


@dataclass(frozen=True)
class ConsentResult:
    pathway: str                    # prior_informed_consent / informed_notification / attribution
    detail: str                     # e.g. "PIC (6-12 months)"
    governance_status: str          # clear / unclear
    governance_score: int           # 0–4
    escalation_triggered: bool


@dataclass(frozen=True)
class RiskResult:
    overall_score: float
    risk_category: str
    dimensional_scores: Dict[str, float]
    mitigation_plan: List[Dict]


@dataclass(frozen=True)
class GreenResult:
    duration_ms: float
    energy_wh: float
    co2_grams: float


@dataclass(frozen=True)
class AssessmentRecord:
    """
    Immutable aggregate output for a single heritage item.

    Produced by the EAIFCH pipeline after all six modules have run.
    Modifications require a new assessment with full audit trail.
    """
    # Identity
    item_id: str
    assessment_id: str
    assessed_at: str                # ISO timestamp

    # Module outputs
    sensitivity: SensitivityResult
    consent: ConsentResult
    risk: RiskResult
    green: GreenResult

    # Verbatim cultural metadata (preserved without quantification loss)
    cultural_metadata: Dict[str, Any]

    # Integrity
    audit_hash: str                 # SHA-256 of record content

    # Dublin Core mappings
    dc_subject: str = "cultural_heritage"
    dc_rights: str = ""
    dc_access_rights: str = ""

    # Schema.org mappings
    schema_access_mode: str = "textual"
    schema_conditions_of_access: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def to_pdf_metadata(self) -> Dict:
        """Returns a flat dict suitable for PDF metadata embedding."""
        return {
            "Title": f"EAIFCH Assessment — {self.item_id}",
            "Author": "EAIFCH v1.1",
            "Subject": self.dc_subject,
            "Keywords": f"{self.sensitivity.level}, {self.consent.pathway}",
            "Rights": self.dc_rights,
            "AccessRights": self.dc_access_rights,
            "AssessmentID": self.assessment_id,
            "AssessedAt": self.assessed_at,
            "AuditHash": self.audit_hash,
        }

    @classmethod
    def build(cls,
              item_id: str,
              sensitivity: SensitivityResult,
              consent: ConsentResult,
              risk: RiskResult,
              green: GreenResult,
              cultural_metadata: Dict[str, Any]) -> "AssessmentRecord":
        """
        Factory method — computes assessment_id, timestamp, and audit hash.
        The resulting record is frozen (immutable).
        """
        now = datetime.utcnow()
        assessed_at = now.isoformat() + "Z"
        assessment_id = f"EAIFCH_{item_id}_{now.strftime('%Y%m%d%H%M%S')}"

        # Dublin Core
        dc_rights = consent.pathway
        dc_access_rights = consent.detail

        # Schema.org
        schema_conditions = consent.detail

        # Audit hash over deterministic content
        hash_content = json.dumps({
            "item_id": item_id,
            "assessed_at": assessed_at,
            "sensitivity_score": sensitivity.score,
            "sensitivity_level": sensitivity.level,
            "consent_pathway": consent.pathway,
            "governance_status": consent.governance_status,
        }, sort_keys=True)
        audit_hash = hashlib.sha256(hash_content.encode()).hexdigest()

        return cls(
            item_id=item_id,
            assessment_id=assessment_id,
            assessed_at=assessed_at,
            sensitivity=sensitivity,
            consent=consent,
            risk=risk,
            green=green,
            cultural_metadata=cultural_metadata,
            audit_hash=audit_hash,
            dc_subject="cultural_heritage",
            dc_rights=dc_rights,
            dc_access_rights=dc_access_rights,
            schema_access_mode="textual",
            schema_conditions_of_access=schema_conditions,
        )
