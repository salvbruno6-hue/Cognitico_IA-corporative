""""Investigation-first gate for ELO scan missions.

The gate validates an explicit objective before interpretation and requires a
known relationship route for cross-domain investigations. It never infers
causality or promotes learning.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
from .relationship_investigator import investigate_relationships

CONCEPT_OUTCOMES=("SUPPORTED","PARTIALLY_SUPPORTED","UNRESOLVED","CONTRADICTED","INSUFFICIENT_EVIDENCE")
ACTIONS=("INVESTIGATE","BLOCKED","EVOLUTION_GATE","ESCALATE")
# These are governed structural domain adjacencies, not causal conclusions.
KNOWN_DOMAIN_RELATIONS={
    frozenset(("planejamento_demanda","planejamento_pcp")),
    frozenset(("planejamento_pcp","producao_fluxo_modular")),
    frozenset(("producao_fluxo_modular","compras")),
    frozenset(("compras","fornecedores")),
    frozenset(("fornecedores","compras")),
    frozenset(("compras","almoxarifado")),
    frozenset(("almoxarifado","producao_fluxo_modular")),
    frozenset(("planejamento_pcp","rh")),
    frozenset(("orcamento","compras")),
    frozenset(("orcamento","planejamento_pcp")),
}

@dataclass(frozen=True,slots=True)
class InvestigationGateResult:
    status:str; action:str; objective:str; scope:tuple[str,...]; success_criteria:tuple[str,...]
    hypotheses:tuple[dict[str,Any],...]; relevant_source_domains:tuple[str,...]
    relation_plan:tuple[dict[str,Any],...]; evidence_requirements:tuple[str,...]
    concept_outcome:str; evidence:tuple[dict[str,Any],...]; learning_candidate:dict[str,Any]

def _items(values:Any)->tuple[str,...]:
    if values is None:return ()
    if isinstance(values,str):values=(values,)
    return tuple(str(v).strip() for v in values if str(v).strip())

def _hypotheses(values:Any)->tuple[dict[str,Any],...]:
    if not isinstance(values,(list,tuple)):return ()
    out=[]
    for item in values:
        if not isinstance(item,Mapping):continue
        statement=str(item.get("statement","")).strip()
        if not statement:continue
        p=item.get("probability")
        try:p=None if p is None else float(p)
        except (TypeError,ValueError):p=None
        out.append({"id":str(item.get("id",f"H{len(out)+1}")).strip(),"statement":statement,"probability":p})
    return tuple(out)

def _plan(domains:tuple[str,...],edges:tuple[Mapping[str,Any],...])->tuple[dict[str,Any],...]:
    if edges:
        return tuple({"from":str(e.get("source","")),"to":str(e.get("target","")),
                      "relation_type":str(e.get("relation_type","structural")),
                      "provenance":str(e.get("provenance","")),"relationship_status":"resolved_edge",
                      "causality_established":False} for e in edges if e.get("source") and e.get("target"))
    if len(domains)<=1:return ()
    return tuple({"from_domain":s,"to_domain":t,"relationship_status":"investigate",
                  "causality_established":False} for s in domains for t in domains
                 if s!=t and frozenset((s,t)) in KNOWN_DOMAIN_RELATIONS)

def build_investigation_gate(request:Mapping[str,Any])->InvestigationGateResult:
    objective=str(request.get("objective","")).strip(); scope=_items(request.get("scope"))
    criteria=_items(request.get("success_criteria")); expected=str(request.get("expected_output","")).strip()
    domains=_items(request.get("relevant_source_domains")); hypotheses=_hypotheses(request.get("hypotheses"))
    prohibited=_items(request.get("prohibited_actions"))
    evidence_req=_items(request.get("evidence_requirements")) or ("source provenance","relationship evidence","observed result or outcome","coherence check")
    records=tuple(request.get("records",())) if isinstance(request.get("records",()),(list,tuple)) else ()
    edges=tuple(request.get("relationship_edges",())) if isinstance(request.get("relationship_edges",()),(list,tuple)) else ()
    missing=[k for k,v in (("objective",objective),("scope",scope),("success_criteria",criteria),("expected_output",expected),("relevant_source_domains",domains),("hypotheses",hypotheses)) if not v]
    cross=len(domains)>1; plan=_plan(domains,edges)
    relation_result=investigate_relationships(records,edges,tenant_scope=str(request.get("tenant_scope",""))) if records and edges else None
    evidence=({"gate":"investigation-first","missing":tuple(missing)},{"cross_domain":cross,"relation_plan_required":cross},{"prohibited_actions":prohibited})
    if relation_result is not None:
        evidence+=({"resolved_paths":len(relation_result.paths),"evidence_gaps":relation_result.evidence_gaps,"causality_established":relation_result.causality_established},)
    if missing or (cross and not plan):
        return InvestigationGateResult("blocked","BLOCKED",objective,scope,criteria,hypotheses,domains,plan,evidence_req,"INSUFFICIENT_EVIDENCE",evidence,{"promotion_state":"candidate_only","canonical_mutation":False})
    return InvestigationGateResult("ready","INVESTIGATE",objective,scope,criteria,hypotheses,domains,plan,evidence_req,"UNRESOLVED",evidence+(({"expected_output":expected},)),{"promotion_state":"candidate_only","canonical_mutation":False})

def classify_concept(*,evidence_count:int,coherent:bool|None,contradicted:bool=False)->str:
    if evidence_count<=0:return "INSUFFICIENT_EVIDENCE"
    if contradicted:return "CONTRADICTED"
    if coherent is True:return "SUPPORTED"
    if coherent is False:return "PARTIALLY_SUPPORTED"
    return "UNRESOLVED"
__all__=["ACTIONS","CONCEPT_OUTCOMES","InvestigationGateResult","build_investigation_gate","classify_concept"]