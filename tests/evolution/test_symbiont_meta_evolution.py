from elo.cognitive.symbiont_meta_evolution import (
    ArchitecturalInvariant,
    CandidateDisposition,
    ELOStructuralModel,
    GateStatus,
    ExternalPattern,
    SymbiontMetaEvolutionEngine,
)


MODEL = ELOStructuralModel(
    version="1.0.0",
    authorities=("ELO Cognitive", "ELO Core", "Evolution Gate"),
    components=("Symbiont", "Cognitive Core", "Governance", "Evidence"),
    invariants=(
        ArchitecturalInvariant("canonical_owner", "One canonical owner per concern"),
        ArchitecturalInvariant("provenance", "Every candidate has source lineage"),
        ArchitecturalInvariant("isolation", "Tenant and experiment isolation"),
        ArchitecturalInvariant("authority_boundary", "External capabilities cannot become authority"),
    ),
    capabilities=("trace-first",),
    known_patterns=("trace-first",),
)


def pattern(name="reflective evolution"):
    return ExternalPattern(
        pattern_id="p-001",
        name=name,
        source="external-research",
        source_ref="github://example/project",
        source_commit="abc123",
        problem="Improve failed agent behavior using execution evidence",
        mechanism="reflective mutation",
        evidence=("ev-1",),
        required_invariants=("canonical_owner", "provenance", "isolation", "authority_boundary"),
    )


def test_reuse_before_create():
    engine = SymbiontMetaEvolutionEngine(MODEL)
    assert engine.classify(pattern("trace-first")) is CandidateDisposition.REUSE


def test_missing_invariant_blocks_candidate():
    p = pattern("new capability")
    p = ExternalPattern(**{**p.__dict__, "required_invariants": ("nonexistent",)})
    engine = SymbiontMetaEvolutionEngine(MODEL)
    assert engine.classify(p) is CandidateDisposition.BLOCK


def test_ready_candidate_requires_all_safety_gates_and_benefit():
    engine = SymbiontMetaEvolutionEngine(MODEL)
    candidate = engine.prepare_candidate(
        pattern(),
        candidate_id="cand-001",
        branch_ref="symbiont/cand-001",
        proposed_changes=("add reflection evaluator",),
    )
    result = engine.evaluate(
        candidate,
        tests_passed=True,
        regressions_passed=True,
        benchmark_improved=True,
        isolation_passed=True,
        provenance_passed=True,
        authority_boundary_passed=True,
        evidence_ids=("ev-1", "ev-2"),
        metrics={"baseline": 0.71, "candidate": 0.79},
    )
    package = engine.approval_package(candidate, result)
    assert package.status is GateStatus.READY_FOR_APPROVAL
    assert package.required_approval == "HUMAN_EVOLUTION_GATE"


def test_regression_failure_blocks_promotion():
    engine = SymbiontMetaEvolutionEngine(MODEL)
    candidate = engine.prepare_candidate(
        pattern(), candidate_id="cand-002", branch_ref="symbiont/cand-002", proposed_changes=("change",)
    )
    result = engine.evaluate(
        candidate,
        tests_passed=True,
        regressions_passed=False,
        benchmark_improved=True,
        evidence_ids=("ev-1",),
    )
    package = engine.approval_package(candidate, result)
    assert package.status is GateStatus.BLOCKED
