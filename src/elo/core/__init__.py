"""Canonical ELO core boundaries."""

from .canonical_identity import CanonicalIdentityRegistry, EloCanonicalIdentity
from .consulting import ConsultingResponse, ConsultingStatus
from .conversation_bridge import ChatBridge, ChatBridgeEvent
from .conversation_intake import ConversationEvent, ConversationIntake, ConversationIntakeResult
from .context_resolution import ContextEvidence, ContextPack, ContextQuery, ContextResolutionEngine, ContextSource
from .evolution_memory import EvolutionMemory, EvolutionRecord
from .gpt_handoff import GPTDecisionHandoff
from .knowledge_admission import AdmissionRequest, AdmissionResult, KnowledgeAdmission
from .maturity_engine import MATURITY_DIMENSIONS, MaturityAssessment
from .source_discovery import DiscoveryPlan, SourceCandidate, SourceDiscoveryEngine

__all__ = [
    "AdmissionRequest", "AdmissionResult", "CanonicalIdentityRegistry", "ChatBridge",
    "ChatBridgeEvent", "ConsultingResponse", "ConsultingStatus", "ContextEvidence",
    "ContextPack", "ContextQuery", "ContextResolutionEngine", "ContextSource",
    "ConversationEvent", "ConversationIntake", "ConversationIntakeResult", "DiscoveryPlan",
    "EloCanonicalIdentity", "EvolutionMemory", "EvolutionRecord", "GPTDecisionHandoff",
    "KnowledgeAdmission", "MATURITY_DIMENSIONS", "MaturityAssessment", "SourceCandidate",
    "SourceDiscoveryEngine",
]
