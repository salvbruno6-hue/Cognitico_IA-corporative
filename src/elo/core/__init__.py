"""Canonical ELO core boundaries."""

from .canonical_identity import CanonicalIdentityRegistry, EloCanonicalIdentity
from .consulting import ConsultingResponse, ConsultingStatus
from .conversation_bridge import ChatBridge, ChatBridgeEvent
from .conversation_intake import ConversationEvent, ConversationIntake, ConversationIntakeResult
from .evolution_memory import EvolutionMemory, EvolutionRecord
from .knowledge_admission import AdmissionRequest, AdmissionResult, KnowledgeAdmission
from .source_discovery import DiscoveryPlan, SourceCandidate, SourceDiscoveryEngine

__all__ = [
    "AdmissionRequest",
    "AdmissionResult",
    "CanonicalIdentityRegistry",
    "ChatBridge",
    "ChatBridgeEvent",
    "ConsultingResponse",
    "ConsultingStatus",
    "ConversationEvent",
    "ConversationIntake",
    "ConversationIntakeResult",
    "DiscoveryPlan",
    "EloCanonicalIdentity",
    "EvolutionMemory",
    "EvolutionRecord",
    "KnowledgeAdmission",
    "SourceCandidate",
    "SourceDiscoveryEngine",
]
