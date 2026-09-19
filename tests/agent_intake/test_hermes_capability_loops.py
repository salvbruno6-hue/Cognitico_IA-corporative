from elo.agent_intake.hermes_capability_loops import (
    CapabilityEvidence,
    CapabilityKind,
    CapabilityState,
    HermesCapabilityLoops,
)


def evidence():
    return CapabilityEvidence(
        mechanism_id="memory",
        source="salvbruno6-hue/ELO-Hermes-Agent",
        revision="b774519a",
        interface="MEMORY.md/USER.md",
        invariants=("reference-boundary", "provenance-preserved"),
        dependencies=("session",),
        relations=("context",),
        evidence_refs=("tools/memory_tool.py",),
    )


def test_discovery_loop_retries_then_passes():
    calls = []

    def evaluate(current):
        calls.append(current.interface)
        if len(calls) == 1:
            return False, ("interface mapping incomplete",)
        return True, ()

    final, history = HermesCapabilityLoops.discover_and_test(
        evidence(),
        evaluate=evaluate,
        test=lambda current: True,
        adjust=lambda current, _issues, _iteration: current,
        max_iterations=3,
    )
    assert final.source.endswith("ELO-Hermes-Agent")
    assert len(history) == 2
    assert history[-1].consistent and history[-1].test_passed


def test_discovery_loop_preserves_provenance():
    try:
        HermesCapabilityLoops.discover_and_test(
            evidence(),
            evaluate=lambda _current: (False, ("bad",)),
            test=lambda _current: False,
            adjust=lambda current, _issues, _iteration: CapabilityEvidence(
                mechanism_id=current.mechanism_id,
                source=current.source,
                revision="CHANGED",
                interface=current.interface,
            ),
            max_iterations=1,
        )
    except ValueError as exc:
        assert "provenance" in str(exc)
    else:
        raise AssertionError("provenance must remain immutable")


def build(current, kind, variant):
    return __import__(
        "elo.agent_intake.hermes_capability_loops", fromlist=["TransformationCandidate"]
    ).TransformationCandidate(
        mechanism_id=current.mechanism_id,
        candidate_id=f"ELO-{current.mechanism_id}",
        kind=kind,
        state=CapabilityState.TRANSFORMING,
        native_name="elo_memory",
        contract=("read_reference_memory", "preserve_provenance"),
        source=current.source,
        revision=current.revision,
        evidence_refs=current.evidence_refs,
        invariants=current.invariants,
        dependencies=current.dependencies,
        relations=current.relations,
        variant=variant,
    )


def test_transformation_loop_creates_native_candidate():
    candidate, notes = HermesCapabilityLoops.transform_until_valid(
        evidence(),
        kind=CapabilityKind.STRUCTURE,
        build=build,
        test=lambda current: (current.native_name == "elo_memory", ()),
        max_iterations=3,
    )
    assert candidate.state == CapabilityState.TRANSFORMED
    assert candidate.kind == CapabilityKind.STRUCTURE
    assert candidate.candidate_id == "ELO-memory"
    assert notes == ()


def test_approval_readiness_is_not_approval():
    candidate, _ = HermesCapabilityLoops.transform_until_valid(
        evidence(),
        kind=CapabilityKind.SKILL,
        build=build,
        test=lambda _current: (True, ()),
    )
    readiness = HermesCapabilityLoops.approval_readiness(
        candidate,
        implementation_passed=True,
        provenance_passed=True,
        consistency_passed=True,
        governance_metadata_complete=True,
        evolution_gate_approved=False,
    )
    assert not readiness.ready
    assert "evolution_gate" in readiness.missing


