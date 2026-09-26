"""Isolated agentic orchestration layer for GPT↔ELO knowledge access.

This package is deliberately outside the canonical ELO core contracts. It may
orchestrate existing ELO capabilities, but it does not own canonical truth,
identity, Soul, Core, Forge, promotion, or persistence authority.
"""

from .ai_entry_runtime import ELOAICognitiveHandoff, ELOAICognitiveHandoffError, ELOAIEntryRuntime
from .entry_contract import (
    DEFAULT_BOOTSTRAP_ARTIFACTS,
    ELOAIEntryBlock,
    ELOAIEntryError,
    ELOAIEntryGate,
    ELOAIEntryMode,
    ELOAIEntryRequest,
    ELOAIEntrySession,
    ELOAIEntryState,
)

__all__ = [
    "DEFAULT_BOOTSTRAP_ARTIFACTS",
    "ELOAICognitiveHandoff",
    "ELOAICognitiveHandoffError",
    "ELOAIEntryBlock",
    "ELOAIEntryError",
    "ELOAIEntryGate",
    "ELOAIEntryMode",
    "ELOAIEntryRequest",
    "ELOAIEntryRuntime",
    "ELOAIEntrySession",
    "ELOAIEntryState",
]
