"""Consolidation contract for the Hermes checkpoint candidate family.

The pre-compress durability guard is a refinement of the existing checkpoint
capability, not a second ELO authority.
"""
from __future__ import annotations
from dataclasses import dataclass

CAPABILITY_ID = "EXT-CHECKPOINT-HERMES"
REFINEMENT_ID = "EXT-CHECKPOINT-HERMES-PRECOMPRESS"
OWNER = "ELO State Recovery"

@dataclass(frozen=True, slots=True)
class CheckpointFamily:
    capability_id: str
    refinement_id: str
    owner: str
    same_authority: bool
    canonical_mutation_permitted: bool

def checkpoint_family() -> CheckpointFamily:
    return CheckpointFamily(CAPABILITY_ID, REFINEMENT_ID, OWNER, True, False)