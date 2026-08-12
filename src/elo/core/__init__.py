"""Canonical ELO core boundaries."""

from .canonical_identity import CanonicalIdentityRegistry, EloCanonicalIdentity
from .evolution_memory import EvolutionMemory, EvolutionRecord
from .knowledge_admission import AdmissionRequest, AdmissionResult, KnowledgeAdmission

__all__ = [
    "AdmissionRequest",
    "AdmissionResult",
    "CanonicalIdentityRegistry",
    "EloCanonicalIdentity",
    "EvolutionMemory",
    "EvolutionRecord",
    "KnowledgeAdmission",
]