def test_approval_readiness_green_requires_all_checks():
    candidate, _ = HermesCapabilityLoops.transform_until_valid(
        evidence(),
        kind=CapabilityKind.FUNCTION,
        build=build,
        test=lambda _current: (True, ()),
    )
    readiness = HermesCapabilityLoops.approval_readiness(
        candidate,
        implementation_passed=True,
        provenance_passed=True,
        consistency_passed=True,
        governance_metadata_complete=True,
        evolution_gate_approved=True,
    )
    assert readiness.ready
    assert readiness.missing == ()

def test_approved_candidate_implementation_loop_activates_after_explicit_decision():
    candidate, _ = HermesCapabilityLoops.transform_until_valid(
        evidence(), kind=CapabilityKind.SKILL, build=build, test=lambda _current: (True, ()),
    )
    readiness = HermesCapabilityLoops.approval_readiness(
        candidate,
        implementation_passed=True,
        provenance_passed=True,
        consistency_passed=True,
        governance_metadata_complete=True,
        evolution_gate_approved=True,
    )
    decision = __import__(
        "elo.agent_intake.hermes_capability_loops",
        fromlist=["ImplementationDecision"],
    ).ImplementationDecision(
        decision_id="decision-001",
        candidate_id=candidate.candidate_id,
        approved=True,
        scope="controlled-runtime",
        evidence_refs=("decision-evidence-001",),
    )
    activation = __import__(
        "elo.agent_intake.hermes_capability_loops",
        fromlist=["ApprovedCandidateImplementationLoop"],
    ).ApprovedCandidateImplementationLoop.activate(
        candidate, readiness=readiness, decision=decision
    )
    assert activation.activated
    assert activation.state == "IMPLEMENTATION_AUTHORIZED"


def test_approved_candidate_implementation_loop_fails_closed_without_gate():
    candidate, _ = HermesCapabilityLoops.transform_until_valid(
        evidence(), kind=CapabilityKind.SKILL, build=build, test=lambda _current: (True, ()),
    )
    readiness = HermesCapabilityLoops.approval_readiness(
        candidate,
        implementation_passed=True,
        provenance_passed=True,
        consistency_passed=True,
        governance_metadata_complete=True,
        evolution_gate_approved=False,
    )
    decision = __import__(
        "elo.agent_intake.hermes_capability_loops",
        fromlist=["ImplementationDecision"],
    ).ImplementationDecision(
        decision_id="decision-002",
        candidate_id=candidate.candidate_id,
        approved=True,
        scope="controlled-runtime",
        evidence_refs=("decision-evidence-002",),
    )
    activation = __import__(
        "elo.agent_intake.hermes_capability_loops",
        fromlist=["ApprovedCandidateImplementationLoop"],
    ).ApprovedCandidateImplementationLoop.activate(
        candidate, readiness=readiness, decision=decision
    )
    assert not activation.activated
    assert activation.state == "BLOCKED"


def test_approved_candidate_implementation_loop_requires_matching_decision():
    candidate, _ = HermesCapabilityLoops.transform_until_valid(
        evidence(), kind=CapabilityKind.SKILL, build=build, test=lambda _current: (True, ()),
    )
    readiness = HermesCapabilityLoops.approval_readiness(
        candidate,
        implementation_passed=True,
        provenance_passed=True,
        consistency_passed=True,
        governance_metadata_complete=True,
        evolution_gate_approved=True,
    )
    decision = __import__(
        "elo.agent_intake.hermes_capability_loops",
        fromlist=["ImplementationDecision"],
    ).ImplementationDecision(
        decision_id="decision-003",
        candidate_id="different-candidate",
        approved=True,
        scope="controlled-runtime",
        evidence_refs=("decision-evidence-003",),
    )
    try:
        __import__(
            "elo.agent_intake.hermes_capability_loops",
            fromlist=["ApprovedCandidateImplementationLoop"],
        ).ApprovedCandidateImplementationLoop.activate(
            candidate, readiness=readiness, decision=decision
        )
    except ValueError as exc:
        assert "does not match" in str(exc)
    else:
        raise AssertionError("mismatched implementation decision must be rejected")
