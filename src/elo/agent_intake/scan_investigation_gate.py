"""Investigation-first gate for ELO scan missions.

Deterministic and provider-neutral. It validates an explicit objective,
scope, criteria, bounded hypotheses and cross-domain relationship plan before
source inspection. It never infers causality or promotes learning.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping

CONCEPT_OUTCOMES=("SUPPORTED","PARTIALLY_SUPPORTED","UNRESOLVED","CONTRADICTED","INSUFFICIENT_EVIDENCE")
ACTIONS=("INVESTIGATE","BLOCKED","EVOLUTION_GATE","ESCALATE")

@dataclass(frozen=True, slots=True)
class InvestigationGateResult:
    status:str
    action:str
    objective:str
    scope:tuple[str,...]
    success_criteria:tuple[str,...]
    hypotheses:tuple[dict[str,Any],...]
    relevant_source_domains:tuple[str,...]
    relation_plan:tuple[dict[str,Any],...]
    evidence_requirements:tuple[str,...]
    concept_outcome:str
    evidence:tuple[dict[str,Any],...]
    learning_candidate:dict[str,Any]

def _items(values:Any)->tuple[str,...]:
    if values is None: return ()
    if isinstance(values,str): values=(values,)
    return tuple(str(v).strip() for v in values if str(v).strip())

def _hypotheses(values:Any)->tuple[dict[str,Any],...]:
    if not isinstance(values,(list,tuple)): return ()
    out=[]
    for item in values:
        if not isinstance(item,Mapping): continue
        statement=str(item.get("statement","")).strip()
        if not statement: continue
        p=item.get("probability")
        try: p=None if p is None else float(p)
        except (TypeError,ValueError): p=None
        out.append({"id":str(item.get("id",f"H{len(out)+1}")).strip(),"statement":statement,"probability":p})
    return tuple(out)

_RELATIONS={
 "planejamento_demanda":("planejamento_pcp","producao_fluxo_modular","compras","rh"),
 "compras":("produtos","gestao"),
 "produtos":("producao_fluxo_modular","compras"),
 "producao_fluxo_modular":("planejamento_pcp","produtos","qualidade"),
 "planejamento_pcp":("producao_fluxo_modular","produtos","rh"),
 "orcamento":("compras","produtos","rh","planejamento_pcp"),
}

def _plan(domains:tuple[str,...])->tuple[dict[str,Any],...]:
    out=[]
    for source in domains:
        for target in _RELATIONS.get(source,()):
            if target in domains:
                out.append({"from_domain":source,"to_domain":target,"relationship_status":"investigate","causality_established":False})
    return tuple(out)

def build_investigation_gate(request:Mapping[str,Any])->InvestigationGateResult:
    objective=str(request.get("objective","")).strip()
    scope=_items(request.get("scope")); criteria=_items(request.get("success_criteria"))
    expected=str(request.get("expected_output","")).strip()
    domains=_items(request.get("relevant_source_domains")); hypotheses=_hypotheses(request.get("hypotheses"))
    prohibited=_items(request.get("prohibited_actions"))
    evidence_req=_items(request.get("evidence_requirements")) or ("source provenance","relationship evidence","observed result or outcome","coherence check")
    missing=[k for k,v in (("objective",objective),("scope",scope),("success_criteria",criteria),("expected_output",expected),("relevant_source_domains",domains),("hypotheses",hypotheses)) if not v]
    cross=len(domains)>1
    plan=_plan(domains) if cross else ()
    evidence=({"gate":"investigation-first","missing":tuple(missing)},{"cross_domain":cross,"relation_plan_required":cross},{"prohibited_actions":prohibited})
    if missing or (cross and not plan):
        return InvestigationGateResult("blocked","BLOCKED",objective,scope,criteria,hypotheses,domains,plan,evidence_req,"INSUFFICIENT_EVIDENCE",evidence,{"promotion_state":"candidate_only","canonical_mutation":False})
    return InvestigationGateResult("ready","INVESTIGATE",objective,scope,criteria,hypotheses,domains,plan,evidence_req,"UNRESOLVED",evidence+({"expected_output":expected},),{"promotion_state":"candidate_only","canonical_mutation":False})

def classify_concept(*,evidence_count:int,coherent:bool|None,contradicted:bool=False)->str:
    if evidence_count<=0: return "INSUFFICIENT_EVIDENCE"
    if contradicted: return "CONTRADICTED"
    if coherent is True: return "SUPPORTED"
    if coherent is False: return "PARTIALLY_SUPPORTED"
    return "UNRESOLVED"

__all__=["ACTIONS","CONCEPT_OUTCOMES","InvestigationGateResult","build_investigation_gate","classify_concept"]
