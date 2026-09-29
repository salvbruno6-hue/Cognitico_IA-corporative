from elo.cognitive.learning_memory_router import LearningRequest, MemoryEntry, RouteAction
from elo.cognitive.symbiont_decision_learning_context import build_decision_learning_context


def request(validated=True):
    return LearningRequest(
        learning_id="l1",
        tenant_scope="tenant-a",
        domain="FORGE",
        learning_kind="skill",
        concept_key="safe-route",
        source_refs=("e1",),
        validated=validated,
    )


def memory(status="VALIDATED", tenant="tenant-a", domain="FORGE", concept="safe-route"):
    return MemoryEntry(
        memory_id="m1",
        tenant_scope=tenant,
        domain=domain,
        learning_kind="skill",
        concept_key=concept,
        source_ref="forge/skill-packs/safe-route",
        status=status,
        destination_id="SPECIALIST_SKILL_CANDIDATE",
    )


def test_validated_reused_learning_enters_next_decision_context():
    context = build_decision_learning_context(
        request(),
        [memory()],
        routing_action=RouteAction.REUSE,
        destination_id="SPECIALIST_SKILL_CANDIDATE",
    )
    assert context.reusable
    assert context.source_memory_ids == ("m1",)
    assert not context.canonical_mutation
    assert not context.authorization_granted


def test_candidate_learning_does_not_influence_decision_yet():
    context = build_decision_learning_context(
        request(),
        [memory()],
        routing_action=RouteAction.CANDIDATE,
        destination_id="SPECIALIST_SKILL_CANDIDATE",
    )
    assert not context.reusable
    assert context.signals == ()


def test_unvalidated_learning_does_not_influence_decision():
    context = build_decision_learning_context(
        request(validated=False),
        [memory()],
        routing_action=RouteAction.REUSE,
        destination_id="SPECIALIST_SKILL_CANDIDATE",
    )
    assert not context.reusable


def test_tenant_domain_and_status_boundaries_are_enforced():
    context = build_decision_learning_context(
        request(),
        [
            memory(tenant="other"),
            memory(domain="OTHER"),
            memory(status="CANDIDATE"),
        ],
        routing_action=RouteAction.REUSE,
        destination_id="SPECIALIST_SKILL_CANDIDATE",
    )
    assert not context.reusable


def test_multiple_matching_memories_are_deduplicated():
    context = build_decision_learning_context(
        request(),
        [memory(), memory()],
        routing_action=RouteAction.AGGREGATE,
        destination_id="SPECIALIST_SKILL_CANDIDATE",
    )
    assert context.source_memory_ids == ("m1",)
