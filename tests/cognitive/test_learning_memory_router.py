from elo.cognitive.learning_memory_router import LearningMemoryRouter,LearningRequest,MemoryEntry,RouteAction

def req(**kw):
    d=dict(learning_id="L-1",tenant_scope="multiteiner",domain="ORCAMENTO",learning_kind="learning",concept_key="PTS tecnica maturidade",source_refs=("SO-155.26",))
    d.update(kw); return LearningRequest(**d)

def test_budget_uses_canonical_owner_and_keeps_legacy_as_evidence():
    r=LearningMemoryRouter().investigate(req(),[MemoryEntry("m1","multiteiner","ORCAMENTO","learning","PTS tecnica maturidade","memory/solicitations_learning/","HISTORICAL")])
    assert r.action is RouteAction.CANDIDATE and r.destination.destination_id=="BUDGET_LEARNING"
    assert "memory/solicitations_learning/" in r.legacy_evidence_refs

def test_existing_canonical_learning_is_reused():
    r=LearningMemoryRouter().investigate(req(validated=True),[MemoryEntry("m1","multiteiner","ORCAMENTO","learning","PTS tecnica maturidade","08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/x.md","VALIDATED_LEARNING","BUDGET_LEARNING")])
    assert r.action is RouteAction.REUSE and r.duplicate_memory_ids==("m1",)

def test_calculation_routes_to_supabase_memory():
    r=LearningMemoryRouter().investigate(req(learning_kind="calculation"),[])
    assert r.destination.destination_id=="BUDGET_CALCULATION_MEMORY" and r.destination.storage=="supabase"

def test_skill_candidate_reuses_forge_owner():
    r=LearningMemoryRouter().investigate(req(domain="FORGE",learning_kind="skill",concept_key="skill pts"),[])
    assert r.destination.destination_id=="SPECIALIST_SKILL_CANDIDATE"

def test_unknown_domain_cannot_create_owner():
    assert LearningMemoryRouter().investigate(req(domain="UNKNOWN"),[]).action is RouteAction.NO_OWNER

def test_cross_tenant_memory_is_not_duplicate():
    r=LearningMemoryRouter().investigate(req(validated=True),[MemoryEntry("m1","other","ORCAMENTO","learning","PTS tecnica maturidade","x","VALIDATED_LEARNING","BUDGET_LEARNING")])
    assert r.action is RouteAction.CANDIDATE and not r.duplicate_memory_ids
