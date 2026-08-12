"""Canonical ELO core boundaries."""

from .canonical_identity import CanonicalIdentityRegistry, EloCanonicalIdentity
from .consulting import ConsultingResponse, ConsultingStatus
from .conversation_intake import ConversationEvent, ConversationIntake, ConversationIntakeResult
from .evolution_memory import EvolutionMemory, EvolutionRecord
from .knowledge_admission import AdmissionRequest, AdmissionResult, KnowledgeAdmission

__all__ = [
    "AdmissionRequest",
    "AdmissionResult",
    "CanonicalIdentityRegistry",
    "ConsultingResponse",
    "ConsultingStatus",
    "ConversationEvent",
    "ConversationIntake",
    "ConversationIntakeResult",
    "EloCanonicalIdentity",
    "EvolutionMemory",
    "EvolutionRecord",
    "KnowledgeAdmission",
]
