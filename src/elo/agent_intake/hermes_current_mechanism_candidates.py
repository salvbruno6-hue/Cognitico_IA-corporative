"""Candidate introductions for newly observed Hermes surfaces.

These are ELO-native contracts only. They describe discovery/validation targets
without importing Hermes runtime code or granting any authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

class CandidateState(str, Enum):
    DISCOVERED = "DISCOVERED"
    CANDIDATE_ONLY = "CANDIDATE_ONLY"
    VALIDATED = "VALIDATED"

@dataclass(frozen=True, slots=True)
class HermesMechanismCandidate:
    candidate_id: str
    mechanism: str
    owner: str
    introduction: str
    source_surface: str
    state: CandidateState = CandidateState.CANDIDATE_ONLY
    canonical_mutation: bool = False

CANDIDATES = (
    HermesMechanismCandidate("EXT-CODE-EXEC-HERMES", "programmatic execute_code tool", "ELO Cognitive Execution", "bounded programmatic orchestration behind the existing execution contract", "Hermes Tool Registry"),
    HermesMechanismCandidate("EXT-API-HERMES", "OpenAI-compatible API server", "ELO External Provider Contracts", "provider-neutral API ingress with explicit identity, scope, evidence and authorization boundaries", "Hermes Integration Surface"),
    HermesMechanismCandidate("EXT-ACP-HERMES", "ACP IDE integration", "ELO External Provider Contracts", "editor-facing capability adapter preserving the same cognitive/execution authority", "Hermes Integration Surface"),
    HermesMechanismCandidate("EXT-PLUGIN-CATALOG-HERMES", "curated plugin catalog", "ELO Skills / Capability Registry", "discovery metadata and provenance intake without automatic capability activation", "Hermes Plugin Catalog"),
    HermesMechanismCandidate("EXT-PROMPT-CACHE-HERMES", "cross-session prompt caching", "ELO Model / Tool Routing", "cache-aware routing metadata with no authority or knowledge-state mutation", "Hermes Provider Runtime"),
)

def get_candidate(candidate_id: str) -> HermesMechanismCandidate:
    for candidate in CANDIDATES:
        if candidate.candidate_id == candidate_id:
            return candidate
    raise KeyError(candidate_id)

def validate_candidate_contract(candidate: HermesMechanismCandidate) -> bool:
    return (
        candidate.state == CandidateState.CANDIDATE_ONLY
        and candidate.canonical_mutation is False
        and all(value.strip() for value in (candidate.candidate_id, candidate.mechanism, candidate.owner, candidate.introduction, candidate.source_surface))
    )

__all__ = ["CANDIDATES", "CandidateState", "HermesMechanismCandidate", "get_candidate", "validate_candidate_contract"]