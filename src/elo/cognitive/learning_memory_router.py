"""Governed investigation and routing of learning memories.

Simbionte uses this mechanism to investigate related memory, resolve an existing
governed owner, and return a routing decision. It never writes or promotes.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import re
from typing import Iterable

class RouteAction(str, Enum):
    REUSE="REUSE"; AGGREGATE="AGGREGATE"; CANDIDATE="CANDIDATE"; BLOCKED="BLOCKED"; NO_OWNER="NO_OWNER"

@dataclass(frozen=True)
class LearningDestination:
    destination_id:str; owner:str; domain:str; learning_kind:str; location:str; storage:str
    canonical:bool=True; accepts_new_learning:bool=True

@dataclass(frozen=True)
class MemoryEntry:
    memory_id:str; tenant_scope:str; domain:str; learning_kind:str; concept_key:str; source_ref:str; status:str
    destination_id:str|None=None; relation_keys:tuple[str,...]=()

@dataclass(frozen=True)
class LearningRequest:
    learning_id:str; tenant_scope:str; domain:str; learning_kind:str; concept_key:str; source_refs:tuple[str,...]
    relation_keys:tuple[str,...]=(); validated:bool=False

@dataclass(frozen=True)
class RoutingDecision:
    action:RouteAction; destination:LearningDestination|None; related_memory_ids:tuple[str,...]
    duplicate_memory_ids:tuple[str,...]; legacy_evidence_refs:tuple[str,...]; reasons:tuple[str,...]

CANONICAL_DESTINATIONS=(
 LearningDestination("SOLICITATION_LEARNING","ELO Cognitive / Solicitation Learning","ANALISE_SOLICITACOES","learning","memory/solicitations_learning/","git"),
 LearningDestination("BUDGET_LEARNING","ELO Budget Specialist","ORCAMENTO","learning","08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/","git"),
 LearningDestination("BUDGET_CALCULATION_MEMORY","ELO Budget Memory","ORCAMENTO","calculation","elo_orcament_calculation_memory","supabase"),
 LearningDestination("CORPORATE_KNOWLEDGE","ELO Knowledge","CORPORATIVO","learning","04-knowledge-handbook/","git"),
 LearningDestination("EVOLUTION_MEMORY","ELO Cognitive / Evolution Memory","EVOLUTION","experience","memory/evolution/","git"),
 LearningDestination("SPECIALIST_SKILL_CANDIDATE","ELO Forge / Specialist Skill Registry","FORGE","skill","forge/skill-packs/","git"),
)
LEGACY_BUDGET_PATHS=frozenset({"memory/solicitations_learning/","memory/evolution/","04-knowledge-handbook/"})

def _normalize(value:str)->str:
    return re.sub(r"[^a-z0-9]+","-",value.strip().lower()).strip("-")

class LearningMemoryRouter:
    """Read-only Simbionte routing over supplied memory evidence."""

    def __init__(self,destinations:Iterable[LearningDestination]=CANONICAL_DESTINATIONS)->None:
        values=tuple(destinations); ids=[x.destination_id for x in values]
        if len(ids)!=len(set(ids)): raise ValueError("duplicate learning destination id")
        self._destinations=values

    def _destination_for(self,request:LearningRequest):
        if request.domain=="ORCAMENTO" and request.learning_kind=="calculation": key="BUDGET_CALCULATION_MEMORY"
        elif request.domain=="ORCAMENTO": key="BUDGET_LEARNING"
        elif request.domain=="ANALISE_SOLICITACOES": key="SOLICITATION_LEARNING"
        elif request.domain=="CORPORATIVO": key="CORPORATE_KNOWLEDGE"
        elif request.domain=="EVOLUTION" and request.learning_kind=="experience": key="EVOLUTION_MEMORY"
        elif request.domain=="FORGE" and request.learning_kind=="skill": key="SPECIALIST_SKILL_CANDIDATE"
        else: return None
        return next((x for x in self._destinations if x.destination_id==key),None)

    def investigate(self,request:LearningRequest,memories:Iterable[MemoryEntry])->RoutingDecision:
        if not request.learning_id or not request.tenant_scope or not request.concept_key:
            return RoutingDecision(RouteAction.BLOCKED,None,(),(),(),("required_identity_missing",))
        destination=self._destination_for(request)
        if destination is None:
            return RoutingDecision(RouteAction.NO_OWNER,None,(),(),(),("no_governed_owner_resolved",))
        concept=_normalize(request.concept_key); rel={_normalize(x) for x in request.relation_keys}
        related=[]; duplicates=[]; legacy=[]
        for memory in memories:
            if memory.tenant_scope!=request.tenant_scope: continue
            if memory.destination_id==destination.destination_id:
                if _normalize(memory.concept_key)==concept: duplicates.append(memory)
                elif rel.intersection(_normalize(x) for x in memory.relation_keys): related.append(memory)
            elif memory.domain==request.domain and _normalize(memory.concept_key)==concept: related.append(memory)
            if request.domain=="ORCAMENTO" and memory.source_ref in LEGACY_BUDGET_PATHS: legacy.append(memory.source_ref)
        dup_ids=tuple(dict.fromkeys(x.memory_id for x in duplicates))
        rel_ids=tuple(dict.fromkeys(x.memory_id for x in related if x.memory_id not in dup_ids))
        legacy_refs=tuple(dict.fromkeys(legacy))
        if dup_ids:
            return RoutingDecision(RouteAction.REUSE,destination,rel_ids,dup_ids,legacy_refs,("existing_canonical_memory_matches_concept",))
        if not request.validated:
            return RoutingDecision(RouteAction.CANDIDATE,destination,rel_ids,(),legacy_refs,("owner_resolved_but_learning_not_validated",))
        return RoutingDecision(RouteAction.AGGREGATE if rel_ids else RouteAction.CANDIDATE,destination,rel_ids,(),legacy_refs,("validated_learning_routes_to_existing_owner",))
