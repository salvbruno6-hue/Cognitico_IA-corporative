"""Canonical ELO core boundaries."""

from .canonical_identity import CanonicalIdentityRegistry, EloCanonicalIdentity
from .conversation_intake import ConversationEvent, ConversationIntake, ConversationIntakeResult
from .evolution_memory import EvolutionMemory, EvolutionRecord
from .knowledge_admission import AdmissionRequest, AdmissionResult, KnowledgeAdmission

__all__ = [
    "AdmissionRequest",
    "AdmissionResult",
    "CanonicalIdentityRegistry",
    "ConversationEvent",
    "ConversationIntake",
    "ConversationIntakeResult",
    "EloCanonicalIdentity",
    "EvolutionMemory",
    "EvolutionRecord",
    "KnowledgeAdmission",
]
