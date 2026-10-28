from pathlib import Path


RUNTIME = Path("apps/elo-web/src/lib/elo-objective-continuity.ts").read_text(encoding="utf-8")
MIGRATION = Path("supabase/migrations/20261028173000_persist_objective_continuity_next_handoff.sql").read_text(encoding="utf-8").lower()
HANDOFF = Path("06-knowledge-engineering/elo-dialogue-handoff/HANDOFF_ELO_TO_GPT.md").read_text(encoding="utf-8")


def test_checkpoint_store_persists_next_trigger_and_prompt() -> None:
    assert "add column if not exists next_trigger jsonb" in MIGRATION
    assert "add column if not exists next_elo_prompt text" in MIGRATION
    assert "jsonb_typeof(next_trigger) = 'object'" in MIGRATION


def test_runtime_writes_derived_handoff_into_same_checkpoint() -> None:
    assert "next_trigger: nextTrigger" in RUNTIME
    assert "next_elo_prompt: nextEloPrompt" in RUNTIME
    assert "next_trigger: persisted.next_trigger" in RUNTIME
    assert "next_elo_prompt: persisted.next_elo_prompt" in RUNTIME


def test_next_prompt_is_checkpoint_bound_and_fail_closed() -> None:
    for token in (
        "checkpoint_version: ${trigger.checkpoint_version}",
        "objective_id: ${trigger.objective_id}",
        "workstream_id: ${trigger.workstream_id}",
        "progress_token: ${trigger.progress_token}",
        "next_action: ${trigger.next_action}",
        "valide state_version antes de agir",
        "execute no máximo um replay",
    ):
        assert token in RUNTIME


def test_terminal_or_human_required_states_have_no_next_handoff() -> None:
    assert 'if (humanRequired || !["CONTINUE", "CORRECT", "REPLAN"].includes(decision)) return null;' in RUNTIME
    assert "human_required=true" in HANDOFF
    assert "next_trigger=null" in HANDOFF
    assert "next_elo_prompt=null" in HANDOFF


def test_persisted_handoff_is_not_a_second_authority() -> None:
    assert "não constituem um segundo store" in HANDOFF
    assert "reler o checkpoint" in HANDOFF
    assert "checkpoint_version" in HANDOFF
