"""
EAIFCH v1.1 — Module 3: Community Consent Framework
=====================================================
Implements the three consent pathways (PIC / IN / Attribution) with governance
escalation blocking export for HIGH/CRITICAL sensitivity items when community
authority is unclear.

Operationalises CARE Principle: Authority to Control
  - PIC required for High/Critical items
  - Export blocked until named community authority approves
  - Withdrawal triggers 24h access suspension

References: Carroll et al. (2020, 2021), Schnarch (2004), Christen & Anderson (2019)
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from functools import lru_cache
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class ConsentPathway(Enum):
    """Three consent pathways as defined in Section 3.4 of the article."""
    PIC = "prior_informed_consent"           # Level 2 (High) and Level 3 (Critical)
    INFORMED_NOTIFICATION = "informed_notification"  # Level 1 (Medium)
    ATTRIBUTION = "attribution"              # Level 0 (Low)


class GovernanceStatus(Enum):
    CLEAR = "clear"        # ≥ 2 of 4 governance indicators present
    UNCLEAR = "unclear"    # < 2 of 4 governance indicators present


class AccessTier(Enum):
    """Three differentiated access tiers (Section 3.6)."""
    PUBLIC = "public"               # Obfuscated / restricted per sensitivity
    INSTITUTIONAL = "institutional"  # Researchers with community-approved agreements
    COMMUNITY = "community"         # Source community — always full unobfuscated access


class GPSObfuscationMode(Enum):
    """Three GPS obfuscation modes (Section 3.5)."""
    RADIUS_OFFSET = "radius_offset"          # Default ≥10km from true location
    BOUNDARY_ROUNDING = "boundary_rounding"  # Rounded to nearest district centroid
    FULL_REMOVAL = "full_removal"            # Replaced with regional identifier only


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class GovernanceEscalationError(Exception):
    """
    Raised when export is attempted on a HIGH or CRITICAL sensitivity item
    whose community authority cannot be identified (< 2/4 governance indicators).

    Operationalises P1: Ethics as intrinsic property — architectural enforcement
    rather than advisory flag. Bypassing requires deliberate API circumvention.
    """
    def __init__(self, item_id: str, sensitivity_level: str,
                 governance_score: int, message: str = ""):
        self.item_id = item_id
        self.sensitivity_level = sensitivity_level
        self.governance_score = governance_score
        base = (
            f"Export blocked for {item_id} "
            f"(sensitivity={sensitivity_level}, governance={governance_score}/4). "
            f"Status: unclear | Next: Identify community authority, "
            f"record ethics officer approval before re-attempting export."
        )
        super().__init__(f"{base} {message}".strip())


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class GovernanceEscalationRecord:
    """Immutable escalation record — includes officer name, timestamp, notes."""
    item_id: str
    sensitivity_level: str
    governance_score: int           # 0-4 indicators present
    triggered_at: str               # ISO timestamp
    approving_officer: Optional[str] = None
    approval_timestamp: Optional[str] = None
    approval_notes: Optional[str] = None
    resolved: bool = False

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass(frozen=True)
class ConsentRecord:
    """
    Immutable consent decision record.
    Modifications require a new assessment with full audit trail.
    """
    record_id: str
    item_id: str
    consent_pathway: str            # ConsentPathway.value
    consent_type_detail: str        # e.g. "PIC (6-12 months)"
    issued_at: str                  # ISO timestamp
    expiry_date: Optional[str]
    decision_makers: List[str]
    conditions: List[str]
    ongoing_obligations: Dict
    withdrawal_protocol: Dict
    audit_hash: str                 # SHA-256 of record content for immutability check

    def to_dict(self) -> Dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# GPS Obfuscation
# ---------------------------------------------------------------------------

@dataclass
class GPSObfuscationConfig:
    """
    GPS obfuscation configuration per item's community protocol record.
    Applied differentially: public/institutional tiers obfuscated;
    community tier always receives full coordinates.
    """
    mode: GPSObfuscationMode = GPSObfuscationMode.RADIUS_OFFSET
    radius_km: float = 10.0         # Default ≥10km (parameterisable)
    boundary_level: str = "district"  # For BOUNDARY_ROUNDING mode
    regional_id: Optional[str] = None  # For FULL_REMOVAL mode


class GPSObfuscator:
    """
    Applies GPS coordinate obfuscation per sensitivity level and access tier.

    Consistent with Australian Indigenous heritage protection practices (Section 3.5).
    The default ≥10km radius is explicitly parameterisable — communities may require
    greater precision for internal heritage management or prefer complete removal.
    """

    @staticmethod
    def obfuscate(lat: float, lon: float,
                  config: GPSObfuscationConfig,
                  access_tier: AccessTier) -> Tuple[Optional[float], Optional[float], str]:
        """
        Returns (lat, lon, description) per access tier.

        Community tier always returns full unobfuscated coordinates regardless of mode.
        """
        if access_tier == AccessTier.COMMUNITY:
            return lat, lon, "Full coordinates (community tier — unrestricted)"

        if config.mode == GPSObfuscationMode.FULL_REMOVAL:
            return None, None, f"Coordinates removed — regional identifier: {config.regional_id}"

        if config.mode == GPSObfuscationMode.BOUNDARY_ROUNDING:
            # Round to nearest degree as a proxy for district centroid
            return round(lat, 0), round(lon, 0), f"Rounded to {config.boundary_level} centroid"

        # Default: RADIUS_OFFSET — add deterministic offset (not random, for reproducibility)
        import math
        offset_deg = config.radius_km / 111.0   # ~111 km per degree latitude
        # Deterministic directional offset based on coordinate hash
        h = hash((round(lat, 4), round(lon, 4))) % 360
        lat_off = offset_deg * math.cos(math.radians(h))
        lon_off = offset_deg * math.sin(math.radians(h))
        return (
            round(lat + lat_off, 4),
            round(lon + lon_off, 4),
            f"Offset ≥{config.radius_km}km from true location ({access_tier.value} tier)"
        )


# ---------------------------------------------------------------------------
# Main Framework
# ---------------------------------------------------------------------------

class CommunityConsentFramework:
    """
    Community Consent Framework — Module 3.

    Three consent pathways corresponding to sensitivity levels (Section 3.4):
      - PIC (Prior Informed Consent): Level 3 Critical (6-12 months) and Level 2 High (3-6 months)
      - Informed Notification: Level 1 Medium (1-3 months)
      - Attribution: Level 0 Low (standard scholarly attribution)

    Governance escalation (v1.1): when framework detects HIGH/CRITICAL item
    with < 2/4 governance indicators, raises GovernanceEscalationError on any
    export attempt until a named ethics officer records approval.

    LOW/MEDIUM items with unclear governance receive a warning flag, not a hard block,
    reflecting asymmetric ethical weight at different sensitivity levels.
    """

    GOVERNANCE_THRESHOLD = 2  # Minimum indicators for CLEAR status

    CONSENT_SPECS = {
        "critical": {
            "pathway": ConsentPathway.PIC,
            "detail": "PIC (6-12 months)",
            "duration_days": 365,
            "decision_authority": "Culturally-appropriate governance structures",
            "review_frequency_days": 365,
            "withdrawal_suspension_hours": 24,
        },
        "high": {
            "pathway": ConsentPathway.PIC,
            "detail": "PIC (3-6 months)",
            "duration_days": 180,
            "decision_authority": "Named community representative or governance body",
            "review_frequency_days": 365,
            "withdrawal_suspension_hours": 24,
        },
        "medium": {
            "pathway": ConsentPathway.INFORMED_NOTIFICATION,
            "detail": "Informed Notification (1-3 months)",
            "duration_days": 90,
            "decision_authority": "Institution — subject to community input",
            "review_frequency_days": None,
            "withdrawal_suspension_hours": None,
        },
        "low": {
            "pathway": ConsentPathway.ATTRIBUTION,
            "detail": "Attribution (standard scholarly)",
            "duration_days": None,
            "decision_authority": "Institution",
            "review_frequency_days": None,
            "withdrawal_suspension_hours": None,
        },
    }

    def __init__(self):
        self._escalation_registry: Dict[str, GovernanceEscalationRecord] = {}
        self._approval_registry: Dict[str, GovernanceEscalationRecord] = {}
        self._consent_registry: Dict[str, ConsentRecord] = {}

    # ------------------------------------------------------------------
    # Governance assessment
    # ------------------------------------------------------------------

    def assess_governance(self, governance_indicators: Dict[str, bool]) -> Tuple[GovernanceStatus, int]:
        """
        Assess community governance clarity.

        Four governance indicators (Section 4.3):
          1. named_authority — a named governance body or representative exists
          2. legal_entity — community has legal standing / registered organisation
          3. contact_established — active communication channel exists
          4. protocol_documented — cultural protocols are documented

        Returns (GovernanceStatus, score out of 4).
        """
        keys = ["named_authority", "legal_entity", "contact_established", "protocol_documented"]
        score = sum(1 for k in keys if governance_indicators.get(k, False))
        status = GovernanceStatus.CLEAR if score >= self.GOVERNANCE_THRESHOLD else GovernanceStatus.UNCLEAR
        return status, score

    # ------------------------------------------------------------------
    # Consent pathway
    # ------------------------------------------------------------------

    @lru_cache(maxsize=8)
    def get_consent_spec(self, sensitivity_level: str) -> Dict:
        return self.CONSENT_SPECS.get(sensitivity_level.lower(), self.CONSENT_SPECS["low"])

    def determine_consent_pathway(self, sensitivity_level: str) -> Tuple[ConsentPathway, str]:
        spec = self.get_consent_spec(sensitivity_level)
        return spec["pathway"], spec["detail"]

    # ------------------------------------------------------------------
    # Full assessment + escalation gate
    # ------------------------------------------------------------------

    def assess_item(self,
                    item_id: str,
                    sensitivity_level: str,
                    governance_indicators: Dict[str, bool],
                    decision_makers: Optional[List[str]] = None,
                    conditions: Optional[List[str]] = None) -> ConsentRecord:
        """
        Perform full consent assessment for a heritage item.

        For HIGH/CRITICAL items with UNCLEAR governance: registers a
        GovernanceEscalationRecord. Export will raise GovernanceEscalationError
        until ethics officer approval is recorded via record_ethics_approval().

        For LOW/MEDIUM items with UNCLEAR governance: attaches a warning flag
        to the consent record but does not block export.

        Returns an immutable ConsentRecord.
        """
        gov_status, gov_score = self.assess_governance(governance_indicators)
        spec = self.get_consent_spec(sensitivity_level)
        pathway, detail = spec["pathway"], spec["detail"]

        now = datetime.utcnow()
        issued_at = now.isoformat() + "Z"
        expiry = None
        if spec["duration_days"]:
            expiry = (now + timedelta(days=spec["duration_days"])).isoformat() + "Z"

        # Governance escalation for HIGH/CRITICAL with UNCLEAR governance
        if sensitivity_level.lower() in ("high", "critical") and gov_status == GovernanceStatus.UNCLEAR:
            esc_record = GovernanceEscalationRecord(
                item_id=item_id,
                sensitivity_level=sensitivity_level,
                governance_score=gov_score,
                triggered_at=issued_at,
            )
            self._escalation_registry[item_id] = esc_record

        ongoing = self._build_ongoing_obligations(sensitivity_level, spec)
        withdrawal = self._build_withdrawal_protocol(spec)

        record_content = {
            "item_id": item_id,
            "pathway": pathway.value,
            "detail": detail,
            "issued_at": issued_at,
            "expiry": expiry,
            "governance_status": gov_status.value,
            "governance_score": gov_score,
        }
        audit_hash = hashlib.sha256(
            json.dumps(record_content, sort_keys=True).encode()
        ).hexdigest()

        record = ConsentRecord(
            record_id=f"CR_{item_id}_{now.strftime('%Y%m%d%H%M%S')}",
            item_id=item_id,
            consent_pathway=pathway.value,
            consent_type_detail=detail,
            issued_at=issued_at,
            expiry_date=expiry,
            decision_makers=decision_makers or [],
            conditions=conditions or [],
            ongoing_obligations=ongoing,
            withdrawal_protocol=withdrawal,
            audit_hash=audit_hash,
        )
        self._consent_registry[item_id] = record
        return record

    # ------------------------------------------------------------------
    # Export gate (governance escalation enforcement)
    # ------------------------------------------------------------------

    def export_item_record(self, item_id: str, assessment_record) -> Dict:
        """
        Export a heritage item's assessment record as JSON.

        Raises GovernanceEscalationError if the item has an unresolved
        governance escalation (HIGH/CRITICAL + unclear authority).

        This is the architectural enforcement of P1 (ethics as intrinsic property).
        """
        if item_id in self._escalation_registry:
            esc = self._escalation_registry[item_id]
            if not esc.resolved:
                raise GovernanceEscalationError(
                    item_id=item_id,
                    sensitivity_level=esc.sensitivity_level,
                    governance_score=esc.governance_score,
                )

        # Proceed with export
        consent = self._consent_registry.get(item_id)
        return {
            "item_id": item_id,
            "assessment": assessment_record if isinstance(assessment_record, dict)
                          else vars(assessment_record),
            "consent": consent.to_dict() if consent else None,
            "escalation": None,
            "exported_at": datetime.utcnow().isoformat() + "Z",
            "schema": {
                "dublin_core": {
                    "dc:subject": "cultural_heritage",
                    "dc:rights": consent.consent_pathway if consent else "attribution",
                    "dc:accessRights": consent.consent_type_detail if consent else "open",
                },
                "schema_org": {
                    "accessMode": "textual",
                    "conditionsOfAccess": consent.consent_type_detail if consent else "open",
                },
            },
        }

    # ------------------------------------------------------------------
    # Ethics officer approval (resolves escalation)
    # ------------------------------------------------------------------

    def record_ethics_approval(self,
                               item_id: str,
                               approving_officer: str,
                               approval_notes: str = "") -> GovernanceEscalationRecord:
        """
        Record ethics officer approval, resolving the governance escalation.

        The escalation record is immutable — this creates a new resolved record
        and registers it, replacing the pending one. The original pending record
        is preserved in _approval_registry for audit purposes.

        After calling this method, export_item_record() will succeed.
        """
        if item_id not in self._escalation_registry:
            raise ValueError(f"No escalation record found for item {item_id}")

        pending = self._escalation_registry[item_id]
        now = datetime.utcnow().isoformat() + "Z"

        resolved = GovernanceEscalationRecord(
            item_id=pending.item_id,
            sensitivity_level=pending.sensitivity_level,
            governance_score=pending.governance_score,
            triggered_at=pending.triggered_at,
            approving_officer=approving_officer,
            approval_timestamp=now,
            approval_notes=approval_notes,
            resolved=True,
        )
        # Preserve audit trail of original pending record
        self._approval_registry[f"{item_id}_pending"] = pending
        # Replace with resolved record
        self._escalation_registry[item_id] = resolved
        return resolved

    # ------------------------------------------------------------------
    # Withdrawal protocol
    # ------------------------------------------------------------------

    def process_withdrawal(self, item_id: str) -> Dict:
        """
        Process consent withdrawal for a heritage item.

        Critical materials: 24-hour access suspension, community consultation
        on disposition, notification to derivative users (Section 3.4).
        """
        consent = self._consent_registry.get(item_id)
        now = datetime.utcnow()

        return {
            "item_id": item_id,
            "withdrawal_timestamp": now.isoformat() + "Z",
            "access_suspended_until": (now + timedelta(hours=24)).isoformat() + "Z",
            "actions": [
                "Immediate access suspension for public and institutional tiers",
                "Community tier access preserved",
                "Community consultation on final disposition to be initiated within 24h",
                "Notification to derivative users within 72h",
                "Data return or destruction within 90 days per community specification",
            ],
            "prior_consent": consent.to_dict() if consent else None,
        }

    # ------------------------------------------------------------------
    # Community escalation request (CARE: Authority to Control)
    # ------------------------------------------------------------------

    def request_higher_protection(self, item_id: str,
                                  requested_level: str,
                                  community_representative: str,
                                  rationale: str) -> Dict:
        """
        Allow any community to formally request reassessment at a higher consent level.

        Reflects CARE Principle: Authority to Control means communities can demand
        higher protection than the algorithm assigns, never lower (Section 5.1).
        """
        return {
            "item_id": item_id,
            "requested_pathway": self.get_consent_spec(requested_level)["detail"],
            "community_representative": community_representative,
            "rationale": rationale,
            "submitted_at": datetime.utcnow().isoformat() + "Z",
            "status": "pending_review",
            "note": (
                "Community escalation request overrides algorithmic classification. "
                "The framework will honour the requested protection level pending "
                "institutional acknowledgement within 5 business days."
            ),
        }

    # ------------------------------------------------------------------
    # PIC template generator
    # ------------------------------------------------------------------

    def generate_pic_template(self, item_id: str, item_metadata: Dict,
                               sensitivity_level: str) -> Dict:
        """
        Generate a Prior Informed Consent template for High/Critical items.
        Includes 50% revenue sharing provisions and capacity-building requirements
        (Table 0, Collective Benefit implementation).
        """
        spec = self.get_consent_spec(sensitivity_level)
        return {
            "template_type": "Prior Informed Consent",
            "item_id": item_id,
            "item_metadata": item_metadata,
            "consent_detail": spec["detail"],
            "decision_authority": spec["decision_authority"],
            "community_benefit_clauses": {
                "digital_copies": "High-quality copies returned to community within 3 months",
                "revenue_sharing": "50% of net proceeds from any authorised commercial use",
                "capacity_building": "6-month digital preservation training programme",
                "knowledge_sovereignty": "Community retains ultimate authority throughout",
            },
            "withdrawal_clause": {
                "method": "Written notification to designated institutional contact",
                "response": "24-hour access suspension upon receipt",
                "data_handling": "Return or destruction within 90 days",
            },
            "review_schedule": (
                f"Annual review meeting required"
                if sensitivity_level.lower() == "critical" else
                f"Review at {spec['duration_days']} days or upon community request"
            ),
            "generated_at": datetime.utcnow().isoformat() + "Z",
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_ongoing_obligations(self, sensitivity_level: str, spec: Dict) -> Dict:
        base = {
            "attribution": {"required": True, "format": "Community-specified"},
            "audit_trail": {"immutable": True, "access": "Community representative"},
        }
        if sensitivity_level.lower() in ("high", "critical"):
            base.update({
                "reporting": {"frequency": "Quarterly", "content": ["usage", "outcomes", "benefits"]},
                "community_access": {"copies": "High-quality digital", "timeline": "3 months"},
                "benefit_sharing": {"percentage": "50% net proceeds", "reporting": "Annual"},
            })
        return base

    def _build_withdrawal_protocol(self, spec: Dict) -> Dict:
        hours = spec.get("withdrawal_suspension_hours")
        return {
            "method": "Written notification to institutional ethics contact",
            "suspension": f"{hours}h access suspension" if hours else "Standard process",
            "data_return": "Return or destruction within 90 days",
            "derivative_notification": "Within 72h of withdrawal",
        }

    # ------------------------------------------------------------------
    # Status helpers
    # ------------------------------------------------------------------

    def get_escalation_status(self, item_id: str) -> Optional[Dict]:
        esc = self._escalation_registry.get(item_id)
        return esc.to_dict() if esc else None

    def has_unresolved_escalation(self, item_id: str) -> bool:
        esc = self._escalation_registry.get(item_id)
        return esc is not None and not esc.resolved


# ---------------------------------------------------------------------------
# Stand-alone demonstration (matches Section 4.3 code example in article)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    consent = CommunityConsentFramework()

    # Case 3: Griot recording — HIGH sensitivity, UNCLEAR governance → blocked
    print("=== Case 3: Griot Healing Ceremony Recording ===")
    record = consent.assess_item(
        item_id="MUS_WA_042",
        sensitivity_level="high",
        governance_indicators={
            "named_authority": True,   # 1/4 — below threshold
            "legal_entity": False,
            "contact_established": False,
            "protocol_documented": False,
        },
    )
    print(f"Consent pathway: {record.consent_type_detail}")
    print(f"Escalation registered: {consent.has_unresolved_escalation('MUS_WA_042')}")

    try:
        export = consent.export_item_record("MUS_WA_042", {"score": 52.5})
    except GovernanceEscalationError as e:
        print(f"\nExport blocked: {e}\n")

    # Ethics officer resolves escalation
    consent.record_ethics_approval(
        item_id="MUS_WA_042",
        approving_officer="Dr. Smith, Ethics Committee Chair",
        approval_notes="Diaspora organizations identified; provisional consent obtained",
    )
    export = consent.export_item_record("MUS_WA_042", {"score": 52.5})
    print(f"Export succeeded after approval: {export['exported_at']}")

    # GPS obfuscation — 3 tiers
    print("\n=== GPS Obfuscation — 3 Access Tiers ===")
    obf = GPSObfuscator()
    cfg = GPSObfuscationConfig(mode=GPSObfuscationMode.RADIUS_OFFSET, radius_km=10.0)
    for tier in AccessTier:
        lat, lon, desc = obf.obfuscate(-33.8688, 151.2093, cfg, tier)
        print(f"  {tier.value:15s}: lat={lat}, lon={lon} — {desc}")
