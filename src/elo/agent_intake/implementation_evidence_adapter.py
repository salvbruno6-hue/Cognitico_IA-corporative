"""Adapter from governed candidate measurements to implementation-loop evidence.

This module only translates existing evaluation output into the immutable
ImplementationEvidence contract. It does not invent provenance, promote a
candidate, execute a candidate, or mutate canonical ELO state.
"""
from __future__ import annotations

from typing import Mapping

from .hermes_current_extensions import CandidateMeasurement, HermesCandidate
from .implementation_loop_evidence import ImplementationEvidence


def measurement_to_implementation_evidence(
    candidate: HermesCandidate,
    measurement: CandidateMeasurement,
    *,
    metric_directions: Mapping[str, str],
    provenance_refs: tuple[str, ...],
    boundary_integrity: bool,
) -> ImplementationEvidence:
    """Translate an existing candidate measurement into the loop evidence package.

    Provenance is mandatory and must be supplied by the caller from real
    evaluation evidence; this adapter never fabricates source references.
    """
    if measurement.candidate_id != candidate.candidate_id:
        raise ValueError("candidate and measurement identifiers do not match")

    return ImplementationEvidence(
        candidate_id=candidate.candidate_id,
        owner=candidate.owner,
        baseline=measurement.baseline,
        adapted=measurement.adapted,
        metric_directions=metric_directions,
        regressions=measurement.regressions,
        repeatable=measurement.repeatable,
        provenance_refs=provenance_refs,
        boundary_integrity=boundary_integrity,
        decision=measurement.result,
    )


__all__ = ["measurement_to_implementation_evidence"]
