"""Operational PCP evidence package.

This module only composes domain evidence already supplied by PCP mappings.
It does not query Supabase, infer causes, learn, persist, or mutate canon.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .pcp_confrontation import PCPConfrontation
from .pcp_integrated_diagnosis import PCPDiagnostic, diagnose_confrontations


@dataclass(frozen=True)
class PCPOperationalEvidencePackage:
    confrontations: tuple[PCPConfrontation, ...]
    diagnosis: PCPDiagnostic
    evidence_ids: tuple[str, ...]
    source_kind: str
    source_ref: str | None


def build_operational_evidence_package(
    confrontations: Sequence[PCPConfrontation],
    *,
    source_kind: str,
    source_ref: str | None = None,
) -> PCPOperationalEvidencePackage:
    items = tuple(confrontations)
    diagnosis = diagnose_confrontations(items)
    evidence_ids = tuple(
        dict.fromkeys(
            evidence_id
            for item in items
            for evidence_id in item.evidence_ids
        )
    )
    return PCPOperationalEvidencePackage(
        confrontations=items,
        diagnosis=diagnosis,
        evidence_ids=evidence_ids,
        source_kind=source_kind,
        source_ref=source_ref,
    )
