from elo.agent_intake.hermes_20260926_candidates import (
    CURRENT_CANDIDATES,
    build_evidence,
    build_native_candidate,
    validate_native_contract,
)


def test_five_current_candidates_are_explicit_and_unique():
    ids = [item.candidate_id for item in CURRENT_CANDIDATES]
    assert len(ids) == 5
    assert len(ids) == len(set(ids))


def test_candidates_have_native_contract_boundaries():
    for spec in CURRENT_CANDIDATES:
        evidence = build_evidence(spec, "2026-09-26")
        candidate = build_native_candidate(evidence, spec)
        passed, issues = validate_native_contract(candidate)
        assert passed, issues
        assert candidate.state.value == "transforming"
        assert candidate.source == "Hermes public capability documentation"
        assert candidate.candidate_id.startswith("ELO-")
        assert all("Hermes" not in dependency for dependency in candidate.dependencies)


def test_provenance_cannot_be_changed_by_candidate_builder():
    spec = CURRENT_CANDIDATES[0]
    evidence = build_evidence(spec, "REV-A")
    candidate = build_native_candidate(evidence, spec)
    assert candidate.revision == "REV-A"
    assert candidate.evidence_refs == ("hermes:EXT-CODE-EXEC-HERMES:source",)


def test_mismatched_mechanism_is_rejected():
    first, second = CURRENT_CANDIDATES[:2]
    evidence = build_evidence(first, "REV-A")
    try:
        build_native_candidate(evidence, second)
    except ValueError as exc:
        assert "mismatch" in str(exc)
    else:
        raise AssertionError("candidate/spec mismatch must fail closed")


def test_native_contract_rejects_missing_evidence():
    spec = CURRENT_CANDIDATES[0]
    candidate = build_native_candidate(build_evidence(spec, "REV-A"), spec)
    broken = candidate.__class__(
        mechanism_id=candidate.mechanism_id,
        candidate_id=candidate.candidate_id,
        kind=candidate.kind,
        state=candidate.state,
        native_name=candidate.native_name,
        contract=candidate.contract,
        source=candidate.source,
        revision=candidate.revision,
        evidence_refs=(),
        invariants=candidate.invariants,
        dependencies=candidate.dependencies,
        relations=candidate.relations,
        transformation_notes=candidate.transformation_notes,
        variant=candidate.variant,
    )
    passed, issues = validate_native_contract(broken)
    assert not passed
    assert "missing evidence" in issues
