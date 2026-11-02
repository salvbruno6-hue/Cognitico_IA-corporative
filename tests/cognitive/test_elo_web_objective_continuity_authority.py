from pathlib import Path


WEB_RUNTIME = Path("apps/elo-web/src/lib/elo-objective-continuity.ts").read_text(encoding="utf-8")
WEB_CORE = Path("apps/elo-web/src/lib/elo-cognitive-core.ts").read_text(encoding="utf-8")
PYTHON_REFERENCE = Path("src/elo/cognitive/objective_continuity.py").read_text(encoding="utf-8")
ARCHITECTURE = Path("docs/architecture/ELO_OBJECTIVE_CONTINUITY_LOOP.md").read_text(encoding="utf-8")


def test_web_checkpoint_runtime_delegates_decision_to_cognitive_core() -> None:
    assert 'orchestrateObjectiveContinuityDecision' in WEB_RUNTIME
    assert 'from "@/lib/elo-cognitive-core"' in WEB_RUNTIME
    assert "function decide(" not in WEB_RUNTIME
    assert "export function orchestrateObjectiveContinuityDecision" in WEB_CORE


def test_web_cognitive_policy_preserves_canonical_no_progress_progression() -> None:
    for token in (
        'input.noProgressStreak >= 4',
        'decision: "ESCALATE"',
        'input.noProgressStreak >= 2',
        'decision: "REPLAN"',
        'input.noProgressStreak >= 1',
        'decision: "CORRECT"',
        'decision: "CONTINUE"',
    ):
        assert token in WEB_CORE

    for decision in ("CONTINUE", "CORRECT", "REPLAN", "ESCALATE", "COMPLETE"):
        assert decision in WEB_CORE
        assert decision in PYTHON_REFERENCE


def test_web_cognitive_policy_preserves_fail_closed_risk_and_cycle_budget() -> None:
    assert '["HIGH", "CRITICAL", "ALTO", "CRITICO"]' in WEB_CORE
    assert "input.iteration >= input.maxCycles" in WEB_CORE
    assert "input.maxCycles < 2" in WEB_CORE
    assert "maxCycles < 2" in WEB_RUNTIME
    assert '"INVALID_OBJECTIVE_POLICY"' in WEB_RUNTIME

    for risk in ("HIGH", "CRITICAL", "ALTO", "CRITICO"):
        assert risk in PYTHON_REFERENCE


def test_persisted_next_action_matches_cognitive_decision_semantics() -> None:
    for token in (
        'CONTINUE: proposedNextAction',
        'CORRECT: "CORRECT"',
        'REPLAN: "REPLAN"',
        'ESCALATE: "HUMAN_APPROVAL_REQUIRED"',
        'COMPLETE: "COMPLETED"',
        'next_action: nextAction',
    ):
        assert token in WEB_RUNTIME

    assert 'ObjectiveLoopDecision.CONTINUE: proposed_next_action' in PYTHON_REFERENCE
    assert 'ObjectiveLoopDecision.CORRECT: "CORRECT"' in PYTHON_REFERENCE
    assert 'ObjectiveLoopDecision.REPLAN: "REPLAN"' in PYTHON_REFERENCE
    assert 'next_action="HUMAN_APPROVAL_REQUIRED"' in PYTHON_REFERENCE
    assert 'next_action="COMPLETED"' in PYTHON_REFERENCE


def test_checkpoint_store_retains_cas_and_persisted_handoff() -> None:
    assert '.eq("state_version", existing.state_version)' in WEB_RUNTIME
    assert "next_trigger: nextTrigger" in WEB_RUNTIME
    assert "next_elo_prompt: nextEloPrompt" in WEB_RUNTIME
    assert "next_trigger: persisted.next_trigger" in WEB_RUNTIME
    assert "next_elo_prompt: persisted.next_elo_prompt" in WEB_RUNTIME


def test_architecture_keeps_decision_and_persistence_as_distinct_authorities() -> None:
    assert "Cognitive supervision and next-action policy: ELO Cognitivo" in ARCHITECTURE
    assert "Production runtime: `apps/elo-web` / ELO Web" in ARCHITECTURE
    assert "Durable production checkpoint store: `public.elo_objective_continuity_checkpoints`" in ARCHITECTURE
    assert "persistence module may store a decision already produced by the cognitive authority" in ARCHITECTURE
    assert "must not become an independent decision authority" in ARCHITECTURE
