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


def observation(**kw):
    from elo.cognitive.symbionte_lab import SymbiontLabObservation

    d = dict(
        observation_id="obs-1",
        tenant_id="multiteiner",
        domain="ORCAMENTO",
        decision_id="decision-1",
        expected_outcome="expected",
        observed_outcome="observed",
        evidence_ids=("evidence-1",),
        source_ref="runtime-1",
        source_commit="commit-1",
        hypothesis="controlled hypothesis",
        baseline="baseline",
        experiment="experiment",
        result="result",
        regression_status="PASS",
        generalization_status="CONFIRMED",
        risk="LOW",
        existing_owner=None,
        scope="symbiont-lab",
    )
    d.update(kw)
    return SymbiontLabObservation(**d)


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


def test_candidate_can_enter_existing_lab_only():
    class LabStub:
        def __init__(self):
            self.calls = 0

        def evaluate(self, lab_observation, *, principal_id, dataset_version):
            self.calls += 1
            return "LAB_EVALUATED"

    lab = LabStub()
    result = SymbiontMemoryLearningBridge().route_to_lab(
        req(),
        (),
        observation=observation(),
        laboratory=lab,
        principal_id="principal-1",
        dataset_version="dataset-1",
    )
    assert result.routing.action is RouteAction.CANDIDATE
    assert result.routing.requires_lab is True
    assert result.evaluation == "LAB_EVALUATED"
    assert result.entered_lab is True
    assert lab.calls == 1


def test_non_candidate_never_calls_lab():
    class LabStub:
        def evaluate(self, *args, **kwargs):
            raise AssertionError("non-candidate route must not enter lab")

    result = SymbiontMemoryLearningBridge().route_to_lab(
        req(validated=True),
        (MemoryEntry("m1", "multiteiner", "ORCAMENTO", "learning", "PTS tecnica maturidade", "canonical", "VALIDATED_LEARNING", "BUDGET_LEARNING"),),
        observation=observation(),
        laboratory=LabStub(),
        principal_id="principal-1",
        dataset_version="dataset-1",
    )
    assert result.routing.action is RouteAction.REUSE
    assert result.evaluation is None
    assert result.entered_lab is False


def test_lab_handoff_requires_tenant_and_domain_alignment():
    class LabStub:
        def evaluate(self, *args, **kwargs):
            return "LAB_EVALUATED"

    try:
        SymbiontMemoryLearningBridge().route_to_lab(
            req(),
            (),
            observation=observation(tenant_id="other"),
            laboratory=LabStub(),
            principal_id="principal-1",
            dataset_version="dataset-1",
        )
    except ValueError as exc:
        assert "tenant" in str(exc)
    else:
        raise AssertionError("tenant mismatch must be rejected")


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
