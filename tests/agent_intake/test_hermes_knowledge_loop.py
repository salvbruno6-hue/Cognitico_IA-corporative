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
