from elo.cognitive.learning_memory_router import LearningRequest, MemoryEntry, RouteAction
from elo.cognitive.symbiont_memory_learning_bridge import SymbiontMemoryLearningBridge


def req(**kw):
    d = dict(
        learning_id="L-1",
        tenant_scope="multiteiner",
        domain="ORCAMENTO",
        learning_kind="learning",
        concept_key="PTS tecnica maturidade",
        source_refs=("controlled:memory-bridge",),
    )
    d.update(kw)
    return LearningRequest(**d)


def test_reuse_never_enters_lab():
    result = SymbiontMemoryLearningBridge().route(
        req(validated=True),
        (MemoryEntry("m1", "multiteiner", "ORCAMENTO", "learning", "PTS tecnica maturidade", "canonical", "VALIDATED_LEARNING", "BUDGET_LEARNING"),),
    )
    assert result.action is RouteAction.REUSE
    assert result.learning_admission == "REUSE_EXISTING"
    assert result.requires_lab is False
    assert result.canonical_mutation is False


def test_aggregate_reuses_owner_without_new_candidate():
    result = SymbiontMemoryLearningBridge().route(
        req(validated=True, relation_keys=("pts-tecnica",)),
        (MemoryEntry("m1", "multiteiner", "ORCAMENTO", "learning", "outro conceito", "canonical", "VALIDATED_LEARNING", "BUDGET_LEARNING", ("pts-tecnica",)),),
    )
    assert result.action is RouteAction.AGGREGATE
    assert result.destination_id == "BUDGET_LEARNING"
    assert result.learning_admission == "AGGREGATE_EXISTING"
    assert result.requires_lab is False


def test_candidate_is_the_only_route_that_enters_governed_learning():
    result = SymbiontMemoryLearningBridge().route(req(), ())
    assert result.action is RouteAction.CANDIDATE
    assert result.learning_admission == "CANDIDATE_FOR_GOVERNED_LEARNING"
    assert result.requires_lab is True


def test_blocked_never_enters_learning():
    result = SymbiontMemoryLearningBridge().route(req(learning_id="", concept_key=""), ())
    assert result.action is RouteAction.BLOCKED
    assert result.learning_admission == "BLOCKED"
    assert result.requires_lab is False


def test_unknown_owner_does_not_create_owner():
    result = SymbiontMemoryLearningBridge().route(req(domain="UNKNOWN"), ())
    assert result.action is RouteAction.NO_OWNER
    assert result.learning_admission == "NO_OWNER"
    assert result.destination_id is None
    assert result.canonical_mutation is False


def test_cross_tenant_memory_is_not_reused():
    result = SymbiontMemoryLearningBridge().route(
        req(validated=True),
        (MemoryEntry("m1", "other", "ORCAMENTO", "learning", "PTS tecnica maturidade", "x", "VALIDATED_LEARNING", "BUDGET_LEARNING"),),
    )
    assert result.action is RouteAction.CANDIDATE
    assert result.duplicate_memory_ids == ()
