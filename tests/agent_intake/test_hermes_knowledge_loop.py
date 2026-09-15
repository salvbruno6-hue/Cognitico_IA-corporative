from elo.agent_intake.hermes_knowledge_loop import (
    CANDIDATE,
    VALIDATED,
    HermesKnowledgeLoop,
    HermesMechanism,
    HermesSnapshot,
)


def snapshot() -> HermesSnapshot:
    return HermesSnapshot(
        source="salvbruno6-hue/ELO-Hermes-Agent",
        revision="b774519a",
        captured_at="2026-09-15T16:00:00Z",
        mechanisms=(
            HermesMechanism(
                mechanism_id="memory",
                category="memory",
                name="Persistent Memory",
                interface="MEMORY.md/USER.md",
                dependencies=("session",),
                relations=("context", "session_search"),
            ),
            HermesMechanism(
                mechanism_id="skills",
                category="extension",
                name="Skills",
                interface="SKILL.md",
            ),
        ),
    )


def test_discovery_creates_candidates_with_provenance():
    candidates = HermesKnowledgeLoop().discover(snapshot())
    assert len(candidates) == 2
    assert all(c.status == CANDIDATE for c in candidates)
    assert candidates[0].provenance["source"] == "salvbruno6-hue/ELO-Hermes-Agent"
    assert "implementation test passes" in candidates[0].promotion_requirements


def test_failed_gate_never_promotes_candidate():
    candidate = HermesKnowledgeLoop().discover(snapshot())[0]
    result = HermesKnowledgeLoop.validate(
        candidate,
        implementation_passed=True,
        provenance_passed=True,
        evolution_gate_approved=False,
    )
    assert result.status == CANDIDATE
    assert HermesKnowledgeLoop.promote([result]) == ()


def test_all_gates_promote_candidate():
    candidate = HermesKnowledgeLoop().discover(snapshot())[0]
    result = HermesKnowledgeLoop.validate(
        candidate,
        implementation_passed=True,
        provenance_passed=True,
        evolution_gate_approved=True,
    )
    assert result.status == VALIDATED
    assert HermesKnowledgeLoop.promote([result]) == (result,)


def test_memory_markdown_keeps_reference_boundary():
    loop = HermesKnowledgeLoop()
    candidates = loop.discover(snapshot())
    memory = loop.build_memory_markdown(snapshot(), candidates)
    assert "authority: reference" in memory
    assert "Discovery never equals learning" in memory
    assert "ELO Evolution Gate" in memory


def test_duplicate_mechanism_ids_are_rejected():
    base = snapshot()
    duplicate = HermesSnapshot(
        source=base.source,
        revision=base.revision,
        captured_at=base.captured_at,
        mechanisms=base.mechanisms + (base.mechanisms[0],),
    )
    try:
        HermesKnowledgeLoop().discover(duplicate)
    except ValueError as exc:
        assert "duplicate mechanism_id" in str(exc)
    else:
        raise AssertionError("duplicate mechanism IDs must be rejected")


def test_missing_source_provenance_is_rejected():
    base = snapshot()
    invalid = HermesSnapshot("", base.revision, base.captured_at, base.mechanisms)
    try:
        HermesKnowledgeLoop().discover(invalid)
    except ValueError as exc:
        assert "source and revision provenance" in str(exc)
    else:
        raise AssertionError("missing source provenance must be rejected")


def test_consistency_loop_creates_variations_until_test_passes():
    candidate = HermesKnowledgeLoop().discover(snapshot())[0]
    attempts = []

    def evaluate(current):
        attempts.append(current.variant)
        if current.variant < 2:
            return False, (f"inconsistency-{current.variant}",)
        return True, ()

    def adjust(current, issues, iteration):
        return current

    final, history = HermesKnowledgeLoop.iterate_until_consistent(
        candidate,
        evaluate=evaluate,
        adjust=adjust,
        test=lambda current: True,
        max_iterations=5,
    )

    assert final.status == CANDIDATE
    assert final.variant == 2
    assert attempts == [0, 1, 2]
    assert len(history) == 3
    assert history[-1].consistent is True
    assert history[-1].test_passed is True
    assert "inconsistency-0" in final.validation_notes
    assert "inconsistency-1" in final.validation_notes


def test_consistency_loop_is_bounded_and_never_promotes():
    candidate = HermesKnowledgeLoop().discover(snapshot())[0]

    def evaluate(_current):
        return False, ("persistent inconsistency",)

    final, history = HermesKnowledgeLoop.iterate_until_consistent(
        candidate,
        evaluate=evaluate,
        adjust=lambda current, _issues, _iteration: current,
        test=lambda _current: False,
        max_iterations=3,
    )

    assert final.status == CANDIDATE
    assert final.variant == 3
    assert len(history) == 3
    assert all(not item.consistent for item in history)
    assert HermesKnowledgeLoop.promote([final]) == ()


def test_consistency_loop_cannot_change_candidate_identity_or_provenance():
    candidate = HermesKnowledgeLoop().discover(snapshot())[0]

    try:
        HermesKnowledgeLoop.iterate_until_consistent(
            candidate,
            evaluate=lambda _current: (False, ("bad",)),
            adjust=lambda current, _issues, _iteration: type(current)(
                candidate_id="OTHER",
                mechanism_id=current.mechanism_id,
                status=current.status,
                evidence=current.evidence,
                provenance=current.provenance,
                promotion_requirements=current.promotion_requirements,
            ),
            test=lambda _current: False,
            max_iterations=1,
        )
    except ValueError as exc:
        assert "candidate identity" in str(exc)
    else:
        raise AssertionError("candidate identity must remain immutable")
