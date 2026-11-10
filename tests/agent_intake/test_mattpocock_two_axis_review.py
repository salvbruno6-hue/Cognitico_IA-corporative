from elo.agent_intake.independent_review import IndependentReviewEvidence, assess_two_axis_review


def review(axis, verdict="PASS", subject="candidate-1", reviewer=None, snapshot=None):
    return IndependentReviewEvidence(
        subject_id=subject,
        subject_owner_id="author",
        reviewer_id=reviewer or axis.lower(),
        review_scope=axis,
        context_snapshot_id=snapshot or f"ctx-{axis.lower()}",
        verdict=verdict,
        evidence_ids=(f"evidence-{axis}",),
        findings=("example finding",) if verdict == "FAIL" else (),
        provenance={"source": "fixture"},
    )


def test_both_axes_pass_is_advisory_only():
    result = assess_two_axis_review(review("STANDARDS"), review("SPEC"), expected_subject_id="candidate-1")
    assert result.status == "REVIEW_PASSED"
    assert result.canonical_mutation is False
    assert len(result.evidence_ids) == 2


def test_failures_are_not_masked_by_other_axis():
    for axis in ("SPEC", "STANDARDS"):
        left = review("STANDARDS", "FAIL" if axis == "STANDARDS" else "PASS")
        right = review("SPEC", "FAIL" if axis == "SPEC" else "PASS")
        result = assess_two_axis_review(left, right, expected_subject_id="candidate-1")
        assert result.status == "REVIEW_FAILED"
        assert result.findings == (f"{axis}: example finding",)


def test_missing_invalid_or_abstaining_axis_blocks_pass():
    base = review("STANDARDS")
    candidates = [None, review("STANDARDS"), review("SPEC", subject="different"), review("SPEC", "ABSTAIN")]
    for second in candidates:
        assert assess_two_axis_review(base, second, expected_subject_id="candidate-1").status == "REVIEW_INCOMPLETE"


def test_same_reviewer_or_snapshot_does_not_count_as_independent():
    for kwargs in ({"reviewer": "same"}, {"snapshot": "shared"}):
        a = review("STANDARDS", **kwargs)
        b = review("SPEC", **kwargs)
        assert assess_two_axis_review(a, b, expected_subject_id="candidate-1").status == "REVIEW_INCOMPLETE"
